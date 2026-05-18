"""Stage 4A — Trade Data Collection via UN Comtrade API (v2, self-contained).

이전 v3.x 의 03/04/05/06 스크립트 통합 버전. lib/ 의존성 제거.

3 데이터 set:
  1. KR <- CN (M) + KR -> CN (X): main treatment IV
  2. ADH 8 <- CN (M): Pierce-Schott / Autor-Dorn-Hanson instrument (8 OHIE)
     ADH 8 = Australia, Denmark, Finland, Germany, Japan, New Zealand, Spain, Switzerland
  3. (optional) CN -> World (X): alternative supply-side IV

핵심 기능:
  - 4-key auto-rotation on 401/403/429 (CLI / env / .env 자동 로드)
  - HS2 chapter chunking (100k row per-call 한도 회피)
  - Resumable (이미 다운로드된 파일 자동 skip)
  - MFG_ONLY HS 28-97 (manufacturing focus, ADH 표준)
  - Rate limit 적응형 (연속 실패 시 backoff)

Usage (Windows PowerShell):
  cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
  python 2_scripts\\build_panel\\4A_trade_collection.py [--kr-cn | --adh | --cn-world | --all]
                                                       [--start-year 2000] [--end-year 2024]
                                                       [--manufacturing-only / --all-hs]
                                                       [--cross-check]

Outputs:
  0_raw/comtrade_korea_china/KR_imp_from_CN_{year}.csv
  0_raw/comtrade_korea_china/KR_exp_to_CN_{year}.csv
  0_raw/comtrade_adh_china/{ISO2}_{year}.csv
  0_raw/comtrade_china_world/CN_exp_world_{year}.csv     # only if --cn-world or --all
  4_trade/trade_collection_validation.md
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

# -----------------------------------------------------------------------------
# Paths & constants
# -----------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]  # trade_mortality_korea/
RAW_DIR = ROOT / "0_raw"
DOTENV_PATH = ROOT / ".env"
VALIDATION_PATH = ROOT / "4_trade" / "trade_collection_validation.md"

KR_CN_DIR = RAW_DIR / "comtrade_korea_china"
ADH_DIR = RAW_DIR / "comtrade_adh_china"
CN_WORLD_DIR = RAW_DIR / "comtrade_china_world"

# Pierce-Schott / ADH instrument set (8 OHIE)
ADH_8 = ["AU", "DK", "FI", "DE", "JP", "NZ", "ES", "CH"]

# ISO2 -> M49 numeric (UN Comtrade reporterCode)
M49 = {
    "KR": 410, "CN": 156,
    "AU": 36, "DK": 208, "FI": 246, "DE": 276,
    "JP": 392, "NZ": 554, "ES": 724, "CH": 756,
}

# HS2 chunk lists
HS2_MFG = [f"{i:02d}" for i in range(28, 98)]   # HS 28-97 (manufacturing, ADH 표준)
HS2_ALL = [f"{i:02d}" for i in range(1, 100)]   # HS 01-99

# Manufacturing share of KR <- CN imports (manufacturing / all-HS).
# Source: KITA + KOSIS HS-chapter aggregates. Korea's import from China is
# dominated by HS 84/85 (machinery/electronics), 72/73 (steel), 27 (mineral fuels).
# HS 28-97 share ≈ 86-92% over 2000-2024. Use 0.88 as conservative midpoint
# for cross-check when only manufacturing chapters are downloaded.
KR_CN_MFG_SHARE = 0.88

# UN Comtrade Plus endpoint (free-tier shape kept for fallback)
COMTRADE_URL = "https://comtradeapi.un.org/data/v1/get/C/A/HS"

# Rate-limit / retry defaults
CALL_DELAY = 1.0           # sec between calls (Plus tier ~100/min)
RETRY_DELAYS = [10, 30, 60, 120]
TRUNCATION_THRESHOLD = 100_000

# KITA 한국무역협회 official KR <- CN import (million USD)
KITA_KR_CN_IMPORT = {
    "2000": 12798, "2005": 38648, "2010": 71574,
    "2015": 90250, "2020": 108885, "2023": 142800,
}

COMTRADE_KEY_NAMES = [
    "COMTRADE_API_KEY",
    "COMTRADE_API_KEY_SECONDARY",
    "COMTRADE_API_KEY_TERTIARY",
    "COMTRADE_API_KEY_QUATERNARY",
]


# -----------------------------------------------------------------------------
# .env loading + key collection
# -----------------------------------------------------------------------------

def load_dotenv(path: Path) -> dict[str, str]:
    """Minimal .env parser. Strips inline comments and surrounding quotes."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in s:
            continue
        key, _, raw = s.partition("=")
        key = key.strip()
        value = raw.strip()
        # inline comment if value not quoted
        if value and value[0] not in ("'", '"'):
            hp = value.find("#")
            if hp >= 0:
                value = value[:hp].strip()
        # strip quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key and value:
            env[key] = value
    return env


def collect_comtrade_keys(cli_key: str | None = None) -> list[str]:
    keys: list[str] = []
    if cli_key:
        keys.append(cli_key)
    for n in COMTRADE_KEY_NAMES:
        v = os.environ.get(n)
        if v:
            keys.append(v)
    dotenv = load_dotenv(DOTENV_PATH)
    for n in COMTRADE_KEY_NAMES:
        v = dotenv.get(n)
        if v:
            keys.append(v)
    seen, deduped = set(), []
    for k in keys:
        if k not in seen:
            seen.add(k)
            deduped.append(k)
    return deduped


# -----------------------------------------------------------------------------
# Comtrade API call wrapper with key rotation + retry
# -----------------------------------------------------------------------------

class KeyPool:
    """Rotates through a list of API keys. Marks keys dead on 401/403/429."""

    def __init__(self, keys: list[str]):
        self.keys = list(keys)
        self.dead: set[int] = set()
        self.cursor = 0

    def current(self) -> str | None:
        if not self.keys or len(self.dead) >= len(self.keys):
            return None
        # advance to next live key
        for _ in range(len(self.keys)):
            if self.cursor not in self.dead:
                return self.keys[self.cursor]
            self.cursor = (self.cursor + 1) % len(self.keys)
        return None

    def rotate(self, mark_dead: bool = False) -> None:
        if mark_dead and self.keys:
            self.dead.add(self.cursor)
        if self.keys:
            self.cursor = (self.cursor + 1) % len(self.keys)

    def all_dead(self) -> bool:
        return bool(self.keys) and len(self.dead) >= len(self.keys)

    def status(self) -> str:
        if not self.keys:
            return "no keys"
        live = len(self.keys) - len(self.dead)
        tail = self.keys[self.cursor][-4:] if self.keys else ""
        return f"key #{self.cursor+1}/{len(self.keys)} (...{tail}), live={live}"


def fetch_comtrade(reporter_code: str, partner_code: str, period: str,
                   flow_code: str, cmd_code: str,
                   pool: KeyPool, max_retries: int = 4) -> pd.DataFrame:
    """One Comtrade call with key rotation + exponential backoff."""
    params = {
        "reporterCode": reporter_code,
        "partnerCode": partner_code,
        "period": period,
        "cmdCode": cmd_code,
        "flowCode": flow_code,
        "freqCode": "A",
    }

    last_err = None
    for attempt in range(max_retries):
        key = pool.current()
        if key is None:
            raise RuntimeError("all API keys exhausted")
        headers = {"Ocp-Apim-Subscription-Key": key}
        try:
            r = requests.get(COMTRADE_URL, params=params, headers=headers, timeout=120)
            if r.status_code in (401, 403, 429):
                pool.rotate(mark_dead=(r.status_code in (401, 403)))
                last_err = f"HTTP {r.status_code}"
                wait = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
                # if it's quota (429) wait longer; if auth (401/403) just rotate
                time.sleep(2 if r.status_code in (401, 403) else wait)
                continue
            r.raise_for_status()
            payload = r.json()
            data = payload.get("data") or []
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(data)
            return df
        except requests.exceptions.RequestException as e:
            last_err = str(e)
            wait = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
            time.sleep(wait)
            continue
        except ValueError as e:
            last_err = f"JSON parse: {e}"
            time.sleep(2)
            continue

    raise RuntimeError(f"fetch failed after {max_retries} attempts: {last_err}")


def fetch_country_year(reporter_iso2: str, partner_iso2: str, year: int,
                       flow: str, pool: KeyPool, hs_codes: list[str]) -> pd.DataFrame:
    """HS2 chunked fetch — bypasses 100k row per-call limit."""
    parts = []
    consec_fail = 0
    reporter_code = str(M49[reporter_iso2])
    partner_code = "0" if partner_iso2 == "WORLD" else str(M49[partner_iso2])

    for hs2 in hs_codes:
        try:
            df = fetch_comtrade(reporter_code, partner_code, str(year), flow, hs2, pool)
            if not df.empty:
                if len(df) >= TRUNCATION_THRESHOLD:
                    print(f"      [warn] HS{hs2} returned {len(df):,} rows (threshold "
                          f"{TRUNCATION_THRESHOLD:,}) — possibly truncated")
                parts.append(df)
            consec_fail = 0
            time.sleep(CALL_DELAY)
        except Exception as e:
            print(f"      [fail] HS{hs2}: {e} ({pool.status()})")
            consec_fail += 1
            if consec_fail >= 8 or pool.all_dead():
                print(f"      [abort] {consec_fail} consecutive fails or all keys dead — stopping chunked fetch")
                break

    if not parts:
        return pd.DataFrame()
    return pd.concat(parts, ignore_index=True)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def file_ok(path: Path, min_bytes: int = 100) -> bool:
    return path.exists() and path.stat().st_size >= min_bytes


def count_rows(path: Path) -> int:
    if not path.exists():
        return -1
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return -1


def needs_refetch(path: Path) -> bool:
    n = count_rows(path)
    return n < 0 or n >= TRUNCATION_THRESHOLD


# -----------------------------------------------------------------------------
# Download workflows
# -----------------------------------------------------------------------------

def download_kr_cn(years: list[int], pool: KeyPool, hs_codes: list[str]) -> dict:
    """Korea-China bilateral, M and X."""
    KR_CN_DIR.mkdir(parents=True, exist_ok=True)
    log = []
    for year in years:
        for direction, flow in [("KR_imp_from_CN", "M"), ("KR_exp_to_CN", "X")]:
            out = KR_CN_DIR / f"{direction}_{year}.csv"
            if file_ok(out) and not needs_refetch(out):
                print(f"  [skip] {direction} {year} ({count_rows(out):,} rows)")
                log.append({"set": "kr_cn", "direction": direction, "year": year,
                            "rows": count_rows(out), "status": "skip"})
                continue
            print(f"  [fetch] {direction} {year} (HS chunked)")
            try:
                df = fetch_country_year("KR", "CN", year, flow, pool, hs_codes)
                if df.empty:
                    log.append({"set": "kr_cn", "direction": direction, "year": year,
                                "rows": 0, "status": "empty"})
                    print(f"    -> empty")
                    continue
                df.to_csv(out, index=False, encoding="utf-8-sig")
                print(f"    -> {len(df):,} rows -> {out.name}")
                log.append({"set": "kr_cn", "direction": direction, "year": year,
                            "rows": len(df), "status": "ok"})
            except Exception as e:
                print(f"    [error] {e}")
                log.append({"set": "kr_cn", "direction": direction, "year": year,
                            "rows": 0, "status": f"err:{e}"})
                if pool.all_dead():
                    print("  [abort] all keys exhausted")
                    return {"log": log, "aborted": True}
    return {"log": log, "aborted": False}


def download_adh_china(years: list[int], pool: KeyPool, hs_codes: list[str]) -> dict:
    """ADH 8 OHIE <- China imports."""
    ADH_DIR.mkdir(parents=True, exist_ok=True)
    log = []
    for iso in ADH_8:
        for year in years:
            out = ADH_DIR / f"{iso}_{year}.csv"
            if file_ok(out) and not needs_refetch(out):
                print(f"  [skip] {iso} {year} ({count_rows(out):,} rows)")
                log.append({"set": "adh", "reporter": iso, "year": year,
                            "rows": count_rows(out), "status": "skip"})
                continue
            print(f"  [fetch] {iso} <- CN {year} (HS chunked)")
            try:
                df = fetch_country_year(iso, "CN", year, "M", pool, hs_codes)
                if df.empty:
                    log.append({"set": "adh", "reporter": iso, "year": year,
                                "rows": 0, "status": "empty"})
                    print("    -> empty")
                    continue
                df.to_csv(out, index=False, encoding="utf-8-sig")
                print(f"    -> {len(df):,} rows -> {out.name}")
                log.append({"set": "adh", "reporter": iso, "year": year,
                            "rows": len(df), "status": "ok"})
            except Exception as e:
                print(f"    [error] {e}")
                log.append({"set": "adh", "reporter": iso, "year": year,
                            "rows": 0, "status": f"err:{e}"})
                if pool.all_dead():
                    print("  [abort] all keys exhausted")
                    return {"log": log, "aborted": True}
    return {"log": log, "aborted": False}


def download_cn_world(years: list[int], pool: KeyPool, hs_codes: list[str]) -> dict:
    """China -> World exports (alternative IV)."""
    CN_WORLD_DIR.mkdir(parents=True, exist_ok=True)
    log = []
    for year in years:
        out = CN_WORLD_DIR / f"CN_exp_world_{year}.csv"
        if file_ok(out) and not needs_refetch(out):
            print(f"  [skip] CN->World {year} ({count_rows(out):,} rows)")
            log.append({"set": "cn_world", "year": year,
                        "rows": count_rows(out), "status": "skip"})
            continue
        print(f"  [fetch] CN -> World {year} (HS chunked)")
        try:
            df = fetch_country_year("CN", "WORLD", year, "X", pool, hs_codes)
            if df.empty:
                log.append({"set": "cn_world", "year": year, "rows": 0, "status": "empty"})
                print("    -> empty")
                continue
            df.to_csv(out, index=False, encoding="utf-8-sig")
            print(f"    -> {len(df):,} rows -> {out.name}")
            log.append({"set": "cn_world", "year": year, "rows": len(df), "status": "ok"})
        except Exception as e:
            print(f"    [error] {e}")
            log.append({"set": "cn_world", "year": year, "rows": 0, "status": f"err:{e}"})
            if pool.all_dead():
                print("  [abort] all keys exhausted")
                return {"log": log, "aborted": True}
    return {"log": log, "aborted": False}


# -----------------------------------------------------------------------------
# KITA cross-check
# -----------------------------------------------------------------------------

def kita_cross_check(kr_cn_full_hs: bool) -> list[dict]:
    """KITA cross-check, mode-aware.

    Full-HS mode (HS 01-99): compare Comtrade total vs KITA total directly, ±5% PASS.
    Mfg-only mode (HS 28-97): compare Comtrade mfg-only vs KITA × KR_CN_MFG_SHARE,
                              ±10% PASS (manufacturing share is approximate).
    """
    results = []
    if kr_cn_full_hs:
        threshold_pass, threshold_warn = 5.0, 10.0
        share = 1.0
        mode_label = "full-HS"
    else:
        threshold_pass, threshold_warn = 10.0, 20.0
        share = KR_CN_MFG_SHARE
        mode_label = f"mfg-only (vs KITA × {KR_CN_MFG_SHARE:.2f})"

    for year_str, official_musd in KITA_KR_CN_IMPORT.items():
        f = KR_CN_DIR / f"KR_imp_from_CN_{year_str}.csv"
        if not file_ok(f):
            results.append({"year": year_str, "comtrade_mUSD": None,
                            "kita_mUSD": official_musd,
                            "kita_adjusted_mUSD": official_musd * share,
                            "diff_pct": None, "status": "missing", "mode": mode_label})
            continue
        try:
            df = pd.read_csv(f, low_memory=False)
            if "primaryValue" in df.columns:
                total_usd = df["primaryValue"].fillna(0).astype(float).sum()
            elif "TradeValue" in df.columns:
                total_usd = df["TradeValue"].fillna(0).astype(float).sum()
            else:
                results.append({"year": year_str, "comtrade_mUSD": None,
                                "kita_mUSD": official_musd,
                                "kita_adjusted_mUSD": official_musd * share,
                                "diff_pct": None, "status": "no_value_col", "mode": mode_label})
                continue
            ct_musd = total_usd / 1e6
            kita_adj = official_musd * share
            diff = (ct_musd - kita_adj) / kita_adj * 100
            if abs(diff) < threshold_pass:
                status = "PASS"
            elif abs(diff) < threshold_warn:
                status = "WARN"
            else:
                status = "FAIL"
            results.append({"year": year_str, "comtrade_mUSD": ct_musd,
                            "kita_mUSD": official_musd,
                            "kita_adjusted_mUSD": kita_adj,
                            "diff_pct": diff, "status": status, "mode": mode_label})
        except Exception as e:
            results.append({"year": year_str, "comtrade_mUSD": None,
                            "kita_mUSD": official_musd,
                            "kita_adjusted_mUSD": official_musd * share,
                            "diff_pct": None, "status": f"err:{e}", "mode": mode_label})
    return results


# -----------------------------------------------------------------------------
# Validation report
# -----------------------------------------------------------------------------

def write_validation_report(logs: dict, kita: list[dict], pool: KeyPool,
                            hs_summary: dict, years: list[int]) -> None:
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Stage 4A — Trade Collection Validation",
        "",
        f"- Years: {years[0]}-{years[-1]} ({len(years)})",
        f"- API keys loaded: {len(pool.keys)} (live at end: {len(pool.keys)-len(pool.dead)})",
        "",
        "## HS coverage by set",
        "",
        f"- KR <-> CN: {hs_summary['kr_cn']}",
        f"- ADH 8 <- CN: {hs_summary['adh']}",
        f"- CN -> World: {hs_summary['cn_world']}",
        "",
    ]

    if "kr_cn" in logs:
        ok = sum(1 for r in logs["kr_cn"]["log"] if r["status"] in ("ok", "skip"))
        tot = len(logs["kr_cn"]["log"])
        lines.append("## Set 1: KR <-> CN bilateral")
        lines.append("")
        lines.append(f"- {ok}/{tot} files OK")
        lines.append("")

    if "adh" in logs:
        ok = sum(1 for r in logs["adh"]["log"] if r["status"] in ("ok", "skip"))
        tot = len(logs["adh"]["log"])
        lines.append("## Set 2: ADH 8 <- CN imports")
        lines.append("")
        lines.append(f"- {ok}/{tot} files OK")
        lines.append("")

    if "cn_world" in logs:
        ok = sum(1 for r in logs["cn_world"]["log"] if r["status"] in ("ok", "skip"))
        tot = len(logs["cn_world"]["log"])
        lines.append("## Set 3: CN -> World exports")
        lines.append("")
        lines.append(f"- {ok}/{tot} files OK")
        lines.append("")

    if kita:
        mode = kita[0].get("mode", "")
        lines.append(f"## KITA Cross-Check (KR <- CN, mode={mode})")
        lines.append("")
        lines.append("| year | Comtrade (mUSD) | KITA full (mUSD) | KITA adj. (mUSD) | diff % | status |")
        lines.append("|------|----------------:|----------------:|----------------:|------:|:------:|")
        for r in kita:
            ct = f"{r['comtrade_mUSD']:,.0f}" if r["comtrade_mUSD"] is not None else "—"
            kita_adj = r.get("kita_adjusted_mUSD", r["kita_mUSD"])
            adj = f"{kita_adj:,.0f}" if kita_adj is not None else "—"
            d = f"{r['diff_pct']:+.2f}" if r["diff_pct"] is not None else "—"
            lines.append(f"| {r['year']} | {ct} | {r['kita_mUSD']:,} | {adj} | {d} | {r['status']} |")
        lines.append("")
        lines.append(f"- Pass threshold depends on mode: full-HS ±5%, mfg-only ±10% (vs KITA × {KR_CN_MFG_SHARE:.2f}).")
        lines.append("")

    VALIDATION_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  -> {VALIDATION_PATH}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kr-cn", action="store_true", help="Download KR<->CN")
    ap.add_argument("--adh", action="store_true", help="Download ADH 8 <- CN")
    ap.add_argument("--cn-world", action="store_true", help="Download CN -> World")
    ap.add_argument("--all", action="store_true", help="All three sets")
    ap.add_argument("--start-year", type=int, default=2000)
    ap.add_argument("--end-year", type=int, default=2024)
    # HS coverage: smart per-set defaults that can be overridden globally
    ap.add_argument("--all-hs", action="store_true",
                    help="Force HS 01-99 for ALL sets (overrides per-set defaults)")
    ap.add_argument("--mfg-only", action="store_true",
                    help="Force HS 28-97 for ALL sets (overrides per-set defaults)")
    ap.add_argument("--kr-cn-mfg-only", action="store_true",
                    help="Force HS 28-97 just for KR-CN (default: HS 01-99 for KITA validation)")
    ap.add_argument("--adh-all-hs", action="store_true",
                    help="Force HS 01-99 just for ADH (default: HS 28-97, ADH standard)")
    ap.add_argument("--cn-world-all-hs", action="store_true",
                    help="Force HS 01-99 just for CN-World (default: HS 28-97)")
    ap.add_argument("--cross-check", action="store_true", help="Run KITA cross-check")
    ap.add_argument("--comtrade-api-key", default=None,
                    help="Override Comtrade API key (else uses .env / env)")
    args = ap.parse_args()

    # If no specific set chosen, default to --all
    if not (args.kr_cn or args.adh or args.cn_world or args.all):
        args.all = True
    if args.all:
        args.kr_cn = args.adh = args.cn_world = True

    years = list(range(args.start_year, args.end_year + 1))

    # Resolve per-set HS coverage. Defaults:
    #   KR-CN  = HS 01-99 (full coverage for endogenous + KITA validation)
    #   ADH    = HS 28-97 (Pierce-Schott / ADH manufacturing standard)
    #   CN-World = HS 28-97 (alternative IV, mfg focus)
    # Global flags --all-hs / --mfg-only override everything.
    # Per-set flags --kr-cn-mfg-only / --adh-all-hs / --cn-world-all-hs override defaults.
    if args.all_hs:
        kr_cn_hs, adh_hs, cn_world_hs = HS2_ALL, HS2_ALL, HS2_ALL
    elif args.mfg_only:
        kr_cn_hs, adh_hs, cn_world_hs = HS2_MFG, HS2_MFG, HS2_MFG
    else:
        kr_cn_hs = HS2_MFG if args.kr_cn_mfg_only else HS2_ALL
        adh_hs = HS2_ALL if args.adh_all_hs else HS2_MFG
        cn_world_hs = HS2_ALL if args.cn_world_all_hs else HS2_MFG

    def hs_label(codes):
        if codes is HS2_ALL:
            return f"HS 01-99 (full, {len(codes)} chapters)"
        elif codes is HS2_MFG:
            return f"HS 28-97 (mfg, {len(codes)} chapters)"
        else:
            return f"HS custom ({len(codes)} chapters)"

    hs_summary = {
        "kr_cn": hs_label(kr_cn_hs),
        "adh": hs_label(adh_hs),
        "cn_world": hs_label(cn_world_hs),
    }
    kr_cn_full_hs = (kr_cn_hs is HS2_ALL)

    print("=" * 72)
    print("Stage 4A — Comtrade Trade Collection")
    print(f"  Years: {years[0]}-{years[-1]} ({len(years)} years)")
    print(f"  KR-CN     HS: {hs_summary['kr_cn']}")
    print(f"  ADH 8-CN  HS: {hs_summary['adh']}")
    print(f"  CN-World  HS: {hs_summary['cn_world']}")
    print(f"  Sets: KR-CN={args.kr_cn}, ADH={args.adh}, CN-World={args.cn_world}")
    print("=" * 72)

    # Load keys
    keys = collect_comtrade_keys(args.comtrade_api_key)
    if not keys:
        print("\n[ERROR] No Comtrade API keys found in CLI / env / .env")
        print(f"        Add COMTRADE_API_KEY to {DOTENV_PATH}")
        return 1
    print(f"\n[auth] {len(keys)} key(s) loaded:")
    for i, k in enumerate(keys, 1):
        print(f"  #{i}: ...{k[-4:]}")
    pool = KeyPool(keys)

    logs = {}

    # Set 1: KR-CN
    if args.kr_cn:
        print(f"\n{'-'*72}\n[Set 1] KR <-> CN bilateral\n{'-'*72}")
        logs["kr_cn"] = download_kr_cn(years, pool, kr_cn_hs)
        if logs["kr_cn"].get("aborted"):
            print("\n[ABORT] all keys exhausted; saving progress and exiting")
            write_validation_report(logs, [], pool, hs_summary, years)
            return 2

    # Set 2: ADH 8 <- CN
    if args.adh:
        print(f"\n{'-'*72}\n[Set 2] ADH 8 <- CN imports\n{'-'*72}")
        logs["adh"] = download_adh_china(years, pool, adh_hs)
        if logs["adh"].get("aborted"):
            print("\n[ABORT] all keys exhausted; saving progress and exiting")
            write_validation_report(logs, [], pool, hs_summary, years)
            return 2

    # Set 3: CN -> World
    if args.cn_world:
        print(f"\n{'-'*72}\n[Set 3] CN -> World exports\n{'-'*72}")
        logs["cn_world"] = download_cn_world(years, pool, cn_world_hs)
        if logs["cn_world"].get("aborted"):
            print("\n[ABORT] all keys exhausted; saving progress and exiting")
            write_validation_report(logs, [], pool, hs_summary, years)
            return 2

    # KITA cross-check (mode-aware: full-HS ±5% vs mfg-only ±10% with share adjustment)
    kita = []
    if args.cross_check:
        thr = "±5%" if kr_cn_full_hs else f"±10% (vs KITA × {KR_CN_MFG_SHARE:.2f})"
        print(f"\n{'-'*72}\n[Cross-check] KITA vs Comtrade (KR <- CN, {thr})\n{'-'*72}")
        kita = kita_cross_check(kr_cn_full_hs)
        for r in kita:
            ct = f"{r['comtrade_mUSD']:,.0f}M" if r["comtrade_mUSD"] is not None else "—"
            kita_adj = r.get("kita_adjusted_mUSD", r["kita_mUSD"])
            adj_label = f"KITA={r['kita_mUSD']:,}M"
            if kr_cn_full_hs is False:
                adj_label = f"KITA×{KR_CN_MFG_SHARE:.2f}={kita_adj:,.0f}M"
            d = f"{r['diff_pct']:+.2f}%" if r["diff_pct"] is not None else "—"
            print(f"  {r['year']}: Comtrade={ct} | {adj_label} | diff={d} [{r['status']}]")

    # Report
    write_validation_report(logs, kita, pool, hs_summary, years)

    print(f"\n{'='*72}\nDONE\n{'='*72}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
