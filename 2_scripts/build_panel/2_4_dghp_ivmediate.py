"""Phase 2 sub-task 2.4 -- DGHP 2017 ivmediate formal implementation.

Joint sample = 138 intersection-complete-case sigungu (= sub-task 2.3 output).
Steps:
  1. Build joint sample (HIRA delta z + mortality long-diff + IV)
  2. N05BA single-mediator DGHP decomposition (point)
  3. Cluster bootstrap (sido, 1000 reps) -> ACME 95% CI
  4. 5 ATC4 reduced-form (univariate + joint multivariate, cluster SE G=13)
  5. Robustness table (Alt 0/1/2/3 + N05BA single)
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
OUT = PROJ / "4_results"
OUT.mkdir(exist_ok=True)

ATC4_LIST = ["N06AB", "N06AX", "N05BA", "N05AX", "A05BA"]

# ============================================================
# Step 1: Build joint sample (138 intersection complete-case)
# ============================================================
print("[step1] build joint sample")
panel = pd.read_parquet(PROJ / "3_derived" / "hira_atc4_panel.parquet")
panel_int = panel[panel["in_intersection_147"]].copy()

raw_wide = panel_int.pivot_table(
    index=["h_code", "year"],
    columns="atc4",
    values="prescription_rate_per_100k",
    aggfunc="first",
).reset_index()
for atc in ATC4_LIST:
    raw_wide[f"log_{atc.lower()}"] = np.log(raw_wide[atc] + 1)
    mu = raw_wide[f"log_{atc.lower()}"].mean()
    sigma = raw_wide[f"log_{atc.lower()}"].std()
    raw_wide[f"z_{atc.lower()}"] = (raw_wide[f"log_{atc.lower()}"] - mu) / sigma

w10 = raw_wide[raw_wide["year"] == 2010].set_index("h_code")
w19 = raw_wide[raw_wide["year"] == 2019].set_index("h_code")
delta_indiv = pd.DataFrame(index=w10.index.intersection(w19.index))
for atc in ATC4_LIST:
    delta_indiv[f"d_z_{atc.lower()}"] = w19[f"z_{atc.lower()}"] - w10[f"z_{atc.lower()}"]
delta_indiv = delta_indiv.dropna().reset_index()

mort = pd.read_parquet(
    PROJ / "8_submission" / "paper_v01_submission" / "01_mortality" / "sigungu_mortality_panel_v02_wa.parquet"
)
iv = pd.read_parquet(
    PROJ / "8_submission" / "paper_v01_submission" / "02_bartik_iv" / "iv_z_x_bilateral.parquet"
)
mort["mort_rate"] = mort["deaths"] / np.maximum(mort["pop_wa"], 1)
mort["log_mort"] = np.log(mort["mort_rate"] + 1e-6)
mb = (
    mort[mort["year"].isin(range(1997, 2000))]
    .groupby(["h_code", "outcome_group"])["log_mort"]
    .mean()
    .reset_index()
)
mb.columns = ["h_code", "outcome_group", "b"]
me = (
    mort[mort["year"].isin(range(2018, 2023))]
    .groupby(["h_code", "outcome_group"])["log_mort"]
    .mean()
    .reset_index()
)
me.columns = ["h_code", "outcome_group", "e"]
panel_main = mb.merge(me, on=["h_code", "outcome_group"]).merge(iv, on="h_code")
panel_main["d_log_asr"] = panel_main["e"] - panel_main["b"]
panel_main = panel_main[np.isfinite(panel_main["z_x"])]
panel_despair = panel_main[panel_main["outcome_group"] == "despair_total"].copy()
panel_despair["z_x_std"] = (
    panel_despair["z_x_per_worker"] - panel_despair["z_x_per_worker"].mean()
) / panel_despair["z_x_per_worker"].std()

delta_indiv["h_code_int"] = delta_indiv["h_code"].astype(int)
panel_despair["h_code_int"] = panel_despair["h_code"].astype(int)
joint = delta_indiv.merge(
    panel_despair[["h_code_int", "d_log_asr", "z_x_std"]],
    on="h_code_int",
    how="inner",
)
joint["sido_code"] = joint["h_code"].astype(str).str.zfill(5).str[:2]
print(f"  joint sample n: {len(joint)}")
print(f"  sido (cluster) G: {joint['sido_code'].nunique()}")
assert len(joint) == 138, f"Expected 138, got {len(joint)}"


# ============================================================
# Step 2: DGHP single-mediator decomposition
# ============================================================
def dghp_decomp(df, mediator="d_z_n05ba"):
    X_fs = sm.add_constant(df["z_x_std"].values)
    fit_fs = sm.OLS(df[mediator].values, X_fs).fit()
    gamma_fs = float(np.asarray(fit_fs.params)[1])
    F_fs = float(fit_fs.fvalue)

    X_2s = sm.add_constant(df[[mediator, "z_x_std"]].values)
    fit_2s = sm.OLS(df["d_log_asr"].values, X_2s).fit()
    delta_m = float(np.asarray(fit_2s.params)[1])
    beta_d = float(np.asarray(fit_2s.params)[2])

    X_rf = sm.add_constant(df["z_x_std"].values)
    fit_rf = sm.OLS(df["d_log_asr"].values, X_rf).fit()
    beta_rf = float(np.asarray(fit_rf.params)[1])

    return {
        "gamma_fs": gamma_fs,
        "F_fs": F_fs,
        "delta_m": delta_m,
        "beta_direct": beta_d,
        "acme": gamma_fs * delta_m,
        "beta_rf": beta_rf,
        "acme_proportion": (gamma_fs * delta_m) / beta_rf,
    }


print("\n[step2] N05BA single-mediator point estimate")
point = {"boot_id": 0, **dghp_decomp(joint)}
for k, v in point.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.6f}")
    else:
        print(f"  {k}: {v}")


# ============================================================
# Step 3: Cluster bootstrap (sido-level, 1000 reps)
# ============================================================
print("\n[step3] cluster bootstrap (sido, 1000 reps)")
np.random.seed(42)
B = 1000
boot = [point]
sidos = joint["sido_code"].unique()
for b in range(1, B + 1):
    boot_sidos = np.random.choice(sidos, size=len(sidos), replace=True)
    boot_df_b = pd.concat(
        [joint[joint["sido_code"] == s] for s in boot_sidos], ignore_index=True
    )
    try:
        boot.append({"boot_id": b, **dghp_decomp(boot_df_b)})
    except Exception:
        pass

boot_df = pd.DataFrame(boot)
boot_df.to_parquet(OUT / "dghp_acme_n05ba_bootstrap.parquet", index=False)
print(f"  bootstrap rows: {len(boot_df)} (point + {len(boot_df) - 1} boot)")
print(f"\n  Bootstrap CI:")
ci_summary = {}
for col in ["gamma_fs", "delta_m", "beta_direct", "acme", "beta_rf", "acme_proportion"]:
    s = boot_df.iloc[1:][col]
    lo, hi = s.quantile(0.025), s.quantile(0.975)
    ci_summary[col] = (boot_df.iloc[0][col], lo, hi)
    print(
        f"    {col}: point = {boot_df.iloc[0][col]:.4f}, 95% CI = [{lo:.4f}, {hi:.4f}]"
    )


# ============================================================
# Step 4: 5 ATC4 reduced-form decomposition (cluster SE)
# ============================================================
def cluster_se(X, y, cluster):
    fit = sm.OLS(y, X).fit()
    G = pd.Series(cluster).nunique()
    N, K = X.shape
    bread = np.linalg.inv(X.T @ X)
    meat = np.zeros((K, K))
    resid = np.asarray(fit.resid)
    cluster_arr = pd.Series(cluster).values
    for c in pd.Series(cluster).unique():
        idx = cluster_arr == c
        Xc = X[idx, :]
        rc = resid[idx]
        s_c = Xc.T @ rc
        meat += np.outer(s_c, s_c)
    G_factor = (G / (G - 1)) * ((N - 1) / (N - K))
    return fit, np.sqrt(np.diag(bread @ meat @ bread * G_factor)), G


print("\n[step4] 5 ATC4 reduced-form decomposition")
results = []

# Univariate
for atc in ATC4_LIST:
    col = f"d_z_{atc.lower()}"
    sub = joint[[col, "d_log_asr", "z_x_std", "sido_code"]].dropna()
    X = sm.add_constant(sub[col].values)
    fit_hc1 = sm.OLS(sub["d_log_asr"].values, X).fit(cov_type="HC1")
    _, se_clu, G = cluster_se(X, sub["d_log_asr"].values, sub["sido_code"])
    X_fs = sm.add_constant(sub["z_x_std"].values)
    fit_fs = sm.OLS(sub[col].values, X_fs).fit(cov_type="HC1")
    beta = float(np.asarray(fit_hc1.params)[1])
    se_h = float(np.asarray(fit_hc1.bse)[1])
    t_h = float(np.asarray(fit_hc1.tvalues)[1])
    t_c = beta / se_clu[1]
    p_c = 2 * (1 - stats.t.cdf(abs(t_c), df=G - 1))
    results.append(
        {
            "atc4": atc,
            "spec": "univariate",
            "beta": beta,
            "se_hc1": se_h,
            "se_cluster": float(se_clu[1]),
            "t_hc1": t_h,
            "t_cluster": t_c,
            "p_cluster": p_c,
            "f_first_stage": float(fit_fs.fvalue),
        }
    )

# Joint multivariate
cols = [f"d_z_{a.lower()}" for a in ATC4_LIST]
sub = joint[cols + ["d_log_asr", "sido_code"]].dropna()
X = sm.add_constant(sub[cols].values)
fit_hc1 = sm.OLS(sub["d_log_asr"].values, X).fit(cov_type="HC1")
_, se_clu, G = cluster_se(X, sub["d_log_asr"].values, sub["sido_code"])
for i, atc in enumerate(ATC4_LIST):
    beta = float(np.asarray(fit_hc1.params)[i + 1])
    se_h = float(np.asarray(fit_hc1.bse)[i + 1])
    t_h = float(np.asarray(fit_hc1.tvalues)[i + 1])
    t_c = beta / se_clu[i + 1]
    p_c = 2 * (1 - stats.t.cdf(abs(t_c), df=G - 1))
    results.append(
        {
            "atc4": atc,
            "spec": "joint_multivariate",
            "beta": beta,
            "se_hc1": se_h,
            "se_cluster": float(se_clu[i + 1]),
            "t_hc1": t_h,
            "t_cluster": t_c,
            "p_cluster": p_c,
            "f_first_stage": float("nan"),
        }
    )

results_df = pd.DataFrame(results)
results_df.to_parquet(OUT / "atc4_reduced_form_decomposition.parquet", index=False)
print(f"  G (cluster sido): {G}")
print(f"\n  5 ATC4 reduced-form decomposition (univariate + joint multivariate):")
with pd.option_context("display.float_format", "{:+.4f}".format):
    print(results_df.to_string(index=False))


# ============================================================
# Step 5: Robustness table (4 alt composite + N05BA)
# ============================================================
print("\n[step5] robustness table")
delta = pd.read_parquet(PROJ / "3_derived" / "hira_delta_m1_panel.parquet")
delta_cc = delta[delta["complete_case"] & delta["in_intersection_147"]].copy()
delta_cc["h_code_int"] = delta_cc["h_code"].astype(int)
delta_cc = delta_cc.merge(
    panel_despair[["h_code_int", "d_log_asr", "z_x_std"]],
    on="h_code_int",
    how="inner",
)
delta_cc["sido_code"] = delta_cc["h_code"].astype(str).str.zfill(5).str[:2]

robust = []
specs = {
    "Alt 0 composite (5 ATC4 mean)": "delta_m1_composite",
    "Alt 1 4-mental (excl A05BA)": "delta_m1_4mental",
    "Alt 2 A05BA-only": "delta_m1_liver",
    "Alt 3 PCA 1st": "delta_m1_pca1",
    "N05BA single (from joint)": "d_z_n05ba",
}
for label, col in specs.items():
    df = joint if col == "d_z_n05ba" else delta_cc.dropna(subset=[col])
    X_fs = sm.add_constant(df["z_x_std"].values)
    fit_fs = sm.OLS(df[col].values, X_fs).fit(cov_type="HC1")
    robust.append(
        {
            "spec": label,
            "mediator": col,
            "n": len(df),
            "gamma_fs": float(np.asarray(fit_fs.params)[1]),
            "F_first_stage": float(fit_fs.fvalue),
            "p_first_stage": float(fit_fs.f_pvalue),
        }
    )
robust_df = pd.DataFrame(robust)
robust_df.to_parquet(OUT / "m1_alt_robustness.parquet", index=False)
print(f"  Robustness table:")
with pd.option_context("display.float_format", "{:+.4f}".format):
    print(robust_df.to_string(index=False))


# ============================================================
# Step 6: Audit-after-action 6-step verify
# ============================================================
print("\n=== Audit-after-action 6-step verify ===\n")

for fn in [
    "dghp_acme_n05ba_bootstrap.parquet",
    "atc4_reduced_form_decomposition.parquet",
    "m1_alt_robustness.parquet",
]:
    fp = OUT / fn
    print(f"  [1] {fn}: exists={fp.exists()}, size={os.path.getsize(fp) / 1024:.1f} KB")

exp_boot = {
    "boot_id",
    "gamma_fs",
    "F_fs",
    "delta_m",
    "beta_direct",
    "acme",
    "beta_rf",
    "acme_proportion",
}
exp_dec = {
    "atc4",
    "spec",
    "beta",
    "se_hc1",
    "se_cluster",
    "t_hc1",
    "t_cluster",
    "p_cluster",
    "f_first_stage",
}
exp_rob = {"spec", "mediator", "n", "gamma_fs", "F_first_stage", "p_first_stage"}
print(f"  [2] bootstrap schema OK: {exp_boot.issubset(set(boot_df.columns))}")
print(f"  [2] decomposition schema OK: {exp_dec.issubset(set(results_df.columns))}")
print(f"  [2] robustness schema OK: {exp_rob.issubset(set(robust_df.columns))}")

print(f"  [3] bootstrap rows: {len(boot_df)} (expected 1001)")
print(f"  [3] decomposition rows: {len(results_df)} (expected 10)")
print(f"  [3] robustness rows: {len(robust_df)} (expected 5)")

acme_pt, acme_lo, acme_hi = ci_summary["acme"]
prop_pt, prop_lo, prop_hi = ci_summary["acme_proportion"]
print(
    f"  [4] ACME point: {acme_pt:+.4f}, 95% CI: [{acme_lo:+.4f}, {acme_hi:+.4f}]"
)
print(
    f"  [4] ACME proportion: {prop_pt:.4f}, 95% CI: [{prop_lo:.4f}, {prop_hi:.4f}]"
)

n05ba_uni = results_df[(results_df["atc4"] == "N05BA") & (results_df["spec"] == "univariate")].iloc[0]
n05ba_jnt = results_df[(results_df["atc4"] == "N05BA") & (results_df["spec"] == "joint_multivariate")].iloc[0]
print(
    f"  [5] N05BA univariate: beta={n05ba_uni['beta']:+.4f}, "
    f"t_cluster={n05ba_uni['t_cluster']:+.3f}, p_cluster={n05ba_uni['p_cluster']:.4f}"
)
print(
    f"  [5] N05BA joint:      beta={n05ba_jnt['beta']:+.4f}, "
    f"t_cluster={n05ba_jnt['t_cluster']:+.3f}, p_cluster={n05ba_jnt['p_cluster']:.4f}"
)

n_acme_neg = (boot_df.iloc[1:]["acme"] < 0).sum()
n_boot_total = len(boot_df) - 1
print(
    f"  [6] ACME < 0 in {n_acme_neg}/{n_boot_total} bootstrap reps "
    f"({100 * n_acme_neg / n_boot_total:.1f}%, sign stability)"
)

print("\n=== sub-task 2.4 complete ===")
