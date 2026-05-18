"""
Phase 2-B Step 2 — Baseline shares 1994 build (initial draft)
================================================================

목표: h_code × KSIC4 → s_{hk, 1994} (시군구 내 KSIC4 산업의 종사자 비중)

Schema (probe v2 결과):
- col 0 = 시도 (2-digit)
- col 1 = 시군구 (3-digit)
- col 3 = KSIC 대분류 (1-letter)
- col 4 = KSIC 중분류 (2-digit)
- col 5 = KSIC 소분류 (1-digit)
- col 14 = 종사자 추정 (positive 94%, max 33524) ← **검증 대상**

cross-check (script 종료 시):
1. 1995 한국통계연감 제조업 종사자 약 290만명 → 본 build 의 D-only sum 과 비교
2. 미매칭 시군구 (5%) 의 sido 분포

산출:
- `3_derived/bartik/baseline_shares_1994_manufacturing.parquet`
  (h_code × KSIC4 long format with employment + share)
- `3_derived/bartik/baseline_shares_1994_all_industries.parquet`
  (전 산업 변형, 비교용)
- `5_logs/integrity_checks/<date>_baseline_shares_1994_validation.md`

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
RAW = PROJ / "0_raw" / "kosis_business_survey" / "microdata_1994_2024" / "1994_연간자료_20260415_74722.csv"
CW_PATH = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
OUT = PROJ / "3_derived" / "bartik"
LOGS = PROJ / "5_logs" / "integrity_checks"
OUT.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
TODAY = date.today().isoformat()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    log = [f"# Phase 2-B Step 2 — Baseline shares 1994 build\n_{TODAY}_\n"]

    # 1) Load
    print("[1] Load raw 1994 microdata ...")
    df = pd.read_csv(RAW, encoding="utf-8-sig", dtype=str, header=None, low_memory=False)
    log.append(f"- raw rows: **{len(df):,}**")

    # 2) Build keys
    df["sido"] = df[0].astype(str).str.zfill(2)
    df["sgg"] = df[1].astype(str).str.zfill(3)
    df["raw_code"] = df["sido"] + df["sgg"]
    df["ksic_letter"] = df[3].astype(str).str.strip()
    df["ksic_2"] = df[4].astype(str).str.zfill(2)
    df["ksic_3"] = df[5].astype(str).str.strip()
    df["ksic4"] = df["ksic_letter"] + df["ksic_2"] + df["ksic_3"]
    # employment candidate (col 14)
    df["emp_c14"] = pd.to_numeric(df[14], errors="coerce")
    # secondary candidate (col 11) for cross-check
    df["emp_c11"] = pd.to_numeric(df[11], errors="coerce")

    # 3) sigungu crosswalk → h_code (1997 baseline)
    print("[2] sigungu crosswalk match ...")
    cw = pd.read_csv(CW_PATH, dtype=str)
    cw_1997 = cw[cw["year"] == "1997"][["raw_code", "h_code", "sido_code"]].drop_duplicates("raw_code")
    df = df.merge(cw_1997, on="raw_code", how="left")
    n_match = df["h_code"].notna().sum()
    log.append(f"- sigungu match (1997 baseline): **{n_match:,}/{len(df):,}** ({n_match/len(df):.1%})")
    log.append(f"- 미매칭 raw_code distinct: {df.loc[df['h_code'].isna(), 'raw_code'].nunique()}")
    unmatch_sample = df.loc[df["h_code"].isna(), "raw_code"].value_counts().head(10).to_dict()
    log.append(f"- 미매칭 top 10 raw_code: {unmatch_sample}")

    # 4) drop unmatched
    df_m = df.dropna(subset=["h_code"]).copy()
    log.append(f"- after drop unmatched: {len(df_m):,}")

    # 5) Manufacturing-only filter (KSIC 대분류 D)
    df_d = df_m[df_m["ksic_letter"] == "D"].copy()
    log.append(f"\n## Manufacturing (D) 만\n- rows: **{len(df_d):,}** (전체의 {len(df_d)/len(df_m):.1%})")

    # 6) Aggregate: h_code × ksic4 → sum(emp)
    log.append("\n## Cross-check: 종사자 컬럼 후보별 전국 sum")
    for col in ["emp_c14", "emp_c11"]:
        s = df_d[col].sum()
        log.append(f"- {col} 전국 합 (D only): {s:,.0f}")
    log.append("- *cross-check anchor*: 1995 한국통계연감 제조업 종사자 ≈ 2,900,000")

    # build agg with col 14 primary
    EMP_COL = "emp_c14"
    agg = (
        df_d.groupby(["h_code", "ksic4"])[EMP_COL]
        .sum()
        .reset_index()
        .rename(columns={EMP_COL: "employment"})
    )
    log.append(f"\n- agg rows (h_code × KSIC4): {len(agg):,}")
    log.append(f"- distinct h_code: {agg['h_code'].nunique()}")
    log.append(f"- distinct KSIC4: {agg['ksic4'].nunique()}")

    # 7) within-h_code share
    h_total = agg.groupby("h_code")["employment"].sum().rename("h_total")
    agg = agg.merge(h_total, on="h_code")
    agg["share"] = agg["employment"] / agg["h_total"].replace(0, np.nan)
    log.append(f"- share NaN rows: {agg['share'].isna().sum()} (h_total=0 시군구)")

    # 8) save manufacturing
    out_m = OUT / "baseline_shares_1994_manufacturing.parquet"
    agg.to_parquet(out_m, index=False)
    log.append(f"\n- saved: `{out_m.relative_to(PROJ)}`")

    # 9) all industries variant (for sensitivity)
    df_all = df_m.copy()
    agg_all = (
        df_all.groupby(["h_code", "ksic4"])[EMP_COL]
        .sum()
        .reset_index()
        .rename(columns={EMP_COL: "employment"})
    )
    h_total_all = agg_all.groupby("h_code")["employment"].sum().rename("h_total")
    agg_all = agg_all.merge(h_total_all, on="h_code")
    agg_all["share"] = agg_all["employment"] / agg_all["h_total"].replace(0, np.nan)
    out_a = OUT / "baseline_shares_1994_all_industries.parquet"
    agg_all.to_parquet(out_a, index=False)
    log.append(f"- saved: `{out_a.relative_to(PROJ)}`")

    log.append(f"- all-industry rows: {len(agg_all):,}, distinct KSIC4: {agg_all['ksic4'].nunique()}")

    # 10) validation table (top KSIC4 by employment, manufacturing)
    log.append("\n## Top 20 KSIC4 (제조업, 종사자 sum)")
    top20 = (
        df_d.groupby("ksic4")[EMP_COL]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )
    log.append("```")
    log.append(top20.to_string(index=False))
    log.append("```")

    # 11) sido-level employment for validation
    log.append("\n## 시도별 제조업 종사자 (cross-check with 1995 통계연감)")
    df_d2 = df_d.merge(cw_1997[["raw_code", "sido_code"]].drop_duplicates("raw_code"), on="raw_code", how="left", suffixes=("", "_dup"))
    by_sido = df_d2.groupby("sido")[EMP_COL].sum().sort_values(ascending=False)
    log.append("```")
    log.append(by_sido.to_string())
    log.append("```")
    log.append(f"- 전국 합 (D only, col 14): **{df_d[EMP_COL].sum():,.0f}**")

    # 12) decision
    log.append("\n## 결정 사항")
    nat_sum = df_d[EMP_COL].sum()
    if 2_500_000 <= nat_sum <= 3_500_000:
        log.append(f"- ✅ **col 14 = 종사자 수 확정** (전국 합 {nat_sum:,.0f} ≈ 1995 통계연감 290만)")
    elif nat_sum < 100_000:
        log.append(f"- ⚠️ col 14 합 너무 작음 ({nat_sum:,.0f}) — 매출액 또는 다른 단위? col 11 시도 필요")
    elif nat_sum > 10_000_000:
        log.append(f"- ⚠️ col 14 합 너무 큼 ({nat_sum:,.0f}) — 단위 미상, codebook 확인 필요")
    else:
        log.append(f"- ⚠️ col 14 합 ({nat_sum:,.0f}) borderline — codebook 으로 확정 필요")

    out_log = LOGS / f"{TODAY}_baseline_shares_1994_validation.md"
    out_log.write_text("\n".join(log), encoding="utf-8")
    print(f"[OK] {out_log}")


if __name__ == "__main__":
    main()
