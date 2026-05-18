"""Read 5-year age code mapping from KOSTAT 파일설계서 codebook."""
import sys, io
import pandas as pd
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1997 codebook
cb_path = Path('0_raw/mortality_kostat/usrcnfrm/파일설계서(공공용)_사망원인통계_사망_연간자료_B형(제공)_1997(코드집포함).xlsx')
xl = pd.ExcelFile(cb_path)
print('Sheets:', xl.sheet_names)

for sname in xl.sheet_names:
 print(f'\n===== {sname} =====')
 s = xl.parse(sname, header=None, dtype=str)
 print('shape:', s.shape)
 # Print rows that mention 5세 or 연령
 text = s.fillna('').astype(str)
 for i, row in text.iterrows:
 joined = ' | '.join(row.values)
 if ('5세' in joined or '연령' in joined or 'age' in joined.lower) and i < 600:
 print(f' row {i}: {joined[:200]}')
