"""
Phase 0 — WEO Historical Forecasts xlsx 를 0_raw/imf_weo_korea_vintage/ 로 배치.

업로드 위치 (Cowork uploads/) 가 priority. 없으면 Downloads 또는 Desktop 시도.
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# project lib
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import RAW_DIR, LOGS_DIR

DEST = RAW_DIR / "imf_weo_korea_vintage"
LOG  = LOGS_DIR / "data_collection" / f"{datetime.now():%Y-%m-%d}_phase0_weo.md"

CANDIDATES = [
    Path(r"C:\Users\82103\AppData\Roaming\Claude\local-agent-mode-sessions\b2ac566b-eb8a-4089-82f5-2f6381cd4f6d\56af0025-aff0-4142-af78-7fd57175e97e\local_eb4f92d2-4def-433d-b666-e29cab4bb99b\uploads\WEOhistorical.xlsx"),
    Path(r"C:\Users\82103\Downloads\WEOhistorical.xlsx"),
    Path(r"C:\Users\82103\Desktop\WEOhistorical.xlsx"),
    Path(r"C:\Users\82103\Documents\WEOhistorical.xlsx"),
]

def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)

    target = DEST / "WEOhistorical.xlsx"
    if target.exists():
        size = target.stat().st_size
        msg = f"[skip] 이미 존재: {target} ({size:,} bytes)"
        print(msg)
        LOG.write_text(f"# Phase 0 — WEO 배치 (skip)\n\n{msg}\n", encoding="utf-8")
        return 0

    for src in CANDIDATES:
        if src.exists():
            shutil.copy2(src, target)
            size = target.stat().st_size
            msg = (
                f"# Phase 0 — WEO 배치 ✅\n\n"
                f"- src: `{src}`\n"
                f"- dst: `{target}`\n"
                f"- size: {size:,} bytes\n"
                f"- timestamp: {datetime.now().isoformat()}\n"
            )
            print(f"[OK] {src} -> {target} ({size:,} bytes)")
            LOG.write_text(msg, encoding="utf-8")
            return 0

    err = (
        f"[ERROR] WEOhistorical.xlsx 를 찾을 수 없음. 시도한 경로:\n"
        + "\n".join(f"  - {p}" for p in CANDIDATES)
        + f"\n\n수동: 아무 위치에서 다음으로 복사:\n  {target}\n"
    )
    print(err)
    LOG.write_text(f"# Phase 0 — WEO 배치 ❌\n\n{err}\n", encoding="utf-8")
    return 1

if __name__ == "__main__":
    sys.exit(main())
