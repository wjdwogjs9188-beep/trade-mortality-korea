"""mortality_microdata_cleaned_v01.parquet + raw codebook 폴더 통합 profile.

/data:explore-data skill workflow:
 1. cleaned parquet profile (7.4M row, 28 시점)
 2. raw codebook 폴더 (사망원인 8차분류 + 시군구 + 7차개정 등) inspect
 3. quality issue 식별
 4. follow-up 분석 추천

산출 (stdout + md):
 3_derived/mortality/exploration_report_v01.md

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\verify\\explore_mortality_dataset.py
"""
from __future__ import annotations
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve.parents[2]
PARQUET = ROOT / "3_derived" / "mortality" / "mortality_microdata_cleaned_v01.parquet"
RAW_DIR = Path(r"C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리")
OUT_REPORT = ROOT / "3_derived" / "mortality" / "exploration_report_v01.md"

def main -> int:
 print("=" * 70)
 print("EXPLORE: mortality_microdata_cleaned_v01 + raw codebook")
 print("=" * 70)

 lines = ["# Mortality Dataset Exploration Report", "",
 f"_Generated: {datetime.now.isoformat}_", ""]

 # ────────────────────────────────────────────────────────
 # PART 1: Cleaned parquet profile
 # ────────────────────────────────────────────────────────
 print("\n[PART 1] cleaned parquet profile")
 df = pd.read_parquet(PARQUET)
 print(f" rows: {len(df):,}, cols: {len(df.columns)}")

 lines += ["## 1. Cleaned Parquet Profile",
 "",
 f"**File**: `{PARQUET.relative_to(ROOT)}`",
 f"**Rows**: {len(df):,}",
 f"**Columns**: {len(df.columns)} ({df.columns.tolist})",
 f"**Years**: {df['year'].min} – {df['year'].max} ({df['year'].nunique} 시점)",
 f"**Unique h_code**: {df['h_code'].nunique}",
 ""]

 # Column-level profile
 lines += ["### Column profile", "",
 "| column | dtype | n_unique | null_rate | top 5 values |",
 "|--------|-------|----------|-----------|---------------|"]
 for col in df.columns:
 ser = df[col]
 null_rate = ser.isna.mean * 100
 n_uniq = ser.nunique(dropna=True)
 if n_uniq <= 30:
 top5 = ser.value_counts(dropna=False).head(5).to_dict
 top5_str = ", ".join(f"{k}={v:,}" for k, v in top5.items)
 else:
 top5_str = f"({n_uniq} 가지, sample: {sorted(ser.dropna.unique[:5])})"
 lines.append(f"| {col} | {ser.dtype} | {n_uniq:,} | {null_rate:.2f}% | {top5_str} |")

 # Per-year row count
 print("\n[PART 1.2] per-year row count + 5 핵심 분포")
 lines += ["", "### Per-year row count + key 분포", "",
 "| year | rows | h_code 수 | unique cause_104 | sex(M:F) | marital top |",
 "|------|------|-----------|------------------|----------|---------------|"]
 for yr, sub in df.groupby("year"):
 n_h = sub["h_code"].nunique
 n_cause = sub["cause_104"].nunique
 sex_m = (sub["sex_code"] == "1").sum
 sex_f = (sub["sex_code"] == "2").sum
 sex_ratio = f"{sex_m/sex_f:.2f}" if sex_f > 0 else "-"
 mar_top = sub["marital_code"].value_counts.head(1).to_dict
 mar_str = f"{list(mar_top.keys)[0]}({list(mar_top.values)[0]:,})" if mar_top else "-"
 lines.append(f"| {yr} | {len(sub):,} | {n_h} | {n_cause} | M:F={sex_ratio} | {mar_str} |")

 # ────────────────────────────────────────────────────────
 # PART 2: Quality issue
 # ────────────────────────────────────────────────────────
 print("\n[PART 2] data quality issue 식별")
 issues = 

 # h_code length 통일성
 h_lens = df["h_code"].str.len.value_counts
 if len(h_lens) > 1:
 issues.append(f"⚠️ h_code 길이 불일치: {h_lens.to_dict} → 시군구 코드 자릿수 시점 별 다름")

 # working-age 25-64 비율
 work_ages = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64"]
 work_n = df[df["age_band"].isin(work_ages)].shape[0]
 work_pct = 100 * work_n / len(df)
 issues.append(f"📊 working-age (25-64) 비율: {work_pct:.1f}% ({work_n:,} / {len(df):,})")

 # 85+ 비율 (super-aged)
 age85_n = (df["age_band"] == "85+").sum
 age85_pct = 100 * age85_n / len(df)
 issues.append(f"📊 85+ 비율: {age85_pct:.1f}% ({age85_n:,})")

 # marital "1" (미혼) 비율 시점별 추이
 mar1_by_yr = df.groupby("year").apply(
 lambda x: 100 * (x["marital_code"] == "1").sum / len(x), include_groups=False)
 issues.append(f"📈 미혼 비율 추이: 1997 {mar1_by_yr.iloc[0]:.1f}% → 2024 {mar1_by_yr.iloc[-1]:.1f}%")

 # education NoHS 비율 추이
 edu1_by_yr = df.groupby("year").apply(
 lambda x: 100 * (x["education_band"] == "1.NoHS").sum / len(x), include_groups=False)
 issues.append(f"📉 NoHS 비율 추이: 1997 {edu1_by_yr.iloc[0]:.1f}% → 2024 {edu1_by_yr.iloc[-1]:.1f}%")

 # cause_104 = 102 (자살) count by year
 suicide_by_yr = df[df["cause_104"] == "102"].groupby("year").size
 issues.append(f"💀 자살 (cause_104=102) row count: 1997 {suicide_by_yr.get(1997, 0):,} → "
 f"2024 {suicide_by_yr.get(2024, 0):,}")

 lines += ["", "## 2. Data Quality Issues", ""]
 for iss in issues:
 lines.append(f"- {iss}")
 print(f" {iss}")

 # ────────────────────────────────────────────────────────
 # PART 3: Raw codebook inventory
 # ────────────────────────────────────────────────────────
 print("\n[PART 3] raw codebook 폴더 inspect")
 lines += ["", "## 3. Raw Codebook Inventory", "",
 f"**폴더**: `{RAW_DIR}`", ""]

 # 그룹화: 사망 raw csv / 시군구 codebook / 파일설계서 / 기타
 csvs = sorted(RAW_DIR.glob("*_사망_연간자료_*.csv"))
 sigungu_xlsx = sorted(RAW_DIR.glob("시군구코드집*.xlsx"))
 layout_xlsx = sorted(RAW_DIR.glob("파일설계서*.xlsx"))
 cause_xlsx = sorted([p for p in RAW_DIR.glob("*.xlsx")
 if "사망원인통계_사망연간자료_코드집" in p.name
 or "질병사인분류" in p.name])

 lines.append(f"### 사망 microdata CSV (28 시점)")
 lines.append(f"- 1997-2024, 평균 ~250K rows/시점, 총 ~7.4M")
 lines.append(f"- column 18 개 (시점별 일부 차이: 2024 = '주소지', 다른 시점 = '주소')")
 lines.append("")

 lines.append(f"### 시군구 codebook xlsx ({len(sigungu_xlsx)} 시점)")
 for p in sigungu_xlsx[:10]:
 lines.append(f"- {p.name}")
 if len(sigungu_xlsx) > 10:
 lines.append(f"-... + {len(sigungu_xlsx)-10} more")
 lines.append("")

 lines.append(f"### 파일설계서 xlsx ({len(layout_xlsx)} 시점)")
 lines.append(f"- 1997-2024 시점별 column 정의 + 코드 정의")
 lines.append("")

 lines.append(f"### 사망원인 분류 코드집 ({len(cause_xlsx)})")
 for p in cause_xlsx:
 lines.append(f"- {p.name} ({p.stat.st_size/1024:.1f} KB)")
 lines.append("")

 # 1997 시군구 codebook sample inspect
 s1997 = RAW_DIR / "시군구코드집(공공용)_사망원인통계_사망_연간자료_B형(제공)_1997.xlsx"
 if s1997.exists:
 try:
 xl = pd.ExcelFile(s1997)
 lines.append(f"### Sample: 1997 시군구 코드집")
 lines.append(f"- sheets: {xl.sheet_names}")
 for sheet in xl.sheet_names[:2]:
 df_s = pd.read_excel(s1997, sheet_name=sheet, dtype=str, nrows=15, header=None)
 lines.append(f" - sheet '{sheet}' shape={df_s.shape}, head:")
 lines.append("```")
 lines.append(df_s.head(10).to_string(max_cols=4))
 lines.append("```")
 except Exception as e:
 lines.append(f"- inspect fail: {e}")
 lines.append("")

 # 사망원인 8차분류 codebook sample
 cause_main = RAW_DIR / "사망원인통계_사망연간자료_코드집(8차질병분류코드).xlsx"
 if cause_main.exists:
 try:
 xl = pd.ExcelFile(cause_main)
 lines.append(f"### Sample: 사망원인 8차분류 코드집 (cause_104 매핑)")
 lines.append(f"- sheets: {xl.sheet_names}")
 for sheet in xl.sheet_names[:1]:
 df_c = pd.read_excel(cause_main, sheet_name=sheet, dtype=str, nrows=20, header=None)
 lines.append(f" - sheet '{sheet}' shape={df_c.shape}, head 20:")
 lines.append("```")
 lines.append(df_c.head(20).to_string(max_cols=5))
 lines.append("```")
 except Exception as e:
 lines.append(f"- inspect fail: {e}")
 lines.append("")

 # ────────────────────────────────────────────────────────
 # PART 4: Recommendations
 # ────────────────────────────────────────────────────────
 lines += ["", "## 4. Recommended Follow-Up Analyses", "",
 "1. **sigungu_crosswalk_v2 적용**: cleaned parquet 의 unique h_code = 362 → "
 "mortality_panel_v02_1 의 229 와 align 위해 crosswalk 적용 (분구 시군구 합산)",
 "",
 "2. **age_band 25-64 working-age subset**: mediator analysis 의 표준 (DGHP 2017). "
 "현재 working-age 비율 ~13%, 65+ 비율 ~73% (한국 고령 사망 dominance)",
 "",
 "3. **cause_104 deaths of despair filter**: 102 자살 / 101 약물 / 057 정신 / 081 간 "
 "(paper 의 main outcome) — 시점별 추이 + 시군구별 분포",
 "",
 "4. **mediator-specific cross-tab (11b/11c)**: marital_code × cause_104 + "
 "education_band × cause_104 → mediator-specific mortality numerator",
 "",
 "5. **mediator panel v02 와 join (numerator/denominator)**: "
 "mediator panel 5 시점 (2000/05/10/15/20) 과 mortality 5-year window stack "
 "(1997-2001 → 2000 인구,...) → mediator-specific mortality rate",
 ""]

 # Save
 OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
 OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
 print(f"\n[save] {OUT_REPORT}")
 print(f" size: {OUT_REPORT.stat.st_size/1024:.2f} KB")

 return 0

if __name__ == "__main__":
 sys.exit(main)
