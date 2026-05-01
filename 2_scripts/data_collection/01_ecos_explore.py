"""ECOS 가계대출 연체율 STAT_CODE 탐색.

기존 파일 (bok_household_연체율.csv) 은 STAT_CODE=141Y005 = 예금은행 지역별 연체율이지만
컬럼이 R4AB00 = 기업대출 연체율(전체1M) 임. 가계대출 연체율 X.

이 스크립트는:
1. ECOS에서 "연체율" / "가계" / "지역" 키워드로 통계표 검색
2. 후보 STAT_CODE 의 ITEM 목록 출력
3. 사용자가 적절한 STAT_CODE + ITEM 조합 결정 가능
"""
import sys
from pathlib import Path

# Add parent to path so we can import lib
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.ecos_api import search_table_by_keyword, list_items
import pandas as pd


def main():
    # 1. "연체" 포함 통계표
    print("\n" + "=" * 70)
    print("(1) '연체' 포함 통계표")
    print("=" * 70)
    df1 = search_table_by_keyword("연체")
    print(f"총 {len(df1)} 개")
    print(df1[["STAT_CODE", "STAT_NAME", "CYCLE"]].to_string(index=False))

    # 2. "가계대출" + "지역"
    print("\n" + "=" * 70)
    print("(2) '가계대출' 포함 통계표")
    print("=" * 70)
    df2 = search_table_by_keyword("가계대출")
    print(f"총 {len(df2)} 개")
    print(df2[["STAT_CODE", "STAT_NAME", "CYCLE"]].head(30).to_string(index=False))

    print("\n" + "=" * 70)
    print("(3) '지역별' 포함 통계표")
    print("=" * 70)
    df3 = search_table_by_keyword("지역별")
    print(f"총 {len(df3)} 개")
    print(df3[["STAT_CODE", "STAT_NAME", "CYCLE"]].head(30).to_string(index=False))

    # 4. 기존 사용 STAT_CODE = 141Y005 의 ITEM 확인 (가계대출 ITEM이 있는지)
    print("\n" + "=" * 70)
    print("(4) 141Y005 = 예금은행 지역별 연체율 — ITEM 목록")
    print("=" * 70)
    items = list_items("141Y005")
    if not items.empty:
        print(items[["ITEM_CODE", "ITEM_NAME", "CYCLE"]].head(40).to_string(index=False))
    else:
        print("(ITEM 없음)")


if __name__ == "__main__":
    main()
