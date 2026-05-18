# Claude Code 위임 prompt — Phase 2 sub-task 2.4: DGHP 2017 ivmediate framework formal implementation

**작성**: 2026-05-07 R-A (공동저자 mode) → 정재헌 → Claude Code
**대상 박사논문**: Trade Exposure and Mortality in Export-Oriented Korea (KER July 2026 target)
**Phase**: 2 sub-task 2.4 (DGHP single-IV mediation framework formal implementation)
**선행 의존성**: ✅ sub-task 2.3 cumulative artifact (M1 panel + delta + first-stage scatter, 138 sigungu effective sample)
**후행 의존성**: paper § 7.2 narrative finalization + § 7.3-7.5 sequential commit
**예상 소요**: ~60-90분

**Strict workflow anchor**: 본 prompt 의 substantive 영역은 사용자 측 Spyder 환경 + Claude Code 환경 위 직접 실행 + 결과 paste form 의 cumulative direction 의 정통 form. R-A sandbox 위 직접 substantive 분석 영역 의 strict prohibition (사용자 메모리 feedback_no_sandbox_analysis.md 의 cumulative anchor).

---

## 본 paper context (self-contained form)

본 paper § 7.2 mechanism analysis 의 DGHP 2017 single-IV mediation framework 위 cumulative findings (사용자 측 Spyder 환경의 cumulative confirm):

- **Composite ΔM1 first-stage F = 1.97 weak IV** (사용자 Spyder 위 verify 완료, 2026-05-07): β = -0.0654, HC1 t = -1.4039, p = 0.1626. Stock-Yogo 25% 도 미달.
- **N05BA Benzo single-mediator pathway** (R-A sandbox 위 추가 verify, 사용자 측 환경 위 본 sub-task 에서 cumulative re-verify 영역): first-stage F = 16.95, γ_FS = -0.222, δ_M = +0.111, ACME = -0.025, β_RF = -0.185, ACME / β_RF = 13.4%
- **5 ATC4 reduced-form decomposition**: N05BA + A05BA strong univariate, joint multivariate R² = 0.18

본 sub-task 의 substantive 영역: 사용자 측 환경 위 formal DGHP ivmediate + bootstrapped CI (1000 reps) + cluster-province SE + 5 ATC4 decomposition 의 cumulative re-verify form 의 evidence-based maximum form 도달.

---

## 1. 목적

DGHP 2017 single-IV mediation framework 의 formal implementation:
1. N05BA single-mediator ACME bootstrapped CI (1000 reps, percentile + BCa)
2. 5 ATC4 reduced-form decomposition with cluster-province SE (G = 13)
3. Alt 0/1/2/3 composite + N05BA single-mediator robustness table
4. paper § 7.2 narrative 의 추가 evidence-based 보강 결과 commit

---

## 2. Input files (Windows path)

| File | Path |
|------|------|
| HIRA panel (raw rate) | `C:\Users\82103\Downloads\trade_mortality_korea\3_derived\hira_atc4_panel.parquet` |
| ΔM1 panel | `C:\Users\82103\Downloads\trade_mortality_korea\3_derived\hira_delta_m1_panel.parquet` |
| First-stage scatter | `C:\Users\82103\Downloads\trade_mortality_korea\3_derived\hira_first_stage_scatter.parquet` |
| Mortality panel | `C:\Users\82103\Downloads\trade_mortality_korea\8_submission\paper_v01_submission\01_mortality\sigungu_mortality_panel_v02_wa.parquet` |
| IV panel | `C:\Users\82103\Downloads\trade_mortality_korea\8_submission\paper_v01_submission\02_bartik_iv\iv_z_x_bilateral.parquet` |
| Intersection 147 | `C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\intersection_main_hira_h_codes.csv` |

---

## 3. Output files (Windows path)

### 3.1 DGHP ACME bootstrap

`C:\Users\82103\Downloads\trade_mortality_korea\4_results\dghp_acme_n05ba_bootstrap.parquet`

Schema: boot_id, gamma_fs, delta_m, beta_direct, acme, beta_rf, acme_proportion (1001 rows = 1 point + 1000 boot)

### 3.2 5 ATC4 reduced-form decomposition

`C:\Users\82103\Downloads\trade_mortality_korea\4_results\atc4_reduced_form_decomposition.parquet`

Schema: atc4, spec ("univariate" / "joint_multivariate"), beta, se_hc1, se_cluster, t_hc1, t_cluster, p_cluster, f_first_stage (10 rows = 5 univariate + 5 joint)

### 3.3 Robustness table

`C:\Users\82103\Downloads\trade_mortality_korea\4_results\m1_alt_robustness.parquet`

5 specs (Alt 0/1/2/3 + N05BA single) cumulative table.

---

## 4. Implementation script (Windows path, Spyder F5 호환)

`C:\Users\82103\Downloads\trade_mortality_korea\2_scripts\build_panel\2_4_dghp_ivmediate.py`

```python
"""Phase 2 sub-task 2.4 — DGHP 2017 ivmediate formal implementation."""
import pandas as pd
import numpy as np
from pathlib import Path

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
OUT = PROJ / "4_results"
OUT.mkdir(exist_ok=True)

# statsmodels uses HC1 + cluster SE
try:
    import statsmodels.api as sm
    HAS_SM = True
except ImportError:
    HAS_SM = False
from scipy import stats

# ============================================================
# Step 1: Build joint sample (138 intersection complete-case)
# ============================================================
panel = pd.read_parquet(PROJ / "3_derived/hira_atc4_panel.parquet")
panel_int = panel[panel['in_intersection_147']]
ATC4_LIST = ['N06AB','N06AX','N05BA','N05AX','A05BA']

raw_wide = panel_int.pivot_table(
    index=['h_code','year'], columns='atc4',
    values='prescription_rate_per_100k', aggfunc='first'
).reset_index()
for atc in ATC4_LIST:
    raw_wide[f'log_{atc.lower()}'] = np.log(raw_wide[atc] + 1)
    mu = raw_wide[f'log_{atc.lower()}'].mean()
    sigma = raw_wide[f'log_{atc.lower()}'].std()
    raw_wide[f'z_{atc.lower()}'] = (raw_wide[f'log_{atc.lower()}'] - mu) / sigma

w10 = raw_wide[raw_wide['year']==2010].set_index('h_code')
w19 = raw_wide[raw_wide['year']==2019].set_index('h_code')
delta_indiv = pd.DataFrame(index=w10.index.intersection(w19.index))
for atc in ATC4_LIST:
    delta_indiv[f'd_z_{atc.lower()}'] = w19[f'z_{atc.lower()}'] - w10[f'z_{atc.lower()}']
delta_indiv = delta_indiv.dropna().reset_index()

# Mortality + IV merge
mort = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/01_mortality/sigungu_mortality_panel_v02_wa.parquet")
iv = pd.read_parquet(PROJ / "8_submission/paper_v01_submission/02_bartik_iv/iv_z_x_bilateral.parquet")
mort['mort_rate'] = mort['deaths'] / np.maximum(mort['pop_wa'], 1)
mort['log_mort'] = np.log(mort['mort_rate'] + 1e-6)
mb = mort[mort['year'].isin(range(1997,2000))].groupby(['h_code','outcome_group'])['log_mort'].mean().reset_index()
mb.columns = ['h_code','outcome_group','b']
me = mort[mort['year'].isin(range(2018,2023))].groupby(['h_code','outcome_group'])['log_mort'].mean().reset_index()
me.columns = ['h_code','outcome_group','e']
panel_main = mb.merge(me, on=['h_code','outcome_group']).merge(iv, on='h_code')
panel_main['d_log_asr'] = panel_main['e'] - panel_main['b']
panel_main = panel_main[np.isfinite(panel_main['z_x'])]
panel_despair = panel_main[panel_main['outcome_group']=='despair_total'].copy()
panel_despair['z_x_std'] = (panel_despair['z_x_per_worker'] - panel_despair['z_x_per_worker'].mean()) / panel_despair['z_x_per_worker'].std()

delta_indiv['h_code_int'] = delta_indiv['h_code'].astype(int)
panel_despair['h_code_int'] = panel_despair['h_code'].astype(int)
joint = delta_indiv.merge(
    panel_despair[['h_code_int','d_log_asr','z_x_std']],
    on='h_code_int', how='inner'
)
joint['sido_code'] = joint['h_code'].astype(str).str.zfill(5).str[:2]
print(f"joint sample n: {len(joint)}")
assert len(joint) == 138, f"Expected 138, got {len(joint)}"

# ============================================================
# Step 2: DGHP single-mediator decomposition
# ============================================================
def dghp_decomp(df, mediator='d_z_n05ba'):
    X_fs = sm.add_constant(df['z_x_std'].values)
    fit_fs = sm.OLS(df[mediator].values, X_fs).fit()
    gamma_fs = float(np.asarray(fit_fs.params)[1])
    F_fs = float(fit_fs.fvalue)

    X_2s = sm.add_constant(df[[mediator,'z_x_std']].values)
    fit_2s = sm.OLS(df['d_log_asr'].values, X_2s).fit()
    delta_m = float(np.asarray(fit_2s.params)[1])
    beta_d = float(np.asarray(fit_2s.params)[2])

    X_rf = sm.add_constant(df['z_x_std'].values)
    fit_rf = sm.OLS(df['d_log_asr'].values, X_rf).fit()
    beta_rf = float(np.asarray(fit_rf.params)[1])

    return {
        'gamma_fs': gamma_fs, 'F_fs': F_fs,
        'delta_m': delta_m, 'beta_direct': beta_d,
        'acme': gamma_fs * delta_m, 'beta_rf': beta_rf,
        'acme_proportion': (gamma_fs * delta_m) / beta_rf
    }

# Point estimate
point = {'boot_id': 0, **dghp_decomp(joint)}
print(f"\nPoint estimate (N05BA single-mediator):")
for k, v in point.items():
    print(f"  {k}: {v:.6f}" if isinstance(v, float) else f"  {k}: {v}")

# ============================================================
# Step 3: Cluster bootstrap (sido-level, 1000 reps)
# ============================================================
np.random.seed(42)
B = 1000
boot = [point]
sidos = joint['sido_code'].unique()
for b in range(1, B+1):
    boot_sidos = np.random.choice(sidos, size=len(sidos), replace=True)
    boot_df = pd.concat([joint[joint['sido_code']==s] for s in boot_sidos], ignore_index=True)
    try:
        boot.append({'boot_id': b, **dghp_decomp(boot_df)})
    except Exception:
        pass

boot_df = pd.DataFrame(boot)
boot_df.to_parquet(OUT / "dghp_acme_n05ba_bootstrap.parquet", index=False)

# CI
print(f"\nBootstrap CI (B = {len(boot_df)-1}):")
for col in ['gamma_fs','delta_m','beta_direct','acme','beta_rf','acme_proportion']:
    s = boot_df.iloc[1:][col]
    lo, hi = s.quantile(0.025), s.quantile(0.975)
    print(f"  {col}: point = {boot_df.iloc[0][col]:.4f}, 95% CI = [{lo:.4f}, {hi:.4f}]")

# ============================================================
# Step 4: 5 ATC4 reduced-form decomposition with cluster SE
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

results = []

# Univariate
for atc in ATC4_LIST:
    col = f'd_z_{atc.lower()}'
    sub = joint[[col,'d_log_asr','z_x_std','sido_code']].dropna()
    X = sm.add_constant(sub[col].values)
    fit_hc1 = sm.OLS(sub['d_log_asr'].values, X).fit(cov_type='HC1')
    _, se_clu, G = cluster_se(X, sub['d_log_asr'].values, sub['sido_code'])

    X_fs = sm.add_constant(sub['z_x_std'].values)
    fit_fs = sm.OLS(sub[col].values, X_fs).fit(cov_type='HC1')

    beta = float(np.asarray(fit_hc1.params)[1])
    se_h = float(np.asarray(fit_hc1.bse)[1])
    t_h = float(np.asarray(fit_hc1.tvalues)[1])
    t_c = beta / se_clu[1]
    p_c = 2 * (1 - stats.t.cdf(abs(t_c), df=G-1))
    results.append({
        'atc4': atc, 'spec': 'univariate',
        'beta': beta, 'se_hc1': se_h, 'se_cluster': float(se_clu[1]),
        't_hc1': t_h, 't_cluster': t_c, 'p_cluster': p_c,
        'f_first_stage': float(fit_fs.fvalue)
    })

# Joint multivariate
cols = [f'd_z_{a.lower()}' for a in ATC4_LIST]
sub = joint[cols + ['d_log_asr','sido_code']].dropna()
X = sm.add_constant(sub[cols].values)
fit_hc1 = sm.OLS(sub['d_log_asr'].values, X).fit(cov_type='HC1')
_, se_clu, G = cluster_se(X, sub['d_log_asr'].values, sub['sido_code'])
for i, atc in enumerate(ATC4_LIST):
    beta = float(np.asarray(fit_hc1.params)[i+1])
    se_h = float(np.asarray(fit_hc1.bse)[i+1])
    t_h = float(np.asarray(fit_hc1.tvalues)[i+1])
    t_c = beta / se_clu[i+1]
    p_c = 2 * (1 - stats.t.cdf(abs(t_c), df=G-1))
    results.append({
        'atc4': atc, 'spec': 'joint_multivariate',
        'beta': beta, 'se_hc1': se_h, 'se_cluster': float(se_clu[i+1]),
        't_hc1': t_h, 't_cluster': t_c, 'p_cluster': p_c,
        'f_first_stage': np.nan
    })

results_df = pd.DataFrame(results)
results_df.to_parquet(OUT / "atc4_reduced_form_decomposition.parquet", index=False)
print(f"\n5 ATC4 reduced-form decomposition (univariate + joint):")
print(results_df.to_string(index=False))

# ============================================================
# Step 5: Robustness table (4 alt composites + N05BA)
# ============================================================
m1 = pd.read_parquet(PROJ / "3_derived/hira_m1_panel.parquet")
delta = pd.read_parquet(PROJ / "3_derived/hira_delta_m1_panel.parquet")
delta_cc = delta[delta['complete_case'] & delta['in_intersection_147']]
delta_cc['h_code_int'] = delta_cc['h_code'].astype(int)
delta_cc = delta_cc.merge(panel_despair[['h_code_int','d_log_asr','z_x_std']], on='h_code_int', how='inner')
delta_cc['sido_code'] = delta_cc['h_code'].astype(str).str.zfill(5).str[:2]

robust = []
specs = {
    'Alt 0 composite (5 ATC4 mean)': 'delta_m1_composite',
    'Alt 1 4-mental (excl A05BA)': 'delta_m1_4mental',
    'Alt 2 A05BA-only': 'delta_m1_liver',
    'Alt 3 PCA 1st': 'delta_m1_pca1',
    'N05BA single (from joint)': 'd_z_n05ba',
}
for label, col in specs.items():
    df = joint if col == 'd_z_n05ba' else delta_cc.dropna(subset=[col])
    X_fs = sm.add_constant(df['z_x_std'].values)
    fit_fs = sm.OLS(df[col].values, X_fs).fit(cov_type='HC1')
    robust.append({
        'spec': label, 'mediator': col, 'n': len(df),
        'gamma_fs': float(np.asarray(fit_fs.params)[1]),
        'F_first_stage': float(fit_fs.fvalue),
        'p_first_stage': float(fit_fs.f_pvalue)
    })
robust_df = pd.DataFrame(robust)
robust_df.to_parquet(OUT / "m1_alt_robustness.parquet", index=False)
print(f"\nRobustness table (4 alt composite + N05BA single):")
print(robust_df.to_string(index=False))

print("\n=== sub-task 2.4 complete ===")
```

---

## 5. PowerShell wrapper

`C:\Users\82103\Downloads\trade_mortality_korea\2_scripts\build_panel\run_dghp_ivmediate.ps1`

```powershell
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pyScript = Join-Path $scriptDir "2_4_dghp_ivmediate.py"
Write-Host "[run_dghp_ivmediate] starting Python: $pyScript"
python $pyScript
Write-Host "Done."
```

---

## 6. 검증 commit 형식 (사용자 측 paste 형식)

```markdown
## Phase 2 sub-task 2.4 완료 — DGHP formal ivmediate

**Output**:
- 4_results/dghp_acme_n05ba_bootstrap.parquet (1001 rows = 1 point + 1000 boot)
- 4_results/atc4_reduced_form_decomposition.parquet (10 rows)
- 4_results/m1_alt_robustness.parquet (5 rows)

**Verify 결과**:
- ACME point: ?, 95% CI: [?, ?]
- ACME / β_RF proportion: 13.4% ± ?
- Cluster-SE 위 N05BA univariate: t = ?, p = ?
- Cluster-SE 위 N05BA joint multivariate: t = ?, p = ?

**P1/P2/P3**: ...

**다음 step**: paper § 7.2 narrative finalization
```

---

## 7. 주의사항 (사용자 메모리 cumulative anchor)

1. **R-A sandbox 직접 분석 절대 금지** (memory: feedback_no_sandbox_analysis.md): 본 sub-task 의 모든 substantive 분석은 사용자 측 Spyder + Claude Code 환경 위 실행. R-A 는 본 prompt + script 만 commit, 결과 paste 위 다음 step.
2. **한자 사용 금지** (memory: feedback_no_hanja.md)
3. **0_raw 절대 수정 금지**
4. **Cluster bootstrap**: sido_code 단위 (G=13)
5. **Audit-after-action 6-step verify**: file integrity + schema + n + NaN ratio + ACME match + bootstrap CI

---

## 8. 실행 명령

Spyder:
```
%runfile C:/Users/82103/Downloads/trade_mortality_korea/2_scripts/build_panel/2_4_dghp_ivmediate.py --wdir
```

또는 Claude Code 위임:
```
이 prompt 의 spec 대로 Python script + PowerShell wrapper 작성 + 실행:
- 2_scripts/build_panel/2_4_dghp_ivmediate.py
- 2_scripts/build_panel/run_dghp_ivmediate.ps1
완료 후 verify 결과를 § 6 형식으로 보고.
```

---

**End of Claude Code 위임 prompt**
