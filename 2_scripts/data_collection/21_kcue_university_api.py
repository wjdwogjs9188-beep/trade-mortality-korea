"""
Phase B-m P1.4 — KCUE 한국대학교육협의회 OpenAPI getSchoolInfo.

핵심: 응답에 schlEstbDt (설립일자) 보유 → 1990 이전 설립 필터 가능.
 → PAP v4.0 § 3.2 z_m_education baseline (외생성 보존) 정확 구축.

API:
 endpoint: http://openapi.academyinfo.go.kr/openapi/service/rest/SchoolInfoService/getSchoolInfo
 인증: data.go.kr 서비스 키 (DATA_GO_KR_API_KEY)
 형식: XML 응답

산출:
 0_raw/edu_university_list_1990/kcue_school_info_<svyYr>.csv (raw 전체)
 0_raw/edu_university_list_1990/universities_pre1990_baseline.csv (1990 이전 설립 4년제 본교)
 5_logs/data_collection/<date>_kcue_university.md
"""
from __future__ import annotations
import sys, time, csv
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import requests

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR, LOGS_DIR, DATA_GO_KR_API_KEY, assert_api_key

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")
 sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = RAW_DIR / "edu_university_list_1990"
LOG = LOGS_DIR / "data_collection" / f"{datetime.now:%Y-%m-%d}_kcue_university.md"

# Portal (data.go.kr) 명시 endpoint → docx outdated endpoint 순으로 시도
API_CANDIDATES = [
 "https://www.academyinfo.go.kr/openapi/service/rest/SchoolInfoService/getSchoolInfo",
 "http://www.academyinfo.go.kr/openapi/service/rest/SchoolInfoService/getSchoolInfo",
 "http://openapi.academyinfo.go.kr/openapi/service/rest/SchoolInfoService/getSchoolInfo",
 "https://openapi.academyinfo.go.kr/openapi/service/rest/SchoolInfoService/getSchoolInfo",
]
API = API_CANDIDATES[0] # default
SVY_YR = 2023 # 가장 최근 조사년도 — 변경 가능
TIMEOUT = 60
NUM_OF_ROWS = 999 # 페이지 최대

def fetch_page(svy_yr: int, page: int, num_rows: int = NUM_OF_ROWS) -> tuple[list[dict], int]:
 """단일 페이지 fetch → (items, totalCount)."""
 assert_api_key("DATA_GO_KR", DATA_GO_KR_API_KEY)
 params = {
 "serviceKey": DATA_GO_KR_API_KEY,
 "svyYr": str(svy_yr),
 "pageNo": str(page),
 "numOfRows": str(num_rows),
 }
 last_err = None
 for endpoint in API_CANDIDATES:
 try:
 r = requests.get(endpoint, params=params, timeout=TIMEOUT)
 r.raise_for_status
 root = ET.fromstring(r.text)
 # 첫 호출 성공 시 endpoint 출력 (debug)
 if endpoint!= API_CANDIDATES[0]:
 print(f" [endpoint fallback] {endpoint}", flush=True)
 break
 except (requests.exceptions.RequestException, ET.ParseError) as e:
 last_err = e
 continue
 else:
 raise RuntimeError(f"All endpoints failed. Last error: {last_err}")

 # 결과 코드 확인
 result_code = root.findtext(".//resultCode", "")
 if result_code!= "00":
 result_msg = root.findtext(".//resultMsg", "")
 raise RuntimeError(f"API error: code={result_code}, msg={result_msg}")

 total = int(root.findtext(".//totalCount", "0"))
 items = 
 for item in root.findall(".//item"):
 d = {child.tag: (child.text or "") for child in item}
 items.append(d)
 return items, total

def fetch_all(svy_yr: int) -> list[dict]:
 """페이지네이션 — 전체 학교 list."""
 print(f"[fetch] svyYr={svy_yr}, pageNo=1", flush=True)
 items, total = fetch_page(svy_yr, 1)
 print(f" totalCount={total}, page 1 returned {len(items)}", flush=True)

 all_items = list(items)
 pages = (total + NUM_OF_ROWS - 1) // NUM_OF_ROWS
 for p in range(2, pages + 1):
 time.sleep(0.5)
 print(f" page {p}/{pages}", end=" ", flush=True)
 try:
 its, _ = fetch_page(svy_yr, p)
 all_items.extend(its)
 print(f"+{len(its)}", flush=True)
 except Exception as e:
 print(f"❌ {e}", flush=True)
 return all_items

def main:
 OUT_DIR.mkdir(parents=True, exist_ok=True)
 LOG.parent.mkdir(parents=True, exist_ok=True)

 print(f"[KCUE] svyYr={SVY_YR}", flush=True)
 try:
 items = fetch_all(SVY_YR)
 except Exception as e:
 print(f"[FL] {e}", flush=True)
 LOG.write_text(f"# KCUE — ❌\n\n{e}\n", encoding="utf-8")
 return 1

 if not items:
 print("[empty]", flush=True)
 return 2

 # raw csv 저장
 raw_out = OUT_DIR / f"kcue_school_info_{SVY_YR}.csv"
 keys = sorted({k for d in items for k in d.keys})
 with raw_out.open('w', encoding='utf-8-sig', newline='') as f:
 w = csv.DictWriter(f, fieldnames=keys)
 w.writeheader
 w.writerows(items)
 print(f"[saved raw] {raw_out} — {len(items)} rows", flush=True)

 # 1990 baseline filter
 # 조건:
 # schlKndNm = '대학교' or '교육대학' or '산업대학' (4년제)
 # psbsDivNm = '본교'
 # schlEstbDt < '1990-01-01'
 TARGET_KIND = {"대학교", "교육대학", "산업대학"}
 pre1990 = 
 for d in items:
 kind = d.get("schlKndNm", "")
 psbs = d.get("psbsDivNm", "")
 estb = d.get("schlEstbDt", "")
 if kind not in TARGET_KIND:
 continue
 if psbs!= "본교":
 continue
 # date filter
 if estb and estb < "1990-01-01":
 pre1990.append(d)

 baseline_out = OUT_DIR / "universities_pre1990_baseline.csv"
 if pre1990:
 keys_subset = ["schlNm", "schlEstbDt", "schlEstbDivNm", "schlKndNm",
 "psbsDivNm", "pbnfAreaNm", "postNoAdrs", "schlId",
 "schlEngNm", "schlUrlAdrs", "lstUpdtDtm"]
 with baseline_out.open('w', encoding='utf-8-sig', newline='') as f:
 w = csv.DictWriter(f, fieldnames=keys_subset)
 w.writeheader
 for d in pre1990:
 w.writerow({k: d.get(k, "") for k in keys_subset})
 print(f"[saved baseline] {baseline_out} — {len(pre1990)} pre-1990 4년제 본교", flush=True)

 # 통계 요약
 from collections import Counter
 kind_dist = Counter(d.get("schlKndNm", "") for d in items)
 sido_dist = Counter(d.get("pbnfAreaNm", "") for d in items)
 pre1990_sido = Counter(d.get("pbnfAreaNm", "") for d in pre1990)
 pre1990_kind = Counter(d.get("schlKndNm", "") for d in pre1990)

 log = [f"# KCUE getSchoolInfo — {datetime.now.isoformat}\n\n"]
 log.append(f"- svyYr: {SVY_YR}\n")
 log.append(f"- 전체 학교: {len(items):,}\n")
 log.append(f"- 1990 이전 설립 4년제 본교: **{len(pre1990)}**\n\n")
 log.append(f"## 학교구분 전체 분포\n\n")
 for k, v in kind_dist.most_common(15):
 log.append(f"- {k}: {v}\n")
 log.append(f"\n## 1990 baseline 의 학교구분\n\n")
 for k, v in pre1990_kind.most_common:
 log.append(f"- {k}: {v}\n")
 log.append(f"\n## 1990 baseline 시도 분포\n\n")
 for k, v in pre1990_sido.most_common(20):
 log.append(f"- {k}: {v}\n")

 LOG.write_text("".join(log), encoding="utf-8")
 print(f"\n[log] {LOG}", flush=True)
 return 0

if __name__ == "__main__":
 sys.exit(main)
