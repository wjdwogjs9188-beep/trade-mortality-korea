"""UN Comtrade China → World HS6 export (alternative IV).

배경: earlier paper version 의 China-World instrument 는 "중국 supply 확장이 한국이 제3시장에서
share 잃게 하는" adverse force 를 측정. Korea-China bilateral 와 다른 mechanism.

출력: 0_raw/comtrade_china_world/CN_exp_world_{year}.csv

사용법 (Windows PowerShell):
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\05_comtrade_china_world.py
"""
import sys
import time
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))

from lib.comtrade_api import fetch
from lib.config import RAW_DIR

OUT_DIR = RAW_DIR / "comtrade_china_world"
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2000, 2025))

def already_downloaded(year: int) -> bool:
 f = OUT_DIR / f"CN_exp_world_{year}.csv"
 return f.exists and f.stat.st_size > 100

def main:
 print(f"China → World HS6 exports, years {YEARS[0]}-{YEARS[-1]}")
 print(f"Total queries: {len(YEARS)}\n")

 log_rows = 
 for year in YEARS:
 if already_downloaded(year):
 print(f" [skip] {year}")
 continue
 try:
 df = fetch(
 reporter_code="156", # China
 partner_code="0", # 0 = World
 period=str(year),
 flow_code="X",
 cmd_code="AG6",
)
 if df.empty:
 print(f" ⚠️ {year}: 응답 없음")
 log_rows.append({"year": year, "rows": 0, "status": "empty"})
 continue
 out = OUT_DIR / f"CN_exp_world_{year}.csv"
 df.to_csv(out, index=False, encoding="utf-8-sig")
 print(f" ✅ {year}: {len(df):,} rows")
 log_rows.append({"year": year, "rows": len(df), "status": "ok"})
 except Exception as e:
 print(f" ❌ {year}: {e}")
 log_rows.append({"year": year, "rows": 0, "status": f"ERR"})
 time.sleep(5)

 log_df = pd.DataFrame(log_rows)
 log_df.to_csv(OUT_DIR / "_download_log.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
 main
