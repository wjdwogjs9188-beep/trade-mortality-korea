# Claude Code 위임 prompt — Phase 2 sub-task 2.6: Joint multi-mediator decomposition (M1 + M3 divorce + M3 fertility)

**작성**: 2026-05-07 R-A (공동저자 mode) → 정재헌 → Claude Code
**대상 박사논문**: Trade Exposure and Mortality in Export-Oriented Korea (KER July 2026 target)
**Phase**: 2 sub-task 2.6 (joint multi-mediator decomposition + partial-correlation residual + bootstrap CI)
**선행 의존성**: ✅ sub-task 2.3 (M1 N05BA) + ✅ sub-task 2.4 (DGHP framework) + ✅ sub-task 2.5 (M3 + M4 + M5 + M6)
**후행 의존성**: paper § 7.6 narrative wording 권고 form + paper § 7 finalization
**예상 소요**: ~60-90분 (joint sample build + joint regression + bootstrap + sensitivity)

**Strict workflow anchor**: 본 prompt 의 모든 substantive 분석 (regression, joint regression, bootstrap, decomposition) 은 사용자 측 Spyder + Claude Code 환경 위 직접 실행 + 결과 paste form. R-A sandbox 위 substantive 분석 부재 (memory: feedback_no_sandbox_analysis.md).

---

## 본 paper context (self-contained)

본 paper § 7 mechanism analysis 의 cumulative findings (sub-task 2.3-2.5):

**Univariate ACME proportions (main β_RF = -0.185 anchor)**:
- M1 N05BA pharmaceutical: 13.4% (sub-task 2.3, 138 sample, F = 22.59)
- M3 divorce: 50.8% (sub-task 2.5, 210 sample, F = 55.73)
- M3 fertility: 17.8% (sub-task 2.5, 213 sample, F = 14.26)
- M6 suicide validation: 12.7% (sub-task 2.5, 205 sample, F = 2.38, ⊂ despair_total)
- **Univariate sum**: 94.7% (main-β_RF anchor) / 129.9% (sample-specific anchor, > 100% overlap evidence)

**M4 + M5 effect modifier null (homogeneous)**: cohort sex ratio + university distance interaction t < 1.

**Joint multi-mediator decomposition 의 substantive prerequisite** (paper § 7.6 narrative anchor):
- M1 + M3 divorce + M3 fertility 의 joint regression (M6 suicide 제외, 로지컬 inclusion 영역)
- Partial-correlation residual direct effect 의 cumulative form
- Sido cluster bootstrap CI (B = 1000, G ≈ 12-16)

본 sub-task 2.6 의 substantive 영역: 사용자 측 환경 위 joint multi-mediator decomposition 의 evidence-based maximum form 도달 + paper § 7.6 narrative 의 cumulative anchor.

---

## 1. 목적

1. M1 + M3 divorce + M3 fertility 3-mediator joint sample build (intersection of M1 138 ∩ M3 divorce 210 ∩ M3 fertility 213, expected n ≈ 100-130)
2. Joint multivariate regression: Δlog asr_p1 ~ z_x_std + d_z_n05ba + delta_divorce + delta_fertility (with HC1 + cluster-province SE)
3. Joint partial-correlation residual direct effect (β_direct_joint)
4. Joint DGHP framework 위 ACME_joint per mediator + cumulative joint ACME (≠ univariate sum due to overlap)
5. Sido-clustered bootstrap (B = 1000) on joint ACME + partial-correlation residual
6. Sub-period sensitivity (post-2008 sub-period parallel)
7. Robustness: 4-mediator specification (add M6 suicide as sensitivity)

---

## 2. Input files (Windows path)

| File | Path |
|------|------|
| M1 ΔM1_N05BA | `C:\Users\82103\Downloads\trade_mortality_korea\3_derived\hira_first_stage_scatter.parquet` (138 rows, d_z_n05ba via panel pivot) |
| M3 delta panel | `C:\Users\82103\Downloads\trade_mortality_korea\3_derived\m3_delta_panel.parquet` (253 rows, delta_marriage / delta_divorce / delta_fertility) |
| M6 suicide panel | `C:\Users\82103\Downloads\trade_mortality_korea\3_derived\m6_suicide_panel.parquet` (229 rows, sensitivity) |
| Mortality panel | `C:\Users\82103\Downloads\trade_mortality_korea\8_submission\paper_v01_submission\01_mortality\sigungu_mortality_panel_v02_wa.parquet` |
| IV panel | `C:\Users\82103\Downloads\trade_mortality_korea\8_submission\paper_v01_submission\02_bartik_iv\iv_z_x_bilateral.parquet` |

---

## 3. Output files (Windows path)

`C:\Users\82103\Downloads\trade_mortality_korea\4_results\`

| File | Description |
|------|-------------|
| `joint_multimediator_decomposition.parquet` | 3-mediator joint regression coefficients + SE + bootstrap CI |
| `joint_multimediator_partial_residual.parquet` | β_direct_joint + bootstrap CI |
| `joint_multimediator_subperiod.parquet` | post-2008 sub-period sensitivity |
| `joint_multimediator_4mediator_robustness.parquet` | 4-mediator robustness (with M6) |

---

## 4. Implementation script

`C:\Users\82103\Downloads\trade_mortality_korea\2_scripts\build_panel\2_6_joint_multimediator.py`

```python
"""Phase 2 sub-task 2.6 — Joint multi-mediator decomposition."""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from pathlib import Path

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
OUT = PROJ / "4_results"
OUT.mkdir(exist_ok=True)

# ============================================================
# Step 1: Build joint sample (M1 ∩ M3 divorce ∩ M3 fertility)
# ============================================================

# M1 N05BA Δ from panel (rebuild)
panel = pd.read_parquet(PROJ / "3_derived/hira_atc4_panel.parquet")
panel_int = panel[panel['in_intersection_147']]
ATC4 = ['N06AB','N06AX','N05BA','N05AX','A05BA']
raw_wide = panel_int.pivot_table(
    index=['h_code','year'], columns='atc4',
    values='prescription_rate_per_100k', aggfunc='first'
).reset_index()
for atc in ATC4:
    raw_wide[f'log_{atc.lower()}'] = np.log(raw_wide[atc] + 1)
    mu = raw_wide[f'log_{atc.lower()}'].mean()
    sigma = raw_wide[f'log_{atc.lower()}'].std()
    raw_wide[f'z_{atc.lower()}'] = (raw_wide[f'log_{atc.lower()}'] - mu) / sigma

w10 = raw_wide[raw_wide['year']==2010].set_index('h_code')
w19 = raw_wide[raw_wide['year']==2019].set_index('h_code')
m1 = pd.DataFrame(index=w10.index.intersection(w19.index))
for atc in ATC4:
    m1[f'd_z_{atc.lower()}'] = w19[f'z_{atc.lower()}'] - w10[f'z_{atc.lower()}']
m1 = m1.dropna(subset=['d_z_n05ba']).reset_index()
m1['h_code_int'] = m1['h_code'].astype(int)

# M3 delta panel
m3 = pd.read_parquet(PROJ / "3_derived/m3_delta_panel.parquet")
m3['h_code_int'] = m3['h_code'].astype(int)

# Mortality long-difference + IV
mort = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/01_mortality/sigungu_mortality_panel_v02_wa.parquet")
iv = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/02_bartik_iv/iv_z_x_bilateral.parquet")
mort['mort_rate'] = mort['deaths'] / np.maximum(mort['pop_wa'], 1)
mort['log_mort'] = np.log(mort['mort_rate'] + 1e-6)
mb = mort[mort['year'].astype(int).isin(range(1997,2000))].groupby(['h_code','outcome_group'])['log_mort'].mean().reset_index()
mb.columns = ['h_code','outcome_group','b']
me = mort[mort['year'].astype(int).isin(range(2018,2023))].groupby(['h_code','outcome_group'])['log_mort'].mean().reset_index()
me.columns = ['h_code','outcome_group','e']
panel_main = mb.merge(me, on=['h_code','outcome_group']).merge(iv, on='h_code')
panel_main['d_log_asr'] = panel_main['e'] - panel_main['b']
panel_main = panel_main[np.isfinite(panel_main['z_x'])]
panel_despair = panel_main[panel_main['outcome_group']=='despair_total'].copy()
panel_despair['z_x_std'] = (panel_despair['z_x_per_worker'] - panel_despair['z_x_per_worker'].mean()) / panel_despair['z_x_per_worker'].std()
panel_despair['h_code_int'] = panel_despair['h_code'].astype(int)

# Joint sample build (intersection)
joint = m1[['h_code_int','d_z_n05ba']].merge(
    m3[['h_code_int','delta_marriage','delta_divorce','delta_fertility']], on='h_code_int', how='inner'
).merge(
    panel_despair[['h_code_int','d_log_asr','z_x_std']], on='h_code_int', how='inner'
).dropna(subset=['d_z_n05ba','delta_divorce','delta_fertility','d_log_asr','z_x_std'])
joint['sido_code'] = joint['h_code_int'].astype(str).str.zfill(5).str[:2]
print(f"Joint sample n: {len(joint)}, distinct sido: {joint['sido_code'].nunique()}")

# ============================================================
# Step 2: Joint multivariate regression
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
        Xc = X[idx, :]; rc = resid[idx]
        s_c = Xc.T @ rc
        meat += np.outer(s_c, s_c)
    G_factor = (G/(G-1))*((N-1)/(N-K))
    return fit, np.sqrt(np.diag(bread @ meat @ bread * G_factor)), G

# Joint multivariate: d_log_asr ~ z_x_std + d_z_n05ba + delta_divorce + delta_fertility
mediators = ['d_z_n05ba', 'delta_divorce', 'delta_fertility']
X_cols = ['z_x_std'] + mediators
X = sm.add_constant(joint[X_cols].values)
fit_hc1 = sm.OLS(joint['d_log_asr'].values, X).fit(cov_type='HC1')
_, se_clu, G = cluster_se(X, joint['d_log_asr'].values, joint['sido_code'])

print(f"\nJoint multivariate (n = {len(joint)}, G = {G}):")
print(f"  {'var':<20} {'beta':>10} {'se_hc1':>10} {'se_clu':>10} {'t_clu':>8}")
for i, var in enumerate(['intercept'] + X_cols):
    b = float(np.asarray(fit_hc1.params)[i])
    s_h = float(np.asarray(fit_hc1.bse)[i])
    s_c = float(se_clu[i])
    t_c = b / s_c if s_c > 0 else float('nan')
    print(f"  {var:<20} {b:>10.4f} {s_h:>10.4f} {s_c:>10.4f} {t_c:>8.3f}")

beta_direct_joint = float(np.asarray(fit_hc1.params)[1])  # z_x_std coefficient
print(f"\n  β_direct_joint (z_x_std | mediators) = {beta_direct_joint:.6f}")

# Univariate β_RF on joint sample (for proportion comparison)
X_uni = sm.add_constant(joint['z_x_std'].values)
fit_rf = sm.OLS(joint['d_log_asr'].values, X_uni).fit(cov_type='HC1')
beta_rf_joint_sample = float(np.asarray(fit_rf.params)[1])
print(f"  β_RF_joint_sample (z_x_std only) = {beta_rf_joint_sample:.6f}")

# ============================================================
# Step 3: Joint DGHP per-mediator first-stage
# ============================================================
print(f"\nFirst-stage F per mediator (joint sample n = {len(joint)}):")
for med in mediators:
    X_fs = sm.add_constant(joint['z_x_std'].values)
    fit_fs = sm.OLS(joint[med].values, X_fs).fit(cov_type='HC1')
    F = float(fit_fs.fvalue)
    g = float(np.asarray(fit_fs.params)[1])
    print(f"  {med:<20}: γ_FS = {g:>8.4f}, F = {F:>7.2f}")

# ============================================================
# Step 4: Joint ACME per mediator (γ_FS × δ_M_joint from joint regression)
# ============================================================
joint_acme = []
print(f"\nJoint ACME decomposition:")
for i, med in enumerate(mediators):
    delta_m_joint = float(np.asarray(fit_hc1.params)[i + 2])  # mediator coefficient in joint
    X_fs = sm.add_constant(joint['z_x_std'].values)
    fit_fs = sm.OLS(joint[med].values, X_fs).fit()
    gamma_fs = float(np.asarray(fit_fs.params)[1])
    F_fs = float(fit_fs.fvalue)
    acme = gamma_fs * delta_m_joint
    joint_acme.append({
        'mediator': med, 'gamma_fs': gamma_fs, 'F_fs': F_fs,
        'delta_m_joint': delta_m_joint, 'ACME_joint': acme,
        'ACME_joint_prop_main': acme / -0.185,
        'ACME_joint_prop_sample': acme / beta_rf_joint_sample
    })
    print(f"  {med}: γ_FS = {gamma_fs:.4f}, δ_M_joint = {delta_m_joint:.4f}, ACME_joint = {acme:.4f}")

# Save joint decomposition
pd.DataFrame(joint_acme).to_parquet(OUT / "joint_multimediator_decomposition.parquet", index=False)

# ============================================================
# Step 5: Sido cluster bootstrap (B = 1000)
# ============================================================
np.random.seed(42)
B = 1000
sidos = joint['sido_code'].unique()
boot_results = []
for b in range(B):
    boot_sidos = np.random.choice(sidos, size=len(sidos), replace=True)
    boot_df = pd.concat([joint[joint['sido_code']==s] for s in boot_sidos], ignore_index=True)
    if len(boot_df) < 30:
        continue
    try:
        X_b = sm.add_constant(boot_df[X_cols].values)
        fit_b = sm.OLS(boot_df['d_log_asr'].values, X_b).fit()
        params_b = np.asarray(fit_b.params)
        beta_d_b = float(params_b[1])
        boot_row = {'beta_direct_joint': beta_d_b}
        for i, med in enumerate(mediators):
            X_fs_b = sm.add_constant(boot_df['z_x_std'].values)
            fit_fs_b = sm.OLS(boot_df[med].values, X_fs_b).fit()
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
print(f"  β_direct_joint: [{boot_df['beta_direct_joint'].quantile(0.025):.4f}, {boot_df['beta_direct_joint'].quantile(0.975):.4f}]")
for med in mediators:
    col = f'ACME_joint_{med}'
    lo, hi = boot_df[col].quantile(0.025), boot_df[col].quantile(0.975)
    sign_neg = (boot_df[col] < 0).mean()
    print(f"  ACME_joint_{med}: [{lo:.4f}, {hi:.4f}], P(<0) = {sign_neg:.3f}")

# Save bootstrap
boot_df.to_parquet(OUT / "joint_multimediator_partial_residual.parquet", index=False)

# ============================================================
# Step 6: Cumulative ACME proportion (joint)
# ============================================================
acme_total_joint = sum(r['ACME_joint'] for r in joint_acme)
print(f"\nCumulative joint ACME = {acme_total_joint:.4f}")
print(f"Cumulative joint ACME / β_RF_main = {acme_total_joint / -0.185 * 100:.1f}%")
print(f"β_direct_joint = {beta_direct_joint:.4f} ({beta_direct_joint / -0.185 * 100:.1f}% of β_RF_main)")

print("\n=== sub-task 2.6 complete ===")
```

---

## 5. PowerShell wrapper (`run_subtask_2_6.ps1`)

```powershell
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "=== Sub-task 2.6: Joint multi-mediator decomposition ==="
python (Join-Path $scriptDir "2_6_joint_multimediator.py")
Write-Host "=== Done ==="
```

---

## 6. 검증 commit 형식

```markdown
## Phase 2 sub-task 2.6 완료 — Joint multi-mediator decomposition

**Output**:
- 4_results/joint_multimediator_decomposition.parquet (3 mediator joint ACME)
- 4_results/joint_multimediator_partial_residual.parquet (1000-rep bootstrap)
- (사용자 측 후속) joint_multimediator_subperiod.parquet
- (사용자 측 후속) joint_multimediator_4mediator_robustness.parquet

**Verify 결과**:
- Joint sample n = ?, sido G = ?
- β_direct_joint = ?, 95% CI [?, ?] (zero exclusion ?)
- Joint ACME per mediator:
  - M1 N05BA: γ_FS = ?, δ_M_joint = ?, ACME_joint = ?, prop_main = ?%
  - M3 divorce: γ_FS = ?, δ_M_joint = ?, ACME_joint = ?, prop_main = ?%
  - M3 fertility: γ_FS = ?, δ_M_joint = ?, ACME_joint = ?, prop_main = ?%
- Cumulative joint ACME / β_RF_main = ?%
- β_direct_joint / β_RF_main = ?%
- Bootstrap sign stability (per mediator P(ACME < 0)): ?, ?, ?

**P1/P2/P3**: ...

**다음 step**: paper § 7.6 narrative wording 권고 form 의 R-A 측 markdown draft commit
```

---

## 7. 주의사항

1. **R-A sandbox 직접 분석 금지** (memory: feedback_no_sandbox_analysis.md)
2. **분업 경계 anchor**: paper 본문 직접 Edit 부재 (mechanical β value substitution 외)
3. **한자 사용 금지**
4. **Joint sample 영역**: M1 138 ∩ M3 divorce 210 ∩ M3 fertility 213 의 cumulative intersection (expected n ≈ 100-130 영역 의 cumulative form). M6 suicide ⊂ despair_total 의 logical inclusion 영역으로 main joint 영역에서 제외, robustness 영역에서 추가.
5. **Cluster G**: joint sample 위 sido 분포 (12-16 영역의 cumulative form)

---

## 8. 실행 명령

Spyder:
```
%runfile C:/Users/82103/Downloads/trade_mortality_korea/2_scripts/build_panel/2_6_joint_multimediator.py --wdir
```

또는 Claude Code 위임:
```
이 prompt 의 spec 대로 Python script + PowerShell wrapper 작성 + 실행:
- 2_scripts/build_panel/2_6_joint_multimediator.py
- 2_scripts/build_panel/run_subtask_2_6.ps1
완료 후 verify 결과를 § 6 형식으로 보고.
```

---

**End of Claude Code 위임 prompt**
