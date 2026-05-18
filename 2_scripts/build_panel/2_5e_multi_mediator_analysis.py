"""Phase 2 sub-task 2.5e -- Multi-mediator analysis (M3 + M4 + M5 + M6).

Steps:
 1. Load M3/M4/M5/M6 mediator panels + IV (z_x_per_worker) + mortality (despair_total)
 2. First-stage F: z_x -> {marriage, divorce, fertility, suicide}
 3. Reduced-form: each mediator -> d_log_asr (control z_x_std), HC1 + cluster SE
 4. DGHP decomposition for first-stage-strong M3 components
 5. Effect modifier check (M4 + M5): d_log_asr ~ z_x + M_pre + z_x x M_pre
 6. Sub-period sensitivity (post-2008 vs pre-2008)
 7. Cluster bootstrap (sido, 1000 reps) on selected DGHP rows
"""
import io
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
DERIVED = PROJ / "3_derived"
OUT = PROJ / "4_results"
OUT.mkdir(exist_ok=True)

# ============================================================
# Step 0: Helpers
# ============================================================
def cluster_se(X: np.ndarray, y: np.ndarray, cluster: pd.Series):
 fit = sm.OLS(y, X).fit
 G = pd.Series(cluster).nunique
 N, K = X.shape
 bread = np.linalg.inv(X.T @ X)
 meat = np.zeros((K, K))
 resid = np.asarray(fit.resid)
 arr = pd.Series(cluster).values
 for c in pd.Series(cluster).unique:
 idx = arr == c
 Xc = X[idx,:]
 rc = resid[idx]
 s_c = Xc.T @ rc
 meat += np.outer(s_c, s_c)
 G_factor = (G / (G - 1)) * ((N - 1) / (N - K))
 return fit, np.sqrt(np.diag(bread @ meat @ bread * G_factor)), G

def first_stage_F(df: pd.DataFrame, mediator: str) -> dict:
 sub = df[[mediator, "z_x_std"]].dropna
 X = sm.add_constant(sub["z_x_std"].values)
 fit = sm.OLS(sub[mediator].values, X).fit(cov_type="HC1")
 return {
 "mediator": mediator,
 "gamma_fs": float(np.asarray(fit.params)[1]),
 "F": float(fit.fvalue),
 "p": float(fit.f_pvalue),
 "n": int(len(sub)),
 }

def reduced_form(df: pd.DataFrame, mediator: str, cluster_col: str = "sido_code") -> dict:
 sub = df[[mediator, "d_log_asr", "z_x_std", cluster_col]].dropna
 X_uni = sm.add_constant(sub[mediator].values)
 fit_uni = sm.OLS(sub["d_log_asr"].values, X_uni).fit(cov_type="HC1")
 _, se_clu_uni, G_uni = cluster_se(X_uni, sub["d_log_asr"].values, sub[cluster_col])
 beta_uni = float(np.asarray(fit_uni.params)[1])
 se_h_uni = float(np.asarray(fit_uni.bse)[1])
 t_clu_uni = beta_uni / se_clu_uni[1]
 p_clu_uni = 2 * (1 - stats.t.cdf(abs(t_clu_uni), df=G_uni - 1))

 X_ctrl = sm.add_constant(sub[[mediator, "z_x_std"]].values)
 fit_ctrl = sm.OLS(sub["d_log_asr"].values, X_ctrl).fit(cov_type="HC1")
 _, se_clu_ctrl, G_c = cluster_se(X_ctrl, sub["d_log_asr"].values, sub[cluster_col])
 beta_ctrl = float(np.asarray(fit_ctrl.params)[1])
 se_h_ctrl = float(np.asarray(fit_ctrl.bse)[1])
 t_clu_ctrl = beta_ctrl / se_clu_ctrl[1]
 p_clu_ctrl = 2 * (1 - stats.t.cdf(abs(t_clu_ctrl), df=G_c - 1))
 return {
 "mediator": mediator,
 "n": int(len(sub)),
 "beta_uni": beta_uni,
 "se_hc1_uni": se_h_uni,
 "se_cluster_uni": float(se_clu_uni[1]),
 "t_cluster_uni": t_clu_uni,
 "p_cluster_uni": p_clu_uni,
 "beta_ctrl": beta_ctrl,
 "se_hc1_ctrl": se_h_ctrl,
 "se_cluster_ctrl": float(se_clu_ctrl[1]),
 "t_cluster_ctrl": t_clu_ctrl,
 "p_cluster_ctrl": p_clu_ctrl,
 "G_cluster": int(G_c),
 }

def dghp_decomp(df: pd.DataFrame, mediator: str) -> dict:
 sub = df[[mediator, "d_log_asr", "z_x_std"]].dropna
 if len(sub) < 5:
 return {k: float("nan") for k in ("gamma_fs", "delta_m", "beta_direct", "acme", "beta_rf", "acme_proportion")}
 X_fs = sm.add_constant(sub["z_x_std"].values)
 fit_fs = sm.OLS(sub[mediator].values, X_fs).fit
 gamma_fs = float(np.asarray(fit_fs.params)[1])
 X_2s = sm.add_constant(sub[[mediator, "z_x_std"]].values)
 fit_2s = sm.OLS(sub["d_log_asr"].values, X_2s).fit
 delta_m = float(np.asarray(fit_2s.params)[1])
 beta_d = float(np.asarray(fit_2s.params)[2])
 X_rf = sm.add_constant(sub["z_x_std"].values)
 fit_rf = sm.OLS(sub["d_log_asr"].values, X_rf).fit
 beta_rf = float(np.asarray(fit_rf.params)[1])
 return {
 "gamma_fs": gamma_fs,
 "delta_m": delta_m,
 "beta_direct": beta_d,
 "acme": gamma_fs * delta_m,
 "beta_rf": beta_rf,
 "acme_proportion": (gamma_fs * delta_m) / beta_rf if beta_rf!= 0 else float("nan"),
 }

def effect_modifier(df: pd.DataFrame, modifier: str, cluster_col: str = "sido_code") -> dict:
 sub = df[[modifier, "d_log_asr", "z_x_std", cluster_col]].dropna
 sub = sub.copy
 sub["interact"] = sub["z_x_std"] * sub[modifier]
 X = sm.add_constant(sub[["z_x_std", modifier, "interact"]].values)
 fit = sm.OLS(sub["d_log_asr"].values, X).fit(cov_type="HC1")
 _, se_clu, G = cluster_se(X, sub["d_log_asr"].values, sub[cluster_col])
 p_int = 2 * (1 - stats.t.cdf(abs(float(np.asarray(fit.params)[3]) / se_clu[3]), df=G - 1))
 return {
 "modifier": modifier,
 "n": int(len(sub)),
 "beta_z_x": float(np.asarray(fit.params)[1]),
 "beta_modifier": float(np.asarray(fit.params)[2]),
 "beta_interact": float(np.asarray(fit.params)[3]),
 "se_hc1_interact": float(np.asarray(fit.bse)[3]),
 "se_cluster_interact": float(se_clu[3]),
 "t_cluster_interact": float(np.asarray(fit.params)[3]) / se_clu[3],
 "p_cluster_interact": p_int,
 "G_cluster": int(G),
 }

# ============================================================
# Step 1: Load mediator panels + IV + mortality (despair_total)
# ============================================================
print("[step1] load mediator panels")
m3 = pd.read_parquet(DERIVED / "m3_delta_panel.parquet")
m4 = pd.read_parquet(DERIVED / "m4_z_marital_pre.parquet")
m5 = pd.read_parquet(DERIVED / "m5_z_education_pre.parquet")
m6 = pd.read_parquet(DERIVED / "m6_suicide_panel.parquet")
print(f" M3 (delta family) rows: {len(m3)}")
print(f" M4 (cohort sex ratio) rows: {len(m4)}")
print(f" M5 (univ distance) rows: {len(m5)}")
print(f" M6 (suicide) rows: {len(m6)}")

iv = pd.read_parquet(PROJ / "8_submission" / "paper_v01_submission" / "02_bartik_iv" / "iv_z_x_bilateral.parquet")
mort = pd.read_parquet(PROJ / "8_submission" / "paper_v01_submission" / "01_mortality" / "sigungu_mortality_panel_v02_wa.parquet")
mort["mort_rate"] = mort["deaths"] / np.maximum(mort["pop_wa"], 1)
mort["log_mort"] = np.log(mort["mort_rate"] + 1e-6)
mb = (
 mort[mort["year"].isin(range(1997, 2000))]
.groupby(["h_code", "outcome_group"])["log_mort"]
.mean
.reset_index(name="b")
)
me = (
 mort[mort["year"].isin(range(2018, 2023))]
.groupby(["h_code", "outcome_group"])["log_mort"]
.mean
.reset_index(name="e")
)
panel_main = mb.merge(me, on=["h_code", "outcome_group"]).merge(iv, on="h_code")
panel_main["d_log_asr"] = panel_main["e"] - panel_main["b"]
panel_main = panel_main[np.isfinite(panel_main["z_x"])]
panel_despair = panel_main[panel_main["outcome_group"] == "despair_total"].copy
panel_despair["z_x_std"] = (
 panel_despair["z_x_per_worker"] - panel_despair["z_x_per_worker"].mean
) / panel_despair["z_x_per_worker"].std
panel_despair["sido_code"] = panel_despair["h_code"].astype(str).str.zfill(5).str[:2]
print(f" despair panel n: {len(panel_despair)}")

# Sub-period split
panel_despair_pre = mort[(mort["outcome_group"] == "despair_total") & (mort["period_pre2008"])].copy if "period_pre2008" in mort.columns else None

# Build joint panel: despair core + each mediator left-joined
joint = panel_despair[["h_code", "z_x_std", "d_log_asr", "sido_code"]].copy
joint["h_code"] = joint["h_code"].astype(int)
for d in (m3, m4, m5, m6):
 d["h_code"] = d["h_code"].astype(int)
joint = (
 joint.merge(m3, on="h_code", how="left")
.merge(m4[["h_code", "z_m_marital", "cohort_sex_ratio_1995"]], on="h_code", how="left")
.merge(m5[["h_code", "z_m_education", "z_m_education_1985", "z_m_education_1990", "z_m_education_1995"]], on="h_code", how="left")
.merge(m6[["h_code", "delta_log_suicide"]], on="h_code", how="left")
)
print(f" joint panel rows: {len(joint)}")
print(f" coverage: M3 marriage {joint['delta_marriage'].notna.sum}, divorce {joint['delta_divorce'].notna.sum}, fertility {joint['delta_fertility'].notna.sum}")
print(f" coverage: M4 z_m_marital {joint['z_m_marital'].notna.sum}, M5 z_m_education {joint['z_m_education'].notna.sum}, M6 delta_suicide {joint['delta_log_suicide'].notna.sum}")
print(f" sido (cluster) G: {joint['sido_code'].nunique}")

# ============================================================
# Step 2: First-stage F by mediator (time-varying mediators only)
# ============================================================
print("\n[step2] first-stage F by mediator")
fs_rows = 
for med in ["delta_marriage", "delta_divorce", "delta_fertility", "delta_log_suicide"]:
 r = first_stage_F(joint, med)
 fs_rows.append(r)
 print(f" {med:>22}: gamma={r['gamma_fs']:+.4f}, F={r['F']:.2f}, p={r['p']:.4f}, n={r['n']}")
fs_df = pd.DataFrame(fs_rows)
fs_df.to_parquet(OUT / "m3_m6_first_stage_table.parquet", index=False)

# ============================================================
# Step 3: Reduced-form mediator -> mortality (cluster SE)
# ============================================================
print("\n[step3] reduced-form mediator -> mortality (univariate + z_x control)")
rf_rows = 
for med in [
 "delta_marriage",
 "delta_divorce",
 "delta_fertility",
 "z_m_marital",
 "z_m_education",
 "delta_log_suicide",
]:
 if med not in joint.columns:
 continue
 r = reduced_form(joint, med)
 rf_rows.append(r)
 print(
 f" {med:>22}: beta_uni={r['beta_uni']:+.4f} (t_clu={r['t_cluster_uni']:+.2f}, p={r['p_cluster_uni']:.4f}); "
 f"beta_ctrl={r['beta_ctrl']:+.4f} (t_clu={r['t_cluster_ctrl']:+.2f}, p={r['p_cluster_ctrl']:.4f}); "
 f"n={r['n']}"
)
rf_df = pd.DataFrame(rf_rows)
rf_df.to_parquet(OUT / "m3_m6_reduced_form_table.parquet", index=False)

# ============================================================
# Step 4: DGHP decomposition (M3 components + M6) with cluster bootstrap
# ============================================================
print("\n[step4] DGHP decomposition (M3 components + M6) with sido cluster bootstrap")
np.random.seed(42)
B = 1000
dghp_targets = ["delta_marriage", "delta_divorce", "delta_fertility", "delta_log_suicide"]
dghp_rows = 
for med in dghp_targets:
 sub = joint[[med, "d_log_asr", "z_x_std", "sido_code", "h_code"]].dropna
 pt = dghp_decomp(sub, med)
 sidos = sub["sido_code"].unique
 boots = 
 for b in range(B):
 bs = np.random.choice(sidos, size=len(sidos), replace=True)
 bdf = pd.concat([sub[sub["sido_code"] == s] for s in bs], ignore_index=True)
 try:
 boots.append(dghp_decomp(bdf, med)["acme"])
 except Exception:
 pass
 boots_arr = np.array(boots)
 lo, hi = np.quantile(boots_arr, [0.025, 0.975])
 prop_pt = pt["acme_proportion"]
 dghp_rows.append(
 {
 "mediator": med,
 "n": int(len(sub)),
 "ACME_point": pt["acme"],
 "ACME_CI_lo": float(lo),
 "ACME_CI_hi": float(hi),
 "ACME_proportion": prop_pt,
 "beta_rf": pt["beta_rf"],
 "gamma_fs": pt["gamma_fs"],
 "delta_m": pt["delta_m"],
 "beta_direct": pt["beta_direct"],
 }
)
 print(
 f" {med:>22}: ACME={pt['acme']:+.4f} [95% CI {lo:+.4f}, {hi:+.4f}], "
 f"prop={prop_pt:+.3f}, gamma_fs={pt['gamma_fs']:+.4f}, delta_m={pt['delta_m']:+.4f}"
)
dghp_df = pd.DataFrame(dghp_rows)
dghp_df.to_parquet(OUT / "multi_mediator_dghp_decomposition.parquet", index=False)

# ============================================================
# Step 5: Effect modifier check (M4 + M5)
# ============================================================
print("\n[step5] effect modifier interaction (M4 + M5 pre-determined)")
em_rows = 
for mod in ["z_m_marital", "z_m_education", "z_m_education_1985", "z_m_education_1990", "z_m_education_1995"]:
 if mod not in joint.columns:
 continue
 r = effect_modifier(joint, mod)
 em_rows.append(r)
 print(
 f" {mod:>22}: beta_z_x={r['beta_z_x']:+.4f}, beta_int={r['beta_interact']:+.4f} "
 f"(t_clu={r['t_cluster_interact']:+.2f}, p={r['p_cluster_interact']:.4f}, n={r['n']})"
)
em_df = pd.DataFrame(em_rows)
em_df.to_parquet(OUT / "m4_m5_effect_modifier.parquet", index=False)

# ============================================================
# Step 6: Sub-period sensitivity (post-2008 vs pre-2008)
# ============================================================
print("\n[step6] sub-period sensitivity (post-2008 split using period_pre2008 flag)")
# Build pre-2008 endpoint and post-2008 baseline windows
sub_period_rows = 
if "period_pre2008" in mort.columns:
 # baseline 1997-1999 -> midpoint 2007 (pre-2008 endpoint)
 mid = (
 mort[mort["year"].isin(range(2005, 2008))]
.groupby(["h_code", "outcome_group"])["log_mort"]
.mean
.reset_index(name="mid")
)
 pre_panel = mb.merge(mid, on=["h_code", "outcome_group"]).merge(iv, on="h_code")
 pre_panel["d_log_asr"] = pre_panel["mid"] - pre_panel["b"]
 pre_d = pre_panel[pre_panel["outcome_group"] == "despair_total"].copy
 pre_d["z_x_std"] = (pre_d["z_x_per_worker"] - pre_d["z_x_per_worker"].mean) / pre_d["z_x_per_worker"].std
 pre_d["sido_code"] = pre_d["h_code"].astype(str).str.zfill(5).str[:2]
 pre_d["h_code"] = pre_d["h_code"].astype(int)

 post = (
 mort[mort["year"].isin(range(2008, 2011))]
.groupby(["h_code", "outcome_group"])["log_mort"]
.mean
.reset_index(name="mid")
)
 post_panel = post.merge(me, on=["h_code", "outcome_group"]).merge(iv, on="h_code")
 post_panel["d_log_asr"] = post_panel["e"] - post_panel["mid"]
 post_d = post_panel[post_panel["outcome_group"] == "despair_total"].copy
 post_d["z_x_std"] = (post_d["z_x_per_worker"] - post_d["z_x_per_worker"].mean) / post_d["z_x_per_worker"].std
 post_d["sido_code"] = post_d["h_code"].astype(str).str.zfill(5).str[:2]
 post_d["h_code"] = post_d["h_code"].astype(int)

 for label, base_df in [("pre2008_1997_2007", pre_d), ("post2008_2008_2022", post_d)]:
 jp = base_df[["h_code", "z_x_std", "d_log_asr", "sido_code"]].merge(joint[["h_code", "delta_log_suicide", "z_m_marital", "z_m_education"]], on="h_code", how="left")
 for med in ["delta_log_suicide", "z_m_marital", "z_m_education"]:
 sub = jp[[med, "d_log_asr", "z_x_std", "sido_code"]].dropna
 if len(sub) < 10:
 continue
 X = sm.add_constant(sub[[med, "z_x_std"]].values)
 fit = sm.OLS(sub["d_log_asr"].values, X).fit(cov_type="HC1")
 _, se_clu, G = cluster_se(X, sub["d_log_asr"].values, sub["sido_code"])
 beta = float(np.asarray(fit.params)[1])
 t = beta / se_clu[1]
 sub_period_rows.append(
 {
 "period": label,
 "mediator": med,
 "n": int(len(sub)),
 "beta": beta,
 "se_cluster": float(se_clu[1]),
 "t_cluster": float(t),
 "p_cluster": float(2 * (1 - stats.t.cdf(abs(t), df=G - 1))),
 }
)
sp_df = pd.DataFrame(sub_period_rows)
if len(sp_df):
 sp_df.to_parquet(OUT / "sub_period_sensitivity.parquet", index=False)
 print(sp_df.to_string(index=False))
else:
 print(" (no sub-period rows produced)")

# ============================================================
# Step 7: Audit-after-action 6-step verify
# ============================================================
print("\n=== Audit-after-action 6-step verify ===")
artifacts = [
 "m3_m6_first_stage_table.parquet",
 "m3_m6_reduced_form_table.parquet",
 "multi_mediator_dghp_decomposition.parquet",
 "m4_m5_effect_modifier.parquet",
]
for fn in artifacts:
 fp = OUT / fn
 print(f" [1] {fn}: exists={fp.exists}, size={os.path.getsize(fp) / 1024:.1f} KB")

print(f" [2] first-stage rows: {len(fs_df)} (expected 4)")
print(f" [2] reduced-form rows: {len(rf_df)} (expected 6)")
print(f" [2] DGHP rows: {len(dghp_df)} (expected 4)")
print(f" [2] effect-modifier rows: {len(em_df)} (expected 5)")

print(" [3] joint sample n =", len(joint), ", sido G =", joint["sido_code"].nunique)

# Validate suicide sign expectation (should be negative if despair_total is)
suicide_dghp = dghp_df[dghp_df["mediator"] == "delta_log_suicide"]
if len(suicide_dghp):
 s = suicide_dghp.iloc[0]
 print(f" [4] suicide validation: beta_rf={s['beta_rf']:+.4f}, ACME={s['ACME_point']:+.4f} [95% CI {s['ACME_CI_lo']:+.4f}, {s['ACME_CI_hi']:+.4f}]")

# Effect modifier interaction direction
for mod in ["z_m_marital", "z_m_education"]:
 em = em_df[em_df["modifier"] == mod]
 if len(em):
 e = em.iloc[0]
 print(f" [5] {mod} interaction: t_clu={e['t_cluster_interact']:+.3f}, p={e['p_cluster_interact']:.4f}")

print("\n=== sub-task 2.5 multi-mediator analysis complete ===")
