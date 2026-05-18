"""
KOSIS 시군구 지적통계 (DT_MLTM_2300) 다운로드 — 연도별 분할 호출.

KOSIS API 의 40,000셀 제한 우회: 연도별로 19번 호출 후 concat.

orgId = 116 (국토교통부 한국국토정보공사)
tblId = DT_MLTM_2300 (지적통계)
itmId = 13103874596T1, 13103874596T2 (두 가지 면적 지표)
prdSe = Y (연도)
range = 2007-2025

저장 경로:
 0_raw/modernization_controls/urbanization/kosis_sigungu_area_2007_2025.csv
"""

import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

API_KEY = os.environ.get("KOSIS_API_KEY", "MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=")
BASE_URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

OUTPUT_DIR = Path(r"C:\Users\82103\Downloads\trade_mortality_korea\0_raw\modernization_controls\urbanization")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "kosis_sigungu_area_2007_2025.csv"
YEAR_RANGE = range(2007, 2026) # 2007..2025

def build_url(year_start: int, year_end: int, sido_code: str = "ALL", itm: str = "13103874596T1+") -> str:
 params = {
 "method": "getList",
 "apiKey": API_KEY,
 "itmId": itm,
 "objL1": sido_code, # 시도 (또는 ALL)
 "objL2": "ALL", # 시군구
 "objL3": "", # 지목 분류 비우기 (총합)
 "objL4": "",
 "objL5": "",
 "objL6": "",
 "objL7": "",
 "objL8": "",
 "format": "json",
 "jsonVD": "Y",
 "prdSe": "Y",
 "startPrdDe": str(year_start),
 "endPrdDe": str(year_end),
 "outputFields": "ORG_ID+TBL_ID+TBL_NM+OBJ_NM+NM+ITM_ID+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE+",
 "orgId": "116",
 "tblId": "DT_MLTM_2300",
 }
 query = "&".join(
 f"{k}={urllib.parse.quote(str(v), safe='+')}"
 for k, v in params.items if v!= ""
)
 return f"{BASE_URL}?{query}"

def fetch_year(year: int, itm: str = "13103874596T1+") -> list[dict]:
 """단일 연도 + 단일 itmId 호출. objL3 비워서 cell 수 감소."""
 url = build_url(year, year, sido_code="ALL", itm=itm)
 req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
 try:
 with urllib.request.urlopen(req, timeout=60) as resp:
 raw = resp.read.decode("utf-8")
 data = json.loads(raw)
 if isinstance(data, dict) and "errMsg" in data:
 err = data.get("errMsg", "").strip
 print(f" [WARN] year={year} itm={itm} API error: {err}")
 return 
 if not isinstance(data, list):
 print(f" [WARN] year={year} unexpected response type: {type(data)}")
 return 
 return data
 except urllib.error.URLError as e:
 print(f" [ERROR] year={year} network error: {e}")
 return 
 except json.JSONDecodeError as e:
 print(f" [ERROR] year={year} JSON parse failed: {e}")
 return 

def fetch_year_by_sido(year: int, itm: str = "13103874596T1+") -> list[dict]:
 """Fallback: 시도별 분할 호출. 17 시도 × 1 연도 = 17 호출."""
 # KOSIS 의 시도 코드: 11(서울)~50(제주). DT_MLTM_2300 가 어떤 코드를 쓸지 모르므로 일단 통합 ALL 실패 시 호출.
 SIDO_CODES_KOSIS = [ # 통계청 표준 시도 코드 추정
 "11", "21", "22", "23", "24", "25", "26", "29",
 "31", "32", "33", "34", "35", "36", "37", "38", "39",
 ]
 out = 
 for sc in SIDO_CODES_KOSIS:
 url = build_url(year, year, sido_code=sc, itm=itm)
 req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
 try:
 with urllib.request.urlopen(req, timeout=60) as resp:
 raw = resp.read.decode("utf-8")
 data = json.loads(raw)
 if isinstance(data, list):
 out.extend(data)
 time.sleep(0.3)
 except Exception:
 continue
 return out

def main:
 all_rows = 
 for year in YEAR_RANGE:
 print(f"[INFO] Year {year}...", end=" ", flush=True)
 # 1차 시도: ALL × ALL, objL3 비움, itm T1 만
 rows = fetch_year(year, itm="13103874596T1+")
 if not rows:
 # 2차 fallback: 시도별 분할
 print("fallback to sido split...", end=" ", flush=True)
 rows = fetch_year_by_sido(year, itm="13103874596T1+")
 print(f"got {len(rows)} rows")
 all_rows.extend(rows)
 time.sleep(0.5)

 if not all_rows:
 print("[ERROR] No data fetched. Check API key + parameter set.")
 return

 # CSV 저장
 import csv
 cols = sorted({k for r in all_rows for k in r.keys})
 with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
 writer = csv.DictWriter(f, fieldnames=cols)
 writer.writeheader
 for row in all_rows:
 writer.writerow(row)
 print(f"\n[OK] CSV saved: {OUTPUT_CSV}")
 print(f" Total rows: {len(all_rows)}, columns: {cols}")

 # 미리보기 5 줄
 print("\n[Preview] First 5 rows:")
 for row in all_rows[:5]:
 c1 = row.get("C1_NM", "") or row.get("C1", "")
 c2 = row.get("C2_NM", "") or row.get("C2", "")
 c3 = row.get("C3_NM", "") or row.get("C3", "")
 itm = row.get("ITM_NM", "")
 prd = row.get("PRD_DE", "")
 dt = row.get("DT", "")
 unit = row.get("UNIT_NM", "")
 print(f" PRD={prd}, C1={c1}, C2={c2}, C3={c3}, ITM={itm}, DT={dt}, UNIT={unit}")

 # 시군구 unique 개수 확인
 sigungu_set = set
 for row in all_rows:
 c1 = row.get("C1_NM", "")
 c2 = row.get("C2_NM", "")
 sigungu_set.add(f"{c1}/{c2}")
 print(f"\n[Diagnostic] Unique 시도/시군구 combinations: {len(sigungu_set)}")
 print(f" Sample: {list(sigungu_set)[:5]}")

if __name__ == "__main__":
 main
