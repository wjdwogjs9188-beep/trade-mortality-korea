"""Check whether pop has 수원시 자치구 in 2010."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pop = pd.read_csv('0_raw/kosis_population/population_combined.csv', dtype=str)
p10 = pop[pop['year'] == '2010']

# 31xxx codes in 2010
gg_codes = sorted([c for c in p10['C1'].unique if len(c) == 5 and c.startswith('31')])
print('Gyeonggi (31xxx) 5-digit codes in 2010 pop:')
for c in gg_codes:
 nm = p10[p10['C1'] == c]['C1_NM'].iloc[0]
 print(f' {c} {nm}')

# Check 33xxx 청주
print('\nChungbuk (33xxx) 5-digit codes in 2010 pop:')
for c in sorted([c for c in p10['C1'].unique if len(c) == 5 and c.startswith('33')]):
 nm = p10[p10['C1'] == c]['C1_NM'].iloc[0]
 print(f' {c} {nm}')

# also 38xxx 창원
print('\nGyeongnam (38xxx) 5-digit codes in 2010 pop:')
for c in sorted([c for c in p10['C1'].unique if len(c) == 5 and c.startswith('38')]):
 nm = p10[p10['C1'] == c]['C1_NM'].iloc[0]
 print(f' {c} {nm}')
