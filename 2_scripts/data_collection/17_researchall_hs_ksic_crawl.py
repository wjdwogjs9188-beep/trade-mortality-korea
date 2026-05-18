"""
researchall.net HS↔KSIC 매핑 — API 직접 호출 (v2, SPA 우회).

API:
 POST https://code.researchall.net/api/connect/ksicAndHs
 body: {"page": N, "limit": L, "searchTarget": ""}
 response: {totalCount, whatIsThisCode, data: [{ksic_code, ksic_def_kr, hs_code, hs_def_kr},...]}

총 rows: 약 6,360 (limit=10 × 636 page).
limit 을 늘릴 수 있으면 페이지 수 ↓ → 더 빠름.

mode:
 --probe: limit 한도 탐색 (10/50/100/500/1000) + totalCount 확인
 --crawl: 풀 크롤 + CSV 산출
 --limit N: crawl 시 사용할 페이지 크기 (default 100)

산출:
 0_raw/hs_ksic_concordance/researchall_HS6_to_KSIC_link.csv
 5_logs/data_collection/<date>_researchall_api.md
"""
from __future__ import annotations
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
try:
 from lib.config import RAW_DIR, LOGS_DIR
except ImportError:
 PROJECT = Path(__file__).resolve.parents[2]
 RAW_DIR = PROJECT / "0_raw"
 LOGS_DIR = PROJECT / "5_logs"

import requests

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")
 sys.stderr.reconfigure(encoding="utf-8", errors="replace")

API_URL = "https://code.researchall.net/api/connect/ksicAndHs"
DEFAULT_DELAY = 1.0
HEADERS = {
 # 사용자 브라우저 cURL 그대로 — 서버가 동일 origin 요청으로 인식
 "accept": "application/json, text/plain, */*",
 "accept-language": "ko,en;q=0.9,ja;q=0.8,fr;q=0.7",
 "content-type": "application/json",
 "dnt": "1",
 "origin": "https://code.researchall.net",
 "priority": "u=1, i",
 "referer": "https://code.researchall.net/search_KSIC_HS_Link",
 "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
 "sec-ch-ua-mobile": "?0",
 "sec-ch-ua-platform": '"Windows"',
 "sec-fetch-dest": "empty",
 "sec-fetch-mode": "cors",
 "sec-fetch-site": "same-origin",
 "sec-gpc": "1",
 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
}

OUT_DIR = RAW_DIR / "hs_ksic_concordance"
PARSED_CSV = OUT_DIR / "researchall_HS6_to_KSIC_link.csv"
RAW_DUMP = OUT_DIR / "researchall_api_raw"
LOG = LOGS_DIR / "data_collection" / f"{datetime.now:%Y-%m-%d}_researchall_api.md"

def fetch(page: int, limit: int, search_target: str = "", retries: int = 3) -> dict | None:
 """단일 API 호출. dict 또는 None."""
 body = {"page": page, "limit": limit, "searchTarget": search_target}
 delay = DEFAULT_DELAY
 for attempt in range(retries):
 try:
 r = requests.post(API_URL, headers=HEADERS, json=body, timeout=30)
 if r.status_code == 200:
 return r.json
 if r.status_code == 429:
 wait = delay * (2 ** attempt) + 5
 print(f" [rate-limit] page={page} → wait {wait}s")
 time.sleep(wait)
 continue
 print(f" [http {r.status_code}] page={page}")
 return None
 except (requests.exceptions.RequestException, ValueError) as e:
 wait = delay * (2 ** attempt)
 print(f" [retry {attempt+1}] page={page}: {e} → wait {wait}s")
 time.sleep(wait)
 return None

def probe -> int:
 OUT_DIR.mkdir(parents=True, exist_ok=True)
 LOG.parent.mkdir(parents=True, exist_ok=True)

 log = [f"# Probe — {datetime.now.isoformat}\n\n", f"API: `POST {API_URL}`\n\n"]
 print(f"[probe] limit 한도 탐색 (10 / 50 / 100 / 500 / 1000)")

 best_limit = 10
 total = None
 sample_data = None

 for L in [1000, 500, 100, 50, 10]:
 print(f"\n trying limit={L}")
 r = fetch(1, L)
 if r is None:
 print(f" [fail] limit={L}")
 log.append(f"- limit {L}: ❌ http error\n")
 continue
 rows = r.get("data") or 
 total_now = r.get("totalCount") or len(rows)
 what = r.get("whatIsThisCode")
 print(f" [ok] limit={L}: returned {len(rows)} rows, totalCount={total_now}, whatIsThisCode={what}")
 log.append(f"- limit {L}: ✅ rows={len(rows)}, totalCount={total_now}\n")
 if len(rows) >= L * 0.9: # 거의 limit 만큼 받음 → 작동
 best_limit = max(best_limit, L)
 total = total_now
 sample_data = rows[:3]
 # 가장 큰 limit 작동하면 break
 break
 time.sleep(DEFAULT_DELAY)

 log.append(f"\n## 권장\n\n")
 if total is None:
 log.append(f"⚠️ probe 실패 — 모든 limit 에서 응답 없음\n")
 print("\n[fail] 모든 limit 시도 실패")
 return 1

 pages_needed = (total + best_limit - 1) // best_limit
 print(f"\n[result] total = {total:,} rows, best_limit = {best_limit}, pages_needed = {pages_needed}")
 log.append(f"- 총 row: **{total:,}**\n")
 log.append(f"- 최대 limit: **{best_limit}**\n")
 log.append(f"- 풀 크롤 페이지 수: **{pages_needed}** (1초 간격 → 약 {pages_needed:.0f}초)\n")
 log.append(f"\n## 표 column 샘플\n\n")
 if sample_data:
 keys = list(sample_data[0].keys)
 log.append(f"- columns: `{keys}`\n")
 log.append(f"- sample row: `{sample_data[0]}`\n")

 log.append(f"\n## 다음 명령\n\n")
 log.append(f"```\n")
 log.append(f"python 2_scripts/data_collection/17_researchall_hs_ksic_crawl.py --crawl --limit {best_limit}\n")
 log.append(f"```\n")

 LOG.write_text("".join(log), encoding="utf-8")
 print(f"\n[log] {LOG}")
 return 0

def crawl(limit: int) -> int:
 OUT_DIR.mkdir(parents=True, exist_ok=True)
 RAW_DUMP.mkdir(parents=True, exist_ok=True)
 LOG.parent.mkdir(parents=True, exist_ok=True)

 log = [f"# Crawl — {datetime.now.isoformat}\n\n", f"API: `POST {API_URL}`, limit={limit}\n\n"]

 # 첫 page 로 totalCount 확인
 print(f"[crawl] limit={limit} — 첫 page 로 totalCount 확인")
 r = fetch(1, limit)
 if r is None:
 print("[fail] page 1 응답 없음")
 log.append("❌ page 1 fetch fail\n")
 LOG.write_text("".join(log), encoding="utf-8")
 return 1

 total = r.get("totalCount") or 0
 pages = (total + limit - 1) // limit
 print(f" total = {total:,}, pages = {pages}")
 log.append(f"- total: {total:,}, pages: {pages}\n\n")

 all_rows = list(r.get("data") or)
 # raw dump for debug
 (RAW_DUMP / f"page_0001.json").write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")

 failed_pages = 
 for page in range(2, pages + 1):
 time.sleep(DEFAULT_DELAY)
 r = fetch(page, limit)
 if r is None:
 failed_pages.append(page)
 log.append(f"- page {page}: ❌\n")
 # 5 연속 실패 abort
 recent = [p for p in failed_pages if p > page - 6]
 if len(recent) >= 5:
 print(f"\n[abort] 5 연속 실패 → 중단. resume: --crawl --limit {limit}")
 log.append(f"\n⚠️ 5 연속 실패 → 중단\n")
 break
 continue
 rows = r.get("data") or 
 all_rows.extend(rows)
 (RAW_DUMP / f"page_{page:04d}.json").write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
 if page % 10 == 0:
 print(f" page {page}/{pages}: cumulative {len(all_rows):,} rows")

 # CSV 저장
 if all_rows:
 import csv
 keys = list(all_rows[0].keys)
 with PARSED_CSV.open("w", encoding="utf-8-sig", newline="") as f:
 writer = csv.DictWriter(f, fieldnames=keys)
 writer.writeheader
 writer.writerows(all_rows)
 print(f"\n[done] {len(all_rows):,} rows → {PARSED_CSV}")
 log.append(f"\n## 산출\n\n")
 log.append(f"- rows: **{len(all_rows):,}**\n")
 log.append(f"- 예상 vs 실제: {total:,} expected, {len(all_rows):,} got")
 log.append(f" — {'✅ match' if len(all_rows) >= total * 0.99 else '⚠️ 1% 이상 누락'}\n")
 log.append(f"- failed pages: {len(failed_pages)} {failed_pages[:10]}{'...' if len(failed_pages)>10 else ''}\n")
 log.append(f"- CSV: `{PARSED_CSV.name}`\n")
 log.append(f"- raw json dump: `{RAW_DUMP.name}/`\n")

 # 통계
 ksic_codes = sorted({r.get("ksic_code", "") for r in all_rows if r.get("ksic_code")})
 hs_codes = sorted({r.get("hs_code", "") for r in all_rows if r.get("hs_code")})
 log.append(f"\n## 분포\n\n")
 log.append(f"- distinct KSIC: {len(ksic_codes):,}\n")
 log.append(f"- distinct HS: {len(hs_codes):,}\n")
 log.append(f"- KSIC sample: {ksic_codes[:10]}\n")
 log.append(f"- HS sample: {hs_codes[:5]}... {hs_codes[-5:]}\n")
 else:
 log.append(f"\n⚠️ all_rows = 0\n")

 LOG.write_text("".join(log), encoding="utf-8")
 print(f"[log] {LOG}")
 return 0 if all_rows else 2

def main:
 parser = argparse.ArgumentParser
 parser.add_argument("--probe", action="store_true")
 parser.add_argument("--crawl", action="store_true")
 parser.add_argument("--limit", type=int, default=100)
 args = parser.parse_args

 if not (args.probe or args.crawl):
 parser.error("--probe 또는 --crawl 중 하나 선택")

 if args.probe:
 return probe
 return crawl(args.limit)

if __name__ == "__main__":
 sys.exit(main)
