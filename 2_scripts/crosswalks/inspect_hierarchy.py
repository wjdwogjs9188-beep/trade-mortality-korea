"""Deeper inspection: hierarchy patterns, NaN rows, KSIC code patterns."""
import sys, io
from pathlib import Path
import pandas as pd
import re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

XW_DIR = Path('C:/Users/82103/Desktop/뉴 논문/crosswalks')
F_HS = XW_DIR / '60대산업-HSCODE.xlsx'
F_KS = XW_DIR / '60대산업-표준산업분류_V2.xlsx'

# --- HS file: how many rows have 3레벨 vs only higher ---
df_hs = pd.read_excel(F_HS, dtype=str)
print('HS rows:', len(df_hs))
print(' with 레벨3코드:', df_hs['레벨3코드'].notna.sum)
print(' with 레벨2코드 only (no 3):', ((df_hs['레벨3코드'].isna) & (df_hs['레벨2코드'].notna)).sum)
print(' with 레벨1코드 only (no 2/3):', ((df_hs['레벨3코드'].isna) & (df_hs['레벨2코드'].isna) & (df_hs['레벨1코드'].notna)).sum)
print(' with no level info at all:', df_hs[['레벨1코드','레벨2코드','레벨3코드']].isna.all(axis=1).sum)

# 레벨1 only by sector
print('\n레벨1 only — 레벨1코드 distribution:')
mask = (df_hs['레벨3코드'].isna) & (df_hs['레벨2코드'].isna) & (df_hs['레벨1코드'].notna)
print(df_hs.loc[mask, '레벨1코드'].value_counts)

# 레벨1 list
print('\nAll 레벨1코드 values:')
print(df_hs['레벨1코드'].dropna.unique)

# --- KSIC file deeper ---
print('\n' + '=' * 70)
print('연계표 — full content')
print('=' * 70)
ks = pd.read_excel(F_KS, sheet_name='연계표', dtype=str)
ks_filled = ks.copy
for c in ['1레벨', '2레벨', '3레벨']:
 ks_filled[c] = ks_filled[c].ffill
print(ks_filled.to_string)

# Extract KSIC2 patterns
print('\n--- KSIC10 sample tokens ---')
ksic_codes = ks['표준산업분류 10차'].dropna.head(40).tolist
for c in ksic_codes:
 m = re.match(r'^([A-Z])(\d*)\s+(.+)$', c)
 if m:
 letter, digits, name = m.groups
 ksic2 = int(digits[:2]) if len(digits) >= 2 else None
 print(f' {c} → letter={letter} digits={digits} ksic2={ksic2}')
 else:
 print(f' {c} → NO MATCH')
