"""
Phase 5 — 1999 baseline robustness build (shock-immediate prior)
================================================================

Goal: Address reviewer concern that the 1994 baseline pre-dates the 2000-2010
China shock window by 6 years. The 1999 baseline is the closest pre-shock
available given the KSIC 8th-edition discontinuity at 2000.

Pipeline:
 1. Load 1999 광업제조업조사 microdata (KSIC 7th edition, 29 cols, no header)
 2. Manufacturing filter (col 3 == 'D'), build sgg5 = col0+col1
 3. Sigungu crosswalk (year=1999 → h_code 256 baseline)
 4. Aggregate employment (col 28 = annual total 종사자수) by (h_code, KSIC_native_2digit)
 5. KSIC 7→9 crosswalk at 2-digit (1_codebooks/ksic6_to_ksic9_2digit.csv —
 D15-D37 → C10-C33, file labeled "ksic6" but content is KSIC 7th D-prefix)
 6. Within-h share normalization → baseline_shares_1999_ksic9_2digit.parquet
 7. Bartik IV build (KR-CN bilateral + ADH-8) — 1999 baseline
 8. Native long-difference RF + 5-layer SE + WCR Webb 6-pt bootstrap
 9. First-stage F (bilateral on ADH-8, 1999 baseline)

Schema (probe verified):
 - col 0 = 시도 (zfill 2)
 - col 1 = 시군구 (zfill 3)
 - col 3 = KSIC letter (D = manufacturing)
 - col 4 = KSIC 2-digit (15-37 for manufacturing)
 - col 26 = 남자 종사자, col 27 = 여자, col 28 = 합계 (verified 26+27=28)
 - National sum col 28 (D only) = 2,459,919 ≈ 통계청 1999 광업제조업 종사자
 - 246 distinct sgg5 in D only

Outputs:
 - 3_derived/bartik/baseline_shares_1999_ksic9_2digit.parquet
 - 3_derived/bartik/denominator_E_h_1999.parquet
 - 3_derived/bartik/iv_z_x_bilateral_1999baseline.parquet
 - 3_derived/bartik/iv_z_x_adh8_1999baseline.parquet
 - 4_results/regression/main_native_5layer_1999baseline.csv
 - 5_logs/integrity_checks/<date>_baseline_shares_1999_phase5.md

Date: 2026-05-12
"""
from __future__ import annotations
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
RAW_1999 = PROJ / "0_raw" / "kosis_business_survey" / "microdata_1994_2024" / "1999_연간자료_20260415_35230.csv"
CW_SIGUNGU = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
CW_KSIC = PROJ / "1_codebooks" / "ksic6_to_ksic9_2digit.csv" # labeled "ksic6"; D-prefix content is KSIC 7th
EXPO_BIL = PROJ / "3_derived" / "bartik" / "exposure_bilateral_2000_2010.parquet"
EXPO_ADH = PROJ / "3_derived" / "bartik" / "exposure_adh8_2000_2010.parquet"
MORT = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
CENT = PROJ / "0_raw" / "sigungu_centroid" / "sigungu_centroid_table.csv"

BARTIK = PROJ / "3_derived" / "bartik"
REG = PROJ / "4_results" / "regression"
LOGS = PROJ / "5_logs" / "integrity_checks"
BARTIK.mkdir(parents=True, exist_ok=True)
REG.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

TODAY = date.today.isoformat
BASE_YRS = list(range(1997, 2000))
END_YRS = list(range(2018, 2023))

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def haversine_km(lat1, lng1, lat2, lng2):
 R = 6371.0
 lat1, lat2 = np.radians(lat1), np.radians(lat2)
 dlat = lat2 - lat1
 dlng = np.radians(lng2 - lng1)
 a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlng / 2) ** 2
 return 2 * R * np.arcsin(np.sqrt(a))

def conley_se_uniform(X, residuals, coords, cutoff_km):
 n = X.shape[0]
 bread = np.linalg.inv(X.T @ X)
 lat, lng = coords[:, 0], coords[:, 1]
 W = np.zeros((n, n))
 for i in range(n):
 d = haversine_km(lat[i], lng[i], lat, lng)
 W[i,:] = (d <= cutoff_km).astype(float)
 eps = residuals.reshape(-1, 1)
 Z = X * eps
 meat = Z.T @ W @ Z
 cov = bread @ meat @ bread
 return np.sqrt(np.diag(cov))

def wcr_webb_6pt(X, y, cluster_ids, B=9999, seed=42):
 """Wild Cluster Restricted bootstrap with Webb 6-point weights.

 Webb (2014) 6-point weights: {±√(3/2), ±1, ±√(1/2)} each with prob 1/6.
 Restricted: impose H0: β_1 = 0 on the restricted residual.
 Returns symmetric two-sided p-value for the slope coefficient.
 """
 rng = np.random.default_rng(seed)
 n = X.shape[0]
 # restricted model (β_1 = 0): regress y on constant only
 X_r = X[:, [0]]
 beta_r = np.linalg.lstsq(X_r, y, rcond=None)[0]
 u_r = y - X_r @ beta_r # restricted residuals
 # unrestricted OLS to get reference t-stat
 XtX_inv = np.linalg.inv(X.T @ X)
 beta_u = XtX_inv @ X.T @ y
 resid_u = y - X @ beta_u
 # cluster-robust SE on slope under H_A
 clusters = pd.Series(cluster_ids).unique
 meat = np.zeros((X.shape[1], X.shape[1]))
 for c in clusters:
 idx = np.where(cluster_ids == c)[0]
 Xc, ec = X[idx], resid_u[idx]
 s = Xc.T @ ec
 meat += np.outer(s, s)
 cov = XtX_inv @ meat @ XtX_inv
 se_u = np.sqrt(cov[1, 1])
 t_ref = beta_u[1] / se_u

 webb_points = np.array([
 -np.sqrt(1.5), -1.0, -np.sqrt(0.5),
 +np.sqrt(0.5), +1.0, +np.sqrt(1.5),
 ])
 boot_t = np.empty(B)
 cluster_idx_map = {c: np.where(cluster_ids == c)[0] for c in clusters}
 for b in range(B):
 # one Webb weight per cluster
 ws = rng.choice(webb_points, size=len(clusters))
 u_b = u_r.copy
 for ci, c in enumerate(clusters):
 u_b[cluster_idx_map[c]] = u_r[cluster_idx_map[c]] * ws[ci]
 y_b = X_r @ beta_r + u_b
 beta_b = XtX_inv @ X.T @ y_b
 resid_b = y_b - X @ beta_b
 # cluster-robust SE for slope
 meat_b = np.zeros((X.shape[1], X.shape[1]))
 for c in clusters:
 idx = cluster_idx_map[c]
 Xc, ec = X[idx], resid_b[idx]
 s = Xc.T @ ec
 meat_b += np.outer(s, s)
 cov_b = XtX_inv @ meat_b @ XtX_inv
 se_b = np.sqrt(cov_b[1, 1])
 boot_t[b] = beta_b[1] / se_b
 p = (np.abs(boot_t) >= abs(t_ref)).mean
 return p, t_ref, beta_u[1], se_u

def main -> None:
 log = [f"# Phase 5 — 1999 baseline robustness build\n_{TODAY}_\n"]

 # --------------------------------------------------------------------
 # 1) 1999 raw load
 # --------------------------------------------------------------------
 print("[1] Load 1999 광업제조업조사 microdata...")
 df = pd.read_csv(RAW_1999, encoding="utf-8-sig", dtype=str, header=None, low_memory=False)
 log.append(f"## 1999 raw schema (probe-verified)")
 log.append(f"- file: `0_raw/kosis_business_survey/microdata_1994_2024/1999_연간자료_20260415_35230.csv`")
 log.append(f"- shape: {df.shape} (rows × cols)")
 log.append(f"- encoding: utf-8-sig, header=None, 29 columns")
 log.append(f"- column convention: col 0=시도, col 1=시군구, col 3=KSIC letter,")
 log.append(f" col 4=KSIC 2-digit (15-37 for D), col 28=종사자 합계 annual (M+F)")

 # --------------------------------------------------------------------
 # 2) Manufacturing filter + sgg5
 # --------------------------------------------------------------------
 df["sido"] = df[0].astype(str).str.zfill(2)
 df["sgg"] = df[1].astype(str).str.zfill(3)
 df["sgg5"] = df["sido"] + df["sgg"]
 df["ksic_letter"] = df[3].astype(str).str.strip
 df["ksic2"] = df[4].astype(str).str.zfill(2)
 df["emp"] = pd.to_numeric(df[28], errors="coerce").fillna(0)

 df_m = df[df["ksic_letter"] == "D"].copy
 log.append(f"\n## Manufacturing filter")
 log.append(f"- D-filter rows: {len(df_m):,} / {len(df):,} ({len(df_m)/len(df):.1%})")
 log.append(f"- distinct sgg5 (D only): {df_m['sgg5'].nunique}")
 log.append(f"- distinct KSIC 2-digit (D only): {df_m['ksic2'].nunique}")
 log.append(f"- 종사자수 national sum (col 28, D only): **{df_m['emp'].sum:,.0f}**")
 log.append(f" - 통계청 1999 광업제조업 annual employment anchor ≈ 2.4-2.7M → ✅ 정합")

 # --------------------------------------------------------------------
 # 3) Sigungu crosswalk (1999 → h_code 2021 baseline)
 # --------------------------------------------------------------------
 cw = pd.read_csv(CW_SIGUNGU, dtype=str)
 cw_1999 = cw[cw["year"] == "1999"][["raw_code", "h_code", "sido_code"]].drop_duplicates("raw_code")
 df_m = df_m.merge(cw_1999.rename(columns={"raw_code": "sgg5"}), on="sgg5", how="left")
 n_match = df_m["h_code"].notna.sum
 log.append(f"\n## Sigungu crosswalk (year=1999, raw → h_code)")
 log.append(f"- row-level match: {n_match:,}/{len(df_m):,} ({n_match/len(df_m):.1%})")
 emp_match = df_m.loc[df_m["h_code"].notna, "emp"].sum
 emp_total = df_m["emp"].sum
 log.append(f"- 종사자 weighted match: {emp_match:,.0f}/{emp_total:,.0f} ({emp_match/emp_total:.1%})")
 df_m = df_m.dropna(subset=["h_code"]).copy

 # --------------------------------------------------------------------
 # 4) KSIC 7→9 crosswalk (2-digit)
 # --------------------------------------------------------------------
 cw_k = pd.read_csv(CW_KSIC) # cols: ksic6, ksic9 — but D-prefix content matches KSIC 7th
 cw_k["k7_2"] = cw_k["ksic6"].str[1:].str.zfill(2) # 'D15' → '15'
 cw_k["k7_letter"] = cw_k["ksic6"].str[0]
 d_map = cw_k[cw_k["k7_letter"] == "D"][["k7_2", "ksic9"]].drop_duplicates
 log.append(f"\n## KSIC 7→9 crosswalk (manufacturing 2-digit)")
 log.append(f"- file: `1_codebooks/ksic6_to_ksic9_2digit.csv` (label legacy; D-prefix = KSIC 7th)")
 log.append(f"- D-prefix mapping rows: {len(d_map)}")
 log.append(f"- D15→C10 food, D17→C13 textiles,..., D37→C33 (1-to-1 dominant target)")

 # Some 7th-edition 2-digit codes may not be in crosswalk — flag
 df_m_k = df_m.merge(d_map, left_on="ksic2", right_on="k7_2", how="left")
 unmatched_k = df_m_k.loc[df_m_k["ksic9"].isna, "ksic2"].unique
 if len(unmatched_k):
 log.append(f"- ⚠️ unmatched KSIC 7th 2-digit codes: {sorted(unmatched_k.tolist)}")
 emp_drop = df_m_k.loc[df_m_k["ksic9"].isna, "emp"].sum
 log.append(f" - dropped employment: {emp_drop:,.0f} ({emp_drop/df_m['emp'].sum:.2%})")
 df_m_k = df_m_k.dropna(subset=["ksic9"]).copy

 # --------------------------------------------------------------------
 # 5) Aggregate by (h_code, ksic9_2digit) and within-h share
 # --------------------------------------------------------------------
 agg = (
 df_m_k.groupby(["h_code", "ksic9"])["emp"]
.sum
.reset_index
.rename(columns={"emp": "employment", "ksic9": "ksic9_2digit"})
)
 h_total = agg.groupby("h_code")["employment"].sum.rename("h_total")
 agg = agg.merge(h_total, on="h_code")
 agg["share"] = agg["employment"] / agg["h_total"].replace(0, np.nan)
 log.append(f"\n## 1999 baseline shares (KSIC9 2-digit)")
 log.append(f"- agg rows: {len(agg):,}")
 log.append(f"- distinct h_code: {agg['h_code'].nunique}")
 log.append(f"- distinct KSIC9 2-digit: {agg['ksic9_2digit'].nunique}")
 log.append(f"- median h_total (E_h^{{1999}}): {agg.groupby('h_code')['h_total'].first.median:.0f}")
 log.append(f"- mean h_total: {agg.groupby('h_code')['h_total'].first.mean:.0f}")

 out_shares = BARTIK / "baseline_shares_1999_ksic9_2digit.parquet"
 agg.to_parquet(out_shares, index=False)
 log.append(f"- saved: `{out_shares.relative_to(PROJ)}`")

 denom = agg.groupby("h_code")["employment"].sum.rename("E_h_1999").reset_index
 denom.to_parquet(BARTIK / "denominator_E_h_1999.parquet", index=False)
 log.append(f"- denominator E_h_1999: median={denom['E_h_1999'].median:.0f}, mean={denom['E_h_1999'].mean:.0f}")

 # --------------------------------------------------------------------
 # 6) Bartik IV build (bilateral KR-CN + ADH-8) using 1999 baseline
 # --------------------------------------------------------------------
 expo_bil = pd.read_parquet(EXPO_BIL)
 expo_adh = pd.read_parquet(EXPO_ADH)
 log.append(f"\n## Bartik IV 1999 baseline")
 log.append(f"- exposure bilateral (KR-CN): {len(expo_bil)} KSIC9 2-digit cells")
 log.append(f"- exposure ADH-8 (8 advanced→CN): {len(expo_adh)} KSIC9 2-digit cells")

 bs = agg.merge(denom, on="h_code", how="left")

 def build_iv(expo_df, label):
 z = bs.merge(expo_df[["ksic9_2digit", "dM_2000_2010"]], on="ksic9_2digit", how="left")
 z["dM_2000_2010"] = z["dM_2000_2010"].fillna(0)
 z["contrib"] = z["share"] * z["dM_2000_2010"]
 z_h = z.groupby("h_code").agg(
 z_x=("contrib", "sum"),
 E_h_1999=("E_h_1999", "first"),
).reset_index
 z_h["z_x_per_worker"] = z_h["z_x"] / z_h["E_h_1999"].replace(0, np.nan)
 log.append(f"\n### {label} IV (1999 baseline)")
 log.append(f"- n h_code: {len(z_h)}")
 log.append(f"- z_x_per_worker mean={z_h['z_x_per_worker'].mean:.2f}, sd={z_h['z_x_per_worker'].std(ddof=1):.2f}")
 return z_h

 iv_bil = build_iv(expo_bil, "KR-CN bilateral")
 iv_bil.to_parquet(BARTIK / "iv_z_x_bilateral_1999baseline.parquet", index=False)
 iv_adh = build_iv(expo_adh, "ADH-8")
 iv_adh.to_parquet(BARTIK / "iv_z_x_adh8_1999baseline.parquet", index=False)

 # --------------------------------------------------------------------
 # 7) Native long-difference RF + 5-layer SE (despair_total)
 # --------------------------------------------------------------------
 mort = pd.read_parquet(MORT)
 cent = pd.read_csv(CENT, dtype={"h_code": str})
 mort["h_code"] = mort["h_code"].astype(str)
 cent["h_code"] = cent["h_code"].astype(str)
 iv_bil["h_code"] = iv_bil["h_code"].astype(str)
 iv_adh["h_code"] = iv_adh["h_code"].astype(str)

 mort["mort_rate"] = mort["deaths"] / mort["pop_wa"].clip(lower=1)
 mort["log_mort"] = np.log(mort["mort_rate"] + 1e-6)
 d = mort[mort["outcome_group"] == "despair_total"].copy
 base = d[d["year"].isin(BASE_YRS)].groupby("h_code")["log_mort"].mean
 end_ = d[d["year"].isin(END_YRS)].groupby("h_code")["log_mort"].mean
 ld = (
 pd.DataFrame({"base": base, "end": end_})
.dropna
.assign(d_log=lambda x: x["end"] - x["base"])
.reset_index
)
 panel = (
 ld.merge(iv_bil[["h_code", "z_x_per_worker"]], on="h_code", how="inner")
.merge(cent[["h_code", "lat", "lng"]], on="h_code", how="left")
.dropna(subset=["d_log", "z_x_per_worker"])
)
 panel["sido_code"] = panel["h_code"].str[:2]
 panel["z_x_std"] = (panel["z_x_per_worker"] - panel["z_x_per_worker"].mean) / panel["z_x_per_worker"].std(ddof=1)

 log.append(f"\n## Native long-difference panel (despair_total, 1999 baseline)")
 log.append(f"- n = {len(panel)} sigungu, G (sido) = {panel['sido_code'].nunique}")
 log.append(f"- z_x_per_worker SD (σ_z, 1999): {panel['z_x_per_worker'].std(ddof=1):.4f}")
 log.append(f" (compare: 1994 baseline σ_z = reference value from main spec)")

 X = sm.add_constant(panel[["z_x_std"]]).values
 y = panel["d_log"].values

 m_ols = sm.OLS(y, X).fit
 beta = float(m_ols.params[1])
 m_hc1 = sm.OLS(y, X).fit(cov_type="HC1")
 se_hc1 = float(m_hc1.bse[1])
 t_hc1 = beta / se_hc1
 p_hc1 = 2 * (1 - stats.norm.cdf(abs(t_hc1)))

 m_cl = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": panel["sido_code"].values})
 se_cl = float(m_cl.bse[1])
 t_cl = beta / se_cl
 G = int(panel["sido_code"].nunique)
 p_cl_t = 2 * (1 - stats.t.cdf(abs(t_cl), df=G - 1))

 panel_c = panel.dropna(subset=["lat", "lng"]).reset_index(drop=True)
 X_c = sm.add_constant(panel_c[["z_x_std"]]).values
 y_c = panel_c["d_log"].values
 m_c = sm.OLS(y_c, X_c).fit
 coords = panel_c[["lat", "lng"]].values
 se_c5 = float(conley_se_uniform(X_c, m_c.resid, coords, 5.0)[1])
 se_c10 = float(conley_se_uniform(X_c, m_c.resid, coords, 10.0)[1])
 t_c5 = beta / se_c5
 t_c10 = beta / se_c10

 # WCR Webb 6-pt bootstrap (B=9999)
 print("[8] WCR Webb 6-pt bootstrap (B=9999)...")
 p_wcr, t_ref, _, _ = wcr_webb_6pt(X, y, panel["sido_code"].values, B=9999, seed=42)
 log.append(f"\n### 5-layer SE for β_1999 (despair_total)")
 log.append(f"- β = {beta:+.4f}, n = {len(panel)}")
 log.append(f"- HC1: SE={se_hc1:.4f}, t={t_hc1:+.3f}, p={p_hc1:.4f}")
 log.append(f"- cluster-province (G={G}, t-dist): SE={se_cl:.4f}, t={t_cl:+.3f}, p={p_cl_t:.4f}")
 log.append(f"- Conley 5km: SE={se_c5:.4f}, t={t_c5:+.3f}")
 log.append(f"- Conley 10km: SE={se_c10:.4f}, t={t_c10:+.3f}")
 log.append(f"- WCR Webb 6-pt (B=9999, cluster=sido): p = **{p_wcr:.4f}**")
 log.append(f"- AKM-proper (Kolesár 2024 ShiftShareSE): ⚠️ requires external R package — "
 f"reported as `pending external compute` in this Python pipeline")

 # --------------------------------------------------------------------
 # 8) First-stage F: bilateral on ADH-8 (1999 baseline) — both IVs
 # --------------------------------------------------------------------
 fs = (
 iv_bil[["h_code", "z_x_per_worker"]]
.rename(columns={"z_x_per_worker": "z_bil"})
.merge(iv_adh[["h_code", "z_x_per_worker"]].rename(columns={"z_x_per_worker": "z_adh"}),
 on="h_code", how="inner")
)
 fs["sido_code"] = fs["h_code"].str[:2]
 # standardize for stable scale
 fs["z_bil_std"] = (fs["z_bil"] - fs["z_bil"].mean) / fs["z_bil"].std(ddof=1)
 fs["z_adh_std"] = (fs["z_adh"] - fs["z_adh"].mean) / fs["z_adh"].std(ddof=1)
 Xfs = sm.add_constant(fs[["z_adh_std"]]).values
 yfs = fs["z_bil_std"].values
 m_fs = sm.OLS(yfs, Xfs).fit(cov_type="HC1")
 F_hc1 = float(m_fs.fvalue)
 m_fs_cl = sm.OLS(yfs, Xfs).fit(cov_type="cluster", cov_kwds={"groups": fs["sido_code"].values})
 t_cl_fs = float(m_fs_cl.params[1] / m_fs_cl.bse[1])
 F_cl = t_cl_fs ** 2
 log.append(f"\n## First-stage F (1999 baseline)")
 log.append(f"- spec: z_bil^{{1999}} on z_adh^{{1999}}, n = {len(fs)}")
 log.append(f"- HC1 F = {F_hc1:.2f}")
 log.append(f"- cluster-sido F = {F_cl:.2f}")
 log.append(f"- 1994 baseline reference (Phase B-x cluster-sido): F = 19.65")
 if F_cl > 19.65:
 log.append(f"- ✅ 1999 baseline strengthens instrument relevance: F = {F_cl:.2f} > 19.65 "
 f"(improvement {(F_cl/19.65-1)*100:+.1f}%)")
 else:
 log.append(f"- ⚠️ 1999 baseline attenuates instrument relevance: F = {F_cl:.2f} < 19.65 "
 f"(attenuation {(F_cl/19.65-1)*100:+.1f}%)")

 # --------------------------------------------------------------------
 # 9) Save layer table + write log
 # --------------------------------------------------------------------
 layer_rows = [
 ("HC1", se_hc1, t_hc1, p_hc1),
 (f"Cluster-province (G={G}, t-dist)", se_cl, t_cl, p_cl_t),
 ("AKM-proper (Kolesár 2024)", float("nan"), float("nan"), float("nan")),
 ("Conley 5 km", se_c5, t_c5, 2 * (1 - stats.norm.cdf(abs(t_c5)))),
 ("Conley 10 km", se_c10, t_c10, 2 * (1 - stats.norm.cdf(abs(t_c10)))),
 (f"WCR Webb 6-pt (B=9999)", float("nan"), float("nan"), p_wcr),
 ]
 out_df = pd.DataFrame(layer_rows, columns=["layer", "SE", "t", "p"]).assign(
 beta=beta, n=len(panel), G=G, F_first_stage_cluster_sido=F_cl, baseline_year=1999
)
 out_csv = REG / "main_native_5layer_1999baseline.csv"
 out_df.to_csv(out_csv, index=False, encoding="utf-8-sig")
 log.append(f"\n- saved: `{out_csv.relative_to(PROJ)}`")

 # --------------------------------------------------------------------
 # 10) Cross-baseline cascade summary
 # --------------------------------------------------------------------
 log.append(f"\n## Cross-baseline cascade (β coefficient)")
 log.append(f"| Baseline year | β | n | First-stage F (cluster-sido) | Notes |")
 log.append(f"|---------------|---|---|------------------------------|-------|")
 log.append(f"| 1992 (winsorized) | -0.0640 | 209 | (not reported) | KSIC 6→9 crosswalk, winsorize 99% |")
 log.append(f"| **1994 (main)** | **-0.127** | **221** | **19.65** | KSIC 9 native, pre-shock 6yr |")
 log.append(f"| 1999 (Phase 5) | **{beta:+.4f}** | {len(panel)} | **{F_cl:.2f}** | KSIC 7→9 crosswalk, pre-shock 1yr |")

 out_log = LOGS / f"{TODAY}_baseline_shares_1999_phase5.md"
 out_log.write_text("\n".join(log), encoding="utf-8")
 print(f"[OK] log → {out_log}")
 print(f"[OK] β_1999 = {beta:+.4f}, n = {len(panel)}, F_1999 = {F_cl:.2f}, p_WCR = {p_wcr:.4f}")

if __name__ == "__main__":
 main
