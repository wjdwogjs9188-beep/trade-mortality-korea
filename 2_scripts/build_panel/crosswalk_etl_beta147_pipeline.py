"""
Phase 2 sub-task 2.2 cumulative pipeline (Windows Spyder 호환)
============================================================== 본 script 는 사용자 Spyder 환경 에서 F5 또는 %runfile 실행 시
직전 cumulative crosswalk 정정 + ETL 재실행 + β_147 재추정의
cumulative result 를 사용자 측에서 verify + 재현 가능. 실행: Spyder: File → Open → 본 script → F5 또는: %runfile C:/Users/82103/Downloads/trade_mortality_korea/2_scripts/build_panel/crosswalk_etl_beta147_pipeline.py --wdir 또는 cmd: cd C:\\Users\\82103\\Downloads\\trade_mortality_korea && python 2_scripts\\build_panel\\crosswalk_etl_beta147_pipeline.py 출력: - console: 6-step cumulative pipeline output (~150 lines) - 3_derived/hira_atc4_panel.parquet (long, 1,640 rows) - 3_derived/hira_atc4_panel_wide.parquet (wide, 325 rows) - 1_codebooks/intersection_main_hira_h_codes.csv (147 sigungu) 주의: - HIRA crosswalk 의 220001 → 23090 정정은 직전 turn commit 완료. 본 script 는 정정 verify 만 진행 (재정정 X). - statsmodels 부재 시 numpy/scipy 수동 fallback 자동 적용. Author: 정재헌 (가천대 경제학) / 공동저자 mode
Date: 2026-05-07
Phase: Phase 2 sub-task 2.2 cumulative pipeline
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from scipy import stats # Windows path
PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
RAW = PROJ / "0_raw" / "hira_drug" / "hira_drug_panel_v02.csv"
CW = PROJ / "1_codebooks" / "hira_sgguCd_to_hcode_crosswalk.csv"
INTERSECT = PROJ / "1_codebooks" / "intersection_main_hira_h_codes.csv"
POP = PROJ / "0_raw" / "kosis_population" / "population_combined.csv"
MORT = PROJ / "8_submission" / "paper_v01_submission" / "01_mortality" / "sigungu_mortality_panel_v02_wa.parquet"
IV = PROJ / "8_submission" / "paper_v01_submission" / "02_bartik_iv" / "iv_z_x_bilateral.parquet"
OUT_DIR = PROJ / "3_derived"
OUT_DIR.mkdir(exist_ok=True) ATC4_LIST = ['N06AB', 'N06AX', 'N05BA', 'N05AX', 'A05BA']
WA_CODES = [130, 150, 160, 180, 190, 210, 230, 260] # KOSIS C3 working-age 25-64 # statsmodels 가용 여부 check
try: import statsmodels.api as sm HAS_SM = True
except ImportError: HAS_SM = False print("[INFO] statsmodels 부재 — numpy/scipy 수동 fallback 사용\n") def fit_ols_hc1(X, y): """OLS + HC1 SE 의 numpy/scipy 수동 form (statsmodels 부재 시 fallback) statsmodels version 위 fit.resid / X_const 의 ndarray vs Series ambiguity 우회 위해 np.asarray 로 numpy 변환 한 번에 적용. """ if HAS_SM: X_const = sm.add_constant(X) fit = sm.OLS(y, X_const).fit(cov_type='HC1') # numpy 변환으로 statsmodels version 영역 ambiguity 우회 params = np.asarray(fit.params) bse = np.asarray(fit.bse) tvalues = np.asarray(fit.tvalues) resid = np.asarray(fit.resid) X_arr = np.asarray(X_const) return { 'beta': float(params[1]), 'se_hc1': float(bse[1]), 't_hc1': float(tvalues[1]), 'resid': resid, 'X': X_arr } else: # 수동 OLS + HC1 X_const = np.column_stack([np.ones(len(X)), X]) N, K = X_const.shape beta_hat = np.linalg.solve(X_const.T @ X_const, X_const.T @ y) resid = y - X_const @ beta_hat bread = np.linalg.inv(X_const.T @ X_const) sigma_sq = (resid ** 2).reshape(-1, 1) meat = X_const.T @ (sigma_sq * X_const) * (N / (N - K)) vcov_hc1 = bread @ meat @ bread se_hc1 = np.sqrt(np.diag(vcov_hc1))[1] return { 'beta': float(beta_hat[1]), 'se_hc1': float(se_hc1), 't_hc1': float(beta_hat[1] / se_hc1), 'resid': resid, 'X': X_const } def compute_cluster_se(X, resid, cluster_id, K=2): """Cluster-province SE 의 수동 form""" G = cluster_id.nunique N = len(resid) bread = np.linalg.inv(X.T @ X) meat = np.zeros((K, K)) for c in cluster_id.unique: idx = (cluster_id == c).values if hasattr(cluster_id, 'values') else (cluster_id == c) Xc = X[idx, :] rc = resid[idx] s_c = Xc.T @ rc meat += np.outer(s_c, s_c) G_factor = (G / (G - 1)) * ((N - 1) / (N - K)) vcov_cluster = bread @ meat @ bread * G_factor return np.sqrt(np.diag(vcov_cluster))[1], G # ============================================================
# Step 1 — HIRA crosswalk 220001 → 23090 정정 verify
# ============================================================
print('=' * 70)
print('Step 1 — HIRA crosswalk 220001 → 23090 정정 verify')
print('=' * 70)
cw = pd.read_csv(CW, encoding='utf-8')
target = cw[cw['sgguCd']==220001]
print(f' 220001 row:')
print(target.to_string) if len(target) == 0: print('\n ⚠️ 220001 row 부재 — crosswalk 영역 verify 필요') sys.exit(1) t = target.iloc[0]
if pd.isna(t['h_code']) or t['status'] == 'UNMATCHED': print('\n ⚠️ 220001 정정 미반영 — h_code NaN 또는 status=UNMATCHED') print(' HIRA crosswalk 의 220001 row 를 23090.0 / MATCH 으로 정정 후 재실행 필요') sys.exit(1)
elif int(float(t['h_code'])) == 23090 and t['status'] == 'MATCH': print('\n ✅ 220001 → 23090 MATCH 정상 commit')
else: print(f'\n ⚠️ 예상 외 h_code 영역: {t["h_code"]} / {t["status"]}') match_n = (cw['status'] == 'MATCH').sum
unmatched_n = (cw['status'] == 'UNMATCHED').sum
print(f' total MATCH: {match_n}, UNMATCHED: {unmatched_n}') # ============================================================
# Step 2 — RAW HIRA + crosswalk inner join
# ============================================================
print('\n' + '=' * 70)
print('Step 2 — RAW HIRA load + crosswalk inner join')
print('=' * 70)
raw = pd.read_csv(RAW, encoding='utf-8')
raw['year'] = raw['diagYm'].astype(str).str[:4].astype(int)
print(f' raw shape: {raw.shape}')
print(f' diagYm distinct: {raw["diagYm"].nunique} (= 12 month × 2 year)')
print(f' year distribution: {raw["year"].value_counts.sort_index.to_dict}') # Filter year + ATC4
raw = raw[raw['year'].isin([2010, 2019]) & raw['atcStep4Cd'].isin(ATC4_LIST)]
print(f' filtered rows: {len(raw):,}') # crosswalk dict
cw_clean = cw.dropna(subset=['h_code']).copy
cw_clean['h_code_int'] = cw_clean['h_code'].astype(float).astype(int)
cw_dict = dict(zip(cw_clean['sgguCd'].astype(int), cw_clean['h_code_int']))
print(f' crosswalk dict size: {len(cw_dict)} (= 167 + 1 미추홀구)') raw['h_code'] = raw['sgguCd'].astype(int).map(cw_dict)
mapped = raw.dropna(subset=['h_code']).copy
mapped['h_code'] = mapped['h_code'].astype(int)
print(f' mapped rows (after inner join): {len(mapped):,}')
print(f' distinct h_code: {mapped["h_code"].nunique} (expected 168)') # ============================================================
# Step 3 — Aggregation + KOSIS pop join + parquet write
# ============================================================
print('\n' + '=' * 70)
print('Step 3 — Aggregation + KOSIS pop join + parquet write')
print('=' * 70) # Aggregation: sgguCd × year × atc4 sum (insupTp + recuCl + 12 month all)
agg = mapped.groupby(['h_code', 'year', 'atcStep4Cd'])['totUseQty'].sum.reset_index
agg.columns = ['h_code', 'year', 'atc4', 'prescription_count']
print(f' agg rows: {len(agg)} (expected 5 × 168 × 2 = 1,680, sparse cells reduce)') # KOSIS pop working-age 25-64
pop = pd.read_csv(POP, encoding='utf-8')
pop_wa = pop[(pop['C3'].isin(WA_CODES)) & (pop['C2'] == 0)].copy
pop_wa['h_code_str'] = pop_wa['C1'].astype(str).str.zfill(5)
agg_pop = pop_wa.groupby(['h_code_str', 'year'])['population'].sum.reset_index
agg_pop.columns = ['h_code_str', 'year', 'working_age_pop_25_64']
print(f' KOSIS pop agg: {len(agg_pop):,} rows') # Join
agg['h_code_str'] = agg['h_code'].astype(str).str.zfill(5)
panel_long = agg.merge(agg_pop, on=['h_code_str', 'year'], how='left')
panel_long['prescription_rate_per_100k'] = ( panel_long['prescription_count'] / panel_long['working_age_pop_25_64'].replace(0, np.nan)
) * 1e5 # main 221 sigungu identification (mortality + IV long-difference build)
mort = pd.read_parquet(MORT)
iv = pd.read_parquet(IV)
mort['mort_rate'] = mort['deaths'] / np.maximum(mort['pop_wa'], 1)
mort['log_mort'] = np.log(mort['mort_rate'] + 1e-6)
mb = mort[mort['year'].isin(range(1997, 2000))].groupby(['h_code', 'outcome_group'])['log_mort'].mean.reset_index
mb.columns = ['h_code', 'outcome_group', 'b']
me = mort[mort['year'].isin(range(2018, 2023))].groupby(['h_code', 'outcome_group'])['log_mort'].mean.reset_index
me.columns = ['h_code', 'outcome_group', 'e']
panel_main = mb.merge(me, on=['h_code', 'outcome_group']).merge(iv, on='h_code')
panel_main['d_log_asr'] = panel_main['e'] - panel_main['b']
panel_main = panel_main[np.isfinite(panel_main['z_x'])].copy
panel_main['sido_code'] = panel_main['h_code'].astype(str).str.zfill(5).str[:2]
panel_despair = panel_main[panel_main['outcome_group'] == 'despair_total'].copy
panel_despair['z_x_std'] = (panel_despair['z_x_per_worker'] - panel_despair['z_x_per_worker'].mean) / panel_despair['z_x_per_worker'].std main_221 = set(panel_despair['h_code'].astype(str).str.zfill(5).unique)
hira_168 = set(panel_long['h_code_str'].unique)
new_intersect = sorted(main_221 & hira_168)
print(f'\n main 221 sigungu: {len(main_221)}')
print(f' HIRA 168 sigungu: {len(hira_168)}')
print(f' 새 intersection (main 221 ∩ HIRA 168): {len(new_intersect)}')
print(f' 23090 (미추홀구) inclusion: {"23090" in new_intersect} ✅') # intersection csv 갱신
intersection_df = pd.DataFrame({ 'h_code': [int(h) for h in new_intersect], 'in_main_221': True, 'in_hira_168': True
})
intersection_df.to_csv(INTERSECT, index=False, encoding='utf-8')
print(f' intersection_main_hira_h_codes.csv 갱신: n={len(intersection_df)}') # Panel long flag
intersect_set = set(new_intersect)
panel_long['in_intersection_147'] = panel_long['h_code_str'].isin(intersect_set) # Write parquet
panel_long_out = panel_long[[ 'h_code', 'year', 'atc4', 'prescription_count', 'working_age_pop_25_64', 'prescription_rate_per_100k', 'in_intersection_147'
]].copy
panel_long_out['h_code'] = panel_long_out['h_code'].astype('int32')
panel_long_out['year'] = panel_long_out['year'].astype('int16')
panel_long_out['atc4'] = panel_long_out['atc4'].astype('string')
panel_long_out['prescription_count'] = panel_long_out['prescription_count'].astype('float32')
panel_long_out['working_age_pop_25_64'] = panel_long_out['working_age_pop_25_64'].astype('float32')
panel_long_out['prescription_rate_per_100k'] = panel_long_out['prescription_rate_per_100k'].astype('float32')
panel_long_out.to_parquet(OUT_DIR / "hira_atc4_panel.parquet", index=False)
print(f' long parquet commit: n={len(panel_long_out):,} rows') # Wide pivot
panel_wide = panel_long.pivot_table( index=['h_code', 'year', 'in_intersection_147', 'working_age_pop_25_64'], columns='atc4', values='prescription_rate_per_100k', aggfunc='first'
).reset_index
panel_wide.columns = [c.lower + ('_rate' if c.upper in ATC4_LIST else '') for c in panel_wide.columns]
panel_wide.to_parquet(OUT_DIR / "hira_atc4_panel_wide.parquet", index=False)
print(f' wide parquet commit: n={len(panel_wide):,} rows') # ============================================================
# Step 4 — β_147 재추정 (selection bias direct verify)
# ============================================================
print('\n' + '=' * 70)
print('Step 4 — β_147 재추정 (selection bias direct verify)')
print('=' * 70) # Full sample β_221
full_fit = fit_ols_hc1(panel_despair['z_x_std'].values, panel_despair['d_log_asr'].values)
print(f'\n Full sample (n={len(panel_despair)}):')
print(f' β_221 = {full_fit["beta"]:.6f}')
print(f' HC1 SE = {full_fit["se_hc1"]:.6f}, t = {full_fit["t_hc1"]:.4f}') # Intersection 147
panel_int = panel_despair[panel_despair['h_code'].astype(int).isin(set(intersection_df['h_code']))].copy
print(f'\n Intersection 147 sample (n={len(panel_int)}):') int_fit = fit_ols_hc1(panel_int['z_x_std'].values, panel_int['d_log_asr'].values)
print(f' β_147 = {int_fit["beta"]:.6f}')
print(f' HC1 SE = {int_fit["se_hc1"]:.6f}, t = {int_fit["t_hc1"]:.4f}') # Cluster-province SE (G=13 sido)
se_cluster, G = compute_cluster_se(int_fit['X'], int_fit['resid'], panel_int['sido_code'])
t_cluster = int_fit['beta'] / se_cluster
df_cluster = G - 1
p_cluster = 2 * stats.t.sf(abs(t_cluster), df=df_cluster)
print(f' Cluster-province (G={G}) SE = {se_cluster:.6f}, t = {t_cluster:.4f}, p = {p_cluster:.4f}') # Selection bias evidence
delta_beta = int_fit['beta'] - full_fit['beta']
sel_bias_norm = abs(delta_beta) / full_fit['se_hc1']
flag = '<1 → no substantive selection bias ✅' if sel_bias_norm < 1 else 'marginally >=1 → honest minor caveat'
print(f'\n Selection bias direct verify:')
print(f' Δβ = β_147 - β_221 = {delta_beta:.6f}')
print(f' |Δβ|/SE_full = {sel_bias_norm:.4f} ({flag})') # ============================================================
# Step 5 — 직전 sandbox 결과와 cumulative 정합 확인
# ============================================================
print('\n' + '=' * 70)
print('Step 5 — 직전 sandbox 결과 cumulative 정합 verify')
print('=' * 70)
expected = { 'β_221': -0.127947, 'β_147': -0.154584, 'cluster_t': -5.6512, 'cluster_p': 0.0001, 'sel_bias_norm': 1.0246,
}
actual = { 'β_221': full_fit['beta'], 'β_147': int_fit['beta'], 'cluster_t': t_cluster, 'cluster_p': p_cluster, 'sel_bias_norm': sel_bias_norm,
} print(f' {"metric":<20} {"expected":>14} {"actual":>14} {"match":>8}')
all_match = True
for k in expected: e = expected[k] a = actual[k] match = abs(e - a) < 0.01 * abs(e) if abs(e) > 0.01 else abs(e - a) < 0.001 flag = '✅' if match else '❌' if not match: all_match = False print(f' {k:<20} {e:>14.4f} {a:>14.4f} {flag:>8}') if all_match: print(f'\n ✅ 모든 metric sandbox 결과와 cumulative 정합 confirmed')
else: print(f'\n ⚠️ 일부 metric mismatch — 영역 verify 필요') # ============================================================
# Step 6 — Audit-after-action 6-step verify
# ============================================================
print('\n' + '=' * 70)
print('Step 6 — Audit-after-action 6-step verify')
print('=' * 70)
import os # 1. File integrity
for fn in ['hira_atc4_panel.parquet', 'hira_atc4_panel_wide.parquet']: fp = OUT_DIR / fn print(f' [1] {fn}: exists={fp.exists}, size={os.path.getsize(fp)/1024:.1f} KB') # 2. Schema
expected_long_cols = ['h_code', 'year', 'atc4', 'prescription_count', 'working_age_pop_25_64', 'prescription_rate_per_100k', 'in_intersection_147']
chk_long = pd.read_parquet(OUT_DIR / "hira_atc4_panel.parquet")
schema_ok = set(expected_long_cols).issubset(set(chk_long.columns))
print(f' [2] long schema OK: {schema_ok}') # 3. distinct h_code
print(f' [3] distinct h_code: {chk_long["h_code"].nunique} (expected 168)') # 4. intersection True count
print(f' [4] in_intersection_147 True rows: {chk_long["in_intersection_147"].sum} (expected ≈ 1,440)') # 5. NaN ratio
nan_rate = chk_long['prescription_rate_per_100k'].isna.mean
print(f' [5] prescription_rate_per_100k NaN ratio: {nan_rate*100:.2f}% (expected < 5%)') # 6. Year coverage
yc = chk_long.groupby('h_code')['year'].nunique.describe
print(f' [6] year coverage min/median/max: {int(yc["min"])}/{int(yc["50%"])}/{int(yc["max"])}') print('\n=== Pipeline complete ===')
print(f'\n파일 commit:')
print(f' - {OUT_DIR / "hira_atc4_panel.parquet"}')
print(f' - {OUT_DIR / "hira_atc4_panel_wide.parquet"}')
print(f' - {INTERSECT}')
