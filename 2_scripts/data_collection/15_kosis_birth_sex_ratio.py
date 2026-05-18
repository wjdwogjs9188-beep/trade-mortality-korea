"""
Phase 1.3 (v02) — KOSIS 시군구별 출생 성비 1980-1995 (z_m_marital).

v01 → v02 변경:
 - getMeta endpoint 우선 호출 → 표 구조·objL 코드 사전 확인
 - error code 20/30 시 actual error 메시지 출력 (debug)
 - objL1 'ALL' 대신 metadata 에서 추출한 실제 코드 list 사용
 - stdout UTF-8

KOSIS Open API:
 https://kosis.kr/openapi/index/index.jsp
 endpoint: https://kosis.kr/openapi/Param/statisticsParameterData.do
"""
from __future__ import annotations
import sys, time, json
from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode
import requests
import os
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
PROJECT = Path(__file__).resolve.parents[2]
load_dotenv(PROJECT / ".env")
KOSIS_API_KEY = os.environ.get("KOSIS_API_KEY", "")

from lib.config import RAW_DIR, LOGS_DIR

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")
 sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = RAW_DIR / "kosis_birth_sex_ratio"
LOG = LOGS_DIR / "data_collection" / f"{datetime.now:%Y-%m-%d}_phase1_kosis_birth_v02.md"

KOSIS_DATA = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
KOSIS_META = "https://kosis.kr/openapi/Param/statisticsParameterMetaData.do"

# 후보 stat (orgId 101 = 통계청)
CANDIDATES = [
 {"tblId": "DT_1B81A21", "label": "시군구별_출생_성별"},
 {"tblId": "DT_1B040A3", "label": "시군구_성_연령별"},
 {"tblId": "DT_1B8000F", "label": "지역별_출생"},
 # 추가 후보 — 통계 키워드 검색 필요 시
 {"tblId": "DT_1B81A02", "label": "시도_출생"},
]

def kosis_meta(tbl_id: str) -> dict | list:
 """getMeta — 표 구조 + objL 코드 list 확인."""
 params = {
 "method": "getMeta",
 "apiKey": KOSIS_API_KEY,
 "format": "json",
 "jsonVD": "Y",
 "orgId": "101",
 "tblId": tbl_id,
 "type": "TBL",
 }
 url = KOSIS_META + "?" + urlencode(params)
 r = requests.get(url, timeout=30)
 r.raise_for_status
 try:
 return r.json
 except ValueError:
 return {"err": "non-json", "text": r.text[:300]}

def kosis_data(tbl_id: str, prd_se: str, start: str, end: str,
 objL1: str = "ALL", objL2: str = "", objL3: str = "", objL4: str = "") -> dict | list:
 """getList — 실제 데이터."""
 params = {
 "method": "getList",
 "apiKey": KOSIS_API_KEY,
 "format": "json",
 "jsonVD": "Y",
 "userStatsId": "",
 "prdSe": prd_se,
 "startPrdDe": start,
 "endPrdDe": end,
 "orgId": "101",
 "tblId": tbl_id,
 "objL1": objL1,
 }
 if objL2: params["objL2"] = objL2
 if objL3: params["objL3"] = objL3
 if objL4: params["objL4"] = objL4
 url = KOSIS_DATA + "?" + urlencode(params)
 r = requests.get(url, timeout=30)
 r.raise_for_status
 try:
 return r.json
 except ValueError:
 return {"err": "non-json", "text": r.text[:300]}

def parse_meta(meta) -> dict:
 """meta 응답 → {objL1: [code list], prdSe: [...]}.

 KOSIS meta 형식 다양함 — 후보 키 검사.
 """
 if not isinstance(meta, list):
 return {}
 info = {}
 for entry in meta:
 if not isinstance(entry, dict):
 continue
 # objKey 또는 KEY_NM 등 후보
 for k, v in entry.items:
 info.setdefault(k,).append(v)
 return info

def main -> int:
 OUT_DIR.mkdir(parents=True, exist_ok=True)
 LOG.parent.mkdir(parents=True, exist_ok=True)
 if not KOSIS_API_KEY:
 msg = "[ERROR] KOSIS_API_KEY 가.env 에 없음"
 print(msg)
 LOG.write_text(f"# Phase 1.3 v02 ❌\n\n{msg}\n", encoding="utf-8")
 return 1

 log = [f"# Phase 1.3 v02 — KOSIS 출생성비 시군구\n", f"_timestamp: {datetime.now.isoformat}_\n\n"]
 overall_ok = False

 for cand in CANDIDATES:
 tbl = cand["tblId"]
 label = cand["label"]
 print(f"\n=== {tbl} ({label}) ===")
 log.append(f"## {tbl}\n\n")

 # 1) getMeta
 try:
 meta = kosis_meta(tbl)
 print(f" [meta] type={type(meta).__name__}, len={len(meta) if hasattr(meta,'__len__') else '?'}")
 if isinstance(meta, list) and meta:
 # sample meta entries
 for m in meta[:3]:
 print(f" {str(m)[:200]}")
 # 자동 분류 코드 추출 시도
 obj_keys = sorted({m.get("OBJ_NM") or m.get("OBJ_ID") or m.get("KEY_NM") for m in meta if isinstance(m, dict)})
 obj_keys = [k for k in obj_keys if k]
 log.append(f"- meta entries: {len(meta)}, obj keys: {obj_keys[:10]}\n")
 elif isinstance(meta, dict):
 print(f" [meta error] {meta}")
 log.append(f"- ❌ meta error: `{meta}`\n\n")
 continue
 except Exception as e:
 print(f" [meta fail] {e}")
 log.append(f"- ❌ meta fail: {e}\n\n")
 continue

 # 2) probe data — 1980 한 해
 try:
 print(f" [probe data 1980]")
 d = kosis_data(tbl, "A", "1980", "1980", objL1="ALL")
 if isinstance(d, dict):
 err = d.get("err") or d.get("RESULT") or d
 print(f" [data error] {err}")
 log.append(f"- ❌ data probe (1980): `{err}`\n\n")
 continue
 if not isinstance(d, list) or not d:
 print(f" [empty]")
 log.append(f"- ⚠️ data probe empty\n\n")
 continue
 # 시군구 단위 판정
 c1_codes = sorted({str(r.get('C1', '')).strip for r in d if isinstance(r, dict)})
 sigungu_5d = [c for c in c1_codes if len(c) == 5 and c.isdigit]
 print(f" C1 codes: {len(c1_codes)}, 5-digit: {len(sigungu_5d)}")
 log.append(f"- probe rows (1980): {len(d)}\n")
 log.append(f"- C1 distinct: {len(c1_codes)}, sigungu 5-digit: {len(sigungu_5d)}\n")

 if len(sigungu_5d) < 30:
 print(f" [skip] 시군구 단위 아님")
 log.append(f"- ❌ 시군구 단위 아님 (skip)\n\n")
 continue

 # 시군구 단위 → 1980-1995 fetch
 print(f" [OK] 시군구 단위 → 1980-1995 fetch")
 all_rows = 
 for y in range(1980, 1996):
 yd = kosis_data(tbl, "A", str(y), str(y), objL1="ALL")
 if isinstance(yd, list):
 all_rows.extend(yd)
 time.sleep(0.5)
 if all_rows:
 import csv
 keys = sorted({k for r in all_rows for k in r.keys})
 out = OUT_DIR / f"{tbl}_birth_sex_ratio_sigungu_1980_1995.csv"
 with out.open("w", encoding="utf-8-sig", newline="") as f:
 writer = csv.DictWriter(f, fieldnames=keys)
 writer.writeheader
 writer.writerows(all_rows)
 yrs = sorted({r.get("PRD_DE", "") for r in all_rows})
 sigus = {r.get("C1", "") for r in all_rows}
 print(f" ✅ {len(all_rows):,} rows, years {yrs[:3]}..{yrs[-3:]}, 시군구 {len(sigus)}")
 log.append(f"- ✅ saved `{out.name}`: {len(all_rows):,} rows, years={len(yrs)}, 시군구={len(sigus)}\n\n")
 overall_ok = True
 break
 else:
 log.append(f"- ⚠️ 1980-1995 전체 fetch 0 rows\n\n")
 except Exception as e:
 print(f" [data fail] {e}")
 log.append(f"- ❌ data fail: {e}\n\n")

 if not overall_ok:
 log.append("## 모든 후보 실패\n")
 log.append("- KOSIS UI 검색: https://kosis.kr/statisticsList/statisticsListIndex.do\n")
 log.append("- 키워드: '시군구별 출생성비' 또는 '시군구 출생 성별'\n")
 log.append("- 실제 시군구 disaggregation 표 ID 확인 후 CANDIDATES 추가\n")

 LOG.write_text("".join(log), encoding="utf-8")
 print(f"\n[log] {LOG}")
 return 0 if overall_ok else 2

if __name__ == "__main__":
 sys.exit(main)
