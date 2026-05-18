"""
Native long-difference (1997-1999 ↔ 2018-2022) 5-layer SE re-computation
========================================================================
Spec: Δ_long log_asr_p1 (despair_total) ~ z_x_h_std
  - n = 221 sigungu
  - β should ≈ -0.127212 (consistency check)
  - 5 SE layers: HC1, Cluster-sido (G=16), AKM-proper (verified ext.),
                 Conley 5km, Conley 10km

Author: regenerated 2026-05-12
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
MORT = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
IV = PROJ / "3_derived" / "bartik" / "iv_z_x_bilateral.parquet"
CENT = PROJ / "0_raw" / "sigungu_centroid" / "sigungu_centroid_table.csv"

BASE_YRS = list(range(1997, 2000))
END_YRS = list(range(2018, 2023))


def haversine_km(lat1, lng1, lat2, lng2):
    R = 6371.0
    lat1, lat2 = np.radians(lat1), np.radians(lat2)
    dlat = lat2 - lat1
    dlng = np.radians(lng2 - lng1)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlng / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def conley_se_uniform(X, residuals, coords, cutoff_km):
    """Conley (1999) spatial HAC, uniform kernel within cutoff."""
    n, k = X.shape
    bread = np.linalg.inv(X.T @ X)
    lat = coords[:, 0]
    lng = coords[:, 1]
    W = np.zeros((n, n))
    for i in range(n):
        d = haversine_km(lat[i], lng[i], lat, lng)
        W[i, :] = (d <= cutoff_km).astype(float)
    eps = residuals.reshape(-1, 1)
    Z = X * eps
    meat = Z.T @ W @ Z
    cov = bread @ meat @ bread
    return np.sqrt(np.diag(cov))


def main():
    mort = pd.read_parquet(MORT)
    iv = pd.read_parquet(IV)
    cent = pd.read_csv(CENT, dtype={"h_code": str})

    mort["h_code"] = mort["h_code"].astype(str)
    iv["h_code"] = iv["h_code"].astype(str)
    cent["h_code"] = cent["h_code"].astype(str)

    # Match the canonical R native-build formula (compute_sigma_z.R, run_robustness_native_v02.R):
    #   mort_rate = deaths / max(pop_wa, 1); log_mort = log(mort_rate + 1e-6)
    mort["mort_rate"] = mort["deaths"] / mort["pop_wa"].clip(lower=1)
    mort["log_mort"] = np.log(mort["mort_rate"] + 1e-6)

    d = mort[mort["outcome_group"] == "despair_total"].copy()
    base = d[d["year"].isin(BASE_YRS)].groupby("h_code")["log_mort"].mean()
    end = d[d["year"].isin(END_YRS)].groupby("h_code")["log_mort"].mean()
    ld = (
        pd.DataFrame({"base": base, "end": end})
        .dropna()
        .assign(d_log=lambda x: x["end"] - x["base"])
        .reset_index()
    )

    df = (
        ld.merge(iv[["h_code", "z_x_per_worker"]], on="h_code", how="inner")
        .merge(cent[["h_code", "lat", "lng"]], on="h_code", how="left")
        .dropna(subset=["d_log", "z_x_per_worker"])
    )
    df["sido_code"] = df["h_code"].str[:2]
    df["z_x_std"] = (df["z_x_per_worker"] - df["z_x_per_worker"].mean()) / df["z_x_per_worker"].std(ddof=1)
    print(f"[panel] n = {len(df)} sigungu")
    print(f"[panel] G (sido) = {df['sido_code'].nunique()}")
    print(f"[panel] z_x_per_worker SD (σ_z) = {df['z_x_per_worker'].std(ddof=1):.4f}")

    X = sm.add_constant(df[["z_x_std"]]).values
    y = df["d_log"].values

    # OLS
    m_ols = sm.OLS(y, X).fit()
    beta = m_ols.params[1]
    resid = m_ols.resid
    n_obs = len(y)
    print(f"\n[OLS] β_std = {beta:+.6f}")
    print(f"[OLS] R² = {m_ols.rsquared:.4f}")

    # HC1
    m_hc1 = sm.OLS(y, X).fit(cov_type="HC1")
    se_hc1 = m_hc1.bse[1]
    t_hc1 = beta / se_hc1
    p_hc1 = 2 * (1 - stats.norm.cdf(abs(t_hc1)))

    # Cluster-sido (CR1)
    m_cl = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": df["sido_code"].values})
    se_cl = m_cl.bse[1]
    t_cl = beta / se_cl
    # statsmodels uses t-dist with G-1 df for cluster
    G = df["sido_code"].nunique()
    p_cl_t = 2 * (1 - stats.t.cdf(abs(t_cl), df=G - 1))
    p_cl_norm = 2 * (1 - stats.norm.cdf(abs(t_cl)))

    # Conley 5km / 10km
    df_c = df.dropna(subset=["lat", "lng"]).reset_index(drop=True)
    X_c = sm.add_constant(df_c[["z_x_std"]]).values
    y_c = df_c["d_log"].values
    m_c = sm.OLS(y_c, X_c).fit()
    res_c = m_c.resid
    coords = df_c[["lat", "lng"]].values
    se_c5 = conley_se_uniform(X_c, res_c, coords, 5.0)[1]
    se_c10 = conley_se_uniform(X_c, res_c, coords, 10.0)[1]
    t_c5 = beta / se_c5
    t_c10 = beta / se_c10
    p_c5 = 2 * (1 - stats.norm.cdf(abs(t_c5)))
    p_c10 = 2 * (1 - stats.norm.cdf(abs(t_c10)))

    print(f"\n[Conley] n with valid centroid = {len(df_c)} / {len(df)}")

    rows = [
        ("HC1 (White 1980)", se_hc1, t_hc1, p_hc1),
        ("Cluster-sido CR1 (G=16, t-dist)", se_cl, t_cl, p_cl_t),
        ("Cluster-sido CR1 (G=16, normal)", se_cl, t_cl, p_cl_norm),
        ("AKM-proper (Kolesár 2024, external)", 0.025848, beta / 0.025848, 8.5843e-07),
        ("Conley 5 km (uniform kernel)", se_c5, t_c5, p_c5),
        ("Conley 10 km (uniform kernel)", se_c10, t_c10, p_c10),
        ("WCR Webb 6-pt (B=9999, external)", float("nan"), float("nan"), 1.0 / 9999),
    ]
    print(f"\n{'Layer':<40s}{'SE':>10s}{'t':>10s}{'p':>14s}")
    print("-" * 74)
    for layer, se, t, p in rows:
        se_s = f"{se:.4f}" if not np.isnan(se) else "—"
        t_s = f"{t:+.3f}" if not np.isnan(t) else "—"
        p_s = f"{p:.4e}" if p < 1e-3 else f"{p:.4f}"
        print(f"{layer:<40s}{se_s:>10s}{t_s:>10s}{p_s:>14s}")

    out = PROJ / "4_results" / "regression" / "main_native_5layer_2026-05-12.csv"
    out_df = pd.DataFrame(rows, columns=["layer", "SE", "t", "p"]).assign(
        beta=beta, n=len(df), G=G
    )
    out_df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"\n[saved] {out}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
