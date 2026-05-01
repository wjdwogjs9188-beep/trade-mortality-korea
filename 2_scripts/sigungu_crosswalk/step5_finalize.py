"""
Step 5 — 최종 crosswalk 산출물 작성

Outputs:
  1_codebooks/sigungu_crosswalk.csv       (final per-year mapping for joining)
  1_codebooks/sigungu_changes_history.md  (human-readable change log)
"""
from __future__ import annotations
import sys
import io
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
DERIVED = ROOT / "3_derived" / "sigungu"
OUT_CSV = ROOT / "1_codebooks" / "sigungu_crosswalk.csv"
OUT_MD = ROOT / "1_codebooks" / "sigungu_changes_history.md"


def main() -> None:
    src = DERIVED / "step3_h_code_mapping.csv"
    df = pd.read_csv(src)

    # Final column order, types
    df = df[["year", "raw_code", "h_code", "h_name", "sido_code", "sido_name", "event_note"]]
    df["year"] = df["year"].astype(int)
    df["raw_code"] = df["raw_code"].astype(int)
    df["h_code"] = df["h_code"].astype(int)
    df["sido_code"] = df["sido_code"].astype(int)
    df["event_note"] = df["event_note"].fillna("")
    df = df.sort_values(["year", "sido_code", "h_code", "raw_code"]).reset_index(drop=True)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"[step5] wrote: {OUT_CSV} ({len(df):,} rows)")

    # Changes history
    notes = df[df["event_note"] != ""].copy()
    # Compress to one row per (raw_code, event_note, h_code)
    g = (
        notes.groupby(["raw_code", "h_code", "h_name", "sido_code", "sido_name", "event_note"])
        .agg(year_min=("year", "min"), year_max=("year", "max"))
        .reset_index()
        .sort_values(["sido_code", "raw_code"])
    )

    lines: list[str] = []
    add = lines.append
    add("# 시군구 행정 변경 이력 (1997-2023)")
    add("")
    add(
        "본 crosswalk 가 반영하는 합병/승격/개칭/cross-sido 이벤트 목록. "
        "h_code = 2021 KOSTAT baseline 기준 stable panel ID. "
        "행 단위 raw_code → h_code 매핑은 `sigungu_crosswalk.csv` 참조."
    )
    add("")
    add(f"총 이벤트 (raw_code 기준): **{len(g):,}**")
    add("")
    add("| sido | raw_code | h_code | h_name | year range | event |")
    add("|------|---------:|-------:|--------|------------|-------|")
    for _, row in g.iterrows():
        add(
            f"| {int(row.sido_code)} {row.sido_name} "
            f"| {int(row.raw_code)} | {int(row.h_code)} | {row.h_name} "
            f"| {int(row.year_min)}-{int(row.year_max)} | {row.event_note} |"
        )
    add("")
    add("## h_code 정의 정책 요약")
    add("")
    add(
        "1. **2021 KOSTAT baseline (262 entries) = h_code 기준 셋**\n"
        "2. 1997-2021 raw_code 가 2021 baseline 에 존재하면 `h_code = raw_code`.\n"
        "3. 2021 baseline 에 없는 pre-2021 raw_code (29건) — 위 표대로 successor entity 의 2021 코드로 매핑.\n"
        "4. 2022 raw_code = 2021 raw_code (forward-fill, 100% 매칭).\n"
        "5. 2023 raw_code (KOSTAT 코드집 별도 수신) — 2021 baseline 과 within-sido sigungu 명칭으로 매칭.\n"
        "   - 군 (county) 256건은 raw_code 이 +200 일괄 renumber → h_code 는 2021 코드 유지.\n"
        "   - 군위군 (경북→대구 2023.7.1): h_code 37310 유지, sido_code 만 2023부터 22.\n"
        "   - 미추홀구/세종/통합청주시/통합창원시: 명칭 normalization 으로 매칭.\n"
        "6. 2023 sido name override: 강원도 → 강원특별자치도 (2023.6.11 변경).\n"
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[step5] wrote: {OUT_MD}")

    # Summary stats
    print(f"[step5] year range: {df.year.min()}-{df.year.max()}")
    print(f"[step5] distinct h_code: {df.h_code.nunique()}")
    print(f"[step5] distinct sido_code: {sorted(df.sido_code.unique().tolist())}")
    print(f"[step5] event rows: {len(notes):,} / total {len(df):,}")


if __name__ == "__main__":
    main()
