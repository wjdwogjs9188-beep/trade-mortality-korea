"""mediator panel v01 → v02 cleaning + alignment.

Decisions (사용자 권고 수락):
 a) 1990 drop — 행정구역 mismatch + paper 시점 (1997-2024) 외
 b) age filter: working-age 25-64 — DGHP 2017 mediation 표준
 c) education 4 카테고리:
 1: 노HS (raw 1+2+3 = 무학/초등/중학)
 2: HS (raw 4 = 고등학교)
 3: 전문대 (raw 5 = 대학 2/3년제)
 4: 대졸+ (raw 6+7+8 = 대학 4년제 + 석사 + 박사)
 d) sigungu_crosswalk_v2 적용 — mortality panel v02_1 의 hybrid sigungu merge 와 일치

Input:
 3_derived/population/mediator_panel_marriage_v01.parquet
 3_derived/population/mediator_panel_education_v01.parquet
 1_codebooks/sigungu_crosswalk_v2.csv

Output:
 3_derived/population/mediator_panel_marriage_v02.parquet
 3_derived/population/mediator_panel_education_v02.parquet
 3_derived/population/mediator_panel_v02_validation.md

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\10_mediator_panel_clean_align.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve.parents[2]
POP_DIR = ROOT / "3_derived" / "population"
XW_PATH = ROOT / "1_codebooks" / "sigungu_crosswalk_v2.csv"

# ────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────

# Working-age age bands (25-64)
WORKING_AGE_BANDS = [
 "25-29", "30-34", "35-39", "40-44",
 "45-49", "50-54", "55-59", "60-64",
]

# Marriage 4 카테고리 (raw KOSIS 코드 그대로)
VALID_MARITAL = {"1", "2", "3", "4"} # 1미혼 2배우자 3사별 4이혼

# Education 4 카테고리 매핑 (raw → 표준)
EDU_REMAP = {
 "1": "1.NoHS", # 무학
 "2": "1.NoHS", # 초등
 "3": "1.NoHS", # 중학
 "4": "2.HS", # 고등학교
 "5": "3.SomeCollege", # 대학 2/3년제
 "6": "4.Bachelor+", # 대학 4년제
 "7": "4.Bachelor+", # 석사
 "8": "4.Bachelor+", # 박사
}

# Year keep (1990 drop)
YEARS_KEEP = [1995, 2000, 2005, 2010, 2015, 2020]

# ────────────────────────────────────────────────────────
# Functions
# ────────────────────────────────────────────────────────

def filter_year_age(df: pd.DataFrame) -> pd.DataFrame:
 """Year >= 1995 + age_band working-age (25-64) filter."""
 df = df[df["year"].isin(YEARS_KEEP)].copy
 df["age_band"] = df["age_band"].astype(str)
 df = df[df["age_band"].isin(WORKING_AGE_BANDS)].copy
 return df

def clean_marriage(mar_v01: pd.DataFrame) -> pd.DataFrame:
 """Marriage panel cleaning: '.' drop + working-age + valid code."""
 print("\n[1] Marriage panel cleaning")
 print(f" v01 input: {len(mar_v01):,} rows")

 mar = filter_year_age(mar_v01)
 print(f" after year/age filter: {len(mar):,} rows")

 mar["marital_code"] = mar["marital_code"].astype(str).str.strip
 mar = mar[mar["marital_code"].isin(VALID_MARITAL)].copy
 print(f" after marital_code filter (1/2/3/4): {len(mar):,} rows")

 return mar

def clean_education(edu_v01: pd.DataFrame) -> pd.DataFrame:
 """Education panel cleaning: 4 카테고리 통합 + working-age."""
 print("\n[2] Education panel cleaning")
 print(f" v01 input: {len(edu_v01):,} rows")

 edu = filter_year_age(edu_v01)
 print(f" after year/age filter: {len(edu):,} rows")

 edu["education_code"] = edu["education_code"].astype(str).str.strip
 edu["education_band"] = edu["education_code"].map(EDU_REMAP)
 before = len(edu)
 edu = edu.dropna(subset=["education_band"])
 print(f" after education code remap (drop unmapped): {before:,} → {len(edu):,}")

 # Re-aggregate after band remap (raw 1+2+3 → NoHS 합산)
 grouped = (edu.groupby(
 ["h_code", "year", "sex_code", "age_band", "education_band"], observed=True
)["population"].sum.reset_index)
 print(f" after re-aggregate to 4 bands: {len(grouped):,} rows")

 return grouped

def apply_sigungu_crosswalk(df: pd.DataFrame, xw: pd.DataFrame) -> pd.DataFrame:
 """sigungu_crosswalk_v2 적용 — raw_code → h_code 통합.

 xw column: h_code, raw_code, year (mortality panel 사용 logic).
 mediator panel 의 h_code (= MDIS raw 시도+시군구 5자리) 를 xw.raw_code 로 lookup,
 xw.h_code 로 align (분구 시군구 합산).
 """
 print("\n[3] sigungu_crosswalk_v2 적용 (분구 시군구 합산)")
 print(f" before: {len(df):,} rows, unique h_code = {df['h_code'].nunique}")

 # xw 의 year 도 string 일 수 있음
 xw["year"] = pd.to_numeric(xw["year"], errors="coerce")

 # df 의 h_code (5자리) 가 xw.raw_code 와 매칭되는지
 # year 매칭 (sigungu_crosswalk 가 year-specific)
 df = df.merge(
 xw[["raw_code", "h_code", "year"]].rename(columns={"h_code": "h_code_aligned"}),
 left_on=["h_code", "year"], right_on=["raw_code", "year"], how="left"
)

 # h_code_aligned 가 NaN 이면 매칭 안 된 것 (1995 의 일부 코드 가능성)
 n_missing = df["h_code_aligned"].isna.sum
 print(f" 매칭 안 된 row: {n_missing:,} ({100*n_missing/len(df):.1f}%)")
 if n_missing > 0:
 sample_miss = df[df["h_code_aligned"].isna][["h_code", "year"]].drop_duplicates.head(20)
 print(f" unmatched (h_code, year) sample 20:")
 print(sample_miss.to_string)

 # unmatched 는 raw h_code 그대로 keep (drop 하면 정보 손실)
 df["h_code_final"] = df["h_code_aligned"].fillna(df["h_code"])
 df = df.drop(columns=["h_code", "raw_code", "h_code_aligned"]).rename(
 columns={"h_code_final": "h_code"}
)

 # Re-aggregate (분구 시군구 합산)
 group_cols = [c for c in df.columns if c not in ("population",)]
 df_grouped = df.groupby(group_cols, observed=True)["population"].sum.reset_index

 print(f" after crosswalk + re-aggregate: {len(df_grouped):,} rows, unique h_code = {df_grouped['h_code'].nunique}")
 return df_grouped

def write_validation_md(mar_v02: pd.DataFrame, edu_v02: pd.DataFrame, out_path: Path) -> None:
 """validation report markdown."""
 lines = [
 "# mediator_panel v02 validation",
 "",
 "## Decisions applied",
 "- 1990 drop (행정구역 mismatch)",
 "- age filter: working-age 25-64 (DGHP 2017 mediation 표준)",
 "- education 4 카테고리: NoHS/HS/SomeCollege/Bachelor+",
 "- sigungu_crosswalk_v2 적용 (mortality panel v02_1 align)",
 "",
 "## Marriage panel summary",
 f"- rows: {len(mar_v02):,}",
 f"- years: {sorted(mar_v02['year'].unique)}",
 f"- unique h_code: {mar_v02['h_code'].nunique}",
 f"- marital_code values: {sorted(mar_v02['marital_code'].unique)}",
 f"- age_band values: {sorted(mar_v02['age_band'].unique)}",
 "",
 "### Per-year cells + weighted pop sum:",
 ]
 for yr, sub in mar_v02.groupby("year"):
 lines.append(f"- {yr}: {len(sub):,} cells, {sub['h_code'].nunique} h_code, "
 f"pop sum {sub['population'].sum:,.0f}")

 lines += [
 "",
 "## Education panel summary",
 f"- rows: {len(edu_v02):,}",
 f"- years: {sorted(edu_v02['year'].unique)}",
 f"- unique h_code: {edu_v02['h_code'].nunique}",
 f"- education_band values: {sorted(edu_v02['education_band'].unique)}",
 f"- age_band values: {sorted(edu_v02['age_band'].unique)}",
 "",
 "### Per-year cells + weighted pop sum:",
 ]
 for yr, sub in edu_v02.groupby("year"):
 lines.append(f"- {yr}: {len(sub):,} cells, {sub['h_code'].nunique} h_code, "
 f"pop sum {sub['population'].sum:,.0f}")

 lines += [
 "",
 "## Next step",
 "- 11_mediator_mortality_rate.py: mortality numerator (혼인/교육 코드별 사망)",
 " + mediator denominator merge → mediator-specific mortality rate panel",
 "",
 ]
 out_path.write_text("\n".join(lines), encoding="utf-8")
 print(f"\n[validation md] {out_path}")

def main -> int:
 print("=" * 70)
 print("mediator_panel v01 → v02 cleaning + alignment")
 print("=" * 70)

 # Read v01
 mar_v01 = pd.read_parquet(POP_DIR / "mediator_panel_marriage_v01.parquet")
 edu_v01 = pd.read_parquet(POP_DIR / "mediator_panel_education_v01.parquet")

 # year cast
 mar_v01["year"] = pd.to_numeric(mar_v01["year"], errors="coerce").astype("Int64")
 edu_v01["year"] = pd.to_numeric(edu_v01["year"], errors="coerce").astype("Int64")

 # Read crosswalk
 if not XW_PATH.exists:
 print(f"\n[WARN] sigungu_crosswalk_v2.csv 없음: {XW_PATH}")
 print(" step 3 (crosswalk) skip — h_code 그대로 유지 (mortality panel 과 align 안 됨)")
 xw = None
 else:
 xw = pd.read_csv(XW_PATH, dtype=str)
 print(f"\nsigungu_crosswalk_v2 loaded: {len(xw):,} rows, "
 f"unique raw_code = {xw['raw_code'].nunique}, "
 f"unique h_code = {xw['h_code'].nunique}")

 # Clean marriage + education
 mar_clean = clean_marriage(mar_v01)
 edu_clean = clean_education(edu_v01)

 # Apply crosswalk
 if xw is not None:
 mar_v02 = apply_sigungu_crosswalk(mar_clean, xw)
 edu_v02 = apply_sigungu_crosswalk(edu_clean, xw)
 else:
 mar_v02 = mar_clean
 edu_v02 = edu_clean

 # Save v02
 mar_out = POP_DIR / "mediator_panel_marriage_v02.parquet"
 edu_out = POP_DIR / "mediator_panel_education_v02.parquet"
 mar_v02.to_parquet(mar_out, index=False)
 edu_v02.to_parquet(edu_out, index=False)
 print(f"\n[save] {mar_out}")
 print(f" rows: {len(mar_v02):,}, h_code: {mar_v02['h_code'].nunique}")
 print(f"[save] {edu_out}")
 print(f" rows: {len(edu_v02):,}, h_code: {edu_v02['h_code'].nunique}")

 # Validation md
 write_validation_md(mar_v02, edu_v02,
 POP_DIR / "mediator_panel_v02_validation.md")

 # Summary
 print("\n" + "=" * 70)
 print("v02 inventory")
 print("=" * 70)
 print("\nMarriage v02 — per-year:")
 for yr, sub in mar_v02.groupby("year"):
 print(f" {yr}: {len(sub):,} cells, {sub['h_code'].nunique} h_code, "
 f"pop sum {sub['population'].sum:,.0f}")

 print("\nEducation v02 — per-year:")
 for yr, sub in edu_v02.groupby("year"):
 print(f" {yr}: {len(sub):,} cells, {sub['h_code'].nunique} h_code, "
 f"pop sum {sub['population'].sum:,.0f}")

 print("\n" + "=" * 70)
 print("완료. 다음:")
 print(" 11_mediator_mortality_rate.py: mortality 의 혼인/교육 코드별 사망")
 print(" + mediator panel denominator merge → mediator-specific mortality rate")
 print("=" * 70)

 return 0

if __name__ == "__main__":
 sys.exit(main)
