"""KOSIS 인구 panel 모든 파일 강제 삭제 (UI 다운로드 전 정리).

이전 cleanup 로직이 truncated 파일을 못 잡아서, 모든 31개 파일 + combined 파일 일괄 삭제.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import RAW_DIR

OUT_DIR = RAW_DIR / "kosis_population"
files = sorted(OUT_DIR.glob("*.csv"))

print(f"=== KOSIS 인구 panel 강제 cleanup ===")
print(f"위치: {OUT_DIR}")
print(f"발견된 csv: {len(files)} 개\n")
for f in files[:5]:
    print(f"  - {f.name}")
if len(files) > 5:
    print(f"  ... 외 {len(files) - 5} 개")

print("\n⚠️ 이 파일들은 모두 truncated 상태 (서울 5개 자치구만 포함).")
print("   KOSIS UI 에서 새로 다운로드 받기 위해 일괄 삭제.\n")

ans = input("정말 삭제하시겠습니까? (yes / no): ").strip().lower()
if ans not in ("yes", "y"):
    print("중단.")
    sys.exit()

deleted = 0
for f in files:
    try:
        f.unlink()
        deleted += 1
    except Exception as e:
        print(f"  ❌ {f.name}: {e}")
print(f"\n✅ {deleted}/{len(files)} 개 삭제 완료")
print("\n다음 단계: KOSIS UI 에서 데이터 다운로드 후 위 폴더에 저장")
print("   URL: https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B040M5")
