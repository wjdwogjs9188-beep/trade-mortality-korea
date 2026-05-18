"""
Phase 1.2 (v08) — ECOS Test 1 macro 변수.

v07 → v08 (probe 결과: 402Y014=725 items, 401Y015=837 items → timeout 원인):
  - 402Y014 / 401Y015 의 root ITEM = '*AA' (총지수) 발견
  - main fetch: ITEM_CODE1='*AA' 만 호출 → 25년 × 12month = 300 rows 즉시 응답
  - GDP (200Y110): v05 csv 그대로 skip
  - sub-category robustness 가 후일 필요하면 별도 스크립트 (v09+)
"""
from __future__ import annotations
import sys, time
from pathlib import Path
from datetime import datetime
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import RAW_DIR, LOGS_DIR, ECOS_API_KEY, assert_api_key
from lib.ecos_api import search_statistic

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = RAW_DIR / "ecos_macro_extra"
LOG = LOGS_DIR / "data_collection" / f"{datetime.now():%Y-%m-%d}_phase1_ecos_v08.md"

BASE = "https://ecos.bok.or.kr/api/StatisticSearch"
TIMEOUT = 70


def fetch_with_item(stat: str, cycle: str, start: str, end: str, item1: str) -> pd.DataFrame:
    """단일 ITEM_CODE1 호출. URL 인코딩 (% 우회용)."""
    assert_api_key("ECOS", ECOS_API_KEY)
    # 한 번 fetch 로 충분 — item 좁혀서 응답 작음
    url = f"{BASE}/{ECOS_API_KEY}/json/kr/1/100000/{stat}/{cycle}/{start}/{end}/{item1}"
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    body = data.get("StatisticSearch", {})
    rows = body.get("row", []) or []
    if not rows:
        result = data.get("RESULT") or body.get("RESULT")
        if result:
            print(f"    [API msg] {result}", flush=True)
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if "DATA_VALUE" in df.columns:
        df["DATA_VALUE"] = pd.to_numeric(df["DATA_VALUE"], errors="coerce")
    return df


SPECS = [
    {
        "label": "분기GDP_지출_실질",
        "stat": "200Y110",
        "cycle": "Q",
        "fetch": lambda: search_statistic("200Y110", "Q", "2000Q1", "2024Q4"),
        "skip_if_exists": True,
    },
    {
        "label": "수출물가지수_총지수",
        "stat": "402Y014",
        "cycle": "M",
        "fetch": lambda: fetch_with_item("402Y014", "M", "200001", "202412", "*AA"),
    },
    {
        "label": "수입물가지수_총지수",
        "stat": "401Y015",
        "cycle": "M",
        "fetch": lambda: fetch_with_item("401Y015", "M", "200001", "202412", "*AA"),
    },
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log = [f"# Phase 1.2 v08 — ECOS Test 1 macro\n", f"_timestamp: {datetime.now().isoformat()}_\n\n"]
    overall_ok = True

    for spec in SPECS:
        label, stat, cycle = spec["label"], spec["stat"], spec["cycle"]
        if spec.get("skip_if_exists"):
            existing = list(OUT_DIR.glob(f"{stat}_*.csv"))
            if existing:
                print(f"\n=== {label} : {stat} — skip ({existing[0].name}) ===")
                log.append(f"## {label}\n- ⏭ skip (existing: `{existing[0].name}`)\n\n")
                continue

        print(f"\n=== {label} : {stat} ({cycle}) ===", flush=True)
        try:
            df = spec["fetch"]()
        except Exception as e:
            print(f"  ❌ {e}", flush=True)
            log.append(f"## {label}\n- ❌ `{stat}`: {str(e)[:120]}\n\n")
            overall_ok = False
            continue

        if df.empty:
            print(f"  ⚠️ empty", flush=True)
            log.append(f"## {label}\n- ⚠️ `{stat}`: empty\n\n")
            overall_ok = False
            continue

        fname = f"{stat}_{cycle}_2000_2024_{label}.csv"
        out = OUT_DIR / fname
        df.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"  ✅ {len(df):,} rows -> {fname}", flush=True)
        log.append(f"## {label}\n- ✅ `{stat}` ({cycle}): {len(df):,} rows -> `{fname}`\n")
        if "ITEM_NAME1" in df.columns:
            items = sorted(set(df["ITEM_NAME1"].dropna()))[:6]
            log.append(f"  - ITEM_NAME1: `{items}`\n")
        if "TIME" in df.columns:
            times = sorted(df["TIME"].dropna().astype(str).unique())
            log.append(f"  - TIME range: {times[0]} ~ {times[-1]} ({len(times)} 시점)\n")
        log.append("\n")

    LOG.write_text("".join(log), encoding="utf-8")
    print(f"\n[log] {LOG}", flush=True)
    return 0 if overall_ok else 2


if __name__ == "__main__":
    sys.exit(main())
