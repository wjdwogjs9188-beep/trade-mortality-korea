"""Phase 2 sub-task 2.2 audit script — explore-data + validate-data 합본 (Windows path)

본 script 는 사용자 Spyder 환경 에서 직접 실행 가능.
실행: F5 또는 python audit_2_2_hira.py
출력: console (R-A 의 audit cycle 결과 와 동일)
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Windows path
PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
RAW = PROJ / "0_raw" / "hira_drug" / "hira_drug_panel_v02.csv"
PANEL_LONG = PROJ / "3_derived" / "hira_atc4_panel.parquet"
PANEL_WIDE = PROJ / "3_derived" / "hira_atc4_panel_wide.parquet"
CW = PROJ / "1_codebooks" / "hira_sgguCd_to_hcode_crosswalk.csv"
INTERSECT = PROJ / "1_codebooks" / "intersection_main_hira_h_codes.csv"
SIGUNGU_CW = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"

# Load
raw = pd.read_csv(RAW, encoding='utf-8')
raw['year'] = raw['diagYm'].astype(str).str[:4].astype(int)
pl = pd.read_parquet(PANEL_LONG)
pw = pd.read_parquet(PANEL_WIDE)
cw = pd.read_csv(CW, encoding='utf-8')
intersect = pd.read_csv(INTERSECT, encoding='utf-8')
sigungu_cw = pd.read_csv(SIGUNGU_CW, encoding='utf-8')

# ============================================================
# 1. EXPLORE — RAW + Panel basic profile
# ============================================================
print('=' * 70); print('1. RAW HIRA profile'); print('=' * 70)
print(f'  shape: {raw.shape}')
print(f'  columns: {raw.columns.tolist()}')
print(f'  diagYm distinct: {raw["diagYm"].nunique()}')
print(f'  year distribution:')
print(raw['year'].value_counts().sort_index().to_string())

# Year × Month grid
print(f'\n  Year × Month grid (P1 root cause):')
raw['month'] = raw['diagYm'].astype(str).str[4:6].astype(int)
print(raw.groupby(['year','month']).size().unstack(fill_value=0).to_string())

# 2010 vs 2019 long-difference
print(f'\n=== 2. 2010 vs 2019 long-difference (substantive finding) ===')
print(f'  {"ATC4":<8} {"2010 median":>14} {"2019 median":>14} {"Δlog":>10} {"% growth":>12}')
for atc in sorted(pl['atc4'].unique()):
    s10 = pl[(pl['atc4']==atc) & (pl['year']==2010)]['prescription_rate_per_100k'].median()
    s19 = pl[(pl['atc4']==atc) & (pl['year']==2019)]['prescription_rate_per_100k'].median()
    if pd.notna(s10) and pd.notna(s19) and s10 > 0:
        dlog = np.log(s19) - np.log(s10)
        growth = (s19/s10 - 1) * 100
        print(f'  {atc:<8} {s10:>14,.0f} {s19:>14,.0f} {dlog:>10.4f} {growth:>11.1f}%')

# Cross-ATC4 correlation
print(f'\n=== 3. Cross-ATC4 correlation matrix ===')
rate_cols = ['n06ab_rate', 'n06ax_rate', 'n05ba_rate', 'n05ax_rate', 'a05ba_rate']
rate_cols = [c for c in rate_cols if c in pw.columns]
corr = pw[rate_cols].corr()
print(corr.round(3).to_string())

# ============================================================
# 4. VALIDATE — sparse cell composition + raw cross-check
# ============================================================
print('\n' + '=' * 70)
print('4. Sparse cell composition (intersection 146 × 5 × 2 = 1,460 expected)')
print('=' * 70)

expected_intersect = pd.MultiIndex.from_product([
    sorted(intersect['h_code'].astype(int).unique()),
    [2010, 2019],
    sorted(pl['atc4'].unique())
], names=['h_code', 'year', 'atc4']).to_frame(index=False)
actual_intersect = pl[pl['in_intersection_146']][['h_code', 'year', 'atc4']].copy()
actual_intersect['h_code'] = actual_intersect['h_code'].astype(int)
actual_intersect['present'] = True
merged = expected_intersect.merge(actual_intersect, on=['h_code', 'year', 'atc4'], how='left')
sparse = merged[merged['present'].isna()].copy()
print(f'  expected: {len(expected_intersect):,}, actual: {len(actual_intersect):,}, sparse: {len(sparse):,}')

# Sparse 6 sigungu identification
sparse_h = sorted(sparse['h_code'].unique())
print(f'\n  Sparse 6 sigungu 의 substantive 식별:')
for h in sparse_h:
    sub = sigungu_cw[sigungu_cw['h_code']==h].drop_duplicates(['h_code'])
    if len(sub) > 0:
        r = sub.iloc[0]
        sparse_year = sparse[sparse['h_code']==h]['year'].unique()
        event_note = r['event_note'] if pd.notna(r['event_note']) else '(no event_note)'
        print(f'    h_code={h} year={sparse_year[0]}: {r["sido_name"]} {r["h_name"]}')
        print(f'        event_note: {event_note}')

# Aggregation cross-check (5 random cells)
print(f'\n=== 5. Methodology aggregation cross-check (5 random cells) ===')
cw_clean = cw.dropna(subset=['h_code']).copy()
cw_clean['h_code_int'] = cw_clean['h_code'].astype(float).astype(int)
cw_dict = dict(zip(cw_clean['sgguCd'].astype(int), cw_clean['h_code_int']))
raw['h_code'] = raw['sgguCd'].astype(int).map(cw_dict)
raw_agg = raw.dropna(subset=['h_code']).copy()
raw_agg['h_code'] = raw_agg['h_code'].astype(int)

np.random.seed(42)
intersect_rows = pl[pl['in_intersection_146'] & ~pl['prescription_count'].isna()]
sample_idx = np.random.choice(len(intersect_rows), 5, replace=False)
for _, r in intersect_rows.iloc[sample_idx].iterrows():
    h, y, a = int(r['h_code']), int(r['year']), r['atc4']
    panel_count = r['prescription_count']
    raw_sub = raw_agg[(raw_agg['h_code']==h) & (raw_agg['year']==y) & (raw_agg['atcStep4Cd']==a)]
    raw_sum = raw_sub['totUseQty'].sum()
    flag = 'OK' if abs(panel_count - raw_sum) < 1 else 'MISMATCH'
    print(f'    h={h} y={y} a={a}: panel={panel_count:,.0f} vs raw_sum={raw_sum:,.0f} [{flag}]')

# Selection bias intersection vs non-intersection
print(f'\n=== 6. Selection bias: intersection 146 vs non-intersection 21 ===')
print(f'  {"ATC4":<8} {"int median":>14} {"non-int median":>16} {"ratio":>10}')
for atc in sorted(pl['atc4'].unique()):
    s_int = pl[(pl['atc4']==atc) & (pl['in_intersection_146'])]['prescription_rate_per_100k'].dropna()
    s_non = pl[(pl['atc4']==atc) & (~pl['in_intersection_146'])]['prescription_rate_per_100k'].dropna()
    if len(s_int) > 0 and len(s_non) > 0:
        ratio = s_int.median() / s_non.median()
        print(f'  {atc:<8} {s_int.median():>14,.0f} {s_non.median():>16,.0f} {ratio:>10.3f}')

# UNMATCHED sgguCd
print(f'\n=== 7. UNMATCHED sgguCd 정정 ===')
raw_sgg = set(raw['sgguCd'].astype(int).unique())
cw_sgg = set(cw['sgguCd'].astype(int).unique())
print(f'  raw sgguCd: {len(raw_sgg)}, crosswalk sgguCd: {len(cw_sgg)}, both: {len(raw_sgg & cw_sgg)}')
# Crosswalk h_code NaN check
nan_h = cw[cw['h_code'].isna()]
print(f'  crosswalk rows with h_code NaN: {len(nan_h)}')
if len(nan_h) > 0:
    for _, r in nan_h.iterrows():
        print(f'    sgguCd={r["sgguCd"]} ({r.get("sgguCdNm","?")}) — h_code mapping 부재')

# msupUseAmt vs totUseQty
print(f'\n=== 8. msupUseAmt vs totUseQty alternative metric ===')
cell_agg = raw.groupby(['sgguCd','year','atcStep4Cd']).agg(
    totUseQty_sum=('totUseQty','sum'),
    msupUseAmt_sum=('msupUseAmt','sum')
).reset_index()
log_corr = np.corrcoef(np.log1p(cell_agg['totUseQty_sum']), np.log1p(cell_agg['msupUseAmt_sum']))[0,1]
print(f'  cell n: {len(cell_agg):,}')
print(f'  log-log Pearson r: {log_corr:.4f}')
print(f'  ATC4 별 unit ratio (msupUseAmt/totUseQty median):')
for atc in sorted(raw['atcStep4Cd'].unique()):
    sub = raw[raw['atcStep4Cd']==atc]
    ratio = sub['msupUseAmt'].median() / max(sub['totUseQty'].median(), 1)
    print(f'    {atc}: ratio = {ratio:.2f}')

print('\n=== Audit complete ===')
