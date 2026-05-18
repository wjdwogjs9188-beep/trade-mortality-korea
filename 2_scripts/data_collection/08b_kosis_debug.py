"""KOSIS API 응답 진단 — 어떤 형식으로 오는지 직접 확인."""
import sys
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import KOSIS_API_KEY

BASE_URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

def call(label: str, params: dict):
 print(f"\n{'#' * 70}")
 print(f"# {label}")
 print(f"{'#' * 70}")
 r = requests.get(BASE_URL, params=params, timeout=60)
 print(f"status: {r.status_code}")
 print(f"content-type: {r.headers.get('content-type', '?')}")
 print(f"size: {len(r.content)} bytes")
 print(f"raw first 800 chars:")
 print("─" * 70)
 print(r.text[:800])
 print("─" * 70)

# Case A: jsonVD 없음 (어제 수정 — fail 한 케이스)
call("Case A: jsonVD 없음, outputFields 없음", {
 "method": "getList",
 "apiKey": KOSIS_API_KEY,
 "itmId": "T10+",
 "objL1": "ALL",
 "objL2": "ALL",
 "objL3": "ALL",
 "format": "json",
 "prdSe": "Y",
 "startPrdDe": "2020",
 "endPrdDe": "2020",
 "orgId": "101",
 "tblId": "DT_1B040M5",
})

# Case B: jsonVD=N 명시
call("Case B: jsonVD=N 명시", {
 "method": "getList",
 "apiKey": KOSIS_API_KEY,
 "itmId": "T10+",
 "objL1": "ALL",
 "objL2": "ALL",
 "objL3": "ALL",
 "format": "json",
 "jsonVD": "N",
 "prdSe": "Y",
 "startPrdDe": "2020",
 "endPrdDe": "2020",
 "orgId": "101",
 "tblId": "DT_1B040M5",
})

# Case C: jsonVD=Y + 라벨 필드 명시
call("Case C: jsonVD=Y + outputFields(C1_NM C2_NM C3_NM PRD_DE DT)", {
 "method": "getList",
 "apiKey": KOSIS_API_KEY,
 "itmId": "T10+",
 "objL1": "ALL",
 "objL2": "ALL",
 "objL3": "ALL",
 "format": "json",
 "jsonVD": "Y",
 "prdSe": "Y",
 "startPrdDe": "2020",
 "endPrdDe": "2020",
 "orgId": "101",
 "tblId": "DT_1B040M5",
 "outputFields": "C1+C1_NM+C2+C2_NM+C3+C3_NM+ITM_NM+UNIT_NM+PRD_DE+",
})
