"""mediator_panel_marriage/education_v01 의 4 issue verify.

Issue 1: marital_code = '.' (MDIS missing) — 어느 시점에 분포하는지
Issue 2: 2005 anomaly (pop sum 100%) — marital_code 분포 by age 확인
Issue 3: h_code 522 (1990 261 + 나머지 union) — 시점별 unique h_code list
Issue 4: 1990 sigungu 2자리 → mapping 작성용 raw 코드 list

선행: 08_*_parse_crosstab 산출 parquet 존재

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\09_mediator_panel_validate.py

산출 (stdout):
 - 시점별 marital_code distribution (count, weight sum)
 - 시점별 education_code distribution
 - 시점별 unique h_code count + sample
 - 1990 unique h_code 전체 list (2자리 sigungu mapping 작성용)
 - 2005 anomaly 원인 진단 (marital_code by age)
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve.parents[2]
POP_DIR = ROOT / "3_derived" / "population"
RAW_DIR = ROOT / "0_raw" / "mdis_population_census"
DATA_43590 = RAW_DIR / "2%_표본_인구_20260430_43590_데이터"
DATA_65001 = RAW_DIR / "2%_표본_인구_20260504_65001_데이터"

def part1_marital_code_distribution(mar: pd.DataFrame) -> None:
 """Issue 1: marital_code 분포 by year."""
 print("\n" + "=" * 70)
 print("PART 1: marital_code distribution per year (cell count + weight sum)")
 print("=" * 70)
 for yr, sub in mar.groupby("year"):
 print(f"\n[{yr}] total: {len(sub):,} cells")
 dist = sub.groupby("marital_code").agg(
 cells=("population", "size"),
 pop=("population", "sum"),
)
 dist["pop_pct"] = dist["pop"] / dist["pop"].sum * 100
 print(dist.to_string)

def part2_education_code_distribution(edu: pd.DataFrame) -> None:
 """Issue 1b: education_code 분포 by year."""
 print("\n" + "=" * 70)
 print("PART 2: education_code distribution per year")
 print("=" * 70)
 for yr, sub in edu.groupby("year"):
 print(f"\n[{yr}] total: {len(sub):,} cells")
 dist = sub.groupby("education_code").agg(
 cells=("population", "size"),
 pop=("population", "sum"),
)
 dist["pop_pct"] = dist["pop"] / dist["pop"].sum * 100
 print(dist.to_string)

def part3_2005_anomaly_diagnosis -> None:
 """Issue 2: 2005 anomaly 원인 — raw CSV 의 marital_code by age 직접 확인."""
 print("\n" + "=" * 70)
 print("PART 3: 2005 anomaly diagnosis — marital_code by age in raw CSV")
 print("=" * 70)

 csv_2005 = DATA_65001 / "2005_2%_표본_인구_20260504_65001.csv"
 csv_2010 = DATA_65001 / "2010_2%_표본_인구_20260504_65001.csv"

 for label, csv_path, age_col, mar_col, weight_col in [
 ("2005", csv_2005, "만연령", "혼인상태코드", "가중값"),
 ("2010", csv_2010, "만연령", "혼인상태코드", "가중값"),
 ]:
 print(f"\n[{label}] {csv_path.name}")
 df = pd.read_csv(csv_path, encoding="cp949", dtype=str,
 usecols=[age_col, mar_col, weight_col], low_memory=False)
 df["age_int"] = pd.to_numeric(df[age_col], errors="coerce")
 df["weight"] = pd.to_numeric(df[weight_col], errors="coerce")

 # marital_code distribution by age band
 df["age_band_simple"] = pd.cut(df["age_int"],
 bins=[0, 14, 19, 29, 49, 64, 200],
 right=False,
 labels=["0-13", "14-18", "19-28", "29-48", "49-63", "64+"])

 print(f" marital_code by age band:")
 ct = (df.groupby(["age_band_simple", mar_col], observed=True)["weight"]
.sum.unstack(fill_value=0))
 print(ct.to_string)

 # 미성년 (15세 미만) 의 marital_code 분포
 minor = df[df["age_int"] < 15]
 print(f"\n 15세 미만 (n={len(minor):,}) 의 marital_code distribution:")
 print(minor[mar_col].value_counts(dropna=False).head(10).to_string)

def part4_h_code_inventory(mar: pd.DataFrame) -> None:
 """Issue 3: h_code 시점별 unique inventory."""
 print("\n" + "=" * 70)
 print("PART 4: h_code per-year inventory")
 print("=" * 70)

 h_by_year = {yr: set(sub["h_code"].unique) for yr, sub in mar.groupby("year")}

 print(f"\nUnique h_code count per year:")
 for yr in sorted(h_by_year):
 print(f" {yr}: {len(h_by_year[yr])}")

 # Intersection / Union
 all_yrs = sorted(h_by_year.keys)
 union = set.union(*h_by_year.values)
 intersection = set.intersection(*h_by_year.values)
 print(f"\n Union (모든 시점에 등장한 h_code): {len(union)}")
 print(f" Intersection (모든 시점 공통): {len(intersection)}")

 # 1990 vs 2000 의 차이
 if 1990 in h_by_year and 2000 in h_by_year:
 only_1990 = h_by_year[1990] - h_by_year[2000]
 only_2000 = h_by_year[2000] - h_by_year[1990]
 print(f"\n 1990 only (not in 2000): {len(only_1990)} → sample {sorted(only_1990)[:10]}")
 print(f" 2000 only (not in 1990): {len(only_2000)} → sample {sorted(only_2000)[:10]}")

def part5_1990_sigungu_for_mapping(mar: pd.DataFrame) -> None:
 """Issue 4: 1990 unique h_code 전체 list (2자리 → 3자리 mapping 작성용)."""
 print("\n" + "=" * 70)
 print("PART 5: 1990 unique h_code 전체 list (mapping 작성용)")
 print("=" * 70)

 h_1990 = sorted(mar[mar["year"] == 1990]["h_code"].unique)
 print(f"\n1990 unique h_code: {len(h_1990)}")
 print(f"format: 5 char string ('11011' = sido 11 + sigungu 011)")
 print(f"\nFull list (10 per row):")
 for i in range(0, len(h_1990), 10):
 print(" " + ", ".join(h_1990[i:i+10]))

 # 시도 별 분류
 print("\n시도별 1990 sigungu 수:")
 sido_count = {}
 for h in h_1990:
 sido = h[:2]
 sido_count[sido] = sido_count.get(sido, 0) + 1
 sido_names = {"11": "서울", "21": "부산", "22": "대구", "23": "인천",
 "24": "광주", "25": "대전", "31": "경기", "32": "강원",
 "33": "충북", "34": "충남", "35": "전북", "36": "전남",
 "37": "경북", "38": "경남", "39": "제주"}
 for sido, n in sorted(sido_count.items):
 print(f" {sido} {sido_names.get(sido, '?')}: {n}")

def main -> int:
 print("=" * 70)
 print("mediator_panel_v01 4 issue validation")
 print("=" * 70)

 mar = pd.read_parquet(POP_DIR / "mediator_panel_marriage_v01.parquet")
 edu = pd.read_parquet(POP_DIR / "mediator_panel_education_v01.parquet")

 print(f"\nmarriage panel: {len(mar):,} rows")
 print(f"education panel: {len(edu):,} rows")

 part1_marital_code_distribution(mar)
 part2_education_code_distribution(edu)
 part3_2005_anomaly_diagnosis
 part4_h_code_inventory(mar)
 part5_1990_sigungu_for_mapping(mar)

 print("\n" + "=" * 70)
 print("완료. 다음 step:")
 print(" - PART 1/2: '.' 또는 missing code drop logic 결정")
 print(" - PART 3: 2005 anomaly 원인에 따라 age filter (15+ 또는 6+) 적용")
 print(" - PART 4/5: 1990 sigungu mapping table 작성 + sigungu_crosswalk_v2 align")
 print("=" * 70)
 return 0

if __name__ == "__main__":
 sys.exit(main)
