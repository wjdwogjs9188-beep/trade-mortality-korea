"""Stage 3C — Individual-level mediator panel build (Tier B 추가사항 2).

Aggregates microdata by individual-level columns:
- marriage_status_code (1=미혼, 2=유배우자, 3=사별, 4=이혼, 9=미상)
- education_code (1=무학, 2=초등, 3=중등, 4=고등, 5=대학재학, 6=대학졸업, 7=대학원, 9=미상)
- occupation_code (KSCO; 13=무직 dominant ~70% → low information; left as raw)

Outputs (3_derived/mortality/)
-----------------------------
- mortality_panel_v02_marriage.parquet (h × year × outcome × marriage → deaths)
- mortality_panel_v02_education.parquet (h × year × outcome × education → deaths)
- mortality_panel_v02_occupation.parquet (h × year × outcome × occupation → deaths)
- mediator_panel_audit.md

Use cases (Case-Deaton mediator framework)
------------------------------------------
- 結婚사망률 / 학력별 사망률 → 무역 노출 trade exposure 와 mediator interaction
- death share by mediator group (분모 = sigungu × year deaths) → Korea-specific mediator effect
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve.parents[2]
MICRO = REPO / "3_derived" / "mortality" / "mortality_microdata_combined.parquet"
OUT_DIR = REPO / "3_derived" / "mortality"
OUT_MARRIAGE = OUT_DIR / "mortality_panel_v02_marriage.parquet"
OUT_EDUCATION = OUT_DIR / "mortality_panel_v02_education.parquet"
OUT_OCCUPATION = OUT_DIR / "mortality_panel_v02_occupation.parquet"
OUT_AUDIT = OUT_DIR / "mediator_panel_audit.md"

OUTCOME_GROUPS_V02: dict[str, set[str] | str] = {
 "suicide_102": {"102"},
 "drug_101": {"101"},
 "psych_057": {"057"},
 "liver_081": {"081"},
 "despair_total": {"057", "081", "101", "102"},
 "cancer": {f"{i:03d}" for i in range(27, 48)},
 "cardiovascular": {"067", "068", "069", "070"},
 "respiratory": {f"{i:03d}" for i in range(73, 79)},
 "external_other": {"097", "098", "099", "100", "103", "104"},
 "other": "fallback",
}
PRIMARY_PARTITION = ["suicide_102", "drug_101", "psych_057", "liver_081",
 "cancer", "cardiovascular", "respiratory", "external_other"]
OUTCOMES_ALL = ["suicide_102", "drug_101", "psych_057", "liver_081", "despair_total",
 "cancer", "cardiovascular", "respiratory", "external_other", "other"]

MARRIAGE_LABELS = {"1": "미혼", "2": "유배우자", "3": "사별", "4": "이혼", "9": "미상"}
EDUCATION_LABELS = {"1": "무학", "2": "초등", "3": "중등", "4": "고등",
 "5": "대학재학", "6": "대학졸업", "7": "대학원", "9": "미상"}

def assign_outcomes(cause: str) -> list[str]:
 if cause is None or pd.isna(cause):
 return ["other"]
 matched = 
 for grp in PRIMARY_PARTITION:
 codes = OUTCOME_GROUPS_V02[grp]
 if cause in codes:
 matched.append(grp)
 break
 if not matched:
 matched.append("other")
 if cause in OUTCOME_GROUPS_V02["despair_total"]:
 matched.append("despair_total")
 return matched

def main -> None:
 print("[load] microdata...")
 keep_cols = ["h_code", "year", "sex_code", "cause_104",
 "marriage_status_code", "education_code", "occupation_code"]
 df = pd.read_parquet(MICRO, columns=keep_cols)
 print(f" {len(df):,} rows")

 # Filter valid
 df = df[
 df["h_code"].notna
 & df["sex_code"].isin(["1", "2"])
 & df["cause_104"].notna
 ].copy
 print(f" valid: {len(df):,}")

 # Assign outcomes
 df["outcomes"] = df["cause_104"].map(assign_outcomes)
 df = df.explode("outcomes").rename(columns={"outcomes": "outcome_group"})

 # === Marriage panel ===
 print("[marriage] building panel...")
 df_m = df.copy
 df_m["marriage_status_code"] = df_m["marriage_status_code"].fillna("9")
 marr = (
 df_m.groupby(["h_code", "year", "outcome_group", "marriage_status_code"], as_index=False)
.size.rename(columns={"size": "deaths"})
)
 marr["marriage_label"] = marr["marriage_status_code"].map(MARRIAGE_LABELS)
 marr.to_parquet(OUT_MARRIAGE, index=False, compression="snappy")
 print(f" {len(marr):,} rows → {OUT_MARRIAGE.relative_to(REPO)}")

 # === Education panel ===
 print("[education] building panel...")
 df_e = df.copy
 df_e["education_code"] = df_e["education_code"].fillna("9")
 edu = (
 df_e.groupby(["h_code", "year", "outcome_group", "education_code"], as_index=False)
.size.rename(columns={"size": "deaths"})
)
 edu["education_label"] = edu["education_code"].map(EDUCATION_LABELS)
 edu.to_parquet(OUT_EDUCATION, index=False, compression="snappy")
 print(f" {len(edu):,} rows → {OUT_EDUCATION.relative_to(REPO)}")

 # === Occupation panel (raw KSCO codes; 13=무직 dominant) ===
 print("[occupation] building panel...")
 df_o = df.copy
 df_o["occupation_code"] = df_o["occupation_code"].fillna("99")
 occ = (
 df_o.groupby(["h_code", "year", "outcome_group", "occupation_code"], as_index=False)
.size.rename(columns={"size": "deaths"})
)
 occ.to_parquet(OUT_OCCUPATION, index=False, compression="snappy")
 print(f" {len(occ):,} rows → {OUT_OCCUPATION.relative_to(REPO)}")

 # === Audit report ===
 L = 
 L.append("# Stage 3C — Individual-Level Mediator Panel Audit")
 L.append("")
 L.append("- Generated: 2026-05-03")
 L.append("- Source: `3_derived/mortality/mortality_microdata_combined.parquet`")
 L.append("- Use case: Case-Deaton mediator framework (marriage / education / occupation 별 사망률)")
 L.append("")
 L.append("## Marriage status (despair_total 분포 verification)")
 L.append("")
 despair_marriage = (
 marr[marr["outcome_group"] == "despair_total"]
.groupby("marriage_label")["deaths"].sum
.sort_values(ascending=False)
)
 total_despair = int(despair_marriage.sum)
 L.append("| marriage_status | label | deaths | share |")
 L.append("|---|---|---:|---:|")
 for code in ["1", "2", "3", "4", "9"]:
 label = MARRIAGE_LABELS[code]
 n = int(despair_marriage.get(label, 0))
 pct = 100 * n / total_despair if total_despair else 0
 L.append(f"| {code} | {label} | {n:,} | {pct:.2f}% |")
 L.append(f"| **TOTAL** | — | **{total_despair:,}** | 100% |")
 L.append("")
 L.append("## Education code (despair_total 분포)")
 L.append("")
 despair_edu = (
 edu[edu["outcome_group"] == "despair_total"]
.groupby("education_label")["deaths"].sum
.sort_values(ascending=False)
)
 total_edu = int(despair_edu.sum)
 L.append("| education_code | label | deaths | share |")
 L.append("|---|---|---:|---:|")
 for code in ["1", "2", "3", "4", "5", "6", "7", "9"]:
 label = EDUCATION_LABELS[code]
 n = int(despair_edu.get(label, 0))
 pct = 100 * n / total_edu if total_edu else 0
 L.append(f"| {code} | {label} | {n:,} | {pct:.2f}% |")
 L.append("")
 L.append("## Occupation (top 10 KSCO codes, 모든 outcome)")
 L.append("")
 occ_top = (
 occ.groupby("occupation_code")["deaths"].sum.sort_values(ascending=False).head(10)
)
 L.append("| occupation_code | deaths | share |")
 L.append("|---|---:|---:|")
 occ_total = int(occ["deaths"].sum)
 for code, n in occ_top.items:
 pct = 100 * int(n) / occ_total
 L.append(f"| {code} | {int(n):,} | {pct:.2f}% |")
 L.append("")
 L.append("**Note**: KSCO 13 = 무직 ~70% dominance → occupation 단독 mediator 효과 약함. 1-12 codes (취업자) restricted-sample analysis 권고.")
 L.append("")
 L.append("## Use cases")
 L.append("")
 L.append("1. **Marriage gradient**: 미혼/이혼 vs 유배우자 자살률 비교 (Case-Deaton 핵심 finding).")
 L.append("2. **Education gradient**: 학력 high → low 사망률 gradient (한국에서도 미국과 동일 패턴 verify).")
 L.append("3. **Trade × mediator interaction**: trade exposure 가 marriage breakdown / education low 경로로 사망률 증가시키는지 mechanism 분리.")
 L.append("4. **분모 정의**: 분모는 KOSIS 인구 panel + 미시 분포 (KOSIS 가족조사) 별도 join 필요. 본 mediator panel = 분자 only.")
 L.append("")
 L.append("## 한계")
 L.append("")
 L.append("- 분모 부재: marriage/education 별 사망률 (incident rate) 계산하려면 KOSIS 인구 panel 의 marriage·education 별 인구 분포 별도 다운 필요.")
 L.append("- 1997-1999 일부 microdata 의 occupation_code 결측률 높음 (~5%) — restricted-sample 권고.")
 L.append("- 한국 시군구 단위에서 marriage × education 4-way table 은 cell sparseness 증가 (despair는 자살 13k/year 정도).")
 OUT_AUDIT.write_text("\n".join(L), encoding="utf-8")
 print(f" -> {OUT_AUDIT.relative_to(REPO)}")
 print("\n[done]")

if __name__ == "__main__":
 main
