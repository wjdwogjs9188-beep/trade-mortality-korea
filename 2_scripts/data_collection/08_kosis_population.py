"""KOSIS Open API — 시군구/성/연령(5세)별 주민등록연앙인구 다운.

표: DT_1B040M5 (시군구/성/연령(5세)별 주민등록연앙인구, 1993-2023)

연도별 분할 호출 (단일 연도당 ~16k 행, 100k 한도 안전).

산출:
 0_raw/kosis_population/population_5yr_{year}.csv (31개 파일)
 0_raw/kosis_population/population_5yr_combined.csv (합본)

용도:
 Phase 2 panel build 의 사망률 분모 (사망 / 인구 × 100,000)
 연앙인구 = 7월 1일 추정. 사망률 계산 표준.
"""
import sys
import json
import re
import time
from pathlib import Path
import requests
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR, KOSIS_API_KEY, assert_api_key

def parse_kosis_response(text: str):
 """KOSIS API 의 비표준 JSON 파싱.

 KOSIS 응답은 [{TBL_ID:"...",ORG_ID:"...",...}] 형식 (property 이름에 따옴표 없음).
 표준 JSON 으로 변환 후 json.loads.
 """
 # error response 인지 먼저 체크 (정상 JSON 으로 옴)
 text = text.strip
 if text.startswith("{"): # error 형식
 try:
 return json.loads(text)
 except Exception:
 pass

 # 비표준 → 표준 변환 (property 이름에 따옴표 추가)
 fixed = re.sub(
 r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)',
 r'\1"\2"\3',
 text
)
 return json.loads(fixed)

# ───────────────────────── 설정 ─────────────────────────
BASE_URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
TBL_ID = "DT_1B040M5"
ORG_ID = "101"

OUT_DIR = RAW_DIR / "kosis_population"
OUT_DIR.mkdir(parents=True, exist_ok=True)

START_YEAR = 1993
END_YEAR = 2023
DELAY = 0.5 # 호출 간격 (초)
# 단일 연도 호출 (objL1=ALL 로 모든 시군구 한 번에 — KOSIS 응답 ~10MB/year 정상)

def fetch_year(year: int, retries: int = 3) -> pd.DataFrame:
 """단일 연도 — objL1=ALL 로 모든 시군구 한 번에 받기 (응답 ~10MB).

 KOSIS 가 비표준 JSON (property 따옴표 없음) 반환 → parse_kosis_response 로 처리.
 jsonVD 와 outputFields 모두 제거 — KOSIS default 응답 = 모든 필드 포함.
 """
 params = {
 "method": "getList",
 "apiKey": KOSIS_API_KEY,
 "itmId": "T10+",
 "objL1": "ALL", # ⭐ 모든 시군구 (KOSIS UI 시군구 선택 시 'ALL')
 "objL2": "ALL",
 "objL3": "ALL",
 "objL4": "",
 "objL5": "",
 "objL6": "",
 "objL7": "",
 "objL8": "",
 "format": "json",
 # jsonVD 제거 — 라벨 보존
 # outputFields 제거 — default 모든 필드
 "prdSe": "Y",
 "startPrdDe": str(year),
 "endPrdDe": str(year),
 "orgId": ORG_ID,
 "tblId": TBL_ID,
 }
 last_exc = None
 for attempt in range(retries):
 try:
 r = requests.get(BASE_URL, params=params, timeout=300)
 r.raise_for_status
 data = parse_kosis_response(r.text)
 if isinstance(data, dict) and ("err" in data or data.get("errMsg")):
 raise RuntimeError(f"KOSIS API err: {data}")
 if not isinstance(data, list):
 raise RuntimeError(f"예상 외 응답 type: {type(data).__name__}")
 return pd.DataFrame(data)
 except (requests.RequestException, ValueError, RuntimeError, json.JSONDecodeError) as e:
 last_exc = e
 wait = (attempt + 1) * 5
 print(f" ⚠️ {year} 시도 {attempt+1} 실패 ({type(e).__name__}). {wait}초 대기")
 time.sleep(wait)
 raise RuntimeError(f"{year} 최종 실패: {last_exc}")

def cleanup_old_bad_files:
 """이전 잘못된 파일 정리:
 - DT 1컬럼만 (jsonVD=Y 시절)
 - 또는 unique 시군구 < 200 개 (sido 분할 안 한 시절, sigungu 부족)
 """
 bad = 
 for f in OUT_DIR.glob("*.csv"):
 if "combined" in f.name:
 bad.append((f, "combined (재생성 필요)"))
 continue
 try:
 with open(f, "r", encoding="utf-8-sig") as fh:
 header = fh.readline.strip
 if header == "DT":
 bad.append((f, "DT-only (jsonVD bug)"))
 continue
 # unique C1 카운트
 df = pd.read_csv(f, dtype=str, usecols=["C1"], on_bad_lines="skip")
 n_c1 = df["C1"].nunique
 if n_c1 < 100: # 200 시군구가 정상, 100 미만이면 부족
 bad.append((f, f"unique C1={n_c1} (시군구 부족)"))
 except Exception:
 continue
 if bad:
 print(f"⚠️ 이전 잘못된 파일 {len(bad)}개 발견:")
 for f, reason in bad[:5]:
 print(f" - {f.name}: {reason}")
 if len(bad) > 5:
 print(f"... 외 {len(bad) - 5} 개")
 ans = input("\n삭제하고 재다운로드할까요? (yes/no): ").strip.lower
 if ans in ("yes", "y"):
 for f, _ in bad:
 f.unlink
 print(f"✅ {len(bad)}개 삭제 완료")
 return True
 else:
 print("중단.")
 return False
 return True

def main:
 assert_api_key("KOSIS", KOSIS_API_KEY)
 print("=" * 70)
 print("KOSIS 시군구/성/연령(5세)별 주민등록연앙인구 다운로드")
 print(f" 대상 기간: {START_YEAR}-{END_YEAR} ({END_YEAR-START_YEAR+1}년)")
 print(f" 표 ID: {TBL_ID}")
 print(f" 저장 위치: {OUT_DIR}")
 print("=" * 70)
 print

 # 잘못된 이전 파일 정리
 if not cleanup_old_bad_files:
 return

 answer = input("진행하시겠습니까? (yes / no): ").strip.lower
 if answer not in ("yes", "y"):
 print("중단.")
 return

 t0 = time.time
 success = 
 fail = 

 for year in range(START_YEAR, END_YEAR + 1):
 out = OUT_DIR / f"population_5yr_{year}.csv"
 if out.exists:
 n = sum(1 for _ in open(out, "r", encoding="utf-8-sig", errors="replace")) - 1
 print(f"[{year}] ⏭ 이미 존재 ({n:,} 행) — skip")
 success.append((year, n, "skip"))
 continue

 try:
 print(f"[{year}] 다운로드 중...", end=" ", flush=True)
 df = fetch_year(year)
 df.to_csv(out, index=False, encoding="utf-8-sig")
 print(f"✅ {len(df):,} 행 → {out.name}")
 success.append((year, len(df), "ok"))
 except Exception as e:
 print(f"❌ 실패: {e}")
 fail.append((year, str(e)))

 time.sleep(DELAY)

 elapsed = time.time - t0
 print(f"\n{'=' * 70}")
 print(f" 완료 — 총 {elapsed/60:.1f} 분")
 print(f" 성공: {len(success)} 연도")
 print(f" 실패: {len(fail)} 연도")
 print(f"{'=' * 70}\n")

 # 합본 만들기
 if success:
 print("합본 만드는 중...")
 all_dfs = 
 for year, _, _ in success:
 f = OUT_DIR / f"population_5yr_{year}.csv"
 if f.exists:
 df = pd.read_csv(f, dtype=str)
 all_dfs.append(df)
 if all_dfs:
 combined = pd.concat(all_dfs, ignore_index=True)
 combined_out = OUT_DIR / "population_5yr_combined.csv"
 combined.to_csv(combined_out, index=False, encoding="utf-8-sig")
 print(f"✅ 합본 저장: {combined_out} ({len(combined):,} 행)")

 if fail:
 print("\n⚠️ 실패한 연도:")
 for year, err in fail:
 print(f" {year}: {err[:80]}")

if __name__ == "__main__":
 main
