"""ECOS 132Y001 / 132Y003 — 0 행 반환 원인 진단.

가설:
  1. cycle 또는 period 형식 문제
  2. item wildcard '?' 가 이 table 에선 안 먹힘
  3. 페이지네이션 쪽 이슈
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.ecos_api import list_items, fetch_page
import pandas as pd


def debug_table(stat_code: str):
    print(f"\n{'#' * 60}")
    print(f"# {stat_code}")
    print(f"{'#' * 60}\n")

    print("--- ITEM 목록 (LV1, 처음 30개) ---")
    try:
        items = list_items(stat_code)
        print(f"총 {len(items)} items")
        if not items.empty:
            cols = [c for c in ["ITEM_CODE", "ITEM_NAME", "CYCLE",
                                 "DATA_START", "DATA_END", "ITEM_LEVEL", "POS_NO"]
                    if c in items.columns]
            print(items[cols].head(30).to_string(index=False))
    except Exception as e:
        print(f"❌ list_items 실패: {e}")
        return

    # 다양한 cycle/period 시도
    print(f"\n--- 다양한 fetch 시도 ---")
    test_cases = [
        ("Q", "200801", "200804"),  # 2008 Q1 ~ Q4
        ("Q", "200804", "200804"),  # 2008 Q4 단일
        ("Q", "201501", "201504"),  # 2015 Q1~Q4
        ("Q", "201801", "202404"),  # 늦은 시작
        ("M", "200801", "200812"),  # cycle M 시도
        ("A", "2008", "2024"),      # cycle A 시도
    ]
    for cycle, start, end in test_cases:
        try:
            data = fetch_page(
                "StatisticSearch",
                "1", "100",
                stat_code, cycle, start, end,
                "?", "?", "?", "?",
            )
            body = data.get("StatisticSearch", {})
            rows = body.get("row", [])
            total = body.get("list_total_count", 0)
            print(f"  cycle={cycle}, {start}~{end}: rows={len(rows)}, total={total}")
            if rows:
                print(f"    sample keys: {list(rows[0].keys())[:10]}")
                print(f"    sample row: {rows[0]}")
                break
        except Exception as e:
            print(f"  cycle={cycle}, {start}~{end}: ❌ {str(e)[:100]}")


if __name__ == "__main__":
    for code in ["132Y001", "132Y003"]:
        debug_table(code)
