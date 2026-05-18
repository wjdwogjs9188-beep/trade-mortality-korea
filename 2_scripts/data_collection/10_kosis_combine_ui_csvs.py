"""KOSIS UI 분할 다운로드 4개 csv 병합 + 인코딩 변환.

입력: 0_raw/kosis_population/101_DT_1B040M5_*.csv (4개 분할, cp949 인코딩)
출력:
 0_raw/kosis_population/population_combined.csv (UTF-8, 합본)
 0_raw/kosis_population/population_combined.parquet (선택, 빠른 read)

KOSIS UI csv 구조:
 ["[A]행정구역(시군구)별", "행정구역(시군구)별", "[SBB]성별", "성별",
 "[YRE]연령별", "연령별", "시점", "주민등록연앙인구[명]"]
 → C1=행정구역코드, C1_NM=명칭, C2=성별코드, C2_NM=성별,
 C3=연령코드, C3_NM=연령, year, population
"""
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR

OUT_DIR = RAW_DIR / "kosis_population"

def load_one(path: Path) -> pd.DataFrame:
 """CP949 csv 읽기."""
 df = pd.read_csv(path, encoding="cp949", dtype=str)
 return df

def main:
 files = sorted(OUT_DIR.glob("101_DT_1B040M5_*.csv"))
 print(f"=== KOSIS UI 다운로드 합본 ===")
 print(f"발견된 파일: {len(files)}개")
 for f in files:
 print(f" {f.name} ({f.stat.st_size:,} bytes)")
 print

 if len(files) == 0:
 print("❌ 0_raw/kosis_population/101_DT_1B040M5_*.csv 없음")
 return

 parts = 
 for f in files:
 print(f"→ 읽는 중: {f.name}")
 df = load_one(f)
 print(f" shape: {df.shape}, 컬럼: {list(df.columns)}")
 parts.append(df)

 combined = pd.concat(parts, ignore_index=True)
 print(f"\n합본 shape: {combined.shape}")

 # 컬럼 표준화 — KOSIS UI csv 의 한글 컬럼명을 C1/C1_NM/C2/C2_NM/C3/C3_NM/year/population 으로
 cols = combined.columns.tolist
 print(f"\n원본 컬럼: {cols}")

 # KOSIS UI 표준 패턴 매핑
 rename_map = {}
 for c in cols:
 if "[A]" in c or "[" in c and "행정구역" in str(combined[c].iloc[0]) if len(combined) > 0 else False:
 rename_map[c] = "C1" # 코드
 elif "행정구역" in c and "[" not in c:
 rename_map[c] = "C1_NM"
 elif "[SBB]" in c:
 rename_map[c] = "C2"
 elif "성별" == c or c == "성별":
 rename_map[c] = "C2_NM"
 elif "[YRE]" in c:
 rename_map[c] = "C3"
 elif "연령별" == c:
 rename_map[c] = "C3_NM"
 elif "시점" in c:
 rename_map[c] = "year"
 elif "인구" in c or "주민등록" in c:
 rename_map[c] = "population"

 print(f"\n매핑 후보: {rename_map}")

 # 더 안정적인 방식: 컬럼 위치 기준 (KOSIS UI 표준 순서)
 if len(cols) == 8:
 positional = {cols[0]: "C1", cols[1]: "C1_NM",
 cols[2]: "C2", cols[3]: "C2_NM",
 cols[4]: "C3", cols[5]: "C3_NM",
 cols[6]: "year",
 cols[7]: "population"}
 combined = combined.rename(columns=positional)
 print(f"\n위치 기반 rename 적용. 컬럼: {list(combined.columns)}")

 # year 정리: "1993 년" → "1993"
 if "year" in combined.columns:
 combined["year"] = combined["year"].str.extract(r"(\d{4})")[0]

 # 검증
 print(f"\n=== 검증 ===")
 print(f"총 행수: {len(combined):,}")
 if "year" in combined.columns:
 print(f"연도 범위: {combined['year'].min} ~ {combined['year'].max}")
 print(f"연도 수: {combined['year'].nunique}")
 if "C1" in combined.columns:
 n_5digit = (combined["C1"].str.len == 5).sum
 n_2digit = (combined["C1"].str.len == 2).sum
 unique_c1 = combined["C1"].nunique
 unique_5dig = combined[combined["C1"].str.len == 5]["C1"].nunique
 print(f"unique C1: {unique_c1} (시군구 5자리: {unique_5dig}, 시도/전국 2자리: {n_2digit:,} 행)")
 if "C2" in combined.columns:
 print(f"unique C2 (성별): {combined['C2'].nunique} ({combined['C2'].unique})")
 if "C3" in combined.columns:
 print(f"unique C3 (연령): {combined['C3'].nunique}")

 # 저장 (UTF-8)
 out_csv = OUT_DIR / "population_combined.csv"
 combined.to_csv(out_csv, index=False, encoding="utf-8-sig")
 print(f"\n✅ 합본 저장 (UTF-8): {out_csv}")
 print(f" size: {out_csv.stat.st_size:,} bytes")

 # parquet 옵션 (빠른 read)
 try:
 out_pq = OUT_DIR / "population_combined.parquet"
 combined.to_parquet(out_pq, index=False)
 print(f"✅ Parquet 저장: {out_pq}")
 except Exception as e:
 print(f"⚠️ parquet 저장 실패 (선택): {e}")

if __name__ == "__main__":
 main
