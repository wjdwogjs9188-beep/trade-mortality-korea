"""
Pre-WTO Comtrade 1992-1996 다운 — pre-WTO placebo 입력
========================================================

Comtrade API 로 KR-CN bilateral 1992-1996 다운.
Pre-WTO China (2001 12월 가입 전) 시점의 KR-CN trade flow 가
1990s 시군구 mortality 와 무관해야 본 paper 의 BHJ shock-only
exogeneity 가 직접 입증.

5 year × {imp, exp} = 10 csv 다운.

Comtrade API endpoint: https://comtradeapi.un.org/data/v1/get/
Reporter: KOR (410), Partner: CHN (156)
HS classification: HS92 (이 시점 가용한 가장 detailed)

Author: R-A
Date  : 2026-05-05
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import os
import requests
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
OUT_DIR = PROJ / "0_raw" / "comtrade_korea_china"

# .env 로딩 (Comtrade API key)
ENV_PATH = PROJ / ".env"
COMTRADE_KEY = None
if ENV_PATH.exists():
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("COMTRADE_API_KEY=") and "#" not in line:
            COMTRADE_KEY = line.split("=", 1)[1].strip()
            break

if not COMTRADE_KEY:
    # fallback: env
    COMTRADE_KEY = os.environ.get("COMTRADE_API_KEY")

if not COMTRADE_KEY:
    print("[FAIL] COMTRADE_API_KEY .env 또는 env 변수 부재")
    sys.exit(1)

print(f"[OK] Comtrade key loaded: {COMTRADE_KEY[:8]}...")

# Comtrade endpoint
BASE = "https://comtradeapi.un.org/data/v1/get/C/A/HS"

def download_year_flow(year: int, flow_code: str, label: str) -> Path | None:
    """
    flow_code: 'M' = imports, 'X' = exports
    label: filename suffix (imp_from / exp_to)
    """
    out_path = OUT_DIR / f"KR_{label}_CN_{year}.csv"
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"[skip] {out_path.name} (already exists, {out_path.stat().st_size/1024:.0f} KB)")
        return out_path

    params = {
        "subscription-key": COMTRADE_KEY,
        "reporterCode": "410",  # Korea
        "partnerCode": "156",   # China
        "period": str(year),
        "flowCode": flow_code,
        "cmdCode": "AG6",       # HS 6-digit
        "freqCode": "A",        # annual
        "typeCode": "C",        # commodity
        "clCode": "HS",
        "partner2Code": "0",
        "customsCode": "C00",
        "motCode": "0",
        "format": "csv",
    }
    url = f"{BASE}/{year}/410/156"
    print(f"[GET] {label} {year} ...")
    try:
        r = requests.get(BASE, params=params, timeout=120)
        r.raise_for_status()
    except Exception as e:
        print(f"  [FAIL] {e}")
        return None

    # Comtrade returns JSON sometimes; csv if format=csv specified
    content = r.text
    if content.startswith("<") or "<html" in content[:100].lower():
        print(f"  [FAIL] HTML response (likely error): {content[:200]}")
        return None
    if len(content) < 200:
        print(f"  [WARN] short response: {content}")
        return None

    out_path.write_text(content, encoding="utf-8")
    print(f"  [OK] {out_path.name} ({out_path.stat().st_size/1024:.0f} KB)")
    return out_path


def main():
    print("=" * 60)
    print("Pre-WTO Comtrade 1992-1996 download")
    print("=" * 60)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for year in range(1992, 1997):
        for flow_code, label in [("M", "imp_from"), ("X", "exp_to")]:
            p = download_year_flow(year, flow_code, label)
            results.append({"year": year, "label": label, "ok": p is not None})
            time.sleep(2)  # rate limit 안전

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    n_ok = df["ok"].sum()
    print(f"\nTotal: {n_ok}/10 csv downloaded.")
    if n_ok < 10:
        print("일부 실패. API 한도 확인 또는 다른 key 시도.")


if __name__ == "__main__":
    main()
