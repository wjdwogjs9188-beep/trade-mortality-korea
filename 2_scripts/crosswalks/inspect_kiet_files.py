"""Inspect KIET 60-industry × HSCODE and 60-industry × KSIC mapping xlsx."""
import sys, io
from pathlib import Path
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

XW_DIR = Path('C:/Users/82103/Desktop/뉴 논문/crosswalks')
F_HS = XW_DIR / '60대산업-HSCODE.xlsx'
F_KS = XW_DIR / '60대산업-표준산업분류_V2.xlsx'

# --- HSCODE file ---
print('=' * 70)
print('60대산업-HSCODE.xlsx')
print('=' * 70)
xl = pd.ExcelFile(F_HS)
print('sheets:', xl.sheet_names)
df_hs = pd.read_excel(F_HS, sheet_name=xl.sheet_names[0], dtype=str)
print('shape:', df_hs.shape)
print('columns:', df_hs.columns.tolist)
print('---head---')
print(df_hs.head(5).to_string)
print('---hsc length distrib---')
print(df_hs['hsc'].dropna.str.len.value_counts.sort_index)
print('---hsc sample by length---')
for L in sorted(df_hs['hsc'].dropna.str.len.unique):
 sub = df_hs[df_hs['hsc'].str.len == L]['hsc'].head(5).tolist
 print(f' len={L}: {sub}')

# --- KSIC mapping file ---
print('\n' + '=' * 70)
print('60대산업-표준산업분류_V2.xlsx')
print('=' * 70)
xl2 = pd.ExcelFile(F_KS)
print('sheets:', xl2.sheet_names)

for s in xl2.sheet_names:
 print(f'\n--- sheet: {s} ---')
 d = pd.read_excel(F_KS, sheet_name=s, dtype=str)
 print('shape:', d.shape)
 print('columns:', d.columns.tolist)
 print(d.head(20).to_string)
