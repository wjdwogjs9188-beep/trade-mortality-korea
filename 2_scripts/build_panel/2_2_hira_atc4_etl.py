"""Phase 2 sub-task 2.2 -- HIRA ATC4 panel ETL.

Input:
 0_raw/hira_drug/hira_drug_panel_v02.csv (152,208 row, 168 sgguCd, ATC4 5 cat, 2010-2019)
 1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv (168, 167 MATCH)
 1_codebooks/intersection_main_hira_h_codes.csv (146 both TRUE)
 0_raw/kosis_population/population_combined.csv (working age 25-64 = C3 in {130,150,160,180,190,210,230,260}, C2=0 is sex total)

Output:
 3_derived/hira_atc4_panel.parquet (long)
 3_derived/hira_atc4_panel_wide.parquet (wide)
"""
import io
import os
import sys
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROJ = Path("C:/Users/82103/Downloads/trade_mortality_korea")
RAW_HIRA_CSV = PROJ / "0_raw" / "hira_drug" / "hira_drug_panel_v02.csv"
CW_PATH = PROJ / "1_codebooks" / "hira_sgguCd_to_hcode_crosswalk.csv"
INTERSECT_PATH = PROJ / "1_codebooks" / "intersection_main_hira_h_codes.csv"
POP_PATH = PROJ / "0_raw" / "kosis_population" / "population_combined.csv"
OUT_DIR = PROJ / "3_derived"
OUT_DIR.mkdir(exist_ok=True)

ATC4_LIST = ["N06AB", "N06AX", "N05BA", "N05AX", "A05BA"]
WA_C3_CODES = [130, 150, 160, 180, 190, 210, 230, 260]
YEAR_MIN, YEAR_MAX = 2010, 2019

def step1_load_hira:
 print("[step1] load HIRA raw")
 hira = pd.read_csv(RAW_HIRA_CSV, encoding="utf-8")
 print(f" raw rows: {len(hira):,}")
 hira["year"] = (hira["diagYm"] // 100).astype("int16")
 hira = hira[(hira["year"] >= YEAR_MIN) & (hira["year"] <= YEAR_MAX)]
 print(f" after year filter {YEAR_MIN}-{YEAR_MAX}: {len(hira):,}")
 hira = hira[hira["atcStep4Cd"].isin(ATC4_LIST)]
 print(f" after ATC4 5-cat filter: {len(hira):,}")
 agg = (
 hira.groupby(["sgguCd", "year", "atcStep4Cd"], as_index=False)["totUseQty"]
.sum
.rename(columns={"atcStep4Cd": "atc4", "totUseQty": "prescription_count"})
)
 print(f" aggregated (sgguCd, year, atc4) rows: {len(agg):,}")
 return agg

def step2_apply_crosswalk(hira_agg):
 print("[step2] apply crosswalk (sgguCd -> h_code)")
 cw = pd.read_csv(CW_PATH, encoding="utf-8")
 cw_match = cw[cw["status"] == "MATCH"][["sgguCd", "h_code"]].copy
 cw_match["h_code"] = cw_match["h_code"].astype("int32")
 print(f" crosswalk MATCH rows: {len(cw_match):,}")
 merged = hira_agg.merge(cw_match, on="sgguCd", how="inner")
 n_lost = len(hira_agg) - len(merged)
 print(f" after inner merge: {len(merged):,} (lost {n_lost} from UNMATCHED sgguCd)")
 return merged

def step3_population_join(df):
 print("[step3] KOSIS population join (working age 25-64, C2=0 sex total)")
 pop = pd.read_csv(POP_PATH, encoding="utf-8")
 pop_wa = pop[(pop["C2"] == 0) & (pop["C3"].isin(WA_C3_CODES))]
 pop_wa_agg = (
 pop_wa.groupby(["C1", "year"])["population"]
.sum
.reset_index
.rename(columns={"C1": "h_code", "population": "working_age_pop_25_64"})
)
 pop_wa_agg["h_code"] = pop_wa_agg["h_code"].astype("int32")
 print(f" pop working-age rows (h_code, year): {len(pop_wa_agg):,}")
 out = df.merge(pop_wa_agg, on=["h_code", "year"], how="left")
 miss_pop = out["working_age_pop_25_64"].isna.sum
 print(f" pop missing after join: {miss_pop} / {len(out):,}")
 out["prescription_rate_per_100k"] = (
 out["prescription_count"] / out["working_age_pop_25_64"].replace(0, pd.NA) * 1e5
)
 return out

def step4_intersection_flag(df):
 print("[step4] intersection flag (146 main n HIRA)")
 inter = pd.read_csv(INTERSECT_PATH, encoding="utf-8")
 intersect_h_codes = set(inter["h_code"].astype(int))
 print(f" intersection h_codes: {len(intersect_h_codes)}")
 df["in_intersection_146"] = df["h_code"].astype(int).isin(intersect_h_codes)
 return df

def step5_write_outputs(df):
 print("[step5] write parquet outputs")
 long_out = df[
 [
 "h_code",
 "year",
 "atc4",
 "prescription_count",
 "working_age_pop_25_64",
 "prescription_rate_per_100k",
 "in_intersection_146",
 ]
 ].copy
 long_out["h_code"] = long_out["h_code"].astype("int32")
 long_out["year"] = long_out["year"].astype("int16")
 long_out["atc4"] = long_out["atc4"].astype("string")
 long_out["prescription_count"] = long_out["prescription_count"].astype("float32")
 long_out["working_age_pop_25_64"] = long_out["working_age_pop_25_64"].astype("float32")
 long_out["prescription_rate_per_100k"] = long_out["prescription_rate_per_100k"].astype("float32")
 long_path = OUT_DIR / "hira_atc4_panel.parquet"
 long_out.to_parquet(long_path, index=False)
 print(f" wrote {long_path.name}: {len(long_out):,} rows")

 wide = df.pivot_table(
 index=["h_code", "year", "in_intersection_146", "working_age_pop_25_64"],
 columns="atc4",
 values="prescription_rate_per_100k",
 aggfunc="first",
).reset_index
 wide.columns.name = None
 rename_map = {c: c.lower + "_rate" for c in ATC4_LIST if c in wide.columns}
 wide = wide.rename(columns=rename_map)
 for c in [c.lower + "_rate" for c in ATC4_LIST]:
 if c in wide.columns:
 wide[c] = wide[c].astype("float32")
 wide["h_code"] = wide["h_code"].astype("int32")
 wide["year"] = wide["year"].astype("int16")
 wide["working_age_pop_25_64"] = wide["working_age_pop_25_64"].astype("float32")
 wide_path = OUT_DIR / "hira_atc4_panel_wide.parquet"
 wide.to_parquet(wide_path, index=False)
 print(f" wrote {wide_path.name}: {len(wide):,} rows")
 return long_out, wide

def step6_verify(long_out, wide):
 print("\n=== Audit-after-action 6-step verify ===\n")

 # 1. File integrity
 for fn in ["hira_atc4_panel.parquet", "hira_atc4_panel_wide.parquet"]:
 fp = OUT_DIR / fn
 print(f" [1] {fn}: exists={fp.exists}, size={os.path.getsize(fp) / 1024:.1f} KB")

 # 2. Schema check
 expected_long = [
 "h_code",
 "year",
 "atc4",
 "prescription_count",
 "working_age_pop_25_64",
 "prescription_rate_per_100k",
 "in_intersection_146",
 ]
 expected_wide_core = ["h_code", "year", "in_intersection_146", "working_age_pop_25_64"]
 expected_wide_rates = [c.lower + "_rate" for c in ATC4_LIST]
 pl = pd.read_parquet(OUT_DIR / "hira_atc4_panel.parquet")
 pw = pd.read_parquet(OUT_DIR / "hira_atc4_panel_wide.parquet")
 miss_l = set(expected_long) - set(pl.columns)
 miss_w = set(expected_wide_core + expected_wide_rates) - set(pw.columns)
 print(f" [2] long schema OK: {not miss_l} (missing={miss_l})")
 print(f" [2] wide schema OK: {not miss_w} (missing={miss_w})")

 # 3. NaN profile
 nan_rate = long_out["prescription_rate_per_100k"].isna.mean
 print(f" [3] prescription_rate_per_100k NaN ratio: {nan_rate:.4f} (threshold 0.10)")
 if nan_rate >= 0.10:
 print(" [3] WARNING: NaN ratio exceeds 10% -- issue")

 # 4. Intersection sample row count
 intersect_rows = long_out[long_out["in_intersection_146"]]
 expected_intersect = 5 * 146 * 10
 print(
 f" [4] intersection long rows: {len(intersect_rows):,} (expected {expected_intersect:,})"
)
 intersect_wide = wide[wide["in_intersection_146"]]
 print(f" [4] intersection wide rows: {len(intersect_wide):,} (expected {146 * 10:,})")

 # 5. Year coverage per sigungu
 year_cov = long_out.groupby("h_code")["year"].nunique
 print(
 f" [5] year coverage min/median/max: {year_cov.min}/"
 f"{year_cov.median:.0f}/{year_cov.max}"
)
 print(f" [5] distinct h_code in long: {long_out['h_code'].nunique}")

 # 6. Outlier check by ATC4
 print(" [6] outliers by ATC4 (rate per 100k):")
 summary_rows = 
 for atc in ATC4_LIST:
 sub = long_out[long_out["atc4"] == atc]["prescription_rate_per_100k"].dropna
 if len(sub) == 0:
 print(f" {atc}: no rows")
 continue
 med = sub.median
 p99 = sub.quantile(0.99)
 n_out = (sub > p99).sum
 print(f" {atc}: n={len(sub):,}, median={med:,.0f}, p99={p99:,.0f}, n_outlier={n_out}")
 summary_rows.append((atc, len(sub), med, p99, n_out))

 print("\n=== Verify complete ===\n")
 return {
 "nan_rate": float(nan_rate),
 "intersect_rows_long": int(len(intersect_rows)),
 "intersect_rows_wide": int(len(intersect_wide)),
 "year_cov_min": int(year_cov.min),
 "year_cov_max": int(year_cov.max),
 "h_code_n": int(long_out["h_code"].nunique),
 "atc4_summary": summary_rows,
 }

def main:
 hira_agg = step1_load_hira
 hira_cw = step2_apply_crosswalk(hira_agg)
 hira_full = step3_population_join(hira_cw)
 hira_full = step4_intersection_flag(hira_full)
 long_out, wide = step5_write_outputs(hira_full)
 step6_verify(long_out, wide)

if __name__ == "__main__":
 main
