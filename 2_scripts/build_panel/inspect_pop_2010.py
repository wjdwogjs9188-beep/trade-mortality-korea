"""Inspect KOSIS population panel for 2010 (sigungu codes, 9 city totals)."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pop = pd.read_csv('0_raw/kosis_population/population_combined.csv', dtype=str)
print('shape:', pop.shape)
print('years:', sorted(pop['year'].unique)[:5], '...', sorted(pop['year'].unique)[-3:])

p2010 = pop[pop['year'] == '2010']
print('2010 rows:', len(p2010))
print('2010 C1 unique n:', p2010['C1'].nunique)

c1_vals = p2010['C1'].unique
five_digit = [c for c in c1_vals if len(c) == 5]
print('5-digit n:', len(five_digit))

# city totals: 5-digit codes ending '00' that should be excluded
city_totals = sorted([c for c in five_digit if c.endswith('00')])
print('city total candidates (ending 00):', city_totals)

# C2 sex
print('C2 (sex):')
print(p2010[['C2','C2_NM']].drop_duplicates.values.tolist)

# C3 age bins
print('C3 (age) bins:')
print(p2010[['C3','C3_NM']].drop_duplicates.sort_values('C3').values.tolist)
