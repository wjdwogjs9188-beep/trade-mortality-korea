"""Step 2: 사망 microdata 27년치 시군구 코드 추출.

처리:
 - cp949 인코딩으로 27개 CSV 의 (시도, 시군구) 컬럼만 usecols 읽기
 - 1997-2022: raw_code = sido(2) + sigungu(3) zfill → 5자리
 - 2023: sigungu 자체가 5자리 — 그대로 사용
 - (year, raw_code, n_deaths) 분포 산출

산출:
 3_derived/sigungu/step2_raw_sigungu_by_year.csv
 columns: year, raw_code, sido_raw, sgg_raw, n_deaths
"""
from pathlib import Path
import sys

import pandas as pd
from tqdm import tqdm

ROOT = Path(r"C:/Users/82103/Downloads/trade_mortality_korea")
DATA_DIR = ROOT / "0_raw" / "mortality_kostat" / "사망사료 정리"
OUT_DIR = ROOT / "3_derived" / "sigungu"
OUT = OUT_DIR / "step2_raw_sigungu_by_year.csv"

SIDO_COL = "사망자주소행정구역시도코드"
SGG_COL = "사망자주소행정구역시군구코드"

def main -> int:
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")
 OUT_DIR.mkdir(parents=True, exist_ok=True)

 files = sorted(DATA_DIR.glob("*_사망_연간자료_B형_*.csv"))
 print(f"입력 {len(files)}개 CSV")
 if not files:
 print("⚠ 파일 없음", file=sys.stderr)
 return 1

 all_rows: list[pd.DataFrame] = 
 total_records = 0

 for f in tqdm(files, desc="years"):
 year = int(f.name[:4])
 df = pd.read_csv(
 f, encoding="cp949",
 usecols=[SIDO_COL, SGG_COL],
 dtype=str,
 on_bad_lines="warn",
 low_memory=False,
)
 df.columns = ["sido_raw", "sgg_raw"]

 # raw_code 통합
 if year <= 2022:
 # sido 2자리 + sgg 3자리 → 5자리 (zfill 안전장치)
 sido = df["sido_raw"].fillna("").str.strip.str.zfill(2)
 sgg = df["sgg_raw"].fillna("").str.strip.str.zfill(3)
 df["raw_code"] = sido + sgg
 else:
 # 2023: sgg 자체 5자리
 sido = df["sido_raw"].fillna("").str.strip.str.zfill(2)
 sgg = df["sgg_raw"].fillna("").str.strip
 df["raw_code"] = sgg.str.zfill(5)

 df["year"] = year
 # null/빈 raw_code 마스크
 df["is_missing"] = (df["raw_code"].str.strip.isin(["", "00000"])) | df["raw_code"].isna

 # 집계
 agg = (df.groupby(["year", "sido_raw", "sgg_raw", "raw_code", "is_missing"], dropna=False)
.size
.reset_index(name="n_deaths"))
 all_rows.append(agg)
 total_records += len(df)

 print(f"\n총 사망 레코드: {total_records:,}")

 out = pd.concat(all_rows, ignore_index=True)
 out = out.sort_values(["year", "raw_code"]).reset_index(drop=True)
 out.to_csv(OUT, index=False, encoding="utf-8-sig")
 print(f"저장: {OUT} ({len(out):,} rows)")

 # 요약 출력
 print("\n--- 연도별 unique raw_code 수 (결측 제외) ---")
 summary = (out[~out["is_missing"]]
.groupby("year")
.agg(n_unique=("raw_code", "nunique"),
 n_deaths=("n_deaths", "sum"))
.reset_index)
 print(summary.to_string(index=False))

 print("\n--- 결측·이상 raw_code 분포 (year, raw_code, n_deaths) ---")
 miss = out[out["is_missing"]]
 if not miss.empty:
 print(miss.to_string(index=False, max_rows=50))
 else:
 print("결측 없음")

 print("\n--- 2023 vs 2022 raw_code 길이 분포 (확인용) ---")
 for y in [2022, 2023]:
 sub = out[(out["year"] == y) & ~out["is_missing"]]
 lens = sub["raw_code"].str.len.value_counts.sort_index
 print(f" {y}: {dict(lens)}, n_unique={sub['raw_code'].nunique}")

 return 0

if __name__ == "__main__":
 sys.exit(main)
