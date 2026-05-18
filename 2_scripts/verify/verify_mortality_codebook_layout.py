"""사망 microdata 시점별 파일설계서 xlsx 의 column layout 추출.

11a (position-based parse) 가 fail 시 fallback — 코드집 xlsx 의 정확 column
position + 길이 + 코드 정의를 가져와서 시점별 COL_POS dict build 위함.

대상 xlsx (사용자 폴더 내):
 파일설계서(공공용)_사망원인통계_사망_연간자료_B형(제공)_1997(코드집포함).xlsx
... 1998 ~ 2024
 파일설계서_(공공용)1997_1999년_사망원인통계_B형.xlsx
 파일설계서_(공공용)2010_2017년_인구동향(사망)_B형 (2).xlsx

산출 (stdout):
 - 각 xlsx 의 sheet list
 - 각 sheet 의 항목정보 (항목번호, 항목명, 시작컬럼, 길이) 추출
 - 7 시점 (1997, 2000, 2005, 2008, 2010, 2017, 2024) sample 비교

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\verify\\verify_mortality_codebook_layout.py
"""
from __future__ import annotations
import sys
import re
from pathlib import Path
import pandas as pd

CODEBOOK_DIR = Path(r"C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리")

# 7 시점 sample (1997-2024 변화 capture 위해)
SAMPLE_YEARS = [1997, 2000, 2005, 2008, 2010, 2017, 2024]

# 우리가 알아내야 할 항목 (시점별 column position 매핑 build 용)
TARGET_COLUMNS = [
 ("year", ["연도"]),
 ("sido", ["주소행정구역시도", "주소지행정구역시도", "시도코드"]),
 ("sigungu", ["주소행정구역시군구", "주소지행정구역시군구", "시군구코드"]),
 ("sex", ["성별코드", "성별"]),
 ("age_5y", ["연령5세", "사망연령"]),
 ("marital", ["혼인상태"]),
 ("education", ["교육정도"]),
 ("national", ["국적구분"]),
 ("cause_104", ["104항목"]),
]

def find_codebook_for_year(year: int) -> Path | None:
 """시점별 파일설계서 xlsx 찾기."""
 candidates = [
 f"파일설계서(공공용)_사망원인통계_사망_연간자료_B형(제공)_{year}(코드집포함).xlsx",
 f"파일설계서(공공용)_사망원인통계_사망연간자료B형(제공)_{year}(코드집포함).xlsx",
 f"파일설계서(공공용)_사망원인통계_사망_연간자료_B형(제공)_{year}.xlsx",
 ]
 for name in candidates:
 p = CODEBOOK_DIR / name
 if p.exists:
 return p

 # 일반 검색
 for p in CODEBOOK_DIR.glob(f"*{year}*.xlsx"):
 if "파일설계서" in p.name and "코드집" in p.name:
 return p
 return None

def extract_columns_from_codebook(xlsx_path: Path) -> dict:
 """파일설계서 xlsx 의 sheet 들에서 항목 layout + code 정의 추출.

 sheet 구조 (KOSIS 표준 가정):
 - "총괄" or "항목정보": 항목번호, 항목명, 길이, 타입, 시작컬럼
 - "코드정보": 항목번호, 항목명, 코드, 코드의미
 """
 print(f"\n{'='*70}")
 print(f"FILE: {xlsx_path.name}")
 print(f"{'='*70}")

 try:
 xl = pd.ExcelFile(xlsx_path)
 except Exception as e:
 print(f" [FL] {type(e).__name__}: {e}")
 return {}

 print(f" sheets: {xl.sheet_names}")
 out = {"file": xlsx_path.name, "sheets": {}}

 for sheet in xl.sheet_names:
 try:
 df = pd.read_excel(xlsx_path, sheet_name=sheet, dtype=str, header=None)
 except Exception as e:
 print(f" [skip sheet '{sheet}'] {e}")
 continue

 print(f"\n [sheet '{sheet}'] shape={df.shape}")

 # 항목정보 sheet 인 경우 전체 출력 + target column position search
 if "항목" in sheet or "총괄" in sheet:
 # head 100 row (대부분 항목 다 봄)
 print(df.head(100).to_string(max_cols=8, max_colwidth=30))

 # Target column position search
 print(f"\n >>> Target column position search:")
 for target_name, keywords in TARGET_COLUMNS:
 for col in df.columns:
 col_str = df[col].astype(str)
 for kw in keywords:
 mask = col_str.str.contains(kw, na=False, regex=False)
 if mask.any:
 for idx in df.index[mask][:2]:
 row_vals = df.iloc[idx].tolist
 # 항목번호 / 항목명 / 길이 / 시작컬럼 등 출력
 print(f" {target_name} ({kw}): row {idx} → "
 f"{[str(v)[:25] for v in row_vals[:7]]}")
 break
 elif "코드정보" in sheet or "코드" in sheet:
 # 코드 정의 sheet — 항목번호, 항목명, 코드, 의미
 print(df.head(50).to_string(max_cols=5, max_colwidth=30))

 return out

def main -> int:
 print("=" * 70)
 print("사망 microdata 파일설계서 xlsx 시점별 column layout 추출")
 print("=" * 70)
 print(f" search dir: {CODEBOOK_DIR}")
 print(f" sample years: {SAMPLE_YEARS}")

 for year in SAMPLE_YEARS:
 xlsx_path = find_codebook_for_year(year)
 if xlsx_path is None:
 print(f"\n[SKIP {year}] codebook xlsx not found")
 continue
 extract_columns_from_codebook(xlsx_path)

 print("\n" + "=" * 70)
 print("완료. 다음:")
 print(" - 위 결과 paste → 11a 의 COL_POS dict 시점별 update")
 print(" - 또는 11a 가 정상이면 codebook fallback 불필요")
 print("=" * 70)
 return 0

if __name__ == "__main__":
 sys.exit(main)
