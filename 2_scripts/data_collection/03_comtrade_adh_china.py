"""UN Comtrade ADH 표준 8 국가 × China imports HS6 × 2000-2024 다운로드.

ADH 8 = Australia, Denmark, Finland, Germany, Japan, New Zealand, Spain, Switzerland

배경: 기존 222222222.csv 는
- 9년치만 (2000-2008)
- G8 (CA/FR/DE/AU/IT/JP/GB/US) 사용 (ADH 아님)
- 286,182 행

이 스크립트는 ADH 표준 8국 × 25년 × HS6 panel 새로 구축.
출력: 0_raw/comtrade_adh_china/{ISO2}_{YEAR}.csv

사용법 (Windows PowerShell):
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\03_comtrade_adh_china.py
"""
import sys
import time
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))

from lib.comtrade_api import ADH_8, fetch_adh_china_imports
from lib.config import RAW_DIR

OUT_DIR = RAW_DIR / "comtrade_adh_china"
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2000, 2025)) # 25년
LOG_FILE = OUT_DIR / "_download_log.csv"

def already_downloaded(reporter: str, year: int) -> bool:
 f = OUT_DIR / f"{reporter}_{year}.csv"
 return f.exists and f.stat.st_size > 100

def main:
 print(f"ADH 8 = {ADH_8}")
 print(f"Years = {YEARS[0]}-{YEARS[-1]} ({len(YEARS)}년)")
 print(f"Total queries: {len(ADH_8) * len(YEARS)}\n")

 log_rows = 
 successes = 0
 fails = 0

 for reporter in ADH_8:
 for year in YEARS:
 if already_downloaded(reporter, year):
 print(f" [skip] {reporter} {year}")
 continue
 try:
 from lib.comtrade_api import fetch_country_year
 df = fetch_country_year(reporter, "CN", year, "M")
 if df.empty:
 print(f" ⚠️ {reporter} {year}: 응답 없음")
 log_rows.append({"reporter": reporter, "year": year, "rows": 0, "status": "empty"})
 fails += 1
 continue
 out = OUT_DIR / f"{reporter}_{year}.csv"
 df.to_csv(out, index=False, encoding="utf-8-sig")
 print(f" ✅ {reporter} {year}: {len(df):,} rows → {out.name}")
 log_rows.append({"reporter": reporter, "year": year, "rows": len(df), "status": "ok"})
 successes += 1
 except Exception as e:
 print(f" ❌ {reporter} {year}: {e}")
 log_rows.append({"reporter": reporter, "year": year, "rows": 0, "status": f"ERR: {e}"})
 fails += 1
 # rate limit 가능, 잠시 대기
 time.sleep(5)

 # log 저장
 log_df = pd.DataFrame(log_rows)
 log_df.to_csv(LOG_FILE, index=False, encoding="utf-8-sig")
 print(f"\n{'='*70}")
 print(f"완료: {successes} 성공, {fails} 실패")
 print(f"로그: {LOG_FILE}")

if __name__ == "__main__":
 main
