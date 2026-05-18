"""Additional sanity checks for the 2010 panel."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

panel = pd.read_parquet('3_derived/mortality_panel_2010.parquet')
xw = pd.read_csv('1_codebooks/sigungu_crosswalk.csv', dtype=str)
xw_y = xw[xw['year']=='2010'][['h_code','h_name','sido_code','sido_name']].drop_duplicates()

print(f'panel rows: {len(panel):,}')
print(f'unique h_code: {panel["h_code"].nunique()}')
print(f'unique outcome_group: {panel["outcome_group"].unique()}')

# Missing pop?
miss = panel[panel['population'].isna()]
print(f'\nMissing population cells: {len(miss):,}')
if len(miss):
    print('  with deaths > 0:', (miss['deaths'] > 0).sum())
    print('  sample:')
    print(miss.head(10).to_string(index=False))

# Pop = 0 but deaths > 0?
zero_pop = panel[(panel['population'] == 0) & (panel['deaths'] > 0)]
print(f'\nZero-pop cells with deaths > 0: {len(zero_pop):,}')
if len(zero_pop):
    print(zero_pop.head(10).to_string(index=False))

# === V4: 시군구별 자살률 분포 ===
sui = panel[panel['outcome_group']=='despair_total'].copy()
sui_h = sui.groupby('h_code', as_index=False).agg(deaths=('deaths','sum'), pop=('population','sum'))
sui_h['rate_per100k'] = sui_h['deaths'] / sui_h['pop'] * 1e5
sui_h = sui_h.merge(xw_y, on='h_code', how='left')

print('\n=== Despair total rate by 시도 (deaths-weighted) ===')
sd = sui_h.groupby('sido_name').agg(deaths=('deaths','sum'), pop=('pop','sum')).reset_index()
sd['rate'] = sd['deaths']/sd['pop']*1e5
print(sd.sort_values('rate', ascending=False).to_string(index=False))

print('\n=== Top 10 시군구 (despair rate) ===')
top = sui_h.sort_values('rate_per100k', ascending=False).head(10)
print(top[['h_code','h_name','sido_name','deaths','pop','rate_per100k']].to_string(index=False))

print('\n=== Bottom 10 시군구 (despair rate, pop>=10000) ===')
bot = sui_h[sui_h['pop']>=10000].sort_values('rate_per100k', ascending=True).head(10)
print(bot[['h_code','h_name','sido_name','deaths','pop','rate_per100k']].to_string(index=False))

# 광역시 vs 도
print('\n=== 광역시 vs 도 (despair rate) ===')
metros = ['서울특별시','부산광역시','대구광역시','인천광역시','광주광역시','대전광역시','울산광역시']
sui_h['type'] = sui_h['sido_name'].apply(lambda s: '광역시/특별시' if s in metros else '도')
gby = sui_h.groupby('type').agg(deaths=('deaths','sum'), pop=('pop','sum'))
gby['rate'] = gby['deaths']/gby['pop']*1e5
print(gby.to_string())

# Suicide alone (code 102 only)
print('\n=== 자살(102 only) by sex×age ===')
# Already aggregated to outcome_group. Need to redo from raw — skip; instead show despair rate by sex & age
sui_sa = panel[panel['outcome_group']=='despair_total'].groupby(['sex','age_kosis']).agg(d=('deaths','sum'), p=('population','sum')).reset_index()
sui_sa['rate'] = sui_sa['d']/sui_sa['p']*1e5
print(sui_sa.to_string(index=False))
