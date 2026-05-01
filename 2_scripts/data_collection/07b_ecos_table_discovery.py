"""ECOS 통계표 ID 진단 — empty 였던 5개에 대해 keyword 검색으로 후보 찾기.

empty 였던 통계표:
  - 200Y003: GRDP (지역내총생산)
  - 132Y001: 산업별대출금 전산업
  - 132Y003: 산업별대출금 용도별
  - 731Y001: 환율
  - 036Y002: 통화량 M1M2Lf

이 스크립트가 ECOS에 keyword 검색해서 정확한 STAT_CODE 후보 보여줌.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.ecos_api import search_table_by_keyword


KEYWORDS = [
    "GRDP",
    "지역내총생산",
    "환율",
    "통화",
    "M1",
    "M2",
    "본원통화",
    "산업별대출",
    "산업별 대출",
    "예금은행 산업",
]


def main():
    for kw in KEYWORDS:
        print(f"\n{'=' * 60}")
        print(f"  '{kw}' 포함 통계표")
        print(f"{'=' * 60}")
        try:
            df = search_table_by_keyword(kw)
        except Exception as e:
            print(f"  ❌ 에러: {e}")
            continue
        if df.empty:
            print("  (결과 없음)")
            continue
        cols = [c for c in ["STAT_CODE", "STAT_NAME", "CYCLE",
                             "SRCH_YN", "DATA_END", "DATA_START"]
                if c in df.columns]
        print(df[cols].head(15).to_string(index=False))


if __name__ == "__main__":
    main()
