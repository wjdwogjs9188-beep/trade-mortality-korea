"""Phase 2 sub-task 2.3 -- M1 composite outcome variable.

Inputs:
 3_derived/hira_atc4_panel.parquet (long, from sub-task 2.2)
 1_codebooks/intersection_main_hira_h_codes.csv (146 both-TRUE)
 8_submission/paper_v01_submission/02_bartik_iv/iv_z_x_bilateral.parquet (z_x, z_x_per_worker)

Outputs:
 3_derived/hira_m1_panel.parquet (wide, h x year x M1 alts)
 3_derived/hira_delta_m1_panel.parquet (long-difference DM1)
 3_derived/hira_first_stage_scatter.parquet

Notes vs prompt spec:
- prompt assumes a 147-intersection cumulative commit (220001 -> 23090 crosswalk fix).
 Current panel has 146 intersection (167 MATCH crosswalk). We proceed with the
 actual 146 sample and column `in_intersection_146` and report the gap as a P1
 issue at end.
"""
import io
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import statsmodels.api as sm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
PANEL_LONG = PROJ / "3_derived" / "hira_atc4_panel.parquet"
INTERSECT_PATH = PROJ / "1_codebooks" / "intersection_main_hira_h_codes.csv"
IV_PATH = (
 PROJ / "8_submission" / "paper_v01_submission" / "02_bartik_iv" / "iv_z_x_bilateral.parquet"
)
OUT_DIR = PROJ / "3_derived"

ATC4_LIST = ["N06AB", "N06AX", "N05BA", "N05AX", "A05BA"]
MENTAL_ATC4 = ["N06AB", "N06AX", "N05BA", "N05AX"]
INTERSECT_COL = "in_intersection_147"
INTERSECT_N = 147

def step1_load:
 print("[step1] load HIRA panel + intersection")
 panel = pd.read_parquet(PANEL_LONG)
 intersect = pd.read_csv(INTERSECT_PATH, encoding="utf-8")
 print(f" panel rows: {len(panel):,}")
 print(f" intersection sigungu: {len(intersect)}")
 print(f" panel intersection flag rows: {panel[INTERSECT_COL].sum}")
 return panel

def step2_wide_log_z(panel):
 print("[step2] wide pivot + log + z-score")
 wide = panel.pivot_table(
 index=["h_code", "year", INTERSECT_COL, "working_age_pop_25_64"],
 columns="atc4",
 values="prescription_rate_per_100k",
 aggfunc="first",
).reset_index
 wide.columns.name = None
 print(f" wide rows: {len(wide):,}, atc4 cols: {[c for c in wide.columns if c in ATC4_LIST]}")

 for atc in ATC4_LIST:
 if atc not in wide.columns:
 wide[atc] = np.nan
 wide[f"log_{atc.lower}"] = np.log(wide[atc] + 1)

 z_stats = {}
 for atc in ATC4_LIST:
 col_log = f"log_{atc.lower}"
 mu = wide[col_log].mean
 sigma = wide[col_log].std
 wide[f"z_{atc.lower}"] = (wide[col_log] - mu) / sigma
 z_stats[atc] = (mu, sigma)
 print(f" {atc}: mu_log={mu:.3f}, sigma_log={sigma:.3f}")
 return wide, z_stats

def step3_composites(wide):
 print("[step3] M1 composite (Alt 0/1/2/3)")
 z_cols_5 = [f"z_{a.lower}" for a in ATC4_LIST]
 z_cols_4 = [f"z_{a.lower}" for a in MENTAL_ATC4]

 wide["m1_composite"] = wide[z_cols_5].mean(axis=1, skipna=False)
 wide["m1_4mental"] = wide[z_cols_4].mean(axis=1, skipna=False)
 wide["m1_liver"] = wide["z_a05ba"]

 mask_complete = wide[z_cols_5].notna.all(axis=1)
 n_complete = int(mask_complete.sum)
 print(f" complete-case rows for PCA: {n_complete} / {len(wide)}")
 pca = PCA(n_components=1)
 pca_fit = pca.fit_transform(wide.loc[mask_complete, z_cols_5].values)
 wide["m1_pca1"] = np.nan
 wide.loc[mask_complete, "m1_pca1"] = pca_fit.flatten
 pca_evar = float(pca.explained_variance_ratio_[0])
 pca_loadings = pca.components_[0].tolist
 print(f" PCA 1st explained variance: {pca_evar:.3f}")
 print(f" PCA 1st loadings: {dict(zip(ATC4_LIST, [round(x, 3) for x in pca_loadings]))}")

 cor = wide[z_cols_5].corr
 print(" z cross-ATC4 correlation:")
 print(cor.round(3).to_string)
 return wide, pca_evar, pca_loadings

def step4_long_diff(wide):
 print("[step4] long-difference (M1_2019 - M1_2010)")
 cols = ["m1_composite", "m1_4mental", "m1_liver", "m1_pca1"]

 w10 = (
 wide[wide["year"] == 2010][["h_code", INTERSECT_COL] + cols]
.copy
.rename(columns={c: f"{c}_2010" for c in cols})
)
 w19 = (
 wide[wide["year"] == 2019][["h_code"] + cols]
.copy
.rename(columns={c: f"{c}_2019" for c in cols})
)
 delta = w10.merge(w19, on="h_code", how="outer")
 for c in cols:
 delta[f"delta_{c}"] = delta[f"{c}_2019"] - delta[f"{c}_2010"]
 delta["complete_case"] = (
 delta["m1_composite_2010"].notna & delta["m1_composite_2019"].notna
)
 delta[INTERSECT_COL] = delta[INTERSECT_COL].fillna(False)
 print(f" delta panel sigungu: {len(delta)}")
 print(
 f" complete-case ALL: {int(delta['complete_case'].sum)}, "
 f"intersection: {int((delta[INTERSECT_COL] & delta['complete_case']).sum)}"
)
 return delta

def step5_first_stage(delta):
 print("[step5] first-stage z_x x DM1 (intersection complete-case)")
 iv = pd.read_parquet(IV_PATH)
 iv["h_code"] = iv["h_code"].astype(int)
 delta_for_merge = delta.copy
 delta_for_merge["h_code"] = delta_for_merge["h_code"].astype(int)

 fs = delta_for_merge.merge(
 iv[["h_code", "z_x", "z_x_per_worker"]], on="h_code", how="inner"
)
 print(f" delta x IV merge: {len(fs)} sigungu")

 fs_clean = fs[fs["complete_case"]].copy
 fs_int = fs_clean[fs_clean[INTERSECT_COL]].copy
 print(f" intersection complete-case for first-stage: {len(fs_int)}")

 if len(fs_int) >= 5 and fs_int["z_x_per_worker"].std > 0:
 zx = fs_int["z_x_per_worker"]
 fs_int["z_x_std"] = (zx - zx.mean) / zx.std
 X = sm.add_constant(fs_int["z_x_std"])
 fit = sm.OLS(fs_int["delta_m1_composite"], X).fit(cov_type="HC1")
 fs_F = float(fit.fvalue)
 fs_p = float(fit.f_pvalue)
 gamma = float(fit.params.iloc[1])
 gamma_se = float(fit.bse.iloc[1])
 gamma_t = float(fit.tvalues.iloc[1])
 print(f" first-stage F={fs_F:.2f}, p={fs_p:.4f}")
 print(
 f" gamma_FS={gamma:+.6f} (SE={gamma_se:.6f}, t={gamma_t:+.4f}) on z_x_std"
)
 else:
 fs_F = fs_p = gamma = gamma_se = gamma_t = float("nan")
 print(" insufficient sample for first-stage")
 return fs_clean, {"F": fs_F, "p": fs_p, "gamma": gamma, "se": gamma_se, "t": gamma_t}

def step6_write(wide, delta, fs_clean):
 print("[step6] write parquet outputs")
 wide_out = wide[
 [
 "h_code",
 "year",
 "m1_composite",
 "m1_4mental",
 "m1_liver",
 "m1_pca1",
 "working_age_pop_25_64",
 INTERSECT_COL,
 ]
 ].copy
 for c in ["m1_composite", "m1_4mental", "m1_liver", "m1_pca1", "working_age_pop_25_64"]:
 wide_out[c] = wide_out[c].astype("float32")
 wide_out["h_code"] = wide_out["h_code"].astype("int32")
 wide_out["year"] = wide_out["year"].astype("int16")
 p1 = OUT_DIR / "hira_m1_panel.parquet"
 wide_out.to_parquet(p1, index=False)
 print(f" wrote {p1.name}: {len(wide_out):,} rows, {os.path.getsize(p1) / 1024:.1f} KB")

 delta_out = delta[
 [
 "h_code",
 "delta_m1_composite",
 "delta_m1_4mental",
 "delta_m1_liver",
 "delta_m1_pca1",
 INTERSECT_COL,
 "complete_case",
 ]
 ].copy
 for c in ["delta_m1_composite", "delta_m1_4mental", "delta_m1_liver", "delta_m1_pca1"]:
 delta_out[c] = delta_out[c].astype("float32")
 delta_out["h_code"] = delta_out["h_code"].astype("int32")
 p2 = OUT_DIR / "hira_delta_m1_panel.parquet"
 delta_out.to_parquet(p2, index=False)
 print(f" wrote {p2.name}: {len(delta_out):,} rows, {os.path.getsize(p2) / 1024:.1f} KB")

 fs_out = fs_clean[
 ["h_code", "z_x", "z_x_per_worker", "delta_m1_composite", INTERSECT_COL]
 ].copy
 fs_out["h_code"] = fs_out["h_code"].astype("int32")
 fs_out["z_x"] = fs_out["z_x"].astype("float64")
 fs_out["z_x_per_worker"] = fs_out["z_x_per_worker"].astype("float64")
 fs_out["delta_m1_composite"] = fs_out["delta_m1_composite"].astype("float32")
 p3 = OUT_DIR / "hira_first_stage_scatter.parquet"
 fs_out.to_parquet(p3, index=False)
 print(f" wrote {p3.name}: {len(fs_out):,} rows, {os.path.getsize(p3) / 1024:.1f} KB")
 return wide_out, delta_out, fs_out

def step7_verify(wide_out, delta_out, fs_out, pca_evar, fs_stats):
 print("\n=== Audit-after-action 6-step verify ===\n")

 # 1. file integrity
 for fn in [
 "hira_m1_panel.parquet",
 "hira_delta_m1_panel.parquet",
 "hira_first_stage_scatter.parquet",
 ]:
 fp = OUT_DIR / fn
 print(f" [1] {fn}: exists={fp.exists}, size={os.path.getsize(fp) / 1024:.1f} KB")

 # 2. schema
 exp_wide = {
 "h_code",
 "year",
 "m1_composite",
 "m1_4mental",
 "m1_liver",
 "m1_pca1",
 "working_age_pop_25_64",
 INTERSECT_COL,
 }
 exp_delta = {
 "h_code",
 "delta_m1_composite",
 "delta_m1_4mental",
 "delta_m1_liver",
 "delta_m1_pca1",
 INTERSECT_COL,
 "complete_case",
 }
 exp_fs = {"h_code", "z_x", "z_x_per_worker", "delta_m1_composite", INTERSECT_COL}
 print(f" [2] m1_panel schema OK: {exp_wide.issubset(set(wide_out.columns))}")
 print(f" [2] delta_panel schema OK: {exp_delta.issubset(set(delta_out.columns))}")
 print(f" [2] first_stage schema OK: {exp_fs.issubset(set(fs_out.columns))}")

 # 3. M1 composite distribution
 m1 = wide_out["m1_composite"].dropna
 print(
 f" [3] m1_composite: n={len(m1)}, min={m1.min:.3f}, max={m1.max:.3f}, "
 f"mean={m1.mean:.3f}, std={m1.std:.3f}"
)
 for c in ["m1_4mental", "m1_liver", "m1_pca1"]:
 s = wide_out[c].dropna
 print(f" [3] {c}: n={len(s)}, mean={s.mean:.3f}, std={s.std:.3f}")

 # 4. complete-case
 cc_total = int(delta_out["complete_case"].sum)
 cc_int = int((delta_out[INTERSECT_COL] & delta_out["complete_case"]).sum)
 print(f" [4] complete-case sigungu (all): {cc_total} / {len(delta_out)}")
 print(f" [4] complete-case sigungu (intersection {INTERSECT_N}): {cc_int} / {INTERSECT_N}")

 # 5. PCA explained variance
 print(f" [5] PCA 1st explained variance: {pca_evar:.3f} (expected > 0.60)")
 if pca_evar < 0.60:
 print(" [5] WARNING: PCA explained variance below 0.60 -- P3 issue")

 # 6. First-stage F
 print(
 f" [6] first-stage F={fs_stats['F']:.2f}, p={fs_stats['p']:.4f}, "
 f"gamma_FS={fs_stats['gamma']:+.6f} (t={fs_stats['t']:+.3f})"
)

 print("\n=== Verify complete ===\n")

def main:
 panel = step1_load
 wide, _ = step2_wide_log_z(panel)
 wide, pca_evar, _ = step3_composites(wide)
 delta = step4_long_diff(wide)
 fs_clean, fs_stats = step5_first_stage(delta)
 wide_out, delta_out, fs_out = step6_write(wide, delta, fs_clean)
 step7_verify(wide_out, delta_out, fs_out, pca_evar, fs_stats)

if __name__ == "__main__":
 main
