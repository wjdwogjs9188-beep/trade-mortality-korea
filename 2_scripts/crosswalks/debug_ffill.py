"""Debug ffill: which rows end up with lvl3 NaN, and whether ffill bleeds across lvl1."""
import sys, io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

F_KS = 'C:/Users/82103/Desktop/뉴 논문/crosswalks/60대산업-표준산업분류_V2.xlsx'
ks = pd.read_excel(F_KS, sheet_name='연계표', dtype=str)

print('=== BEFORE ffill ===')
print(ks[['1레벨','2레벨','3레벨','표준산업분류 10차']].head(60).to_string)

print('\n=== AFTER simple ffill ===')
ks_f = ks.copy
for c in ['1레벨','2레벨','3레벨']:
 ks_f[c] = ks_f[c].ffill
print(ks_f[['1레벨','2레벨','3레벨','표준산업분류 10차']].head(60).to_string)

print('\n=== Rows where lvl3 is NaN even after ffill ===')
nan3 = ks_f[ks_f['3레벨'].isna]
print(nan3[['1레벨','2레벨','3레벨','표준산업분류 10차']].to_string)

print('\n=== Rows 50-60 detail (ffilled) ===')
print(ks_f.iloc[50:60][['1레벨','2레벨','3레벨','표준산업분류 10차']].to_string)
