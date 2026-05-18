"""
identification diagnostic Test 2 (pre-WTO lead orthogonality) — KR-CN bilateral 1995-1999.

기존: comtrade_korea_china/ 에 2000-2024 (50 files = 25년 × 2 direction) 보유.
신규: 1995-1999 (10 files = 5년 × 2 direction) 추가 호출.

전략:
 1. 단일 호출 시도 (1990s 무역량 작아서 100k 안 넘을 가능성 높음)
 2. 100k+ truncated 면 HS2 chapter 분할 fallback
 3. 4-way API key 로테이션 (rate limit 분산)
 4. skip if exists (resume 가능)

산출:
 0_raw/comtrade_korea_china/KR_imp_from_CN_<year>.csv (5)
 0_raw/comtrade_korea_china/KR_exp_to_CN_<year>.csv (5)
 5_logs/data_collection/<date>_comtrade_kr_cn_pre_wto.md
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from datetime import datetime
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR, LOGS_DIR
from lib.comtrade_api import fetch, M49

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")
 sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = RAW_DIR / "comtrade_korea_china"
LOG = LOGS_DIR / "data_collection" / f"{datetime.now:%Y-%m-%d}_comtrade_kr_cn_pre_wto.md"

YEARS = [1995, 1996, 1997, 1998, 1999]
DIRECTIONS = [
 # (label, flow_code, reporter, partner) flow: M=import X=export
 ("KR_imp_from_CN", "M", "KR", "CN"),
 ("KR_exp_to_CN", "X", "KR", "CN"),
]

CALL_DELAY = 1.0
HS2_MFG = [f"{i:02d}" for i in range(28, 98)] # manufacturing 70 chapters
HS2_ALL = [f"{i:02d}" for i in range(1, 100)] # 99 chapters

def fetch_single(year: int, flow: str, reporter: str, partner: str, key_idx: int) -> pd.DataFrame:
 """단일 호출 시도."""
 return fetch(
 reporter_code=str(M49[reporter]),
 partner_code=str(M49[partner]),
 period=str(year),
 flow_code=flow,
 cmd_code="AG6", # HS6 detail
 key_index=key_idx,
)

def fetch_chunked(year: int, flow: str, reporter: str, partner: str, start_key: int) -> pd.DataFrame:
 """HS2 chapter 별로 쪼개서 fetch (100k 회피)."""
 parts = 
 for idx, hs2 in enumerate(HS2_ALL):
 try:
 df = fetch(
 reporter_code=str(M49[reporter]),
 partner_code=str(M49[partner]),
 period=str(year),
 flow_code=flow,
 cmd_code=hs2,
 key_index=start_key + idx,
)
 if not df.empty:
 parts.append(df)
 time.sleep(CALL_DELAY)
 except Exception as e:
 print(f" [chapter {hs2} fail] {e}", flush=True)
 return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame

def main:
 OUT_DIR.mkdir(parents=True, exist_ok=True)
 LOG.parent.mkdir(parents=True, exist_ok=True)

 log = [f"# Comtrade KR-CN bilateral 1995-1999 (pre-WTO)\n", f"_timestamp: {datetime.now.isoformat}_\n\n"]
 log.append("## 호출 결과\n\n")

 total_calls = 0
 saved = 0
 skipped = 0
 truncated = 

 for label, flow, reporter, partner in DIRECTIONS:
 for year in YEARS:
 fname = f"{label}_{year}.csv"
 out = OUT_DIR / fname
 if out.exists:
 n = sum(1 for _ in out.open(encoding='utf-8', errors='replace'))
 print(f"[skip] {fname} (이미 존재, {n} lines)")
 log.append(f"- ⏭ `{fname}` skip ({n} lines existing)\n")
 skipped += 1
 continue

 print(f"\n=== {label} {year} ===", flush=True)
 try:
 df = fetch_single(year, flow, reporter, partner, key_idx=total_calls)
 total_calls += 1
 time.sleep(CALL_DELAY)

 if df.empty:
 print(f" ⚠️ empty response")
 log.append(f"- ⚠️ `{fname}` empty\n")
 continue

 if len(df) >= 100_000:
 print(f" ⚠️ {len(df)} rows — truncated 가능, HS2 chapter 분할 재시도")
 log.append(f"- ⚠️ `{fname}` 단일 호출 {len(df)} → HS2 chunk 분할\n")
 df = fetch_chunked(year, flow, reporter, partner, start_key=total_calls)
 total_calls += len(HS2_ALL)
 truncated.append(fname)

 df.to_csv(out, index=False, encoding="utf-8-sig")
 print(f" ✅ {len(df):,} rows -> {fname}")
 log.append(f"- ✅ `{fname}`: {len(df):,} rows\n")
 saved += 1
 except Exception as e:
 print(f" ❌ {e}")
 log.append(f"- ❌ `{fname}`: {str(e)[:200]}\n")

 log.append(f"\n## 종합\n\n")
 log.append(f"- saved: {saved} files\n")
 log.append(f"- skipped (existing): {skipped}\n")
 log.append(f"- truncated → chunked: {len(truncated)}\n")
 log.append(f"- total API calls: {total_calls}\n")

 LOG.write_text("".join(log), encoding="utf-8")
 print(f"\n[log] {LOG}")
 print(f"[done] saved={saved}, skipped={skipped}, truncated={len(truncated)}")
 return 0 if (saved + skipped) == 10 else 2

if __name__ == "__main__":
 sys.exit(main)
