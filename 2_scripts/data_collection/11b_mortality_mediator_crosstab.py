"""mortality microdata → mediator-specific cross-tab (numerator panel).

Validation issue M1, M2 fix 통합:
 - M1: age_band 25-64 (working-age) filter — mediator panel 과 align
 - M2: sigungu_crosswalk_v2 적용 — mortality_panel_v02_1 의 229 h_code 와 align

산출 2 panel (paper § 5.2 mediator-specific mortality numerator):
 3_derived/mortality/mortality_marital_panel_v01.parquet
 columns: h_code, year, sex_code, age_band, marital_code, cause_104, deaths
 3_derived/mortality/mortality_education_panel_v01.parquet
 columns: h_code, year, sex_code, age_band, education_band, cause_104, deaths

이후 12 단계: numerator panel + mediator panel (denominator) merge → mediator-specific mortality rate

선행:
 11a_mortality_microdata_parse.py 완료 (mortality_microdata_cleaned_v01.parquet)
 10b_mediator_panel_education_v03.py 완료 (3 카테고리 align)

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\11b_mortality_mediator_crosstab.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve.parents[2]
MORT_DIR = ROOT / "3_derived" / "mortality"
XW_PATH = ROOT / "1_codebooks" / "sigungu_crosswalk_v2.csv"

CLEANED_PATH = MORT_DIR / "mortality_microdata_cleaned_v01.parquet"
MAR_OUT = MORT_DIR / "mortality_marital_panel_v01.parquet"
EDU_OUT = MORT_DIR / "mortality_education_panel_v01.parquet"

# Working-age 25-64 (mediator panel 과 일치)
WORKING_AGE_BANDS = [
 "25-29", "30-34", "35-39", "40-44",
 "45-49", "50-54", "55-59", "60-64",
]

def apply_sigungu_crosswalk(df: pd.DataFrame, xw: pd.DataFrame) -> pd.DataFrame:
 """mortality h_code → sigungu_crosswalk_v2 align (분구 시군구 합산).

 xw column: raw_code, h_code (target), year
 """
 xw["year"] = pd.to_numeric(xw["year"], errors="coerce")
 df_m = df.merge(
 xw[["raw_code", "h_code", "year"]].rename(columns={"h_code": "h_code_aligned"}),
 left_on=["h_code", "year"], right_on=["raw_code", "year"], how="left"
)
 n_missing = df_m["h_code_aligned"].isna.sum
 print(f" crosswalk unmatched: {n_missing:,} / {len(df_m):,} ({100*n_missing/len(df_m):.2f}%)")

 # unmatched 는 raw 그대로 keep
 df_m["h_code"] = df_m["h_code_aligned"].fillna(df_m["h_code"])
 df_m = df_m.drop(columns=["raw_code", "h_code_aligned"])
 return df_m

def main -> int:
 print("=" * 70)
 print("11b: mortality → mediator-specific cross-tab (marital + education)")
 print("=" * 70)

 # Step 1: Read cleaned
 print(f"\n[1] read {CLEANED_PATH.name}")
 df = pd.read_parquet(CLEANED_PATH)
 print(f" rows: {len(df):,}, unique h_code: {df['h_code'].nunique}, "
 f"years: {df['year'].min}-{df['year'].max}")

 # Step 2: age_band working-age filter (M1 fix)
 print(f"\n[2] working-age 25-64 filter (M1 fix)")
 before = len(df)
 df["age_band"] = df["age_band"].astype(str)
 df = df[df["age_band"].isin(WORKING_AGE_BANDS)].copy
 print(f" {before:,} → {len(df):,} ({100*len(df)/before:.1f}%)")

 # Step 3: sigungu_crosswalk_v2 적용 (M2 fix)
 print(f"\n[3] sigungu_crosswalk_v2 적용 (M2 fix)")
 if XW_PATH.exists:
 xw = pd.read_csv(XW_PATH, dtype=str)
 print(f" xw loaded: {len(xw):,} rows, {xw['raw_code'].nunique} raw_code, "
 f"{xw['h_code'].nunique} h_code")
 before_h = df["h_code"].nunique
 df = apply_sigungu_crosswalk(df, xw)
 after_h = df["h_code"].nunique
 print(f" unique h_code: {before_h} → {after_h}")
 else:
 print(f" [WARN] {XW_PATH} 없음 — crosswalk skip (raw h_code 그대로)")

 # Step 4: cross-tab marital × cause_104
 print(f"\n[4] marital × cause_104 cross-tab (numerator panel)")
 mar_panel = (df.groupby(
 ["h_code", "year", "sex_code", "age_band", "marital_code", "cause_104"],
 observed=True
).size.reset_index(name="deaths"))
 print(f" cells: {len(mar_panel):,}")
 print(f" total deaths: {mar_panel['deaths'].sum:,}")

 mar_panel.to_parquet(MAR_OUT, index=False)
 print(f" [save] {MAR_OUT.name} ({MAR_OUT.stat.st_size/1024:.2f} KB)")

 # Step 5: cross-tab education × cause_104
 print(f"\n[5] education × cause_104 cross-tab (numerator panel)")
 edu_panel = (df.groupby(
 ["h_code", "year", "sex_code", "age_band", "education_band", "cause_104"],
 observed=True
).size.reset_index(name="deaths"))
 print(f" cells: {len(edu_panel):,}")
 print(f" total deaths: {edu_panel['deaths'].sum:,}")

 edu_panel.to_parquet(EDU_OUT, index=False)
 print(f" [save] {EDU_OUT.name} ({EDU_OUT.stat.st_size/1024:.2f} KB)")

 # Validation summary
 print("\n" + "=" * 70)
 print("VALIDATION SUMMARY")
 print("=" * 70)

 print(f"\n[marital panel] per-year:")
 for yr, sub in mar_panel.groupby("year"):
 print(f" {yr}: {len(sub):,} cells, {sub['h_code'].nunique} h_code, "
 f"deaths sum {sub['deaths'].sum:,}")

 print(f"\n[education panel] per-year:")
 for yr, sub in edu_panel.groupby("year"):
 print(f" {yr}: {len(sub):,} cells, {sub['h_code'].nunique} h_code, "
 f"deaths sum {sub['deaths'].sum:,}")

 # Deaths of despair check (cause_104: 102 자살, 101 약물, 057 정신, 081 간)
 print(f"\n[deaths of despair] cause_104 별 합계 (working-age 25-64):")
 for cause, label in [("102", "자살"), ("101", "약물"), ("057", "정신"), ("081", "간")]:
 n = mar_panel[mar_panel["cause_104"] == cause]["deaths"].sum
 print(f" {cause} {label}: {n:,}")

 print("\n" + "=" * 70)
 print("완료. 다음:")
 print(" 12_mediator_specific_mortality_rate.py:")
 print(" numerator (marital/education panel) / denominator (mediator panel)")
 print(" → mediator-specific mortality rate panel")
 print("=" * 70)

 return 0

if __name__ == "__main__":
 sys.exit(main)
