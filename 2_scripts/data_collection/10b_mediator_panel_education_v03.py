"""mediator_panel_education v02 → v03 재매핑 (4 → 3 카테고리).

Validation issue H1 fix:
 - v02 (4 카테고리): NoHS / HS / SomeCollege / Bachelor+
 - v03 (3 카테고리, mortality 와 align): NoHS / HS / College+

이유: mortality microdata cleaned 의 education_band 가 3 카테고리.
사망 microdata 1997-2007 = 5 카테고리 (5=대학 통합) → 2008+ 의 5 (전문대) /
6 (4년제) / 7 (석사) / 8 (박사) 와 1:N 매핑 불가능.
가장 robust = 3 카테고리 (모든 시점 align): College+ = SomeCollege + Bachelor+ 통합.

mediator panel marriage 는 변경 없음 (이미 mortality 와 align).

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\10b_mediator_panel_education_v03.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve.parents[2]
POP_DIR = ROOT / "3_derived" / "population"

# v02 (4 카테고리) → v03 (3 카테고리) 매핑
EDU_4_TO_3 = {
 "1.NoHS": "1.NoHS",
 "2.HS": "2.HS",
 "3.SomeCollege": "3.College+", # 전문대 → College+ 통합
 "4.Bachelor+": "3.College+", # 4년제 + 석사 + 박사 → College+ 통합
}

def main -> int:
 print("=" * 70)
 print("10b: mediator_panel_education v02 → v03 재매핑 (4 → 3 카테고리)")
 print("=" * 70)

 in_path = POP_DIR / "mediator_panel_education_v02.parquet"
 out_path = POP_DIR / "mediator_panel_education_v03.parquet"

 if not in_path.exists:
 print(f"[FL] input not found: {in_path}")
 return 1

 edu_v02 = pd.read_parquet(in_path)
 print(f"\n[input] {in_path.name}")
 print(f" rows: {len(edu_v02):,}")
 print(f" education_band v02 distribution:")
 print(edu_v02["education_band"].value_counts.to_string)

 # Map 4 → 3
 edu_v02["education_band"] = edu_v02["education_band"].map(EDU_4_TO_3)
 n_unmapped = edu_v02["education_band"].isna.sum
 if n_unmapped > 0:
 print(f" [WARN] {n_unmapped:,} rows unmapped (drop)")
 edu_v02 = edu_v02.dropna(subset=["education_band"])

 # Re-aggregate (3 카테고리로 합산)
 group_cols = ["h_code", "year", "sex_code", "age_band", "education_band"]
 edu_v03 = (edu_v02.groupby(group_cols, observed=True)["population"]
.sum.reset_index)

 print(f"\n[output] {out_path.name}")
 print(f" rows: {len(edu_v03):,}")
 print(f" education_band v03 distribution:")
 print(edu_v03["education_band"].value_counts.to_string)

 edu_v03.to_parquet(out_path, index=False)
 print(f"\n[save] {out_path}")
 print(f" size: {out_path.stat.st_size/1024:.2f} KB")

 # Per-year summary
 print("\n" + "=" * 70)
 print("Per-year cells + pop sum (v03)")
 print("=" * 70)
 for yr, sub in edu_v03.groupby("year"):
 print(f" {yr}: {len(sub):,} cells, {sub['h_code'].nunique} h_code, "
 f"pop sum {sub['population'].sum:,.0f}")

 print("\n" + "=" * 70)
 print("완료. 다음:")
 print(" 11b_mortality_marital_panel.py: mortality marital × cause_104 cross-tab")
 print(" 11c_mortality_education_panel.py: mortality education × cause_104 cross-tab")
 print(" (mortality 도 sigungu_crosswalk_v2 + age 25-64 filter 적용)")
 print("=" * 70)

 return 0

if __name__ == "__main__":
 sys.exit(main)
