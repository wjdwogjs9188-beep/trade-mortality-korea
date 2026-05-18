"""UN Comtrade Korea-China bilateral HS6 × 2000-2024 다운로드.

본 연구의 main treatment IV:
- Korea imports from China (flow=M)
- Korea exports to China (flow=X)

각 연도 2 query × 25년 = 50 calls.

출력:
 0_raw/comtrade_korea_china/KR_imp_from_CN_{year}.csv
 0_raw/comtrade_korea_china/KR_exp_to_CN_{year}.csv

사용법 (Windows PowerShell):
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\04_comtrade_korea_china.py
"""
import sys
import time
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))

from lib.comtrade_api import fetch_country_year
from lib.config import RAW_DIR

OUT_DIR = RAW_DIR / "comtrade_korea_china"
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2000, 2025))
LOG_FILE = OUT_DIR / "_download_log.csv"

def already_downloaded(direction: str, year: int) -> bool:
 f = OUT_DIR / f"{direction}_{year}.csv"
 return f.exists and f.stat.st_size > 100

def main:
 print(f"Korea-China bilateral, years {YEARS[0]}-{YEARS[-1]}")
 print(f"Total queries: {2 * len(YEARS)} (양방향)\n")

 log_rows = 
 for year in YEARS:
 for direction, flow in [("KR_imp_from_CN", "M"), ("KR_exp_to_CN", "X")]:
 if already_downloaded(direction, year):
 print(f" [skip] {direction} {year}")
 continue
 try:
 df = fetch_country_year("KR", "CN", year, flow)
 if df.empty:
 print(f" ⚠️ {direction} {year}: 응답 없음")
 log_rows.append({"direction": direction, "year": year, "rows": 0, "status": "empty"})
 continue
 out = OUT_DIR / f"{direction}_{year}.csv"
 df.to_csv(out, index=False, encoding="utf-8-sig")
 print(f" ✅ {direction} {year}: {len(df):,} rows")
 log_rows.append({"direction": direction, "year": year, "rows": len(df), "status": "ok"})
 except Exception as e:
 print(f" ❌ {direction} {year}: {e}")
 log_rows.append({"direction": direction, "year": year, "rows": 0, "status": f"ERR"})
 time.sleep(5)

 log_df = pd.DataFrame(log_rows)
 log_df.to_csv(LOG_FILE, index=False, encoding="utf-8-sig")
 print(f"\n{'='*70}")
 print(f"로그: {LOG_FILE}")

if __name__ == "__main__":
 main
