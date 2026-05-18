"""Identify the 9 city-total sigungu codes by comparing pop vs crosswalk."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pop = pd.read_csv('0_raw/kosis_population/population_combined.csv', dtype=str)
xw = pd.read_csv('1_codebooks/sigungu_crosswalk.csv', dtype=str)

# 5-digit pop codes
pop_codes = set(c for c in pop['C1'].unique() if len(c) == 5)
xw_hcodes = set(xw['h_code'].unique())

# pop codes not in crosswalk
not_in_xw = sorted(pop_codes - xw_hcodes)
print('pop 5-digit codes NOT in crosswalk h_code:', len(not_in_xw))

# Check name for these
for c in not_in_xw:
    nm = pop[pop['C1'] == c]['C1_NM'].iloc[0]
    print(f'  {c}  {nm}')

# Conversely: codes in xw not in pop
not_in_pop = sorted(xw_hcodes - pop_codes)
print(f'\nh_codes in xw NOT in pop (n={len(not_in_pop)}):')
for c in not_in_pop[:20]:
    nm = xw[xw['h_code'] == c]['h_name'].iloc[0]
    print(f'  {c}  {nm}')
