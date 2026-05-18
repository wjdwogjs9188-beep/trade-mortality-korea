"""
Phase 2-B Step 1b — 1994 광업제조업조사 재 schema probe (header=None)
========================================================================

v1 결과: 첫 row 가 header 로 read 되어 컬럼명이 깨짐.
v2: header=None 으로 재 read, 컬럼별 unique 값 / 길이 / suppression rate 검증.

핵심 question:
1) 시도·시군구·KSIC·종사자 컬럼 위치 (정수 인덱스로 식별)
2) `*` / `**` / `****` 가 suppression flag 인지 placeholder 인지 → suppression rate
3) suppression rate 가 50% 이상이면 baseline shares 계산 불가 → 다른 baseline 필요
4) sido + sigungu 결합 시 5-digit 가 sigungu_crosswalk 와 매칭되는지

산출:
- `5_logs/integrity_checks/<date>_business_survey_1994_schema_v2.md`

Author: R-A
Date  : 2026-05-04
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
RAW_DIR = PROJ / "0_raw" / "kosis_business_survey" / "microdata_1994_2024"
LOGS = PROJ / "5_logs" / "integrity_checks"
LOGS.mkdir(parents=True, exist_ok=True)
TODAY = date.today().isoformat()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    log = [f"# Phase 2-B Step 1b — 1994 광업제조업조사 schema v2 (header=None)\n_{TODAY}_\n"]

    files = sorted(RAW_DIR.glob("1994*.csv"))
    f = files[0]
    log.append(f"## File: `{f.name}` ({f.stat().st_size/1024**2:.1f} MB)\n")

    # header=None 으로 재 read
    df = pd.read_csv(f, encoding="utf-8-sig", dtype=str, header=None, low_memory=False)
    log.append(f"- shape (header=None): **{df.shape}**")
    log.append(f"- columns: {list(df.columns)}\n")

    # 첫 5 rows
    log.append("## 첫 10 rows (정수 컬럼 인덱스)\n```")
    log.append(df.head(10).to_string())
    log.append("```\n")

    # 컬럼별 진단
    log.append("## 컬럼별 unique·suppression·길이 분석\n")
    log.append("| col | distinct | top 5 values | suppression rate (`*`/`**`/`***`) | length distribution |")
    log.append("|-----|----------|--------------|------------------------------------|---------------------|")
    for c in df.columns:
        s = df[c].astype(str).str.strip()
        n_unique = s.nunique()
        top5 = s.value_counts().head(5).to_dict()
        # suppression markers
        sup_mask = s.str.fullmatch(r"\*+")
        sup_rate = sup_mask.mean()
        len_dist = s.str.len().value_counts().sort_index().to_dict()
        # truncate top5 dict for display
        top5_str = ", ".join([f"{k}:{v}" for k, v in list(top5.items())[:5]])
        log.append(f"| {c} | {n_unique} | {top5_str} | {sup_rate:.1%} | {len_dist} |")

    log.append("")
    # numeric column candidates (low suppression)
    log.append("## 숫자 컬럼 후보 (suppression rate < 30%)\n")
    for c in df.columns:
        s = df[c].astype(str).str.strip()
        sup_rate = s.str.fullmatch(r"\*+").mean()
        if sup_rate < 0.3:
            num = pd.to_numeric(s.replace("*", np.nan).replace("**", np.nan), errors="coerce")
            n_num = num.notna().sum()
            if n_num > len(df) * 0.5:
                log.append(f"- col {c}: numeric ratio={n_num/len(df):.1%}, "
                           f"min={num.min():.0f}, max={num.max():.0f}, "
                           f"mean={num.mean():.1f}, median={num.median():.0f}")

    # 시도 코드 cross-check (col 0 should be 2-digit, 17 distinct)
    log.append("\n## 시도 코드 검증 (col 0 가정)")
    sido = df[0].astype(str).str.strip()
    log.append(f"- distinct: {sido.nunique()} (기대 17 또는 16)")
    log.append(f"- top values: {sido.value_counts().head(20).to_dict()}")
    sido_lengths = sido.str.len().value_counts().to_dict()
    log.append(f"- length distribution: {sido_lengths}")

    # 시군구 코드 cross-check (col 1 should be 3-digit)
    log.append("\n## 시군구 코드 검증 (col 1 가정)")
    sgg = df[1].astype(str).str.strip()
    log.append(f"- distinct: {sgg.nunique()}")
    log.append(f"- top values: {sgg.value_counts().head(20).to_dict()}")
    sgg_lengths = sgg.str.len().value_counts().to_dict()
    log.append(f"- length distribution: {sgg_lengths}")

    # 시도+시군구 결합 후 sigungu_crosswalk 매핑 시도
    log.append("\n## 시도+시군구 결합 → h_code crosswalk 매핑 (1997 raw_code 와)")
    combined = (sido.str.zfill(2) + sgg.str.zfill(3))
    log.append(f"- combined 5-digit distinct: {combined.nunique()}")
    cw_path = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
    if cw_path.exists():
        cw = pd.read_csv(cw_path, dtype=str)
        cw_1997 = cw[cw["year"] == "1997"]
        # try direct match
        match_n = combined.isin(cw_1997["raw_code"]).sum()
        log.append(f"- combined 가 1997 crosswalk raw_code 와 매칭되는 row: **{match_n:,}/{len(df):,}** ({match_n/len(df):.1%})")
        log.append(f"- 1997 crosswalk distinct raw_code: {cw_1997['raw_code'].nunique()}")
        # 시도+시군구 unique 중 미매칭
        unmatched = sorted(set(combined.unique()) - set(cw_1997["raw_code"].unique()))
        log.append(f"- 미매칭 1994 시도+시군구 코드 (top 20): {unmatched[:20]}")
    else:
        log.append("- ⚠️ crosswalk 미존재")

    # KSIC 대분류 cross-check (col 3)
    log.append("\n## KSIC 대분류 (col 3 가정)")
    ksic1 = df[3].astype(str).str.strip()
    log.append(f"- distinct: {ksic1.nunique()}")
    log.append(f"- distribution: {ksic1.value_counts().head(10).to_dict()}")

    # KSIC 중분류 (col 4) + 소분류 (col 5)
    log.append("\n## KSIC 중분류·소분류 (cols 4-5 가정)")
    ksic2 = df[4].astype(str).str.strip()
    ksic3 = df[5].astype(str).str.strip()
    log.append(f"- col 4 distinct: {ksic2.nunique()}, top: {ksic2.value_counts().head(10).to_dict()}")
    log.append(f"- col 5 distinct: {ksic3.nunique()}, top: {ksic3.value_counts().head(10).to_dict()}")
    # KSIC 4-digit 결합 가능성: 알파 + 2자 + 1자 + ?
    ksic_combined_3 = (ksic1 + ksic2.str.zfill(2) + ksic3.str.zfill(1))
    log.append(f"- 결합 (대중소, 4-char): distinct = {ksic_combined_3.nunique()}, sample: {ksic_combined_3.head(5).tolist()}")

    # 종사자 후보 — col 2 (51 sample) 또는 numeric col 6+
    log.append("\n## 종사자 후보 진단 (col 2 와 col 6+)")
    for c in [2] + list(range(6, df.shape[1])):
        if c >= df.shape[1]:
            break
        s = df[c].astype(str).str.strip()
        sup = s.str.fullmatch(r"\*+").mean()
        num = pd.to_numeric(s, errors="coerce")
        n_num = num.notna().sum()
        n_pos = (num > 0).sum()
        log.append(f"- col {c}: suppress={sup:.1%}, numeric={n_num/len(df):.1%}, "
                   f"positive={n_pos/len(df):.1%}, "
                   f"min={num.min() if n_num else 'NA'}, max={num.max() if n_num else 'NA'}, "
                   f"median={num.median() if n_num else 'NA'}")

    # decision 다음 step
    log.append("\n## 다음 step 결정 사항\n")
    log.append("- [ ] 시도·시군구 결합 매핑률 확인 (위 결과로 결정)")
    log.append("- [ ] KSIC 4-digit 구성 방법 (대분류+중분류+소분류 vs 별도 4자리 컬럼)")
    log.append("- [ ] 종사자 컬럼 확정 (suppression rate 가 가장 낮은 numeric)")
    log.append("- [ ] suppression rate 가 50% 초과 시 baseline 후보 변경 (1999 census 또는 KOSIS 시군구 집계)")

    out = LOGS / f"{TODAY}_business_survey_1994_schema_v2.md"
    out.write_text("\n".join(log), encoding="utf-8")
    print(f"[OK] {out}")


if __name__ == "__main__":
    main()
