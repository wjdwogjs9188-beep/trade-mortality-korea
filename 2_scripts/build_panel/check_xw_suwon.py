"""Check crosswalk mapping for 수원시 자치구."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

xw = pd.read_csv('1_codebooks/sigungu_crosswalk.csv', dtype=str)
xw_2010 = xw[xw['year'] == '2010']

# 수원시
print('=== 수원시 자치구 (raw_codes 31011-31014) ===')
for raw in ['31010','31011','31012','31013','31014']:
 sub = xw_2010[xw_2010['raw_code'] == raw]
 if len(sub):
 print(f' raw {raw} → h_code {sub.iloc[0]["h_code"]} {sub.iloc[0]["h_name"]}')
 else:
 print(f' raw {raw} → NOT in 2010 crosswalk')

print('\n=== 청주시 (raw_codes 33010, 33310) ===')
for raw in ['33010','33011','33012','33310']:
 sub = xw_2010[xw_2010['raw_code'] == raw]
 if len(sub):
 print(f' raw {raw} → h_code {sub.iloc[0]["h_code"]} {sub.iloc[0]["h_name"]}')
 else:
 print(f' raw {raw} → NOT in 2010 crosswalk')

# pop check
pop = pd.read_csv('0_raw/kosis_population/population_combined.csv', dtype=str)
p10 = pop[pop['year'] == '2010']

# Sum check: 수원시 자치구 합 vs 수원시 합계 in pop
print('\n=== Pop integrity: 수원시 자치구 sum vs city total ===')
city = p10[(p10['C1'] == '31010') & (p10['C2'] == '0') & (p10['C3'] == '000')]['population'].astype(float).sum
districts = p10[(p10['C1'].isin(['31011','31012','31013','31014'])) & (p10['C2'] == '0') & (p10['C3'] == '000')]['population'].astype(float).sum
print(f' city total (31010): {city:,.0f}')
print(f' 자치구 합: {districts:,.0f}')
print(f' diff: {city - districts:.0f}')

# Same for 청주
print('\n=== Pop integrity: 청주시 자치구 sum vs city total ===')
city = p10[(p10['C1'] == '33010') & (p10['C2'] == '0') & (p10['C3'] == '000')]['population'].astype(float).sum
districts = p10[(p10['C1'].isin(['33011','33012'])) & (p10['C2'] == '0') & (p10['C3'] == '000')]['population'].astype(float).sum
print(f' city total (33010): {city:,.0f}')
print(f' 자치구 합: {districts:,.0f}')
print(f' diff: {city - districts:.0f}')
