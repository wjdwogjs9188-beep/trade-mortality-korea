"""ECOS 가계대출 연체율 panel 다운로드.

목표: 시도별 분기 가계대출 연체율 2008Q1 ~ 2024Q4

배경: 기존 bok_household_연체율.csv 는
- STAT_CODE 141Y005 = 예금은행 지역별 연체율 (기업+가계 통합)
- 그러나 ITEM_CODE R4AB00 = 기업대출 연체율 (가계 X)
- 2019.12 1개월치만 (109행)

이 스크립트는:
1. 141Y005 의 모든 ITEM 조회 → 가계대출 연체율 ITEM 식별
2. 후보 ITEM 모두 다운로드 (시도별 × 분기 × 2008-2024)
3. 0_raw/ecos_delinquency/ 에 저장

사용법 (Windows PowerShell):
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\02_ecos_household_delinquency.py
"""
import sys
import time
from pathlib import Path
import pandas as pd

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve.parents[1]))

from lib.ecos_api import (
 list_items, search_statistic, search_table_by_keyword
)
from lib.config import RAW_DIR, LOGS_DIR

OUT_DIR = RAW_DIR / "ecos_delinquency"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------
# Step 1: 후보 통계표 검색
# ----------------------------------------------------------------
def explore -> pd.DataFrame:
 """가계대출 연체율 관련 통계표 후보 목록."""
 candidates = 
 for keyword in ["연체", "가계대출", "지역별 가계", "지역별 예금은행"]:
 df = search_table_by_keyword(keyword)
 df["search_keyword"] = keyword
 candidates.append(df)
 all_tables = pd.concat(candidates, ignore_index=True).drop_duplicates("STAT_CODE")
 return all_tables

# ----------------------------------------------------------------
# Step 2: 특정 STAT_CODE 의 ITEM 출력 → 가계대출 연체율 항목 식별
# ----------------------------------------------------------------
def list_relevant_items(stat_code: str = "141Y005") -> pd.DataFrame:
 """주어진 통계표의 ITEM 중 가계 관련 후보."""
 items = list_items(stat_code)
 if items.empty:
 print(f"⚠️ {stat_code}: ITEM 없음")
 return items
 items.to_csv(OUT_DIR / f"items_{stat_code}.csv", index=False, encoding="utf-8-sig")
 # "가계" / "household" / "주택" 포함 ITEM
 if "ITEM_NAME" in items.columns:
 gachae = items[
 items["ITEM_NAME"].str.contains("가계|주택", na=False, regex=True)
 ]
 return gachae.reset_index(drop=True)
 return items

# ----------------------------------------------------------------
# Step 3: 다운로드
# ----------------------------------------------------------------
def download(
 stat_code: str,
 cycle: str = "M",
 start_period: str = "200801",
 end_period: str = "202412",
) -> pd.DataFrame:
 """ITEM 와일드카드로 통계표 전체 다운로드."""
 print(f"\n다운로드: {stat_code} {cycle} {start_period}-{end_period}")
 df = search_statistic(
 stat_code=stat_code,
 cycle=cycle,
 start_period=start_period,
 end_period=end_period,
 item1="?", item2="?", item3="?", item4="?",
)
 print(f" {len(df):,} 행 받음")
 if not df.empty:
 out = OUT_DIR / f"{stat_code}_{cycle}_{start_period}_{end_period}.csv"
 df.to_csv(out, index=False, encoding="utf-8-sig")
 print(f" → {out.name}")
 return df

def main:
 print("=" * 70)
 print("STEP 1: 후보 통계표 검색")
 print("=" * 70)
 cands = explore
 cands_path = OUT_DIR / "candidate_tables.csv"
 cands.to_csv(cands_path, index=False, encoding="utf-8-sig")
 cols = [c for c in ["STAT_CODE", "STAT_NAME", "CYCLE", "search_keyword"] if c in cands.columns]
 print(cands[cols].to_string(index=False))
 print(f"\n → 저장: {cands_path}")

 print("\n" + "=" * 70)
 print("STEP 2: 141Y005 (예금은행 지역별 연체율) ITEM 확인")
 print("=" * 70)
 items_141 = list_relevant_items("141Y005")
 if not items_141.empty:
 cols = [c for c in ["ITEM_CODE", "ITEM_NAME", "CYCLE"] if c in items_141.columns]
 print(items_141[cols].to_string(index=False))

 # 사용자가 후보 STAT_CODE 보고 결정 후 download 함수에 STAT_CODE 입력
 # 자동으로 가능한 후보 모두 다운로드:
 print("\n" + "=" * 70)
 print("STEP 3: 후보 통계표 모두 다운로드 (시간 오래 걸림)")
 print("=" * 70)
 targets = 
 for _, row in cands.iterrows:
 stat_code = row["STAT_CODE"]
 name = str(row.get("STAT_NAME", ""))
 # 가계 + 연체 + 지역 필터
 if any(kw in name for kw in ["가계", "지역별 연체"]):
 targets.append(stat_code)

 # 중복 제거
 targets = list(dict.fromkeys(targets))
 print(f"다운로드 대상 {len(targets)} 개:")
 for t in targets:
 print(f" - {t}")

 for stat_code in targets:
 try:
 df = download(stat_code)
 except Exception as e:
 print(f" ⚠️ {stat_code}: {e}")
 time.sleep(3)

if __name__ == "__main__":
 main
