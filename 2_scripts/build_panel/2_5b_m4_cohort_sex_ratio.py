"""Phase 2 sub-task 2.5b -- M4 cohort sex ratio (z_m_marital) ETL.

Source: 3_derived/sigungu/cohort_sex_ratio_1995_v01.csv (1995 census, cohorts 0-4 + 5-9)
The 1995 census provides pre-determined birth-cohort sex ratios at the
sigungu level. These cohorts (born 1986-1995) are pre-determined relative to
the trade-shock window (2000-2010), so they serve as effect-modifier
candidates rather than time-varying mediators.

Output: m4_z_marital_pre.parquet with columns
  h_code, cohort_sex_ratio_1995, z_m_marital
(cohort_sex_ratio_1975 / 1985 columns are placeholders; only 1995 census
data is presently available in 3_derived/sigungu/.)
"""
import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
DERIVED = PROJ / "3_derived"


def main():
    src = PROJ / "3_derived" / "sigungu" / "cohort_sex_ratio_1995_v01.csv"
    print(f"[step1] read {src.name}")
    df = pd.read_csv(src)
    print(f"  rows={len(df)}, h_codes={df['h_code'].nunique()}, cohorts={df['cohort'].unique().tolist()}")

    print("\n[step2] aggregate sex ratio by sigungu (pool both cohorts)")
    agg = (
        df.groupby("h_code", as_index=False)
        .agg(pop_male=("pop_male", "sum"), pop_female=("pop_female", "sum"))
    )
    agg["cohort_sex_ratio_1995"] = (
        agg["pop_male"] / np.maximum(agg["pop_female"], 1.0)
    ) * 100.0

    # Per-cohort columns (for sensitivity)
    pivot = df.pivot_table(
        index="h_code",
        columns="cohort",
        values=["pop_male", "pop_female"],
        aggfunc="sum",
    )
    pivot.columns = [f"{a}_{b}" for a, b in pivot.columns]
    pivot = pivot.reset_index()
    if "pop_male_0-4" in pivot.columns and "pop_female_0-4" in pivot.columns:
        pivot["cohort_sex_ratio_1995_0_4"] = (
            pivot["pop_male_0-4"] / np.maximum(pivot["pop_female_0-4"], 1.0)
        ) * 100.0
    if "pop_male_5-9" in pivot.columns and "pop_female_5-9" in pivot.columns:
        pivot["cohort_sex_ratio_1995_5_9"] = (
            pivot["pop_male_5-9"] / np.maximum(pivot["pop_female_5-9"], 1.0)
        ) * 100.0

    out = agg.merge(
        pivot[
            [
                c
                for c in pivot.columns
                if c.startswith("cohort_sex_ratio_") or c == "h_code"
            ]
        ],
        on="h_code",
        how="left",
    )

    print("\n[step3] z-score across sigungu")
    mu = out["cohort_sex_ratio_1995"].mean()
    sigma = out["cohort_sex_ratio_1995"].std()
    out["z_m_marital"] = (out["cohort_sex_ratio_1995"] - mu) / sigma
    print(f"  cohort_sex_ratio_1995: mean={mu:.3f}, std={sigma:.3f}")
    print(f"  z_m_marital:           mean={out['z_m_marital'].mean():+.4f}, std={out['z_m_marital'].std():.4f}")

    # Placeholder for 1975 / 1985 cohort columns (currently unavailable)
    out["cohort_sex_ratio_1975"] = np.nan
    out["cohort_sex_ratio_1985"] = np.nan

    cols = [
        "h_code",
        "cohort_sex_ratio_1975",
        "cohort_sex_ratio_1985",
        "cohort_sex_ratio_1995",
        "cohort_sex_ratio_1995_0_4",
        "cohort_sex_ratio_1995_5_9",
        "z_m_marital",
    ]
    cols = [c for c in cols if c in out.columns]
    out_path = DERIVED / "m4_z_marital_pre.parquet"
    out[cols].to_parquet(out_path, index=False)
    print(f"\n[step4] written: {out_path.name} (rows={len(out)})")
    print("\n=== M4 ETL complete ===")


if __name__ == "__main__":
    main()
