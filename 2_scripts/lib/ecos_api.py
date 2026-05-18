"""한국은행 ECOS Open API 클라이언트.

API spec: https://ecos.bok.or.kr/api/

Endpoints:
 StatisticTableList: 통계표 목록
 StatisticItemList: 통계표내 항목 목록
 StatisticSearch: 통계 데이터 조회
 KeyStatisticList: 100대 통계지표
"""
from __future__ import annotations
from typing import Iterator
import time
from urllib.parse import quote
import requests
import pandas as pd

from.config import ECOS_API_KEY, assert_api_key

BASE_URL = "https://ecos.bok.or.kr/api"
# free tier: 1초당 10건, 1일 10,000건
DEFAULT_DELAY = 0.15

def _build_url(service: str, *parts: str) -> str:
 """ECOS URL 조립. 한글 파라미터는 quote 필요."""
 encoded = "/".join(quote(str(p), safe="") for p in parts)
 return f"{BASE_URL}/{service}/{ECOS_API_KEY}/json/kr/{encoded}"

def fetch_page(service: str, *parts: str, retries: int = 3) -> dict:
 """단일 페이지 fetch. 실패 시 retry."""
 url = _build_url(service, *parts)
 for attempt in range(retries):
 try:
 r = requests.get(url, timeout=30)
 r.raise_for_status
 data = r.json
 return data
 except (requests.exceptions.RequestException, ValueError) as e:
 if attempt < retries - 1:
 time.sleep(2 ** attempt)
 continue
 raise RuntimeError(f"ECOS fetch fail: {url[:120]}\n {e}")
 return {}

def list_tables(start: int = 1, end: int = 1000) -> pd.DataFrame:
 """전체 통계표 목록 조회."""
 assert_api_key("ECOS", ECOS_API_KEY)
 data = fetch_page("StatisticTableList", str(start), str(end))
 body = data.get("StatisticTableList", {})
 rows = body.get("row",)
 if not rows:
 err = data.get("RESULT", {})
 raise RuntimeError(f"ECOS 응답 없음: {err}")
 return pd.DataFrame(rows)

def list_items(stat_code: str, start: int = 1, end: int = 10000) -> pd.DataFrame:
 """특정 통계표의 항목 목록."""
 assert_api_key("ECOS", ECOS_API_KEY)
 data = fetch_page("StatisticItemList", str(start), str(end), stat_code)
 body = data.get("StatisticItemList", {})
 rows = body.get("row",)
 return pd.DataFrame(rows)

def search_statistic(
 stat_code: str,
 cycle: str, # "A" 연 / "Q" 분기 / "M" 월 / "D" 일
 start_period: str, # 분기: 200801, 월: 200801, 연: 2008
 end_period: str,
 item1: str = "?",
 item2: str = "?",
 item3: str = "?",
 item4: str = "?",
 rows_per_page: int = 100000,
) -> pd.DataFrame:
 """통계 데이터 조회. 페이지네이션 자동 처리.

 item* = "?" 면 와일드카드 (전체).
 """
 assert_api_key("ECOS", ECOS_API_KEY)
 all_rows = 
 start_idx = 1
 while True:
 end_idx = start_idx + rows_per_page - 1
 data = fetch_page(
 "StatisticSearch",
 str(start_idx), str(end_idx),
 stat_code, cycle, start_period, end_period,
 item1, item2, item3, item4,
)
 body = data.get("StatisticSearch", {})
 rows = body.get("row",)
 if not rows:
 break
 all_rows.extend(rows)
 list_total = int(body.get("list_total_count", 0))
 if start_idx + len(rows) > list_total:
 break
 start_idx += rows_per_page
 time.sleep(DEFAULT_DELAY)
 if not all_rows:
 return pd.DataFrame
 df = pd.DataFrame(all_rows)
 # 표준 변환
 if "DATA_VALUE" in df.columns:
 df["DATA_VALUE"] = pd.to_numeric(df["DATA_VALUE"], errors="coerce")
 return df

def search_table_by_keyword(keyword: str) -> pd.DataFrame:
 """통계표 이름·코드에 keyword 포함된 표 검색."""
 tables = list_tables
 mask = (
 tables["STAT_NAME"].str.contains(keyword, na=False, regex=False)
 | tables["STAT_CODE"].str.contains(keyword, na=False, regex=False)
)
 return tables[mask].reset_index(drop=True)
