"""
Quick column / coding inspection for 2010 mortality CSV.
Run before main pipeline so we know exact age/sex code domains.
"""
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = '0_raw/mortality_kostat/사망사료 정리/2010_사망_연간자료_B형_20260410_98266.csv'

df = pd.read_csv(PATH, encoding='cp949', dtype=str)
print('shape:', df.shape)
print('---columns---')
for c in df.columns:
 print(' ', c)

print('---age 5yr code unique---')
print(sorted(df['사망연령5세단위코드'].dropna.unique))

print('---sex code unique---')
print(sorted(df['성별코드'].dropna.unique))

print('---104 code stats---')
codes = df['사망원인_104항목분류코드'].dropna
print(' unique n:', codes.nunique)
print(' null n:', df['사망원인_104항목분류코드'].isna.sum)
print(' sample:', sorted(codes.unique)[:25])
print(' 102 (suicide) count:', (codes == '102').sum)

print('---location---')
print(' sido nunique:', df['사망자주소행정구역시도코드'].nunique)
print(' sgg nunique:', df['사망자주소행정구역시군구코드'].nunique)
print(' sido na:', df['사망자주소행정구역시도코드'].isna.sum)
print(' sgg na:', df['사망자주소행정구역시군구코드'].isna.sum)
sido_vals = sorted(df['사망자주소행정구역시도코드'].dropna.unique)
print(' sido vals:', sido_vals)
sgg_sample = df['사망자주소행정구역시군구코드'].dropna.unique[:15]
print(' sgg sample:', list(sgg_sample))
