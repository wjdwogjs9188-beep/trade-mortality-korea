"""How crosswalk handles 수원시 etc. for 2010."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

xw = pd.read_csv('1_codebooks/sigungu_crosswalk.csv', dtype=str)
xw_2010 = xw[xw['year'] == '2010']
print('2010 crosswalk rows:', len(xw_2010))
print('2010 unique h_codes:', xw_2010['h_code'].nunique())
print('2010 unique raw_codes:', xw_2010['raw_code'].nunique())

# look at 수원시 entries
swn = xw_2010[xw_2010['h_name'].str.contains('수원', na=False)]
print('\n수원시 entries in 2010 crosswalk:')
print(swn[['year','raw_code','h_code','h_name','sido_name']].to_string())

# 청주시
cju = xw_2010[xw_2010['h_name'].str.contains('청주', na=False)]
print('\n청주시 entries in 2010 crosswalk:')
print(cju[['year','raw_code','h_code','h_name','sido_name']].to_string())

# Check raw_codes structure
print('\nraw_code format (2010):')
print('  length distrib:', xw_2010['raw_code'].str.len().value_counts())
print('  sample raw_codes:', sorted(xw_2010['raw_code'].unique())[:15])

# Check 2023
xw_2023 = xw[xw['year'] == '2023']
print('\n2023 raw_code length distrib:', xw_2023['raw_code'].str.len().value_counts())
print('2023 raw_code sample:', sorted(xw_2023['raw_code'].unique())[:10])
