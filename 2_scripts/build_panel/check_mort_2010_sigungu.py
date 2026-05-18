"""Check raw sigungu codes in 2010 mortality vs crosswalk."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

df = pd.read_csv('0_raw/mortality_kostat/사망사료 정리/2010_사망_연간자료_B형_20260410_98266.csv',
 encoding='cp949', dtype=str)

# Build raw_code = sido + sgg.zfill(3)
sido = df['사망자주소행정구역시도코드'].str.zfill(2)
sgg = df['사망자주소행정구역시군구코드'].str.zfill(3)
df['raw_code'] = sido + sgg

uniq = df.drop_duplicates('raw_code')[['raw_code']]
print('mortality unique raw_codes 2010:', len(uniq))

xw = pd.read_csv('1_codebooks/sigungu_crosswalk.csv', dtype=str)
xw_2010 = xw[xw['year'] == '2010']
xw_codes = set(xw_2010['raw_code'].unique)

mort_codes = set(uniq['raw_code'])
not_in_xw = sorted(mort_codes - xw_codes)
print('mortality codes NOT in crosswalk:', len(not_in_xw))
for c in not_in_xw:
 cnt = (df['raw_code'] == c).sum
 print(f' {c} n={cnt}')

# Match rate
matched = sum(1 for c in mort_codes if c in xw_codes)
print(f'\nMatch rate (unique codes): {matched}/{len(mort_codes)} = {matched/len(mort_codes)*100:.1f}%')

# Row-level match
df['matched'] = df['raw_code'].isin(xw_codes)
print(f'Row-level match rate: {df["matched"].sum}/{len(df)} = {df["matched"].mean*100:.2f}%')
