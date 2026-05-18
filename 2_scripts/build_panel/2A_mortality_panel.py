"""Mortality panel build (v3, mutually exclusive outcomes).

Pipeline
--------
1. Load 27 KOSTAT mortality CSVs (cp949), standardize columns.
2. Build raw_code (5-digit). Separate foreign/missing-residence rows.
3. Map raw_code → h_code via sigungu_crosswalk_v2 (229 baseline).
4. Assign each death to ONE outcome group (priority order; "other" fallback).
5. Aggregate to panel: h_code × year × sex × age_5yr × outcome → deaths (0-cells included).
6. Run 7 validations + KOSIS unit comparison.

Inputs
------
- 0_raw/mortality_kostat/사망사료 정리/ (27 cp949 CSVs, 1997-2023)
- 1_codebooks/sigungu_crosswalk_v2.csv (229 h_codes)
- 1_codebooks/mortality_104_classification.csv
- 0_raw/kosis_population/population_combined.csv (read for unit comparison only)

Outputs (3_derived/mortality/)
-----------------------------
- mortality_microdata_combined.parquet (~7.2M rows, all 27 years, h_code mapped)
- mortality_panel_v01.parquet (panel, h × yr × sex × age × outcome → deaths)
- unmatched_mortality.parquet (foreign + unmapped rows)
- mortality_panel_validation.md (validation report)

Outcome groups (mutually exclusive, priority order)
---------------------------------------------------
1. despair_total: 102 (suicide), 101 (drug poisoning), 057 (psychoactive substance), 081 (liver)
2. cardiovascular: 067-070
3. cancer: 027-047 (악성신생물만, C00-C97; 048 양성/불명은 'other' 로 흡수)
4. respiratory: 073-078
5. external_other: 097, 098, 099, 100, 103, 104 (= 097-104 minus 102 minus 101)
6. other: every other cause_104 (1-104 not in groups 1-5)

If a cause_104 falls into multiple group definitions, the priority order assigns
it to the highest-listed group only. So 101 ∈ despair_total (not external_other),
081 ∈ despair_total (no digestive group), etc.
"""
from __future__ import annotations
import sys
import re
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve.parents[2]
SRC_DIR = REPO / "0_raw" / "mortality_kostat" / "사망사료 정리"
XW_PATH = REPO / "1_codebooks" / "sigungu_crosswalk_v2.csv"
CODEBOOK_PATH = REPO / "1_codebooks" / "mortality_104_classification.csv"
KOSIS_POP_PATH = REPO / "0_raw" / "kosis_population" / "population_combined.csv"

OUT_DIR = REPO / "3_derived" / "mortality"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_COMBINED = OUT_DIR / "mortality_microdata_combined.parquet"
OUT_PANEL = OUT_DIR / "mortality_panel_v01.parquet"
OUT_UNMATCHED = OUT_DIR / "unmatched_mortality.parquet"
OUT_REPORT = OUT_DIR / "mortality_panel_validation.md"

COL_RENAME = {
 "연도": "year",
 "신고연도": "report_year",
 "신고월": "report_month",
 "신고일": "report_day",
 "사망자주소행정구역시도코드": "sido_code",
 "사망자주소행정구역시군구코드": "sigungu_code",
 "사망연월일": "death_date",
 "사망시": "death_hour",
 "사망장소코드": "death_place_code",
 "사망자직업분류코드": "occupation_code",
 "사망자혼인상태코드": "marriage_status_code",
 "교육정도코드": "education_code",
 "성별코드": "sex_code",
 "사망연령5세단위코드": "age_5yr_code",
 "사망자국적구분코드": "nationality_code",
 "사망자이전국적코드": "prev_nationality_code",
 "사망원인_104항목분류코드": "cause_104",
 "사망원인_57항목분류코드": "cause_57",
}

# Outcome priority order (first match wins → mutual exclusivity)
OUTCOME_PRIORITY: list[tuple[str, set[str]]] = [
 ("despair_total", {"102", "101", "057", "081"}),
 ("cardiovascular", {"067", "068", "069", "070"}),
 ("cancer", {f"{i:03d}" for i in range(27, 48)}), # 027..047 (악성신생물만, C00-C97)
 ("respiratory", {f"{i:03d}" for i in range(73, 79)}), # 073..078
 ("external_other", {"097", "098", "099", "100", "103", "104"}),
 # "other" assigned by fallback below
]

KOSTAT_SUICIDE_OFFICIAL = {
 "2010": 15566, "2011": 15906, "2015": 13513, "2019": 13799,
}

KOSIS_CANCER_OFFICIAL = {
 "1998": 51291,
 "2000": 58197,
 "2005": 65529,
 "2010": 72048,
 "2015": 76855,
 "2020": 82204,
 "2023": 85271,
}

EXPECTED_2023_RECORDS = 352511
EXPECTED_2023_TOLERANCE = 0.01 # ±1%

YEAR_RE = re.compile(r"^(\d{4})_")

def normalize_raw_code(sido: str | float, sgg: str | float) -> str | None:
 if pd.isna(sido) or pd.isna(sgg):
 return None
 sido = str(sido).strip
 sgg = str(sgg).strip
 if not sido or not sgg:
 return None
 if len(sgg) == 5: # 2023+ format: sigungu already 5-digit
 return sgg
 if len(sgg) == 3: # 1997-2022 format: 2-digit sido + 3-digit sgg
 return sido.zfill(2) + sgg
 return sido.zfill(2) + sgg.zfill(3)

def is_foreign_or_unknown(sido: str, sgg: str) -> bool:
 """True if sido='99' or sgg='999' or sgg='99999' (KOSTAT foreign/missing)."""
 if pd.isna(sido) or pd.isna(sgg):
 return True
 return str(sido).strip == "99" or str(sgg).strip in {"999", "99999"}

def assign_outcome(cause: str) -> str:
 """First-match priority. Returns 'other' if cause_104 not in any defined group."""
 if cause is None or pd.isna(cause):
 return "other"
 for grp, codes in OUTCOME_PRIORITY:
 if cause in codes:
 return grp
 return "other"

def load_microdata(path: Path) -> pd.DataFrame:
 m = YEAR_RE.match(path.name)
 if not m:
 raise ValueError(f"could not parse year from {path.name}")
 year = m.group(1)
 df = pd.read_csv(path, encoding="cp949", dtype=str)
 missing = [c for c in COL_RENAME if c not in df.columns]
 if missing:
 raise ValueError(f"{path.name}: missing columns: {missing}")
 df = df.rename(columns=COL_RENAME)
 df["year"] = year
 df["raw_code"] = [
 normalize_raw_code(s, g) for s, g in zip(df["sido_code"], df["sigungu_code"])
 ]
 df["is_foreign_or_unknown"] = [
 is_foreign_or_unknown(s, g) for s, g in zip(df["sido_code"], df["sigungu_code"])
 ]
 return df

def load_crosswalk -> pd.DataFrame:
 xw = pd.read_csv(XW_PATH, dtype=str)
 return xw[["year", "raw_code", "h_code", "h_name"]]

def kosis_unit_summary -> dict:
 pop = pd.read_csv(KOSIS_POP_PATH, dtype=str)
 sigungu_5 = pop[pop["C1"].str.len == 5]["C1"].drop_duplicates.sort_values.head(5).tolist
 return {
 "C1_distinct": int(pop["C1"].nunique),
 "C1_sample_5digit": sigungu_5,
 "C1_lengths": dict(pop["C1"].str.len.value_counts.to_dict),
 "C2_unique": sorted(pop["C2"].dropna.unique),
 "C2_NM_unique": sorted(pop["C2_NM"].dropna.unique),
 "C3_unique_count": int(pop["C3"].nunique),
 "C3_unique": sorted(pop["C3"].dropna.unique),
 "C3_NM_unique": sorted(pop["C3_NM"].dropna.unique),
 "year_range": f'{pop["year"].min}-{pop["year"].max}',
 }

def main -> None:
 files = sorted(SRC_DIR.glob("*_사망_연간자료_B형_*.csv"))
 files = [f for f in files if (m:= YEAR_RE.match(f.name)) and 1997 <= int(m.group(1)) <= 2023]
 if len(files)!= 27:
 print(f"WARNING: expected 27 files (1997-2023), found {len(files)}")
 print(f"[load] {len(files)} files from {SRC_DIR.relative_to(REPO)}")

 xw = load_crosswalk
 print(f"[xw ] {len(xw):,} rows ({xw['h_code'].nunique} h_codes, {xw['year'].min}-{xw['year'].max})")

 # === dtype check on cause_104 ===
 sample = pd.read_csv(files[0], encoding="cp949", dtype=str, nrows=5)
 if not pd.api.types.is_string_dtype(sample["사망원인_104항목분류코드"]):
 sys.exit(f"FL V1 dtype: cause_104 not string (got {sample['사망원인_104항목분류코드'].dtype})")

 yearly_micro: list[pd.DataFrame] = 
 yearly_unmatched: list[pd.DataFrame] = 
 yearly_summary: list[dict] = 
 yearly_outcome_long: list[pd.DataFrame] = 

 for f in files:
 year = YEAR_RE.match(f.name).group(1)
 df = load_microdata(f)
 n_in = len(df)

 # Split foreign / domestic
 foreign_mask = df["is_foreign_or_unknown"]
 domestic = df[~foreign_mask].copy
 n_foreign = int(foreign_mask.sum)

 # Merge crosswalk
 merged = domestic.merge(xw, on=["year", "raw_code"], how="left", validate="many_to_one")
 unmatched_mask = merged["h_code"].isna
 n_unmatched_dom = int(unmatched_mask.sum)

 unmatched_dom = merged[unmatched_mask][["year", "sido_code", "sigungu_code", "raw_code"]].copy
 if len(unmatched_dom) > 0:
 unmatched_dom["reason"] = "domestic_unmapped"
 yearly_unmatched.append(unmatched_dom)

 if n_foreign > 0:
 f_rows = df[foreign_mask][["year", "sido_code", "sigungu_code", "raw_code"]].copy
 f_rows["reason"] = "foreign_or_unknown"
 yearly_unmatched.append(f_rows)

 matched = merged[~unmatched_mask].copy
 sex_invalid = ~matched["sex_code"].isin({"1", "2"})
 age_invalid = matched["age_5yr_code"].isna | (matched["age_5yr_code"] == "99")
 cause_invalid = matched["cause_104"].isna
 n_sex_drop = int(sex_invalid.sum)
 n_age_drop = int(age_invalid.sum)
 n_cause_drop = int(cause_invalid.sum)

 valid = matched[~sex_invalid & ~age_invalid & ~cause_invalid].copy
 valid["outcome_group"] = valid["cause_104"].map(assign_outcome)
 n_valid = len(valid)

 yearly_outcome_long.append(
 valid[["h_code", "year", "sex_code", "age_5yr_code", "cause_104", "outcome_group"]]
)

 # Combined microdata: keep ALL rows (incl. foreign/unmatched) with h_code (NaN for unmapped)
 keep_cols = [
 "year", "report_year", "report_month", "report_day",
 "sido_code", "sigungu_code", "raw_code", "h_code", "h_name",
 "death_date", "death_hour", "death_place_code",
 "occupation_code", "marriage_status_code", "education_code",
 "sex_code", "age_5yr_code", "nationality_code", "prev_nationality_code",
 "cause_104", "cause_57", "is_foreign_or_unknown",
 ]
 # Need to merge xw onto whole df (incl. foreign) to get NaN h_code for foreign+unmapped
 full_merged = df.merge(xw, on=["year", "raw_code"], how="left", validate="many_to_one")
 for c in keep_cols:
 if c not in full_merged.columns:
 full_merged[c] = pd.NA
 yearly_micro.append(full_merged[keep_cols].copy)

 n_suicide = int((valid["cause_104"] == "102").sum)
 yearly_summary.append({
 "year": year,
 "n_in": n_in,
 "n_foreign_unknown": n_foreign,
 "n_domestic_unmapped": n_unmatched_dom,
 "n_sex_drop": n_sex_drop,
 "n_age_drop": n_age_drop,
 "n_cause_drop": n_cause_drop,
 "n_valid": n_valid,
 "n_suicide_102": n_suicide,
 })
 print(f" [{year}] in={n_in:,} foreign={n_foreign} unmapped(dom)={n_unmatched_dom} age99={n_age_drop:,} valid={n_valid:,} suicide102={n_suicide:,}")

 # --- combined microdata ---
 print("[concat] microdata...")
 combined = pd.concat(yearly_micro, ignore_index=True)
 print(f"[combined] {len(combined):,} rows -> {OUT_COMBINED.relative_to(REPO)}")
 combined.to_parquet(OUT_COMBINED, index=False, compression="snappy")

 # --- unmatched ---
 if yearly_unmatched:
 unmatched_df = pd.concat(yearly_unmatched, ignore_index=True)
 unmatched_summary = (
 unmatched_df.groupby(["year", "sido_code", "sigungu_code", "raw_code", "reason"], dropna=False, as_index=False)
.size.rename(columns={"size": "n_records"})
)
 else:
 unmatched_summary = pd.DataFrame(columns=["year", "sido_code", "sigungu_code", "raw_code", "reason", "n_records"])
 unmatched_summary.to_parquet(OUT_UNMATCHED, index=False, compression="snappy")

 # --- outcome long-format ---
 long_all = pd.concat(yearly_outcome_long, ignore_index=True)
 print(f"[long ] {len(long_all):,} rows (one per valid death, with outcome_group)")

 # === V2 mutual exclusivity check (FL-fast) ===
 # Each death record is exactly one row in long_all → counts must equal valid sum
 sum_check = sum(s["n_valid"] for s in yearly_summary)
 if len(long_all)!= sum_check:
 sys.exit(f"FL V2 mutual exclusivity: long={len(long_all):,}!= valid_sum={sum_check:,}")
 # Cross-check that each cause_104 maps to exactly one outcome_group
 cause_to_groups = long_all.groupby("cause_104")["outcome_group"].nunique
 bad = cause_to_groups[cause_to_groups > 1]
 if len(bad) > 0:
 sys.exit(f"FL V2 mutual exclusivity: causes mapping to multiple groups: {bad.to_dict}")

 # --- panel aggregation ---
 print("[aggregate] panel...")
 actuals = (
 long_all.groupby(["h_code", "year", "sex_code", "age_5yr_code", "outcome_group"], as_index=False)
.size.rename(columns={"size": "deaths"})
)

 h_codes = sorted(xw["h_code"].unique)
 years = sorted({s["year"] for s in yearly_summary})
 sexes = ["1", "2"]
 ages_present = sorted(long_all["age_5yr_code"].dropna.unique, key=lambda x: int(x))
 outcomes = [g for g, _ in OUTCOME_PRIORITY] + ["other"]
 print(f" dims: h={len(h_codes)} year={len(years)} sex={len(sexes)} age={len(ages_present)} outcome={len(outcomes)}")
 print(f" expected cells: {len(h_codes)*len(years)*len(sexes)*len(ages_present)*len(outcomes):,}")

 idx = pd.MultiIndex.from_product(
 [h_codes, years, sexes, ages_present, outcomes],
 names=["h_code", "year", "sex_code", "age_5yr_code", "outcome_group"],
)
 panel = pd.DataFrame(index=idx).reset_index
 panel = panel.merge(actuals, how="left",
 on=["h_code", "year", "sex_code", "age_5yr_code", "outcome_group"])
 panel["deaths"] = panel["deaths"].fillna(0).astype("int64")

 h_name_map = xw.drop_duplicates("h_code").set_index("h_code")["h_name"]
 panel["h_name"] = panel["h_code"].map(h_name_map)
 panel = panel[["h_code", "h_name", "year", "sex_code", "age_5yr_code", "outcome_group", "deaths"]]
 panel.to_parquet(OUT_PANEL, index=False, compression="snappy")
 print(f"[panel] {len(panel):,} rows -> {OUT_PANEL.relative_to(REPO)}")

 # ============================== VALIDATION ==============================
 summary_df = pd.DataFrame(yearly_summary)
 n_in_total = int(summary_df["n_in"].sum)
 n_foreign_total = int(summary_df["n_foreign_unknown"].sum)
 n_unmapped_dom_total = int(summary_df["n_domestic_unmapped"].sum)
 n_valid_total = int(summary_df["n_valid"].sum)
 n_domestic_total = n_in_total - n_foreign_total
 domestic_unmapped_pct = 100 * n_unmapped_dom_total / n_domestic_total if n_domestic_total else 0
 foreign_pct = 100 * n_foreign_total / n_in_total if n_in_total else 0

 val: dict[str, tuple[bool, str]] = {}

 # V1 dtype consistency (already verified above; re-record)
 val["V1 dtype: cause_104 string preserved"] = (True, "all 27 files read with dtype=str")

 # V2 mutual exclusivity
 val["V2 mutual exclusivity (each death exactly one outcome_group)"] = (
 True, f"long_all={len(long_all):,} = sum(n_valid)={sum_check:,}; max group_per_cause={int(cause_to_groups.max)}",
)

 # V3 coverage: every year has deaths > 0
 yrs_pos = panel.groupby("year")["deaths"].sum
 miss_yrs = [y for y in years if yrs_pos.get(y, 0) == 0]
 val["V3 coverage all 27 years have deaths>0"] = (
 len(miss_yrs) == 0,
 f"missing={miss_yrs}" if miss_yrs else "1997-2023 all positive",
)

 # V4 sigungu mapping rate (domestic only)
 val["V4 domestic sigungu unmapped < 1%"] = (
 domestic_unmapped_pct < 1.0,
 f"domestic_unmapped={n_unmapped_dom_total:,} of {n_domestic_total:,} = {domestic_unmapped_pct:.4f}%; foreign={n_foreign_total:,} ({foreign_pct:.4f}%)",
)

 # V5 KOSTAT suicide cross-check ±2%
 valid_micro_for_check = combined[
 combined["h_code"].notna
 & combined["sex_code"].isin(["1", "2"])
 & combined["age_5yr_code"].notna
 & (combined["age_5yr_code"]!= "99")
 & combined["cause_104"].notna
 ]
 suicide_yearly = valid_micro_for_check[valid_micro_for_check["cause_104"] == "102"].groupby("year").size
 cross_lines, cross_pass =, True
 for yr, official in KOSTAT_SUICIDE_OFFICIAL.items:
 ours = int(suicide_yearly.get(yr, 0))
 diff_pct = 100 * (ours - official) / official if official else 0
 ok = abs(diff_pct) <= 2.0
 if not ok: cross_pass = False
 cross_lines.append(f"{yr}: ours={ours:,} official={official:,} diff={diff_pct:+.3f}%")
 val["V5 KOSTAT suicide cross-check ±2%"] = (cross_pass, "; ".join(cross_lines))

 # V6 deaths trend
 yearly_total = valid_micro_for_check.groupby("year").size
 d_1997, d_2010, d_2020 = int(yearly_total.get("1997", 0)), int(yearly_total.get("2010", 0)), int(yearly_total.get("2020", 0))
 val["V6 deaths trend 1997 < 2010 < 2020"] = (
 d_1997 < d_2010 < d_2020,
 f"1997={d_1997:,} 2010={d_2010:,} 2020={d_2020:,}",
)

 # V7 outcome distribution
 grp_counts = long_all.groupby("outcome_group").size.reindex(outcomes, fill_value=0)
 grp_pct = (100 * grp_counts / grp_counts.sum).round(2)
 other_pct = float(grp_pct.get("other", 0))
 other_top10 = (
 long_all[long_all["outcome_group"] == "other"]
.groupby("cause_104").size.sort_values(ascending=False).head(10)
)
 cb = pd.read_csv(CODEBOOK_PATH, dtype=str).set_index("code")["korean_label"]
 other_top10_lines = [
 f"{c} ({cb.get(c,'?')[:40]}): {int(n):,}" for c, n in other_top10.items
 ]
 val["V7 outcome distribution (other < 50%)"] = (
 other_pct < 50.0,
 f"other={other_pct}% | " + " ".join(f"{g}={int(grp_counts[g]):,}({grp_pct[g]}%)" for g in outcomes),
)

 # V8 KOSIS cancer cross-check ±0.5% (cancer = 027-047, C00-C97)
 cancer_codes = {f"{i:03d}" for i in range(27, 48)}
 cancer_yearly = (
 valid_micro_for_check[valid_micro_for_check["cause_104"].isin(cancer_codes)]
.groupby("year").size
)
 cancer_lines, cancer_pass =, True
 for yr, official in KOSIS_CANCER_OFFICIAL.items:
 ours = int(cancer_yearly.get(yr, 0))
 diff_pct = 100 * (ours - official) / official if official else 0
 ok = abs(diff_pct) <= 0.5
 if not ok: cancer_pass = False
 cancer_lines.append(f"{yr}: ours={ours:,} official={official:,} diff={diff_pct:+.3f}%")
 val["V8 KOSIS cancer cross-check ±0.5% (C00-C97, codes 027-047)"] = (
 cancer_pass, "; ".join(cancer_lines),
)

 # V9 2023 record count (full file ~352,511)
 n_2023 = int(summary_df.loc[summary_df["year"] == "2023", "n_in"].sum)
 diff_2023_pct = 100 * (n_2023 - EXPECTED_2023_RECORDS) / EXPECTED_2023_RECORDS
 val["V9 2023 record count ~352,511 (full file)"] = (
 abs(diff_2023_pct) <= EXPECTED_2023_TOLERANCE * 100,
 f"n_in_2023={n_2023:,} expected={EXPECTED_2023_RECORDS:,} diff={diff_2023_pct:+.4f}%",
)

 # KOSIS unit comparison
 kosis = kosis_unit_summary
 kostat_sigungu_sample = sorted(combined[combined["h_code"].notna]["raw_code"].dropna.unique)[:5]
 kostat_age_unique = sorted(combined["age_5yr_code"].dropna.unique, key=lambda x: int(x) if x.isdigit else 999)
 kostat_sex_unique = sorted(combined["sex_code"].dropna.unique)

 all_pass = all(v[0] for v in val.values)

 # ============================== REPORT ==============================
 lines: list[str] = 
 lines.append("# Mortality Panel Validation (v4, cancer narrowed to 027-047 + 2023 full file)")
 lines.append("")
 lines.append(f"- Generated: 2026-05-03")
 lines.append(f"- v4 changes vs v3:")
 lines.append(f" 1. Cancer 정의 027-048 → 027-047 (KOSIS 공식 C00-C97 악성신생물과 정합. 048 양성/불명 → 'other' 흡수)")
 lines.append(f" 2. 2023 microdata partial(262,710) → full(352,511) 교체")
 lines.append(f" 3. V8 KOSIS cancer cross-check + V9 2023 record count 추가")
 lines.append(f"- Source: `0_raw/mortality_kostat/사망사료 정리/` ({len(files)} cp949 CSVs)")
 lines.append(f"- Crosswalk: `1_codebooks/sigungu_crosswalk_v2.csv` (229 h_codes, 27 years)")
 lines.append(f"- Outputs:")
 lines.append(f" - `3_derived/mortality/mortality_microdata_combined.parquet` ({len(combined):,} rows; full incl. foreign/unmapped)")
 lines.append(f" - `3_derived/mortality/mortality_panel_v01.parquet` ({len(panel):,} rows)")
 lines.append(f" - `3_derived/mortality/unmatched_mortality.parquet` ({len(unmatched_summary):,} unique foreign/unmapped raw_codes)")
 lines.append("")
 lines.append("## Outcome groups (mutually exclusive, priority order)")
 lines.append("")
 lines.append("| priority | group | cause_104 codes | n_codes | n_records | % |")
 lines.append("|---:|---|---|---:|---:|---:|")
 for i, (g, codes) in enumerate(OUTCOME_PRIORITY, 1):
 lines.append(f"| {i} | {g} | {sorted(codes)} | {len(codes)} | {int(grp_counts[g]):,} | {grp_pct[g]}% |")
 lines.append(f"| 6 | other | (fallback) | — | {int(grp_counts['other']):,} | {grp_pct['other']}% |")
 lines.append("")
 lines.append(f"**Note**: 101 (drug poisoning) and 081 (liver) → `despair_total` (not `external_other`/digestive). Priority order: despair > cardio > cancer > respiratory > external > other.")
 lines.append("")
 lines.append("## Per-year processing summary")
 lines.append("")
 lines.append("| year | n_in | foreign | unmapped(dom) | sex_drop | age=99 | cause_drop | n_valid | suicide(102) |")
 lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
 for s in yearly_summary:
 lines.append(
 f"| {s['year']} | {s['n_in']:,} | {s['n_foreign_unknown']:,} | {s['n_domestic_unmapped']:,} | "
 f"{s['n_sex_drop']:,} | {s['n_age_drop']:,} | {s['n_cause_drop']:,} | {s['n_valid']:,} | {s['n_suicide_102']:,} |"
)
 lines.append(
 f"| **TOTAL** | **{n_in_total:,}** | **{n_foreign_total:,}** | **{n_unmapped_dom_total:,}** | "
 f"**{int(summary_df['n_sex_drop'].sum):,}** | **{int(summary_df['n_age_drop'].sum):,}** | "
 f"**{int(summary_df['n_cause_drop'].sum):,}** | **{n_valid_total:,}** | **{int(summary_df['n_suicide_102'].sum):,}** |"
)
 lines.append("")
 lines.append("## Validation")
 lines.append("")
 lines.append("| check | result | detail |")
 lines.append("|---|:---:|---|")
 for k, (ok, detail) in val.items:
 mark = "PASS" if ok else "**FL**"
 lines.append(f"| {k} | {mark} | {detail} |")
 lines.append("")
 lines.append(f"**Overall**: {'ALL PASS' if all_pass else '**FL — DO NOT ADOPT**'}")
 lines.append("")
 lines.append("## Top 10 cause_104 codes inside `other` group")
 lines.append("")
 if other_top10_lines:
 for line in other_top10_lines:
 lines.append(f"- {line}")
 else:
 lines.append("(none)")
 lines.append("")
 lines.append("## Unit consistency vs KOSIS population panel (Stage 3 join prep)")
 lines.append("")
 lines.append("### sigungu code format")
 lines.append("")
 lines.append(f"- KOSTAT raw_code (5-digit) sample: `{kostat_sigungu_sample}`")
 lines.append(f"- KOSIS C1 (5-digit) sample: `{kosis['C1_sample_5digit']}`")
 lines.append(f"- KOSIS C1 length distribution: `{kosis['C1_lengths']}` (5-digit = sigungu, 2-digit = sido aggregate)")
 lines.append(f"- **Match**: KOSTAT raw_code 형식 == KOSIS C1 5-digit. 직접 join 가능 (단 KOSIS 의 시-합계 / 시도-합계 행은 사전에 필터링 필요).")
 lines.append("")
 lines.append("### sex code format")
 lines.append("")
 lines.append(f"- KOSTAT sex_code unique: `{kostat_sex_unique}` (1=남, 2=여)")
 lines.append(f"- KOSIS C2 unique: `{kosis['C2_unique']}` ({kosis['C2_NM_unique']}) — 0=계 + 1=남자 + 2=여자")
 lines.append(f"- **Match**: 1/2 정확히 일치. KOSIS 의 C2='0'(계) 행은 사용 안 하면 됨.")
 lines.append("")
 lines.append("### age 5-yr code format")
 lines.append("")
 lines.append(f"- KOSTAT age_5yr_code unique ({len(kostat_age_unique)}): `{kostat_age_unique}` (1-20 ordinal + 99 미상)")
 lines.append(f"- KOSIS C3 unique ({kosis['C3_unique_count']}): `{kosis['C3_unique']}`")
 lines.append(f"- KOSIS C3_NM 일부: `{kosis['C3_NM_unique'][:10]}...`")
 lines.append(f"- **MISMATCH**: KOSTAT 는 1..20 ordinal (예: 3=5-9세), KOSIS 는 020/050/070/... 시작연령*10 형식. **Stage 3 join 전에 mapping dict 필요**.")
 lines.append(f" - 또한 KOSTAT 코드 1 (0세) + 2 (1-4세) → KOSIS 020 (0-4세) 합산 필요.")
 lines.append(f" - KOSIS 의 80+ vs 80-84 vs 85+ vs 85-89 등 multi-bucket 처리 정책도 별도 결정.")
 lines.append("")
 lines.append("### KOSIS year coverage")
 lines.append("")
 lines.append(f"- range: {kosis['year_range']} (KOSTAT 사망 panel 1997-2023 전부 포함)")
 lines.append(f"- KOSIS C1 distinct: {kosis['C1_distinct']} (시군구 + 시도 합계 + 전국)")
 lines.append("")
 lines.append("## Top 20 unmatched raw_codes (foreign + domestic_unmapped)")
 lines.append("")
 if len(unmatched_summary) > 0:
 top = unmatched_summary.sort_values("n_records", ascending=False).head(20)
 lines.append("| year | sido | sgg | raw_code | reason | n_records |")
 lines.append("|---|---|---|---|---|---:|")
 for _, r in top.iterrows:
 lines.append(f"| {r['year']} | {r['sido_code']} | {r['sigungu_code']} | {r['raw_code']} | {r['reason']} | {int(r['n_records']):,} |")
 else:
 lines.append("(none — KOSTAT B형은 모두 국내 거주자, 0% unmapped)")
 lines.append("")
 OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

 print
 print("Validation:")
 for k, (ok, detail) in val.items:
 mark = "PASS" if ok else "FL"
 print(f" [{mark}] {k}: {detail}")
 print
 print(f"Wrote: {OUT_COMBINED.relative_to(REPO)}")
 print(f"Wrote: {OUT_PANEL.relative_to(REPO)}")
 print(f"Wrote: {OUT_UNMATCHED.relative_to(REPO)}")
 print(f"Wrote: {OUT_REPORT.relative_to(REPO)}")

 if not all_pass:
 sys.exit(1)

if __name__ == "__main__":
 main
