"""
ECOS StatisticItemList raw probe — 402Y014/401Y015/200Y110 의 실제 항목 구조.

명세서 row 16-29 의 출력값에 따라 컬럼:
 STAT_CODE, STAT_NAME, GRP_CODE, GRP_NAME, ITEM_CODE, ITEM_NAME, P_ITEM_CODE, P_ITEM_NAME, CYCLE,...
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import LOGS_DIR, ECOS_API_KEY, assert_api_key

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")

assert_api_key("ECOS", ECOS_API_KEY)
BASE = f"https://ecos.bok.or.kr/api/StatisticItemList/{ECOS_API_KEY}/json/kr"

def probe(stat: str):
 url = f"{BASE}/1/500/{stat}"
 print(f"\n{'='*72}")
 print(f" {stat} → {url[:100]}...")
 print('='*72)
 r = requests.get(url, timeout=30)
 r.raise_for_status
 data = r.json

 # 응답 최상위 key
 print(f"top keys: {list(data.keys)}")
 body = data.get("StatisticItemList", {})
 print(f" StatisticItemList keys: {list(body.keys) if isinstance(body, dict) else type(body)}")

 if "list_total_count" in body:
 print(f" list_total_count: {body['list_total_count']}")
 if "RESULT" in body:
 print(f" RESULT: {body['RESULT']}")

 rows = body.get("row",) if isinstance(body, dict) else 
 print(f" rows: {len(rows)}")

 # 모든 row 출력 (정상이라면 여러 항목)
 for i, row in enumerate(rows[:30]):
 keys_present = [k for k in ['GRP_CODE', 'GRP_NAME', 'ITEM_CODE', 'ITEM_NAME', 'P_ITEM_CODE', 'P_ITEM_NAME', 'CYCLE', 'START_TIME', 'END_TIME'] if k in row]
 info = " | ".join(f"{k}={str(row.get(k, ''))[:25]}" for k in keys_present)
 print(f" row {i}: {info}")
 if len(rows) > 30:
 print(f"... + {len(rows)-30} more rows")

for stat in ["200Y110", "402Y014", "401Y015"]:
 try:
 probe(stat)
 except Exception as e:
 print(f"\n[ERROR {stat}] {e}")

# 추가: 작동하는 GDP 의 StatisticSearch raw 첫 행도 보기 — 실제 ITEM_CODE1 어떻게 들어있는지
print(f"\n\n{'='*72}")
print(f" 200Y110 의 실제 데이터 첫 5행 (ITEM_CODE1 구조 확인)")
print('='*72)
search_url = f"https://ecos.bok.or.kr/api/StatisticSearch/{ECOS_API_KEY}/json/kr/1/5/200Y110/Q/2024Q1/2024Q4"
r = requests.get(search_url, timeout=30)
data = r.json
rows = data.get("StatisticSearch", {}).get("row",)
for i, row in enumerate(rows):
 print(f" row {i}: {json.dumps(row, ensure_ascii=False)[:200]}")
