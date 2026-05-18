"""UN Comtrade Plus API v1 클라이언트.

API spec: https://comtradeplus.un.org/docs/list-of-references-parameter-codes/

Endpoints:
 /data/v1/get/{typeCode}/{freqCode}/{clCode} 실시간 query
 /data/v1/getMBS/... metadata 조회

Authentication:
 Header: Ocp-Apim-Subscription-Key: <key>
 또는 query param: subscription-key=<key>

Free tier (사용자 등록 후):
 - per call: 최대 100,000 records
 - rate: 10 calls/second
 - daily: ~1,000 calls
"""
from __future__ import annotations
from typing import Iterator
import time
import requests
import pandas as pd

from.config import (COMTRADE_API_KEY, COMTRADE_API_KEY_SECONDARY,
 COMTRADE_KEYS, assert_api_key)

BASE_URL = "https://comtradeapi.un.org/data/v1/get"
DEFAULT_DELAY = 0.15 # ~6 calls/second 안전 마진

# M49 country codes (ADH 표준 8 + Korea + China + 미국 등)
M49 = {
 "AU": 36, # Australia
 "DK": 208, # Denmark
 "FI": 246, # Finland
 "DE": 276, # Germany
 "JP": 392, # Japan
 "NZ": 554, # New Zealand
 "ES": 724, # Spain
 "CH": 757, # Switzerland (757)
 "KR": 410, # South Korea
 "CN": 156, # China
 "US": 842, # United States
 "GB": 826, # United Kingdom
 "FR": 250, # France
 "IT": 380, # Italy
 "CA": 124, # Canada
}

ADH_8 = ["AU", "DK", "FI", "DE", "JP", "NZ", "ES", "CH"]

def get_key(key_index: int = 0) -> str:
 """N-way 로테이션 — key_index를 모듈로 처리해 사용 가능한 키 반환.

 예: 키 4개 등록되어 있으면 0,1,2,3,0,1,2,3,... 순환.
 """
 if not COMTRADE_KEYS:
 raise RuntimeError("Comtrade API key 가.env 에 없습니다.")
 return COMTRADE_KEYS[key_index % len(COMTRADE_KEYS)]

def fetch(
 type_code: str = "C", # C=commodities
 freq_code: str = "A", # A=annual
 cl_code: str = "HS",
 reporter_code: str = "", # M49 (cs)
 period: str = "", # 2020 or 202003
 partner_code: str = "",
 cmd_code: str = "AG6", # AG6 = HS6 detail
 flow_code: str = "", # M=import X=export
 use_secondary: bool = False,
 key_index: int | None = None, # 명시적 인덱스 (None 이면 use_secondary 호환 동작)
 timeout: int = 60,
 retries: int = 3,
) -> pd.DataFrame:
 """단일 API call → DataFrame.

 키 선택:
 - key_index 지정: COMTRADE_KEYS[key_index % len] 사용 (4-way 로테이션)
 - key_index None + use_secondary=False: COMTRADE_API_KEY (primary)
 - key_index None + use_secondary=True: COMTRADE_API_KEY_SECONDARY
 """
 if key_index is not None:
 key = get_key(key_index)
 else:
 key = COMTRADE_API_KEY_SECONDARY if use_secondary else COMTRADE_API_KEY
 assert_api_key("Comtrade", key)

 url = f"{BASE_URL}/{type_code}/{freq_code}/{cl_code}"
 params = {"subscription-key": key}
 if reporter_code: params["reporterCode"] = reporter_code
 if period: params["period"] = period
 if partner_code: params["partnerCode"] = partner_code
 if cmd_code: params["cmdCode"] = cmd_code
 if flow_code: params["flowCode"] = flow_code

 last_exc = None
 for attempt in range(retries):
 try:
 r = requests.get(url, params=params, timeout=timeout)
 if r.status_code == 401:
 raise RuntimeError(f"Comtrade 401 — API key 확인. {r.text[:200]}")
 if r.status_code == 429:
 # rate limit
 wait = (attempt + 1) * 5
 print(f" rate limit hit; sleep {wait}s")
 time.sleep(wait)
 continue
 r.raise_for_status
 data = r.json
 rows = data.get("data") or 
 if not rows:
 return pd.DataFrame
 df = pd.DataFrame(rows)
 df["_query_url"] = r.url
 return df
 except requests.exceptions.RequestException as e:
 last_exc = e
 time.sleep(2 ** attempt)
 raise RuntimeError(f"Comtrade fetch fail after {retries} retries: {last_exc}")

def fetch_country_year(reporter: str, partner: str, year: int, flow: str) -> pd.DataFrame:
 """특정 국가-연도-방향 fetch (HS6 전체)."""
 return fetch(
 reporter_code=str(M49[reporter]),
 partner_code=str(M49[partner]),
 period=str(year),
 flow_code=flow,
 cmd_code="AG6",
)

def fetch_adh_china_imports(years: list[int]) -> Iterator[tuple[str, int, pd.DataFrame]]:
 """ADH 8 국가 × 연도 China imports HS6.

 Yields (reporter_iso2, year, df).
 """
 for reporter in ADH_8:
 for year in years:
 df = fetch_country_year(reporter, "CN", year, "M")
 yield reporter, year, df
 time.sleep(DEFAULT_DELAY)

def fetch_korea_china_bilateral(years: list[int]) -> Iterator[tuple[str, int, pd.DataFrame]]:
 """Korea-China 양자 무역 HS6 (양방향)."""
 for year in years:
 df_imp = fetch_country_year("KR", "CN", year, "M") # Korea imports from China
 yield "KR_imp_from_CN", year, df_imp
 time.sleep(DEFAULT_DELAY)
 df_exp = fetch_country_year("KR", "CN", year, "X") # Korea exports to China
 yield "KR_exp_to_CN", year, df_exp
 time.sleep(DEFAULT_DELAY)

def fetch_china_world_exports(years: list[int]) -> Iterator[tuple[int, pd.DataFrame]]:
 """China → World HS6 export (alternative IV)."""
 for year in years:
 df = fetch(
 reporter_code=str(M49["CN"]),
 partner_code="0", # 0 = World
 period=str(year),
 flow_code="X",
 cmd_code="AG6",
)
 yield year, df
 time.sleep(DEFAULT_DELAY)
