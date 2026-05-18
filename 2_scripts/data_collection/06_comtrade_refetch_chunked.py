"""Truncated 파일 재수집 — HS 2자리 챕터별로 쪼개서 호출.

UN Comtrade API의 100,000행 per-call 한도 회피 방법:
 - reporter × year 단위가 아니라
 - reporter × year × HS2 chapter (01-99) 단위로 호출
 - 각 HS2 챕터는 보통 < 100k 행

대상:
 1. comtrade_adh_china/ 에서 100k+ 였던 파일들
 2. comtrade_china_world/ 에서 100k+ 였던 파일들

전략:
 1. 파일이 없거나 100k+ 인 reporter-year 식별
 2. HS2 챕터 (01-99) 별로 fetch
 3. 모두 합쳐서 reporter_year.csv 로 저장 (덮어쓰기)
 4. 메타: HS chunk 별 행수 / 합계 로그

비용 추정:
 - 42 country-year × 99 HS chapters ≈ 4,158 calls
 - rate 6 calls/sec, 약 12분 + retry 여유 = 20-30분
 - 일일 한도 1,000 → secondary key 사용으로 우회
"""
import sys
import time
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR
from lib.comtrade_api import fetch, M49, ADH_8

ADH_DIR = RAW_DIR / "comtrade_adh_china"
CN_WORLD_DIR = RAW_DIR / "comtrade_china_world"

# HS 2자리 코드 (01-99). 일부 미사용 챕터 있지만 그냥 다 호출 (없으면 빈 응답)
HS2_CODES = [f"{i:02d}" for i in range(1, 100)]

# 기대되는 (reporter, year) 조합 — 파일이 삭제됐어도 이 리스트로 재수집 대상 결정
EXPECTED_YEARS = list(range(2000, 2025)) # 2000-2024
EXPECTED_ADH = [(iso, yr) for iso in ADH_8 for yr in EXPECTED_YEARS] # 8 × 25 = 200
EXPECTED_CN_WORLD = list(EXPECTED_YEARS) # 25

# Rate limit 회피: 호출 간격 + chapter별 key 교대
CALL_DELAY = 1.0 # 초 (기존 0.15 → 1.0)
RETRY_DELAYS = [10, 30, 60, 120] # 4번 재시도, 점진적 증가

# 제조업 HS 챕터만 (선택). ADH는 manufacturing focus → HS 28-97 사용 권장
# 농산물(01-24), 광물(25-27), 미술품·특수(98-99) 는 본 연구 범위 밖
MFG_ONLY = True # False 로 바꾸면 99 챕터 모두 호출
HS2_MFG = [f"{i:02d}" for i in range(28, 98)] # HS 28-97 = 70개 (매뉴팩처링)
HS2_ALL = [f"{i:02d}" for i in range(1, 100)] # HS 01-99 = 99개 (전체)
HS2_CODES_USE = HS2_MFG if MFG_ONLY else HS2_ALL

def count_rows(path: Path) -> int:
 if not path.exists: return -1
 try:
 with open(path, "r", encoding="utf-8", errors="replace") as f:
 return sum(1 for _ in f)
 except Exception:
 return -1

def needs_refetch(path: Path) -> bool:
 """파일이 없거나 100k+ 면 재수집."""
 n = count_rows(path)
 return n < 0 or n >= 100_000

def fetch_country_year_chunked(reporter_iso2: str, partner_iso2: str, year: int,
 flow: str, start_key_idx: int = 0) -> pd.DataFrame:
 """HS2 챕터별로 쪼개서 fetch → 합쳐서 반환.
 Chapter별로 N개 key 라운드로빈 (rate limit 분산 극대화).
 """
 parts = 
 fail_count = 0
 for idx, hs2 in enumerate(HS2_CODES_USE):
 # N개 key 라운드로빈 (start_key_idx 부터 시작해서 챕터별 교대)
 key_idx = start_key_idx + idx
 try:
 df = fetch(
 reporter_code=str(M49[reporter_iso2]),
 partner_code=str(M49[partner_iso2]) if partner_iso2!= "WORLD" else "0",
 period=str(year),
 flow_code=flow,
 cmd_code=hs2,
 key_index=key_idx, # 4-way (또는 N-way) 로테이션
)
 if not df.empty:
 if len(df) >= 100_000:
 print(f" ⚠️ {reporter_iso2} {year} HS{hs2} 자체도 truncated! ({len(df)}행)")
 parts.append(df)
 fail_count = 0
 time.sleep(CALL_DELAY)
 except Exception as e:
 print(f" ❌ {reporter_iso2} {year} HS{hs2} (key#{key_idx % 4}): {e}")
 fail_count += 1
 # 연속 실패 8회 이상이면 모든 키 한도 초과 추정 → 중단
 if fail_count >= 8:
 print(f" 🛑 연속 8회 실패 — 모든 키 일일 한도 초과 추정. 중단.")
 break
 time.sleep(30)
 if not parts:
 return pd.DataFrame
 return pd.concat(parts, ignore_index=True)

def refetch_adh_china:
 """ADH 8국 × 2000-2024 — 누락(삭제) 또는 100k+ 인 파일 모두 재수집."""
 if not ADH_DIR.exists:
 print(f"⚠️ {ADH_DIR} 없음 — 스킵")
 return

 # 기대 조합 (200개) 모두 체크 → 누락이면 -1, truncated면 100k+
 targets = 
 missing = 0
 truncated = 0
 for iso, yr in EXPECTED_ADH:
 p = ADH_DIR / f"{iso}_{yr}.csv"
 if not p.exists:
 targets.append((iso, yr, p))
 missing += 1
 elif count_rows(p) >= 100_000:
 targets.append((iso, yr, p))
 truncated += 1

 print(f"\n=== ADH 재수집 대상: {len(targets)} 개 (누락 {missing}, truncated {truncated}) ===")
 for iso, yr, p in targets[:10]:
 status = "(없음)" if not p.exists else "(truncated)"
 print(f" {iso} {yr} {status}")
 if len(targets) > 10:
 print(f"... 외 {len(targets) - 10} 개")

 for i, (iso, yr, p) in enumerate(targets):
 if p.exists and 0 < count_rows(p) < 100_000:
 print(f"\n[{i+1}/{len(targets)}] {iso} {yr} ⏭ 이미 정상 — skip")
 continue
 # 각 country-year 마다 다른 키부터 시작 (부하 분산)
 start_key = i * len(HS2_CODES_USE)
 print(f"\n[{i+1}/{len(targets)}] {iso} {yr} (HS2 chunked, {len(HS2_CODES_USE)} chapters)")
 df = fetch_country_year_chunked(iso, "CN", yr, flow="M", start_key_idx=start_key)
 if df.empty:
 print(f" ❌ 빈 결과 — 파일 유지")
 continue
 df.to_csv(p, index=False, encoding="utf-8-sig")
 print(f" ✅ {len(df):,} 행 → {p.name}")

def refetch_china_world:
 """CN→World 2000-2024 — 누락(삭제) 또는 100k+ 인 파일 모두 재수집."""
 if not CN_WORLD_DIR.exists:
 print(f"⚠️ {CN_WORLD_DIR} 없음 — 스킵")
 return

 targets = 
 missing = 0
 truncated = 0
 for yr in EXPECTED_CN_WORLD:
 p = CN_WORLD_DIR / f"CN_exp_world_{yr}.csv"
 if not p.exists:
 targets.append((yr, p))
 missing += 1
 elif count_rows(p) >= 100_000:
 targets.append((yr, p))
 truncated += 1

 print(f"\n=== CN→World 재수집 대상: {len(targets)} 개 (누락 {missing}, truncated {truncated}) ===")
 for yr, p in targets:
 status = "(없음)" if not p.exists else "(truncated)"
 print(f" {yr} {status}")

 for i, (yr, p) in enumerate(targets):
 if p.exists and 0 < count_rows(p) < 100_000:
 print(f"\n[{i+1}/{len(targets)}] CN→World {yr} ⏭ 이미 정상 — skip")
 continue
 start_key = i * len(HS2_CODES_USE)
 print(f"\n[{i+1}/{len(targets)}] CN→World {yr} (HS2 chunked, {len(HS2_CODES_USE)} chapters)")
 df = fetch_country_year_chunked("CN", "WORLD", yr, flow="X", start_key_idx=start_key)
 if df.empty:
 print(f" ❌ 빈 결과 — 파일 유지")
 continue
 df.to_csv(p, index=False, encoding="utf-8-sig")
 print(f" ✅ {len(df):,} 행 → {p.name}")

def main:
 print("=" * 70)
 print("Comtrade truncated 파일 HS chunk 재수집")
 print("=" * 70)
 print
 print("주의: 시간이 오래 걸림 (약 30-60분, 4000+ API 호출)")
 print("일일 한도 절반 이상 사용 가능. secondary key 자동 교대.")
 print
 answer = input("진행하시겠습니까? (yes / no): ").strip.lower
 if answer not in ("yes", "y"):
 print("중단.")
 return

 t0 = time.time
 refetch_adh_china
 refetch_china_world
 elapsed = time.time - t0
 print(f"\n⏱ 총 {elapsed/60:.1f} 분 소요")
 print("\n다음:")
 print(" python 2_scripts/00_build_inventory.py # INVENTORY 갱신")

if __name__ == "__main__":
 main
