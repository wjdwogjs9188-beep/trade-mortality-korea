"""Phase 2 sub-task 2.6 - Joint multi-mediator decomposition."""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from pathlib import Path

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
OUT = PROJ / "4_results"
OUT.mkdir(exist_ok=True)

# ============================================================
# Step 1: Build joint sample (M1 n M3 divorce n M3 fertility)
# ============================================================

# M1 N05BA Delta from panel (rebuild)
panel = pd.read_parquet(PROJ / "3_derived/hira_atc4_panel.parquet")
panel_int = panel[panel['in_intersection_147']]
ATC4 = ['N06AB', 'N06AX', 'N05BA', 'N05AX', 'A05BA']
raw_wide = panel_int.pivot_table(
 index=['h_code', 'year'], columns='atc4',
 values='prescription_rate_per_100k', aggfunc='first'
).reset_index
for atc in ATC4:
 raw_wide[f'log_{atc.lower}'] = np.log(raw_wide[atc] + 1)
 mu = raw_wide[f'log_{atc.lower}'].mean
 sigma = raw_wide[f'log_{atc.lower}'].std
 raw_wide[f'z_{atc.lower}'] = (raw_wide[f'log_{atc.lower}'] - mu) / sigma

w10 = raw_wide[raw_wide['year'] == 2010].set_index('h_code')
w19 = raw_wide[raw_wide['year'] == 2019].set_index('h_code')
m1 = pd.DataFrame(index=w10.index.intersection(w19.index))
for atc in ATC4:
 m1[f'd_z_{atc.lower}'] = w19[f'z_{atc.lower}'] - w10[f'z_{atc.lower}']
m1 = m1.dropna(subset=['d_z_n05ba']).reset_index
m1['h_code_int'] = m1['h_code'].astype(int)

# M3 delta panel
m3 = pd.read_parquet(PROJ / "3_derived/m3_delta_panel.parquet")
m3['h_code_int'] = m3['h_code'].astype(int)

# Mortality long-difference + IV
mort = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/01_mortality/sigungu_mortality_panel_v02_wa.parquet")
iv = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/02_bartik_iv/iv_z_x_bilateral.parquet")
mort['mort_rate'] = mort['deaths'] / np.maximum(mort['pop_wa'], 1)
mort['log_mort'] = np.log(mort['mort_rate'] + 1e-6)
mb = mort[mort['year'].astype(int).isin(range(1997, 2000))].groupby(['h_code', 'outcome_group'])['log_mort'].mean.reset_index
mb.columns = ['h_code', 'outcome_group', 'b']
me = mort[mort['year'].astype(int).isin(range(2018, 2023))].groupby(['h_code', 'outcome_group'])['log_mort'].mean.reset_index
me.columns = ['h_code', 'outcome_group', 'e']
panel_main = mb.merge(me, on=['h_code', 'outcome_group']).merge(iv, on='h_code')
panel_main['d_log_asr'] = panel_main['e'] - panel_main['b']
panel_main = panel_main[np.isfinite(panel_main['z_x'])]
panel_despair = panel_main[panel_main['outcome_group'] == 'despair_total'].copy
panel_despair['z_x_std'] = (panel_despair['z_x_per_worker'] - panel_despair['z_x_per_worker'].mean) / panel_despair['z_x_per_worker'].std
panel_despair['h_code_int'] = panel_despair['h_code'].astype(int)

# Joint sample build (intersection)
joint = m1[['h_code_int', 'd_z_n05ba']].merge(
 m3[['h_code_int', 'delta_marriage', 'delta_divorce', 'delta_fertility']], on='h_code_int', how='inner'
).merge(
 panel_despair[['h_code_int', 'd_log_asr', 'z_x_std']], on='h_code_int', how='inner'
).dropna(subset=['d_z_n05ba', 'delta_divorce', 'delta_fertility', 'd_log_asr', 'z_x_std'])
joint['sido_code'] = joint['h_code_int'].astype(str).str.zfill(5).str[:2]
print(f"Joint sample n: {len(joint)}, distinct sido: {joint['sido_code'].nunique}")

# ============================================================
# Step 2: Joint multivariate regression
# ============================================================
def cluster_se(X, y, cluster):
 fit = sm.OLS(y, X).fit
 G = pd.Series(cluster).nunique
 N, K = X.shape
 bread = np.linalg.inv(X.T @ X)
 meat = np.zeros((K, K))
 resid = np.asarray(fit.resid)
 cluster_arr = pd.Series(cluster).values
 for c in pd.Series(cluster).unique:
 idx = cluster_arr == c
 Xc = X[idx,:]
 rc = resid[idx]
 s_c = Xc.T @ rc
 meat += np.outer(s_c, s_c)
 G_factor = (G / (G - 1)) * ((N - 1) / (N - K))
 return fit, np.sqrt(np.diag(bread @ meat @ bread * G_factor)), G

# Joint multivariate: d_log_asr ~ z_x_std + d_z_n05ba + delta_divorce + delta_fertility
mediators = ['d_z_n05ba', 'delta_divorce', 'delta_fertility']
X_cols = ['z_x_std'] + mediators
X = sm.add_constant(joint[X_cols].values)
fit_hc1 = sm.OLS(joint['d_log_asr'].values, X).fit(cov_type='HC1')
_, se_clu, G = cluster_se(X, joint['d_log_asr'].values, joint['sido_code'])

print(f"\nJoint multivariate (n = {len(joint)}, G = {G}):")
print(f" {'var':<20} {'beta':>10} {'se_hc1':>10} {'se_clu':>10} {'t_clu':>8}")
for i, var in enumerate(['intercept'] + X_cols):
 b = float(np.asarray(fit_hc1.params)[i])
 s_h = float(np.asarray(fit_hc1.bse)[i])
 s_c = float(se_clu[i])
 t_c = b / s_c if s_c > 0 else float('nan')
 print(f" {var:<20} {b:>10.4f} {s_h:>10.4f} {s_c:>10.4f} {t_c:>8.3f}")

beta_direct_joint = float(np.asarray(fit_hc1.params)[1]) # z_x_std coefficient
print(f"\n beta_direct_joint (z_x_std | mediators) = {beta_direct_joint:.6f}")

# Univariate beta_RF on joint sample (for proportion comparison)
X_uni = sm.add_constant(joint['z_x_std'].values)
fit_rf = sm.OLS(joint['d_log_asr'].values, X_uni).fit(cov_type='HC1')
beta_rf_joint_sample = float(np.asarray(fit_rf.params)[1])
print(f" beta_RF_joint_sample (z_x_std only) = {beta_rf_joint_sample:.6f}")

# ============================================================
# Step 3: Joint DGHP per-mediator first-stage
# ============================================================
print(f"\nFirst-stage F per mediator (joint sample n = {len(joint)}):")
for med in mediators:
 X_fs = sm.add_constant(joint['z_x_std'].values)
 fit_fs = sm.OLS(joint[med].values, X_fs).fit(cov_type='HC1')
 F = float(fit_fs.fvalue)
 g = float(np.asarray(fit_fs.params)[1])
 print(f" {med:<20}: gamma_FS = {g:>8.4f}, F = {F:>7.2f}")

# ============================================================
# Step 4: Joint ACME per mediator (gamma_FS x delta_M_joint from joint regression)
# ============================================================
joint_acme = 
print(f"\nJoint ACME decomposition:")
for i, med in enumerate(mediators):
 delta_m_joint = float(np.asarray(fit_hc1.params)[i + 2]) # mediator coefficient in joint
 X_fs = sm.add_constant(joint['z_x_std'].values)
 fit_fs = sm.OLS(joint[med].values, X_fs).fit
 gamma_fs = float(np.asarray(fit_fs.params)[1])
 F_fs = float(fit_fs.fvalue)
 acme = gamma_fs * delta_m_joint
 joint_acme.append({
 'mediator': med, 'gamma_fs': gamma_fs, 'F_fs': F_fs,
 'delta_m_joint': delta_m_joint, 'ACME_joint': acme,
 'ACME_joint_prop_main': acme / -0.185,
 'ACME_joint_prop_sample': acme / beta_rf_joint_sample
 })
 print(f" {med}: gamma_FS = {gamma_fs:.4f}, delta_M_joint = {delta_m_joint:.4f}, ACME_joint = {acme:.4f}")

# Save joint decomposition
pd.DataFrame(joint_acme).to_parquet(OUT / "joint_multimediator_decomposition.parquet", index=False)

# ============================================================
# Step 5: Sido cluster bootstrap (B = 1000)
# ============================================================
np.random.seed(42)
B = 1000
sidos = joint['sido_code'].unique
boot_results = 
for b in range(B):
 boot_sidos = np.random.choice(sidos, size=len(sidos), replace=True)
 boot_df = pd.concat([joint[joint['sido_code'] == s] for s in boot_sidos], ignore_index=True)
 if len(boot_df) < 30:
 continue
 try:
 X_b = sm.add_constant(boot_df[X_cols].values)
 fit_b = sm.OLS(boot_df['d_log_asr'].values, X_b).fit
 params_b = np.asarray(fit_b.params)
 beta_d_b = float(params_b[1])
 boot_row = {'beta_direct_joint': beta_d_b}
 for i, med in enumerate(mediators):
 X_fs_b = sm.add_constant(boot_df['z_x_std'].values)
 fit_fs_b = sm.OLS(boot_df[med].values, X_fs_b).fit
 g_b = float(np.asarray(fit_fs_b.params)[1])
 d_b = float(params_b[i + 2])
 boot_row[f'gamma_fs_{med}'] = g_b
 boot_row[f'delta_m_joint_{med}'] = d_b
 boot_row[f'ACME_joint_{med}'] = g_b * d_b
 boot_results.append(boot_row)
 except Exception:
 pass

boot_df = pd.DataFrame(boot_results)
print(f"\nBootstrap successful reps: {len(boot_df)}")
print(f"\nBootstrap 95% CI:")
print(f" beta_direct_joint: [{boot_df['beta_direct_joint'].quantile(0.025):.4f}, {boot_df['beta_direct_joint'].quantile(0.975):.4f}]")
for med in mediators:
 col = f'ACME_joint_{med}'
 lo, hi = boot_df[col].quantile(0.025), boot_df[col].quantile(0.975)
 sign_neg = (boot_df[col] < 0).mean
 print(f" ACME_joint_{med}: [{lo:.4f}, {hi:.4f}], P(<0) = {sign_neg:.3f}")

# Save bootstrap
boot_df.to_parquet(OUT / "joint_multimediator_partial_residual.parquet", index=False)

# ============================================================
# Step 6: Cumulative ACME proportion (joint)
# ============================================================
acme_total_joint = sum(r['ACME_joint'] for r in joint_acme)
print(f"\nCumulative joint ACME = {acme_total_joint:.4f}")
print(f"Cumulative joint ACME / beta_RF_main = {acme_total_joint / -0.185 * 100:.1f}%")
print(f"beta_direct_joint = {beta_direct_joint:.4f} ({beta_direct_joint / -0.185 * 100:.1f}% of beta_RF_main)")

print("\n=== sub-task 2.6 complete ===")
