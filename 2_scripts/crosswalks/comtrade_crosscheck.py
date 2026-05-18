"""Cross-check ksic2_to_hs6 mapping cover against actual Comtrade KR-CN data."""
import sys, io
from pathlib import Path
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

XW_DIR = Path('C:/Users/82103/Desktop/뉴 논문/crosswalks')
MAP = pd.read_csv(XW_DIR / 'ksic2_to_hs6.csv', dtype={'hs6': str})

# Test files: 2010 (KR exp & imp) covers a typical mid-period year
F_EXP = Path('0_raw/comtrade_korea_china/KR_exp_to_CN_2010.csv')
F_IMP = Path('0_raw/comtrade_korea_china/KR_imp_from_CN_2010.csv')

mapped_set = set(MAP['hs6'].unique())
print(f'Mapping table: {len(mapped_set):,} unique HS6')

for label, path in [('KR_exp_2010', F_EXP), ('KR_imp_2010', F_IMP)]:
    if not path.exists():
        print(f'\n[{label}] file missing: {path}')
        continue
    df = pd.read_csv(path, dtype=str)
    print(f'\n=== {label} ===')
    print('  shape:', df.shape)
    print('  cols sample:', df.columns.tolist()[:10])

    # Find HS6 column candidate
    hs_col = None
    for c in ['cmdCode', 'CmdCode', 'cmdcode', 'commodityCode', 'HS6']:
        if c in df.columns:
            hs_col = c
            break
    if not hs_col:
        # try to find by content (6-digit numerics)
        for c in df.columns:
            try:
                sample = df[c].dropna().astype(str).head(20)
                if all(s.isdigit() and 4 <= len(s) <= 6 for s in sample):
                    hs_col = c
                    break
            except Exception:
                pass
    print(f'  HS6 column: {hs_col}')
    if hs_col is None:
        continue

    hs_vals = df[hs_col].dropna().astype(str).str.zfill(6)
    uniq = hs_vals.unique()
    print(f'  unique HS6: {len(uniq)}')
    print(f'  hs6 length distrib: {pd.Series(uniq).str.len().value_counts().to_dict()}')

    matched = sum(1 for h in uniq if h in mapped_set)
    print(f'  cover (unique HS6): {matched}/{len(uniq)} = {matched/len(uniq)*100:.2f}%')

    # value-weighted cover (if value column present)
    val_col = None
    for c in ['primaryValue', 'TradeValue', 'tradeValue', 'value', 'Value']:
        if c in df.columns:
            val_col = c
            break
    if val_col:
        df['_v'] = pd.to_numeric(df[val_col], errors='coerce')
        df['_hs6'] = df[hs_col].astype(str).str.zfill(6)
        df['_matched'] = df['_hs6'].isin(mapped_set)
        tot = df['_v'].sum()
        mtot = df.loc[df['_matched'], '_v'].sum()
        print(f'  value cover: ${mtot:,.0f} / ${tot:,.0f} = {mtot/tot*100:.2f}%')

    # show unmatched HS6 sample
    miss = [h for h in uniq if h not in mapped_set][:15]
    print(f'  unmatched sample (first 15):', miss)
