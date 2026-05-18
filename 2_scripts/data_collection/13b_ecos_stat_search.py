"""
ECOS 정확 stat 코드 발견용 probe.

lib.ecos_api 의 list_tables / search_table_by_keyword 활용.
키워드: 국내총생산, 수출물가, 수입물가 → 실제 가용 stat 목록 출력.

산출:
  5_logs/data_collection/<date>_phase1_ecos_stat_search.md
"""
from __future__ import annotations
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import LOGS_DIR, ECOS_API_KEY, assert_api_key
from lib.ecos_api import list_tables

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LOG = LOGS_DIR / "data_collection" / f"{datetime.now():%Y-%m-%d}_phase1_ecos_stat_search.md"

KEYWORDS = ["국내총생산", "GDP", "수출물가", "수입물가", "물가지수"]


def main():
    assert_api_key("ECOS", ECOS_API_KEY)
    LOG.parent.mkdir(parents=True, exist_ok=True)

    # 전체 통계표 목록 (1-2000)
    print("[fetch] ECOS 통계표 목록 (1-2000)", flush=True)
    df = list_tables(1, 2000)
    print(f"  loaded {len(df)} tables", flush=True)

    # 컬럼 확인
    print(f"\n=== columns: {list(df.columns)}")

    # 표명 컬럼
    name_col = None
    for c in ["STAT_NAME", "TBL_NAME", "STAT_NM", "STAT_KOR_NAME"]:
        if c in df.columns:
            name_col = c
            break
    code_col = None
    for c in ["STAT_CODE", "TBL_ID", "STAT_ID"]:
        if c in df.columns:
            code_col = c
            break
    cycle_col = None
    for c in ["CYCLE", "P_CYCLE", "CYCLE_NM", "PRD_SE"]:
        if c in df.columns:
            cycle_col = c
            break
    print(f"  name_col={name_col}, code_col={code_col}, cycle_col={cycle_col}")

    log = [f"# Phase 1.2 — ECOS stat code 검색\n", f"_{datetime.now().isoformat()}_\n\n"]
    log.append(f"전체 통계표: {len(df)} 개\n")
    log.append(f"key columns: name=`{name_col}`, code=`{code_col}`, cycle=`{cycle_col}`\n\n")

    for kw in KEYWORDS:
        if not name_col:
            print(f"  [skip] name_col 없음")
            break
        match = df[df[name_col].astype(str).str.contains(kw, na=False)]
        print(f"\n=== '{kw}' 매칭: {len(match)}")
        log.append(f"## 키워드: '{kw}' — {len(match)} 매칭\n\n")
        if match.empty:
            log.append(f"(없음)\n\n")
            continue
        cols_show = [c for c in [code_col, name_col, cycle_col] if c]
        # 출력
        for _, row in match.head(15).iterrows():
            code = row.get(code_col, "")
            name = row.get(name_col, "")
            cycle = row.get(cycle_col, "")
            print(f"  {code} | {cycle} | {name}")
            log.append(f"- `{code}` | {cycle} | {name}\n")
        if len(match) > 15:
            log.append(f"- ... 외 {len(match)-15}개 더\n")
        log.append("\n")

    LOG.write_text("".join(log), encoding="utf-8")
    print(f"\n[log] {LOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
