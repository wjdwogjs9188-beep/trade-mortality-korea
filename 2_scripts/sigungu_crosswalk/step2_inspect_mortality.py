"""Step 2 점검: 사망 microdata 27년치 인코딩·헤더·시군구 컬럼 위치 파악.

각 연도 첫 1MB 만 읽고 컬럼명·첫 5행 출력. 시군구 컬럼이름 후보 식별.
"""
from pathlib import Path
import chardet
import pandas as pd

DATA_DIR = Path(r"C:/Users/82103/Downloads/trade_mortality_korea/0_raw/mortality_kostat/사망사료 정리")

files = sorted(DATA_DIR.glob("*_사망_연간자료_B형_*.csv"))
print(f"총 {len(files)}개 CSV")

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

for f in files:
 year = int(f.name[:4])
 if year not in {1997, 2000, 2009, 2010, 2014, 2022, 2023}:
 continue
 print(f"\n{'='*80}\n{year}:: {f.name}")
 with open(f, "rb") as fp:
 raw = fp.read(100_000)
 enc_guess = chardet.detect(raw)
 print(f" size={f.stat.st_size:,} enc_guess={enc_guess}")

 # cp949 / utf-8 둘 다 시도
 for enc in ["cp949", "utf-8-sig", "utf-8"]:
 try:
 df = pd.read_csv(f, encoding=enc, nrows=3, dtype=str)
 print(f" ✓ {enc} 읽기 성공, {df.shape[1]}컬럼")
 print(f" columns: {list(df.columns)}")
 print(f" row0: {df.iloc[0].to_dict}")
 break
 except Exception as e:
 print(f" ✗ {enc}: {type(e).__name__}: {str(e)[:120]}")
