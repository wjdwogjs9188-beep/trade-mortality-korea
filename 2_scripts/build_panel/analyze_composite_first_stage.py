"""
Phase 2 sub-task 2.3 — Composite ΔM1 first-stage 분석 (β = -0.0654 재현)
=======================================================================

본 script 는 R-A 의 직전 sandbox 분석 (composite ΔM1 ~ z_x_per_worker_std
first-stage OLS + HC1 SE + F-test) 을 사용자 Spyder 환경에서 직접 재현 가능한
self-contained form.

실행:
    Spyder: File → Open → 본 script → F5
    또는: %runfile C:/Users/82103/Downloads/trade_mortality_korea/2_scripts/build_panel/analyze_composite_first_stage.py --wdir
    또는 cmd: cd C:\\Users\\82103\\Downloads\\trade_mortality_korea && python 2_scripts\\build_panel\\analyze_composite_first_stage.py

Inputs:
    - 3_derived/hira_first_stage_scatter.parquet (138 sigungu × {h_code, z_x, z_x_per_worker, delta_m1_composite, in_intersection_147})

Outputs:
    - console: β + HC1 SE + t + F + p (= -0.0654, 0.0466, -1.4039, 1.9711, 0.1626)
    - 비교: z_x_raw vs z_x_per_worker_raw vs z_x_per_worker_std (z-score normalized) 3 normalization 영역의 sign/F 비교

Expected output (R-A 직전 sandbox 결과 cumulative 정합 form):
    β = -0.0654 (z_x_per_worker_std normalized)
    HC1 SE = 0.0466, t = -1.4039
    F = 1.9711, p = 0.1626

Author: 정재헌 (가천대 경제학) / R-A 공동저자 mode
Date: 2026-05-07
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Windows path
PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
FS = PROJ / "3_derived" / "hira_first_stage_scatter.parquet"

# statsmodels 가용 여부 check
try:
    import statsmodels.api as sm
    HAS_SM = True
except ImportError:
    HAS_SM = False


def fit_ols_hc1(X_var, y_var, df):
    """OLS + HC1 SE (statsmodels 우선, numpy fallback)"""
    X_raw = df[X_var].values
    y = df[y_var].values
    if HAS_SM:
        X_const = sm.add_constant(X_raw)
        fit = sm.OLS(y, X_const).fit(cov_type='HC1')
        params = np.asarray(fit.params)
        bse = np.asarray(fit.bse)
        tvalues = np.asarray(fit.tvalues)
        return {
            'beta': float(params[1]),
            'se_hc1': float(bse[1]),
            't_hc1': float(tvalues[1]),
            'F': float(fit.fvalue),
            'p_F': float(fit.f_pvalue),
            'r_squared': float(fit.rsquared),
            'n': len(y)
        }
    else:
        # numpy 수동 OLS + HC1
        X_const = np.column_stack([np.ones(len(X_raw)), X_raw])
        N, K = X_const.shape
        beta_hat = np.linalg.solve(X_const.T @ X_const, X_const.T @ y)
        resid = y - X_const @ beta_hat
        bread = np.linalg.inv(X_const.T @ X_const)
        sigma_sq = (resid ** 2).reshape(-1, 1)
        meat = X_const.T @ (sigma_sq * X_const) * (N / (N - K))
        vcov_hc1 = bread @ meat @ bread
        se_hc1 = np.sqrt(np.diag(vcov_hc1))[1]
        t = beta_hat[1] / se_hc1
        # F-stat from t (single regressor)
        F = t ** 2
        # p-value from F (df1=1, df2=N-K)
        from scipy import stats as scstats
        p_F = float(1 - scstats.f.cdf(F, 1, N - K))
        # R-squared
        ss_res = np.sum(resid ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r_squared = 1 - ss_res / ss_tot
        return {
            'beta': float(beta_hat[1]),
            'se_hc1': float(se_hc1),
            't_hc1': float(t),
            'F': float(F),
            'p_F': p_F,
            'r_squared': float(r_squared),
            'n': N
        }


# ============================================================
# 1. Load first-stage scatter
# ============================================================
print('=' * 70)
print('1. Load first-stage scatter parquet')
print('=' * 70)
fs = pd.read_parquet(FS)
print(f'  rows: {len(fs)}')
print(f'  cols: {fs.columns.tolist()}')
print(f'  dtypes:')
for c, t in fs.dtypes.items():
    print(f'    {c:<28} {t}')

# Descriptive stats
print(f'\n  z_x raw: mean={fs["z_x"].mean():.4f}, std={fs["z_x"].std():.4f}')
print(f'  z_x_per_worker raw: mean={fs["z_x_per_worker"].mean():.4f}, std={fs["z_x_per_worker"].std():.4f}')
print(f'  delta_m1_composite: mean={fs["delta_m1_composite"].mean():.4f}, std={fs["delta_m1_composite"].std():.4f}')

# z_x_per_worker_std (z-score normalized, 사용자 측 commit β = -0.0654 의 substantive form)
fs['z_x_per_worker_std'] = (fs['z_x_per_worker'] - fs['z_x_per_worker'].mean()) / fs['z_x_per_worker'].std()
print(f'  z_x_per_worker_std: mean={fs["z_x_per_worker_std"].mean():.4f}, std={fs["z_x_per_worker_std"].std():.4f}')

# z_x_std (raw z_x z-score normalized)
fs['z_x_std'] = (fs['z_x'] - fs['z_x'].mean()) / fs['z_x'].std()

# ============================================================
# 2. First-stage F-test: composite ΔM1 ~ 3 normalization 영역
# ============================================================
print('\n' + '=' * 70)
print('2. composite ΔM1 first-stage F-test (3 normalization 영역)')
print('=' * 70)

specs = [
    ('z_x', 'raw z_x (per-sigungu trade exposure)'),
    ('z_x_std', 'z-score normalized z_x (raw)'),
    ('z_x_per_worker', 'raw z_x_per_worker'),
    ('z_x_per_worker_std', 'z-score normalized z_x_per_worker (사용자 측 main spec)'),
]

print(f'\n  {"X variable":<22} {"β":>12} {"HC1 SE":>10} {"t":>10} {"F":>10} {"p":>10}')
print('  ' + '-' * 80)
for var, desc in specs:
    res = fit_ols_hc1(var, 'delta_m1_composite', fs)
    print(f'  {var:<22} {res["beta"]:>12.4f} {res["se_hc1"]:>10.4f} {res["t_hc1"]:>10.4f} {res["F"]:>10.4f} {res["p_F"]:>10.4f}')

# ============================================================
# 3. 사용자 측 commit β = -0.0654 의 substantive form 의 cumulative confirm
# ============================================================
print('\n' + '=' * 70)
print('3. β = -0.0654 의 substantive form 의 cumulative confirm')
print('=' * 70)
res_main = fit_ols_hc1('z_x_per_worker_std', 'delta_m1_composite', fs)
print(f'\n  Main spec: delta_m1_composite ~ z_x_per_worker_std')
print(f'    β = {res_main["beta"]:.6f}')
print(f'    HC1 SE = {res_main["se_hc1"]:.6f}')
print(f'    HC1 t = {res_main["t_hc1"]:.4f}')
print(f'    F = {res_main["F"]:.4f}')
print(f'    p = {res_main["p_F"]:.4f}')
print(f'    R² = {res_main["r_squared"]:.6f}')
print(f'    n = {res_main["n"]}')

# Expected (R-A 직전 sandbox 결과)
expected = {
    'beta': -0.065368,
    'se_hc1': 0.046564,
    't_hc1': -1.4039,
    'F': 1.9711,
    'p_F': 0.1626,
}
print(f'\n  Expected (R-A sandbox cumulative form):')
print(f'    β = {expected["beta"]:.6f}, HC1 t = {expected["t_hc1"]:.4f}, F = {expected["F"]:.4f}')

match = abs(res_main["beta"] - expected["beta"]) < 0.001
print(f'\n  Match: {"✅ cumulative 정합" if match else "⚠️ minor 영역"}')

# ============================================================
# 4. Stock-Yogo / OP cutoff 영역
# ============================================================
print('\n' + '=' * 70)
print('4. Weak IV concern — Stock-Yogo / OP cutoff 비교')
print('=' * 70)
print(f'\n  본 분석 first-stage F = {res_main["F"]:.4f}')
print(f'\n  Cutoff 비교:')
print(f'    Olea-Pflueger τ=10% effective F cutoff (single IV): 23.1 — 본 F의 {res_main["F"]/23.1*100:.1f}%')
print(f'    Stock-Yogo 10% bias cutoff (single IV): 16.4 — 본 F의 {res_main["F"]/16.4*100:.1f}%')
print(f'    Stock-Yogo 25% bias relaxed cutoff: 7.25 — 본 F의 {res_main["F"]/7.25*100:.1f}%')
print(f'\n  결론: composite ΔM1 위 first-stage 가 weak IV 영역 (Stock-Yogo 25% 도 미달)')
print(f'        → DGHP 2017 single-IV mediation framework 의 composite-level fundamental concern')
print(f'        → N05BA single ATC4 위 first-stage F = 16.95 의 strong-IV alternative path 의 substantive direction')

print('\n=== 분석 complete ===')
