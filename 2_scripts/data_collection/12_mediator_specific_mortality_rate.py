"""mediator-specific mortality rate panel build.

Numerator (mortality 5-year sum) / denominator (mediator panel population)
→ mediator-specific mortality rate (per 100,000 person-year)

5-year stack period mapping (Pierce-Schott 2020):
  period 1: 1997-2001 (mortality sum) → mediator 2000 census
  period 2: 2002-2006 → mediator 2005
  period 3: 2007-2011 → mediator 2010
  period 4: 2012-2016 → mediator 2015
  period 5: 2017-2021 → mediator 2020
  (2022-2024 incomplete period → drop)
  (1995 mediator + 1990 → 사용 안 함)

Outcome (4 deaths of despair + all_cause):
  102 = 자살, 101 = 약물, 057 = 정신, 081 = 간
  + all_cause = 위 + 나머지 cause_104 sum

Rate formula: mortality_rate = deaths_5y / (population × 5) × 100,000

산출:
  3_derived/mortality/mediator_specific_marital_rate_v01.parquet
    columns: h_code, period, census_year, sex_code, age_band,
             marital_code, cause_group, deaths_5y, population, rate_per_100k

  3_derived/mortality/mediator_specific_education_rate_v01.parquet
    동일 구조 + education_band

선행: 11b 완료 (mortality_marital/education_panel_v01)
      10/10b 완료 (mediator_panel_marriage_v02 + education_v03)

실행:
    cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
    python 2_scripts\\data_collection\\12_mediator_specific_mortality_rate.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MORT_DIR = ROOT / "3_derived" / "mortality"
POP_DIR = ROOT / "3_derived" / "population"

# 5-year stack period (mortality 5년 합) → mediator census year (가까운 5년 census)
PERIOD_MAP = {
    1: {"years": [1997, 1998, 1999, 2000, 2001], "census": 2000},
    2: {"years": [2002, 2003, 2004, 2005, 2006], "census": 2005},
    3: {"years": [2007, 2008, 2009, 2010, 2011], "census": 2010},
    4: {"years": [2012, 2013, 2014, 2015, 2016], "census": 2015},
    5: {"years": [2017, 2018, 2019, 2020, 2021], "census": 2020},
}

# Deaths of despair cause_104 (paper § 4 outcome)
DEATHS_OF_DESPAIR = {
    "102": "suicide",      # 자살
    "101": "drug",         # 약물
    "057": "psych",        # 정신질환 (F10-F19 alcohol/drug etc)
    "081": "liver",        # 간질환 (alcoholic + viral)
}


def build_rate_panel(num: pd.DataFrame, den: pd.DataFrame, dim_col: str,
                     panel_label: str) -> pd.DataFrame:
    """numerator (deaths) + denominator (population) → mediator-specific rate."""
    print(f"\n[{panel_label}] build rate panel")

    # ─── Step 1: cause_group classification ───
    # deaths of despair 4 outcome + "all_cause" + "other" (그 외)
    num = num.copy()
    num["cause_group"] = num["cause_104"].map(DEATHS_OF_DESPAIR).fillna("other")

    # ─── Step 2: numerator 5-year sum by period ───
    num_periods_list = []
    for period, cfg in PERIOD_MAP.items():
        sub = num[num["year"].isin(cfg["years"])].copy()
        if sub.empty:
            print(f"  [skip period {period}] 0 rows")
            continue
        agg = (sub.groupby(["h_code", "sex_code", "age_band", dim_col, "cause_group"],
                           observed=True)["deaths"].sum().reset_index())
        agg["period"] = period
        agg["census_year"] = cfg["census"]
        num_periods_list.append(agg)
        print(f"  period {period} ({cfg['years'][0]}-{cfg['years'][-1]}): "
              f"{len(agg):,} cells, deaths {agg['deaths'].sum():,}")

    num_periods = pd.concat(num_periods_list, ignore_index=True)

    # 추가 all_cause (4 outcome + other 합계)
    print(f"  building all_cause aggregate ...")
    all_cause = (num_periods.groupby(
        ["h_code", "period", "census_year", "sex_code", "age_band", dim_col],
        observed=True)["deaths"].sum().reset_index())
    all_cause["cause_group"] = "all_cause"
    num_periods = pd.concat([num_periods, all_cause], ignore_index=True)

    # ─── Step 3: denominator at census year ───
    den = den.copy()
    den["year"] = pd.to_numeric(den["year"], errors="coerce").astype("Int64")

    den_periods_list = []
    for period, cfg in PERIOD_MAP.items():
        sub = den[den["year"] == cfg["census"]].copy()
        if sub.empty:
            print(f"  [skip denom period {period}] census {cfg['census']} 부재")
            continue
        sub = sub[["h_code", "sex_code", "age_band", dim_col, "population"]].copy()
        sub["period"] = period
        sub["census_year"] = cfg["census"]
        den_periods_list.append(sub)
        print(f"  denom period {period} (census {cfg['census']}): "
              f"{len(sub):,} cells, pop {sub['population'].sum():,.0f}")

    den_periods = pd.concat(den_periods_list, ignore_index=True)

    # ─── Step 4: merge ───
    print(f"  merging numerator + denominator ...")
    merged = num_periods.merge(
        den_periods,
        on=["h_code", "period", "census_year", "sex_code", "age_band", dim_col],
        how="left"
    )

    n_no_denom = merged["population"].isna().sum()
    print(f"  merge: {len(merged):,} rows, denom missing: {n_no_denom:,} "
          f"({100*n_no_denom/len(merged):.2f}%)")

    # ─── Step 5: rate = deaths_5y / (pop × 5) × 100,000 ───
    merged["population"] = merged["population"].fillna(0)
    valid = merged["population"] > 0
    merged["rate_per_100k"] = np.nan
    merged.loc[valid, "rate_per_100k"] = (
        merged.loc[valid, "deaths"] / (merged.loc[valid, "population"] * 5) * 100_000
    )

    # column rename + sort
    merged = merged.rename(columns={"deaths": "deaths_5y"})
    merged = merged[[
        "h_code", "period", "census_year", "sex_code", "age_band", dim_col,
        "cause_group", "deaths_5y", "population", "rate_per_100k"
    ]].sort_values(["h_code", "period", "sex_code", "age_band", dim_col, "cause_group"]
                   ).reset_index(drop=True)

    return merged


def main() -> int:
    print("=" * 70)
    print("12: mediator-specific mortality rate panel build")
    print("=" * 70)

    # Load 4 panel
    print("\n[load] 4 panel")
    num_mar = pd.read_parquet(MORT_DIR / "mortality_marital_panel_v01.parquet")
    num_edu = pd.read_parquet(MORT_DIR / "mortality_education_panel_v01.parquet")
    den_mar = pd.read_parquet(POP_DIR / "mediator_panel_marriage_v02.parquet")
    den_edu = pd.read_parquet(POP_DIR / "mediator_panel_education_v03.parquet")

    print(f"  num_mar: {len(num_mar):,} rows, h_code {num_mar['h_code'].nunique()}, "
          f"years {num_mar['year'].min()}-{num_mar['year'].max()}")
    print(f"  num_edu: {len(num_edu):,} rows, h_code {num_edu['h_code'].nunique()}")
    print(f"  den_mar: {len(den_mar):,} rows, h_code {den_mar['h_code'].nunique()}, "
          f"years {sorted(den_mar['year'].unique())}")
    print(f"  den_edu: {len(den_edu):,} rows, h_code {den_edu['h_code'].nunique()}")

    # Build marriage rate panel
    rate_mar = build_rate_panel(num_mar, den_mar, "marital_code", "MARITAL")
    out_mar = MORT_DIR / "mediator_specific_marital_rate_v01.parquet"
    rate_mar.to_parquet(out_mar, index=False)
    print(f"\n[save] {out_mar.name}")
    print(f"  rows: {len(rate_mar):,}, size: {out_mar.stat().st_size/1024:.2f} KB")

    # Build education rate panel
    rate_edu = build_rate_panel(num_edu, den_edu, "education_band", "EDUCATION")
    out_edu = MORT_DIR / "mediator_specific_education_rate_v01.parquet"
    rate_edu.to_parquet(out_edu, index=False)
    print(f"\n[save] {out_edu.name}")
    print(f"  rows: {len(rate_edu):,}, size: {out_edu.stat().st_size/1024:.2f} KB")

    # ─── Validation summary ───
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    for label, df in [("MARITAL", rate_mar), ("EDUCATION", rate_edu)]:
        print(f"\n[{label}] rate per 100K by cause_group × period (mean across cells):")
        # cause_group × period 별 mean rate
        ct = df.groupby(["period", "cause_group"], observed=True).agg(
            cells=("rate_per_100k", "size"),
            valid=("rate_per_100k", lambda x: x.notna().sum()),
            mean_rate=("rate_per_100k", "mean"),
            total_deaths=("deaths_5y", "sum"),
            total_pop=("population", "sum"),
        ).reset_index()
        ct["overall_rate"] = ct["total_deaths"] / (ct["total_pop"] * 5) * 100_000
        print(ct.to_string(index=False))

    # 4 outcome 별 시계열 (전체)
    print(f"\n[deaths of despair 4 outcome 시계열] (marital panel, all cells aggregated):")
    dod_ts = (rate_mar[rate_mar["cause_group"].isin(["suicide", "drug", "psych", "liver"])]
              .groupby(["period", "cause_group"], observed=True)
              .agg(deaths=("deaths_5y", "sum"), pop=("population", "sum")).reset_index())
    dod_ts["rate"] = dod_ts["deaths"] / (dod_ts["pop"] * 5) * 100_000
    pivot = dod_ts.pivot(index="period", columns="cause_group", values="rate")
    print(pivot.round(2).to_string())

    print("\n" + "=" * 70)
    print("완료. Stage 5 진입 가능:")
    print("  - mediator-specific rate panel = paper § 5.2 mediation regression input")
    print("  - DGHP 2017 ivmediate (Stata) 의 mediator outcome 으로 사용")
    print("  - 본 panel + Bartik IV (Stage 4 완료 후) 결합 → main analysis")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
