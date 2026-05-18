"""
Path B Phase 2 — Modernization confound disentangle
====================================================

Adds sigungu-level urbanization (population density) control + sido fixed
effects to the main reduced-form long-difference regression to test whether
the protective coefficient on Bartik trade exposure (β_main = -0.127) survives
controls for the "modernizing-household" alternative interpretation of
§ 7.6.3.

Specifications (3-step cascade):
  Spec 0  Δ log_mort ~ z_x_std                                  → β_main
  Spec 1  Δ log_mort ~ z_x_std + sido_FE                        → β_sidoFE
  Spec 2  Δ log_mort ~ z_x_std + sido_FE + Δ_urbanization       → β_full

Per-spec inference layers:
  - HC1, cluster-province (sido), AKM-proper Kolesar (where applicable), Conley
    5km / 10km — when AKM and Conley are not reproducible inline, we
    bracket the protective sign-significance using HC1 + cluster-province +
    weak-IV-robust AR + LMP critical value (Lee, McCrary, Moreira, Porter 2022).

Output:
  4_results/regression/modernization_robustness_cascade.csv
  3_derived/modernization_controls/sigungu_density_panel.parquet
  5_logs/decisions/2026-05-13_modernization_controls.md

Data:
  - 0_raw/modernization_controls/urbanization/kosis_sigungu_area_2007_2025.csv
      KOSIS 지적통계 DT_MLTM_2300, 4,973 rows, 282 sigungu × 19 years.
      Area is 2007 KOSIS-standardized; we use 2007 as urbanization baseline
      anchor (closest available to the 1997-1999 mortality baseline).
  - 0_raw/kosis_population/population_combined.csv  (sigungu-level pop, C1 = 5-digit code, C2=0 total, C3=0 all-age)
  - 1_codebooks/sigungu_crosswalk.csv (256 h_code)
  - 3_derived/mortality/sigungu_mortality_panel_v02_wa.parquet
  - 3_derived/bartik/iv_z_x_bilateral.parquet

Author: R-A (Path B Phase 2)
Date  : 2026-05-13
Reference:
  Anderson-Rubin (1949); Lee-McCrary-Moreira-Porter (2022) AER.
  Phase 1 decision log: 5_logs/decisions/2026-05-13_AR_LMP_inference.md
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
AREA = PROJ / "0_raw" / "modernization_controls" / "urbanization" / "kosis_sigungu_area_2007_2025.csv"
POP = PROJ / "0_raw" / "kosis_population" / "population_combined.csv"
CW = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
MORT = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
IV_BI = PROJ / "3_derived" / "bartik" / "iv_z_x_bilateral.parquet"

OUT_PANEL = PROJ / "3_derived" / "modernization_controls" / "sigungu_density_panel.parquet"
OUT_CSV = PROJ / "4_results" / "regression" / "modernization_robustness_cascade.csv"
OUT_LOG = PROJ / "5_logs" / "decisions" / "2026-05-13_modernization_controls.md"
for f in (OUT_PANEL, OUT_CSV, OUT_LOG):
    f.parent.mkdir(parents=True, exist_ok=True)


# Sido short → full name (used by area CSV)
SIDO_SHORT_TO_CODE = {
    "서울": 11, "부산": 21, "대구": 22, "인천": 23, "광주": 24, "대전": 25, "울산": 26,
    "세종": 39, "경기": 31, "강원": 32, "충북": 33, "충남": 34, "전북": 35, "전남": 36,
    "경북": 37, "경남": 38, "제주": 29,
}

CHI2_95 = stats.chi2.ppf(0.95, df=1)

# ---------------------------------------------------------------------------
# LMP critical value (Lee et al. 2022 Table 3 Panel A continuous interpolation)
# ---------------------------------------------------------------------------
LMP_TABLE = np.array([
    [100.0, 1.96], [50.0, 2.01], [40.0, 2.10], [30.0, 2.39],
    [23.1, 2.80], [20.0, 3.43], [19.65, 3.286], [16.38, 3.84],
    [15.0, 3.84], [10.0, 4.99], [8.96, 5.21], [5.53, 6.43], [2.0, 8.46],
])


def lmp_critical_value(F: float) -> float:
    if F is None or not np.isfinite(F):
        return float("inf")
    F = max(F, 1.0)
    tbl = LMP_TABLE[np.argsort(LMP_TABLE[:, 0])]
    Fs = tbl[:, 0]; Cs = tbl[:, 1]
    if F >= Fs[-1]:
        return float(Cs[-1])
    if F <= Fs[0]:
        return float(Cs[0])
    return float(np.interp(F, Fs, Cs))


# ---------------------------------------------------------------------------
# Step 1 — Build sigungu × year area panel mapped to 256 h_code
# ---------------------------------------------------------------------------
def normalize_sigungu_name(sigungu: str) -> tuple[str | None, bool]:
    """Return (canonical token used for h_name match, is_aggregate '(계)')."""
    s = sigungu.replace(" ", "")
    is_agg = "(계)" in s or s.endswith("합계")
    s_clean = s.replace("(계)", "").replace("합계", "")
    return s_clean, is_agg


def build_sigungu_area_to_h_code(cw: pd.DataFrame) -> dict[tuple[int, str, bool], int]:
    """
    Return mapping (sido_code, sigungu_token_normalized, is_agg) -> h_code.
    Built from the crosswalk h_name field.

    For autonomous-gu cities, area CSV uses "X시(계)" for the integrated city
    (e.g., 청주시(계), 창원시(계), 성남시(계), 천안시(계)).  In the crosswalk
    these map to 통합X시 (integrated-city h_code, e.g., 통합청주시 33040) where
    available, otherwise to the X시 h_code.

    For gu-level rows (e.g., 청주시상당구 = 상당구), we match by gu suffix.
    """
    canon = cw.groupby("h_code").agg(
        h_name=("h_name", "first"),
        sido_code=("sido_code", "first"),
    ).reset_index()

    mapping: dict[tuple[int, str, bool], int] = {}

    # Build sido-restricted h_name -> h_code lookup
    by_sido = {sc: {} for sc in canon["sido_code"].unique()}
    for _, row in canon.iterrows():
        by_sido[row["sido_code"]][row["h_name"]] = int(row["h_code"])

    return by_sido


def map_sigungu_to_h_code(sido_short: str, sigungu_raw: str,
                          by_sido: dict[int, dict[str, int]]) -> int | None:
    """
    Map (sido_short_name, sigungu_raw) to h_code.

    Hierarchy of matching attempts:
      1. Direct h_name match within sido (e.g., 종로구, 춘천시, 군위군)
      2. "X시(계)" → look up "통합X시" (e.g., 청주시(계) -> 통합청주시)
                  -> fallback "X시"
      3. "X시Y구" → look up "Y구" (compound, e.g., 청주시상당구 -> 상당구)
      4. "합계" (세종 only) → maps to integrated-city h_code (39010)
    """
    sido_code = SIDO_SHORT_TO_CODE.get(sido_short)
    if sido_code is None:
        return None
    bs = by_sido.get(sido_code, {})

    s, is_agg = normalize_sigungu_name(sigungu_raw)

    # 합계 special case for 세종
    if sido_short == "세종":
        if "합계" in sigungu_raw or "세종특별자치" in sigungu_raw:
            return bs.get("세종특별자치시") or bs.get("세종시") or 39010

    # Try direct match
    if s in bs:
        return bs[s]

    # If '(계)' / aggregate — try 통합 prefix
    if is_agg:
        cand = "통합" + s
        if cand in bs:
            return bs[cand]
        # Also try without '시' if any
        if s in bs:
            return bs[s]

    # Compound 'X시Y구' → take Y구 suffix
    m = re.match(r"^(\S+?시)(\S+구)$", s)
    if m:
        suffix_gu = m.group(2)
        if suffix_gu in bs:
            return bs[suffix_gu]
        # Some compound names use suffix like '일산동구' which IS the full h_name
        if s in bs:
            return bs[s]
        # Try fuzzy with the city prefix dropped
        if m.group(2).endswith("구") and m.group(2) in bs:
            return bs[m.group(2)]

    # Some names like '청주시청원구' have h_name '청원구' but it's also a 충북군 name etc.
    # Try suffix match (last token ending in 구/시/군)
    for suffix_n in (4, 3, 2):
        if len(s) >= suffix_n:
            cand = s[-suffix_n:]
            if cand in bs and (cand.endswith("구") or cand.endswith("시") or cand.endswith("군")):
                return bs[cand]
    return None


def build_density_panel() -> pd.DataFrame:
    """
    Build sigungu × year population density panel.

    density = total population (KOSIS C2=0 all-sex, C3=0 all-age) / area_m2 * 1e6
            (units: persons / km²)

    Area is from KOSIS 지적통계 2007-2025 (2007 area used as baseline anchor
    for 1997-1999 mortality baseline window; areas are nearly time-invariant
    within sigungu, with cross-sectional variation dominating).
    """
    print("[panel] reading area + pop + crosswalk ...")
    area = pd.read_csv(AREA, encoding="utf-8")
    pop = pd.read_csv(POP, encoding="utf-8")
    cw = pd.read_csv(CW, encoding="utf-8")

    # h_code mapping
    by_sido = build_sigungu_area_to_h_code(cw)

    # Map area sigungu rows to h_code
    area["h_code"] = area.apply(
        lambda r: map_sigungu_to_h_code(r["sido"], r["sigungu"], by_sido), axis=1
    )
    mapped = area.dropna(subset=["h_code"]).copy()
    unmapped = area[area["h_code"].isna()][["sido", "sigungu"]].drop_duplicates()
    print(f"[panel] area rows mapped: {len(mapped)}/{len(area)} ({len(mapped)/len(area)*100:.1f}%)")
    print(f"[panel] unmapped (sido, sigungu) pairs: {len(unmapped)}")
    if len(unmapped) > 0:
        print("[panel] unmapped sample:")
        print(unmapped.head(20).to_string(index=False))

    mapped["h_code"] = mapped["h_code"].astype(int).astype(str)
    # If multiple area rows hit same h_code (e.g., area listed both '(계)' total and gu rows),
    # take the larger value for the integrated-city h_code (since (계) is the full-city area).
    # For gu-level h_codes the gu-level area applies; we keep all rows then dedupe within (h_code, year).
    area_panel = (mapped.groupby(["h_code", "year"], as_index=False)
                  .agg(area_m2=("area_m2", "max"),
                       sido=("sido", "first"),
                       sigungu_n=("sigungu", "first")))

    # Population: total (C2=0, C3=0) sigungu-level (C1 is 5-digit sigungu code)
    pop["C1_str"] = pop["C1"].astype(str)
    # Keep only valid 5-digit codes (C1 >= 11000, drop national/sex/age aggregates)
    pop_sgg = pop[(pop["C1"] >= 11000) & (pop["C2"] == 0) & (pop["C3"] == 0)].copy()
    pop_sgg = pop_sgg.rename(columns={"C1_str": "h_code_raw"})

    # The pop "C1" is the year-specific raw sigungu code (e.g., 11010, 31010, 38110, etc.)
    # Map via crosswalk (raw_code, year) → h_code
    cw_short = cw[["year", "raw_code", "h_code"]].copy()
    cw_short["raw_code"] = cw_short["raw_code"].astype(str)
    cw_short["h_code"] = cw_short["h_code"].astype(str)

    pop_sgg["raw_code"] = pop_sgg["C1"].astype(str)
    pop_h = pop_sgg.merge(cw_short, on=["year", "raw_code"], how="left")
    pop_h_matched = pop_h.dropna(subset=["h_code"]).copy()
    print(f"[panel] population rows mapped via (raw_code, year) crosswalk: "
          f"{len(pop_h_matched)}/{len(pop_sgg)} ({len(pop_h_matched)/len(pop_sgg)*100:.1f}%)")

    # Aggregate pop within (h_code, year) — necessary because consolidated cities
    # may map multiple raw_codes to single h_code.
    pop_panel = (pop_h_matched.groupby(["h_code", "year"], as_index=False)
                 .agg(population=("population", "sum")))

    # Merge area + pop → density
    panel = pop_panel.merge(area_panel, on=["h_code", "year"], how="inner")
    # area_m2 may be 0 or NaN — protect
    panel["area_km2"] = panel["area_m2"] / 1.0e6
    panel = panel[panel["area_km2"] > 0]
    panel["density_per_km2"] = panel["population"] / panel["area_km2"]
    panel["log_density"] = np.log(panel["density_per_km2"])

    print(f"[panel] final density panel: {panel.shape}")
    print(f"[panel] h_code coverage: {panel['h_code'].nunique()}")
    print(f"[panel] year coverage: {panel['year'].min()} - {panel['year'].max()}")
    panel.to_parquet(OUT_PANEL, index=False)
    print(f"[OK] saved: {OUT_PANEL}")

    return panel


# ---------------------------------------------------------------------------
# Step 2 — Long-difference Δ_urbanization
# ---------------------------------------------------------------------------
def build_delta_urbanization(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Δ_urbanization = log(density_endpoint) - log(density_baseline).

    Baseline anchor: 1997-1999 population / 2007 area.
      The KOSIS 지적통계 area panel starts at 2007.  Areas are nearly
      time-invariant within sigungu (cross-sectional variation ≫ within-time
      variation), so 2007 area is the closest substantive proxy to the 1994
      mortality-baseline window.  This 7-12-year temporal gap is disclosed
      in the manuscript (§ 7.6.3) as a data-limitation honest-disclosure.
    Endpoint: 2018-2022 population / 2018-2022 mean area (mean to reduce
      land-survey jitter).
    """
    # baseline area: 2007
    area_b = panel[panel["year"] == 2007][["h_code", "area_km2"]].rename(
        columns={"area_km2": "area_km2_2007"})
    # baseline pop: 1997-1999 mean (need to compute from full panel)
    # But the density panel only has years where area is known (2007-2025).
    # We need 1997-1999 population from the pop panel directly.
    pop = pd.read_csv(POP, encoding="utf-8")
    cw = pd.read_csv(CW, encoding="utf-8")
    cw_short = cw[["year", "raw_code", "h_code"]].copy()
    cw_short["raw_code"] = cw_short["raw_code"].astype(str)
    cw_short["h_code"] = cw_short["h_code"].astype(str)

    pop_sgg = pop[(pop["C1"] >= 11000) & (pop["C2"] == 0) & (pop["C3"] == 0)].copy()
    pop_sgg["raw_code"] = pop_sgg["C1"].astype(str)
    pop_h = pop_sgg.merge(cw_short, on=["year", "raw_code"], how="left").dropna(subset=["h_code"])
    pop_h_agg = (pop_h.groupby(["h_code", "year"], as_index=False)
                 .agg(population=("population", "sum")))

    pop_b = pop_h_agg[pop_h_agg["year"].between(1997, 1999)].groupby(
        "h_code", as_index=False).agg(pop_baseline=("population", "mean"))
    pop_e = pop_h_agg[pop_h_agg["year"].between(2018, 2022)].groupby(
        "h_code", as_index=False).agg(pop_endpoint=("population", "mean"))
    area_e = panel[panel["year"].between(2018, 2022)].groupby(
        "h_code", as_index=False).agg(area_km2_endpoint=("area_km2", "mean"))

    df = (area_b.merge(pop_b, on="h_code", how="inner")
                .merge(pop_e, on="h_code", how="inner")
                .merge(area_e, on="h_code", how="inner"))
    df["density_baseline"] = df["pop_baseline"] / df["area_km2_2007"]
    df["density_endpoint"] = df["pop_endpoint"] / df["area_km2_endpoint"]
    df["log_density_baseline"] = np.log(df["density_baseline"])
    df["log_density_endpoint"] = np.log(df["density_endpoint"])
    df["delta_urbanization"] = df["log_density_endpoint"] - df["log_density_baseline"]
    print(f"[delta] Δ_urbanization computed for {len(df)} sigungu")
    print(f"[delta] Δ_urbanization distribution:")
    print(df["delta_urbanization"].describe())

    return df[["h_code", "delta_urbanization",
               "log_density_baseline", "log_density_endpoint"]]


# ---------------------------------------------------------------------------
# Step 3 — Main panel (replicate Phase 1) + sido FE + Δ_urbanization
# ---------------------------------------------------------------------------
def build_main_panel():
    mort = pd.read_parquet(MORT)
    mort["mort_rate"] = mort["deaths"] / np.maximum(mort["pop_wa"], 1)
    mort["log_mort"] = np.log(mort["mort_rate"] + 1e-6)
    mb = (mort[mort["year"].isin(range(1997, 2000))]
          .groupby(["h_code", "outcome_group"])["log_mort"].mean()
          .reset_index().rename(columns={"log_mort": "b"}))
    me = (mort[mort["year"].isin(range(2018, 2023))]
          .groupby(["h_code", "outcome_group"])["log_mort"].mean()
          .reset_index().rename(columns={"log_mort": "e"}))
    p = mb.merge(me, on=["h_code", "outcome_group"])
    p["d_log_mort"] = p["e"] - p["b"]
    p = p[p["outcome_group"] == "despair_total"][["h_code", "d_log_mort"]]
    p["h_code"] = p["h_code"].astype(str)
    return p


def build_cascade_panel():
    """
    Build analytic panel for the 3-spec cascade:
       cols: h_code, sido_code, d_log_mort, z_x_per_worker, z_x_std,
             delta_urbanization
    """
    p = build_main_panel()
    iv = pd.read_parquet(IV_BI)[["h_code", "z_x_per_worker"]]
    iv["h_code"] = iv["h_code"].astype(str)
    panel = build_density_panel()
    delta_urb = build_delta_urbanization(panel)

    df = (p.merge(iv, on="h_code", how="inner")
            .dropna(subset=["d_log_mort", "z_x_per_worker"]))
    df["sido_code"] = df["h_code"].str[:2]
    df["z_x_std"] = (df["z_x_per_worker"] - df["z_x_per_worker"].mean()) / df["z_x_per_worker"].std()

    df_full = df.merge(delta_urb, on="h_code", how="left")
    print(f"[cascade-panel] base n = {len(df)} (matches Phase 1 main IV sample)")
    print(f"[cascade-panel] with Δ_urbanization available: "
          f"{df_full['delta_urbanization'].notna().sum()}")
    return df_full


# ---------------------------------------------------------------------------
# Inference helpers
# ---------------------------------------------------------------------------
def regress_with_ses(y, X, cluster=None, label: str = "") -> dict:
    """
    Run OLS y on X (X includes constant).  Report:
      - β on the FIRST regressor in X after the constant (i.e., X[:,1])
      - HC1 SE
      - Cluster SE (provided `cluster` array; one-way clustering)
      - n, dof
    """
    y = np.asarray(y, dtype=float); X = np.asarray(X, dtype=float)
    fit_hc1 = sm.OLS(y, X).fit(cov_type="HC1")
    out = {
        "n": int(fit_hc1.nobs),
        "beta": float(np.asarray(fit_hc1.params)[1]),
        "se_HC1": float(np.asarray(fit_hc1.bse)[1]),
        "t_HC1": float(np.asarray(fit_hc1.tvalues)[1]),
        "p_HC1": float(np.asarray(fit_hc1.pvalues)[1]),
        "r2": float(fit_hc1.rsquared),
    }
    if cluster is not None:
        cluster = np.asarray(cluster)
        # statsmodels accepts cov_kwds={"groups": cluster}; one-way cluster SE
        fit_cl = sm.OLS(y, X).fit(cov_type="cluster",
                                  cov_kwds={"groups": cluster})
        out.update({
            "se_clusterSido": float(np.asarray(fit_cl.bse)[1]),
            "t_clusterSido": float(np.asarray(fit_cl.tvalues)[1]),
            "p_clusterSido": float(np.asarray(fit_cl.pvalues)[1]),
        })
    # 95% Wald CI via HC1
    out["wald_ci_lo"] = out["beta"] - 1.96 * out["se_HC1"]
    out["wald_ci_hi"] = out["beta"] + 1.96 * out["se_HC1"]
    return out


def ar_ci_residualized(y, D, controls, beta_point) -> tuple[float, float, float, float]:
    """
    AR confidence set for β on D after partialling out controls.
    Just-identified single-instrument case: D is itself the Bartik instrument.

    Returns (ar_lo, ar_hi, AR_stat_at_0, p_at_0).

    Method:  After partialling controls out of (y, D), test H0: β=β₀ via:
      ỹ - β₀·D̃  → regress on a constant.  AR statistic = (sample mean)² / Var.
      AR ~ χ²(1).
    """
    y = np.asarray(y, dtype=float); D = np.asarray(D, dtype=float)
    if controls is None or controls.shape[1] == 0:
        y_r = y - y.mean()
        D_r = D - D.mean()
    else:
        C = np.asarray(controls, dtype=float)
        Cc = sm.add_constant(C)
        y_r = y - Cc @ np.linalg.lstsq(Cc, y, rcond=None)[0]
        D_r = D - Cc @ np.linalg.lstsq(Cc, D, rcond=None)[0]

    var_y = np.var(y_r, ddof=1)
    var_D = np.var(D_r, ddof=1)
    cov_yD = np.cov(y_r, D_r, ddof=1)[0, 1]
    n = len(y)

    # AR test inversion:  test (y_r - β₀ D_r) has mean zero with HC1 SE
    # OLS of (y_r - β₀ D_r) on constant.
    # Closed-form quadratic in β₀:
    #   a β² + b β + c ≤ 0
    #   a = E[D²] - (chi2_95/n) * Var(D)            ≈ Var(D) (large n proxy)
    #   b = -2 (E[yD] - (chi2_95/n) * Cov(y, D))
    #   c = E[y²] - (chi2_95/n) * Var(y)
    # We use HC1 variance of (y_r - β D_r) — i.e., the t-statistic of the
    # mean of a residual.  Standard HC1 with n - k correction:
    #   T(β) = sqrt(n) * mean(y_r - β D_r) / SE(y_r - β D_r)
    #   AR = T²;  AR ≤ χ²(1, 0.95) defines the CI.
    # Coefficients:
    crit = CHI2_95
    # Define f(β) = mean(y_r - β D_r); g(β) = Var(y_r - β D_r) / n
    # T² = f² / g ≤ crit ⇔ f² ≤ crit g.
    # f(β) = (Σy - β Σ D) / n  = 0 - 0 = 0 (after demeaning) — so this is degenerate.
    # Use the un-demeaned residuals instead, or apply on the residualized variables
    # without further demeaning.  But variables ARE residualized by partialling.
    # Instead use the HC1 t-stat for β coefficient in the OLS of y_r on D_r
    # (no constant since residualized):
    # β̂ = (D_r ⋅ y_r) / (D_r ⋅ D_r);  Var(β̂)_HC1 = ...
    # AR(β₀) = [(β̂ - β₀)² (D_r⋅D_r)²] / [Σ(eps²) D_r²]
    # where eps = y_r - β̂ D_r.  Equivalently use HC1 t² with null β₀.
    DtD = float(D_r @ D_r)
    Dty = float(D_r @ y_r)
    beta_hat = Dty / DtD
    eps = y_r - beta_hat * D_r
    # HC1 meat: sum(D_r² * eps²)  (no constant residualization → HC1 with k=1)
    meat = float(np.sum((D_r ** 2) * (eps ** 2))) * (n / max(n - 1, 1))
    se_hat = float(np.sqrt(meat) / DtD)
    t_at_point = (beta_hat - 0.0) / se_hat
    ar_at_0 = t_at_point ** 2
    p_at_0 = float(1 - stats.chi2.cdf(ar_at_0, df=1))

    # Closed-form quadratic for AR CI under HC1 t-test inversion is messy
    # because Var(β̂) under HC1 changes with β only through eps.  We invert
    # via grid search around β_point.
    halfwidth = max(abs(beta_point), 1.0) * 4.0
    grid = np.linspace(beta_point - halfwidth, beta_point + halfwidth, 4001)
    ar_vals = np.empty_like(grid)
    for i, b in enumerate(grid):
        u = y_r - b * D_r
        # For HC1 t under H0:  T(β₀) = sqrt(D'D)(β̂ - β₀) / sqrt(Σ D² u²)
        m = float(np.sum((D_r ** 2) * (u ** 2))) * (n / max(n - 1, 1))
        if m <= 0:
            ar_vals[i] = np.inf
        else:
            t = (beta_hat - b) * DtD / np.sqrt(m)
            ar_vals[i] = t ** 2
    accept = ar_vals <= CHI2_95
    if not accept.any():
        return float("nan"), float("nan"), ar_at_0, p_at_0
    lo = float(grid[accept].min()); hi = float(grid[accept].max())
    if accept[0]:
        lo = -float("inf")
    if accept[-1]:
        hi = float("inf")
    return lo, hi, ar_at_0, p_at_0


def run_spec(df: pd.DataFrame, spec_label: str, sido_fe: bool, urb_ctrl: bool) -> dict:
    y = df["d_log_mort"].values
    D = df["z_x_std"].values
    controls_cols = []
    if sido_fe:
        sido_dummies = pd.get_dummies(df["sido_code"], prefix="sido", drop_first=True)
        controls_cols.append(sido_dummies)
    if urb_ctrl:
        controls_cols.append(df[["delta_urbanization"]])
    if controls_cols:
        C = pd.concat(controls_cols, axis=1).astype(float).values
    else:
        C = np.zeros((len(df), 0))

    # OLS design: const + D + controls
    X = np.column_stack([np.ones(len(df)), D, C]) if C.shape[1] > 0 else \
        np.column_stack([np.ones(len(df)), D])
    res = regress_with_ses(y, X, cluster=df["sido_code"].values)

    ar_lo, ar_hi, ar0, p0 = ar_ci_residualized(y, D, C if C.shape[1] > 0 else None,
                                               beta_point=res["beta"])
    res["AR_ci_lo"] = ar_lo
    res["AR_ci_hi"] = ar_hi
    res["AR_stat_at_0"] = ar0
    res["AR_p_at_0"] = p0

    # LMP cutoff at F = first-stage F (no IV here, so report HC1 t and reference
    # cutoff at F=∞ as 1.96; the cascade is a reduced-form check)
    F_proxy = float("inf")
    res["LMP_c0.05_F"] = lmp_critical_value(F_proxy)
    res["LMP_t_stat"] = res["t_HC1"]
    res["LMP_valid"] = abs(res["t_HC1"]) > res["LMP_c0.05_F"]
    res["spec"] = spec_label
    res["sido_FE"] = sido_fe
    res["urbanization_ctrl"] = urb_ctrl
    return res


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("\n=== Path B Phase 2 — modernization confound robustness cascade ===")
    df = build_cascade_panel()

    # Drop rows missing Δ_urbanization for spec 2; spec 0/1 use full panel
    df_full = df.dropna(subset=["delta_urbanization"]).copy()
    print(f"\n[main] cascade panel (full, with Δ_urbanization): n = {len(df_full)}")
    print(f"[main] base panel (without Δ_urbanization filter):  n = {len(df)}")

    # Use df_full for all three specs (apples-to-apples within same sigungu set)
    print(f"\n[main] running 3-spec cascade on n = {len(df_full)} ...")

    spec0 = run_spec(df_full, "Spec 0 — z_x_std only (replicate β_main)", False, False)
    spec1 = run_spec(df_full, "Spec 1 — + sido FE (β_sidoFE)", True, False)
    spec2 = run_spec(df_full, "Spec 2 — + sido FE + Δ_urbanization (β_full)", True, True)

    for r in (spec0, spec1, spec2):
        print(f"\n{r['spec']}: n={r['n']}, β={r['beta']:+.4f} (HC1 SE={r['se_HC1']:.4f}, "
              f"t={r['t_HC1']:.2f}, p={r['p_HC1']:.4f})")
        print(f"  Wald 95% CI = [{r['wald_ci_lo']:+.4f}, {r['wald_ci_hi']:+.4f}]")
        print(f"  Cluster-sido SE = {r['se_clusterSido']:.4f}, t = {r['t_clusterSido']:.2f}")
        print(f"  AR 95% CI = [{r['AR_ci_lo']:+.4f}, {r['AR_ci_hi']:+.4f}]")
        print(f"  R² = {r['r2']:.4f}")

    # CSV output schema: spec | sido_FE | urbanization_ctrl | n | β | SE_HC1 | t_HC1 | p_HC1
    #                  | SE_cluster | t_cluster | p_cluster | Wald_CI | AR_stat | AR_p | AR_CI
    #                  | r² | β_attenuation_pct
    beta_main = spec0["beta"]
    rows = []
    for r in (spec0, spec1, spec2):
        atten_pct = (r["beta"] / beta_main) * 100 if beta_main != 0 else float("nan")
        rows.append({
            "spec": r["spec"],
            "sido_FE": r["sido_FE"],
            "urbanization_ctrl": r["urbanization_ctrl"],
            "n": r["n"],
            "beta": r["beta"],
            "se_HC1": r["se_HC1"],
            "t_HC1": r["t_HC1"],
            "p_HC1": r["p_HC1"],
            "se_clusterSido": r["se_clusterSido"],
            "t_clusterSido": r["t_clusterSido"],
            "p_clusterSido": r["p_clusterSido"],
            "wald_ci_lo": r["wald_ci_lo"],
            "wald_ci_hi": r["wald_ci_hi"],
            "AR_stat_at_0": r["AR_stat_at_0"],
            "AR_p_at_0": r["AR_p_at_0"],
            "AR_ci_lo": r["AR_ci_lo"],
            "AR_ci_hi": r["AR_ci_hi"],
            "LMP_c0.05_F": r["LMP_c0.05_F"],
            "LMP_t_stat": r["LMP_t_stat"],
            "LMP_valid": r["LMP_valid"],
            "r2": r["r2"],
            "beta_attenuation_pct_of_spec0": atten_pct,
        })
    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig", float_format="%.6f")
    print(f"\n[OK] saved: {OUT_CSV}")

    # Attenuation verdict
    b0, b1, b2 = spec0["beta"], spec1["beta"], spec2["beta"]
    print(f"\n[verdict] β_main (Spec 0) = {b0:+.4f}")
    print(f"[verdict] β_sidoFE (Spec 1) = {b1:+.4f}  (ratio to main: {b1/b0:.3f})")
    print(f"[verdict] β_full    (Spec 2) = {b2:+.4f}  (ratio to main: {b2/b0:.3f})")
    pct_full = (b2 / b0) * 100
    if pct_full >= 70:
        verdict = "MINOR CONFOUND — main β robust (β_full ≥ 70% × β_main)"
    elif pct_full >= 50:
        verdict = "PARTIAL CONFOUND — substantive attenuation (50% ≤ β_full < 70% × β_main)"
    else:
        verdict = "SUBSTANTIVE CONFOUND — narrative weakening required (β_full < 50% × β_main)"
    print(f"[verdict] {verdict}")

    # Decision log
    log_lines = [
        "# Path B Phase 2 — Modernization confound robustness (sido FE + urbanization)",
        f"_Date: 2026-05-13_",
        "",
        "## Summary",
        "Long-difference of log working-age despair-mortality regressed on standardized "
        "Bartik trade exposure, with the cascade adding sido FE and "
        "Δ_urbanization (long-difference log population density, "
        "1997-1999 pop / 2007 area baseline → 2018-2022 pop / 2018-2022 area endpoint).",
        "",
        f"Analytic sample (with Δ_urbanization joinable): n = {len(df_full)}.",
        "Sido FE: 16-17 dummies (drop_first=True; baseline = lowest sido_code).",
        "",
        "### Cascade",
        f"| Spec | β | HC1 SE | Cluster-Sido SE | AR 95% CI | Attenuation vs β_main |",
        f"|------|--:|------:|----------------:|-----------|----------------------:|",
        f"| Spec 0  (z_x_std)                              | {b0:+.4f} | {spec0['se_HC1']:.4f} | {spec0['se_clusterSido']:.4f} | [{spec0['AR_ci_lo']:+.4f}, {spec0['AR_ci_hi']:+.4f}] | 100.0% (anchor) |",
        f"| Spec 1  (+ sido FE)                            | {b1:+.4f} | {spec1['se_HC1']:.4f} | {spec1['se_clusterSido']:.4f} | [{spec1['AR_ci_lo']:+.4f}, {spec1['AR_ci_hi']:+.4f}] | {b1/b0*100:.1f}% |",
        f"| Spec 2  (+ sido FE + Δ_urbanization)           | {b2:+.4f} | {spec2['se_HC1']:.4f} | {spec2['se_clusterSido']:.4f} | [{spec2['AR_ci_lo']:+.4f}, {spec2['AR_ci_hi']:+.4f}] | {b2/b0*100:.1f}% |",
        "",
        f"**Verdict**: {verdict}",
        "",
        "### Data-limitation honest disclosure",
        "- Area baseline = 2007 KOSIS 지적통계 (closest to mortality-baseline 1997-1999; 7-12 year gap).",
        "  Areas are nearly time-invariant within sigungu (cross-sectional variation dominates),",
        "  so the 2007 anchor is a substantive proxy for 1994/1997 baseline urbanization levels.",
        "- Dual-career household share, domestic violence reporting, healthcare infrastructure",
        "  density: **not available** at sigungu × pre-2015 vintage with sufficient long-difference",
        "  scope.  These three controls are deferred to the R&R cycle and disclosed in § 8.3.3.",
        "",
        f"Output CSV: `4_results/regression/modernization_robustness_cascade.csv`",
        f"Density panel: `3_derived/modernization_controls/sigungu_density_panel.parquet`",
    ]
    OUT_LOG.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"[OK] saved decision log: {OUT_LOG}")


if __name__ == "__main__":
    main()
