"""truncated/0행 raw 파일 정리.

문제 파일 식별 + 삭제 (사용자 확인 후).

대상:
 - comtrade_adh_china/: 100,000+ 행 = API truncate (DE/ES/FI 일부)
 - comtrade_china_world/: 100,000+ 행 truncate (CN 2015-2017)
 - ecos_delinquency/: 사실 0행 파일은 저장 안 됐음 (download skip)
"""
import sys
from pathlib import Path
import csv

sys.path.insert(0, str(Path(__file__).resolve.parents[1]))
from lib.config import RAW_DIR

COMTRADE_DIRS = [
 RAW_DIR / "comtrade_adh_china",
 RAW_DIR / "comtrade_china_world",
]

def count_rows(path: Path) -> int:
 """csv 행수 (헤더 포함)."""
 try:
 with open(path, "r", encoding="utf-8", errors="replace") as f:
 return sum(1 for _ in f)
 except Exception:
 return -1

def find_truncated -> list[Path]:
 """100,000행 이상 = API truncate 의심 파일."""
 targets = 
 for d in COMTRADE_DIRS:
 if not d.exists: continue
 for p in d.glob("*.csv"):
 n = count_rows(p)
 if n >= 100_000: # 100,001 = header + 100k records (API limit)
 targets.append((p, n))
 return targets

def main:
 print("=" * 70)
 print("Truncated raw 파일 검색")
 print("=" * 70)

 targets = find_truncated
 if not targets:
 print("\n✅ truncated 파일 없음 — 정리 완료 상태")
 return

 print(f"\n⚠️ {len(targets)} 개 파일이 100,000행 이상 (UN Comtrade API 한도)")
 print(" = HS6 데이터가 잘려 있음. 재수집 필요.\n")

 by_dir = {}
 for p, n in targets:
 by_dir.setdefault(p.parent.name,).append((p.name, n))

 for d, files in by_dir.items:
 print(f"--- {d} ({len(files)}개) ---")
 for name, n in files:
 print(f" {name:30s} {n:>8,} 행")
 print

 print("=" * 70)
 answer = input("삭제하시겠습니까? (yes / no): ").strip.lower
 if answer not in ("yes", "y"):
 print("중단. 파일 그대로 유지.")
 return

 deleted = 0
 failed = 0
 for p, n in targets:
 try:
 p.unlink
 deleted += 1
 except Exception as e:
 print(f" ❌ {p.name}: {e}")
 failed += 1

 print(f"\n✅ 삭제 완료: {deleted} 개")
 if failed:
 print(f"❌ 실패: {failed} 개")

 # 다음 단계 안내
 print("\n다음 단계:")
 print(" python 2_scripts/data_collection/06_comtrade_refetch_chunked.py")
 print(" → HS 2자리 챕터별로 쪼개서 재수집 (API truncate 회피)")

if __name__ == "__main__":
 main
