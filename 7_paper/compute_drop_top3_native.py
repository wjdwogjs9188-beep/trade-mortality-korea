"""
Phase 4 — Drop-top-3 industries robustness (native long-difference, Rotemberg α_k weight)
==========================================================================================
Identifies top-3 industries by GPSS-Rotemberg α_k weight on the KR-CN bilateral Bartik IV,
re-builds z_x_h^{dropTop3}, and re-runs the native long-difference reduced-form regression
(BASE 1997-1999 ↔ END 2018-2022, despair_total) with 5-layer SE + WCR Webb 6-point bootstrap.

α_k formula (user spec, GPSS 2020-style simplification):
    α_k = Σ_h (s_{h,k}^{1994})² × (ΔM_k)²  /  Σ_{k'} Σ_h (s_{h,k'}^{1994})² × (ΔM_{k'})²

IV reconstruction (primary spec, full E_h denominator):
    z_x_h^{dropTop3} = Σ_{k ∉ top3} s_{h,k}^{1994} × ΔM_k / E_h^{1994}

Alternative spec (¬top3 denominator):
    z_x_h^{dropTop3, alt} = Σ_{k ∉ top3} s_{h,k}^{1994} × ΔM_k / E_h^{¬top3, 1994}

5-layer SE: HC1 / Cluster-province (G=16, CR1 t-dist) / AKM-proper (ADM 2019 exposure design)
            / Conley 5 km / Conley 10 km
WCR Webb 6-pt B=9,999 via wildboottest.

Author: regenerated 2026-05-12 (Phase 4, KER submission)
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
IV_MAIN = PROJ / "3_derived" / "bartik" / "iv_z_x_bilateral.parquet"
SHARES = PROJ / "3_derived" / "bartik" / "baseline_shares_1994_ksic9_2digit.parquet"
EXPOSURE = PROJ / "3_derived" / "bartik" / "exposure_bilateral_2000_2010.parquet"
DENOM = PROJ / "3_derived" / "bartik" / "denominator_E_h_1994.parquet"
CENT = PROJ / "0_raw" / "sigungu_centroid" / "sigungu_centroid_table.csv"
OUT_REG = PROJ / "4_results" / "regression"
OUT_REG.mkdir(parents=True, exist_ok=True)

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


def manual_wcr_webb(y, X, cluster, B=9999, seed=42):
    """Webb (2023) 6-point WCR bootstrap (restricted null β=0) at the cluster level.
    Uses null-imposed residuals: u_h^r = y_h − X_{-z} γ̂_{|β=0}.
    Test stat = β̂/SE_cluster CR1 (Liang-Zeger with G/(G-1)*(n-1)/(n-k) finite-sample adj).
    Webb 6-point weights: {±√(3/2), ±1, ±√(1/2)} each with prob 1/6.
    """
    rng = np.random.default_rng(seed)
    cluster = np.asarray(cluster)
    unique_clusters, inverse = np.unique(cluster, return_inverse=True)
    G = len(unique_clusters)
    N, K = X.shape

    # full-model β and SE
    XtX_inv = np.linalg.inv(X.T @ X)
    beta_full = XtX_inv @ X.T @ y
    e_full = y - X @ beta_full

    def cluster_se(beta_vec, residuals):
        # CR1: V = c * (X'X)^{-1} Σ_g (X_g' e_g)(e_g' X_g) (X'X)^{-1}
        c = G / (G - 1) * (N - 1) / (N - K)
        meat = np.zeros((K, K))
        for g in range(G):
            mask = inverse == g
            Xg = X[mask]
            eg = residuals[mask]
            sg = Xg.T @ eg
            meat += np.outer(sg, sg)
        V = c * XtX_inv @ meat @ XtX_inv
        return np.sqrt(np.diag(V))

    se_full = cluster_se(beta_full, e_full)
    t_obs = abs(beta_full[1] / se_full[1])

    # restricted model under H0: β=0 → regress y on const only (drop z_x_std column)
    X_r = X[:, :1]  # const only
    XrXr_inv = np.linalg.inv(X_r.T @ X_r)
    gamma_r = XrXr_inv @ X_r.T @ y
    e_r = y - X_r @ gamma_r  # null-imposed residuals

    # Webb 6-point weights
    weights_grid = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5),
                              np.sqrt(0.5),  1.0,  np.sqrt(1.5)])

    boot_t = np.zeros(B)
    for b in range(B):
        # cluster-level weights
        w_cl = rng.choice(weights_grid, size=G)
        w_obs = w_cl[inverse]
        y_b = X_r @ gamma_r + w_obs * e_r  # bootstrap DGP under null
        beta_b = XtX_inv @ X.T @ y_b
        e_b = y_b - X @ beta_b
        se_b = cluster_se(beta_b, e_b)
        boot_t[b] = abs(beta_b[1] / se_b[1])

    p = (1 + (boot_t >= t_obs).sum()) / (1 + B)
    return p


def akm_proper_se_pw(y, z_pw, S, w, E_h):
    """Adão-Kolesár-Morales (2019) AKM SE on PER-WORKER scale.
    Reduced-form: y = α + β × z_pw + e, where z_pw_h = Σ_k s_{h,k} × w_k / E_h.
    Under shock-only exogeneity:
        V(β̂_pw) = (Σ_h z̃_h²)⁻² × Σ_k w_k² × (Σ_h (s_{h,k}/E_h) × ẽ_h)²
    where z̃ and ẽ are demeaned (partialled-out the constant).
    Returns SE(β̂_pw).
    """
    z_d = z_pw - z_pw.mean()
    # OLS: β_pw on demeaned z
    beta_pw = (z_d * y).sum() / (z_d ** 2).sum()
    e = y - y.mean() - beta_pw * z_d  # demeaned residual

    denom = (z_d ** 2).sum() ** 2
    J = S.shape[1]
    M = 0.0
    for k in range(J):
        contrib_k = (S[:, k] / E_h * e).sum()
        M += (w[k] ** 2) * (contrib_k ** 2)
    var_beta_pw = M / denom
    return np.sqrt(var_beta_pw), beta_pw


def run_5layer(df, y_col, label, S_full=None, w_full=None, E_h_col=None, sigma_z=None):
    """Run 5-layer SE on df with `z_x_std` and given y_col."""
    X_df = sm.add_constant(df[["z_x_std"]])  # keep DataFrame for wildboottest
    X = X_df.values
    y = df[y_col].values
    m_ols = sm.OLS(y, X_df).fit()
    beta = m_ols.params.iloc[1] if hasattr(m_ols.params, "iloc") else m_ols.params[1]
    resid = m_ols.resid

    m_hc1 = sm.OLS(y, X_df).fit(cov_type="HC1")
    se_hc1 = (m_hc1.bse.iloc[1] if hasattr(m_hc1.bse, "iloc") else m_hc1.bse[1])
    t_hc1 = beta / se_hc1
    p_hc1 = 2 * (1 - stats.norm.cdf(abs(t_hc1)))

    m_cl = sm.OLS(y, X_df).fit(cov_type="cluster", cov_kwds={"groups": df["sido_code"].values})
    se_cl = (m_cl.bse.iloc[1] if hasattr(m_cl.bse, "iloc") else m_cl.bse[1])
    G = df["sido_code"].nunique()
    t_cl = beta / se_cl
    p_cl_t = 2 * (1 - stats.t.cdf(abs(t_cl), df=G - 1))

    # AKM-proper (ADM 2019) — compute on per-worker scale, rescale to std scale
    if S_full is not None and w_full is not None and E_h_col is not None and sigma_z is not None:
        z_pw = df["z_x_per_worker"].values
        E_h = df[E_h_col].values
        se_akm_pw, beta_pw = akm_proper_se_pw(y, z_pw, S_full, w_full, E_h)
        # β_std = β_pw × σ_z; SE_std = SE_pw × σ_z
        se_akm = se_akm_pw * sigma_z
        t_akm = beta / se_akm
        p_akm = 2 * (1 - stats.norm.cdf(abs(t_akm)))
    else:
        se_akm = t_akm = p_akm = np.nan

    # Conley 5km/10km
    df_c = df.dropna(subset=["lat", "lng"]).reset_index(drop=True)
    if len(df_c) >= 50:
        X_c = sm.add_constant(df_c[["z_x_std"]]).values
        y_c = df_c[y_col].values
        m_c = sm.OLS(y_c, X_c).fit()
        res_c = m_c.resid.values if hasattr(m_c.resid, "values") else m_c.resid
        coords = df_c[["lat", "lng"]].values
        se_c5 = conley_se_uniform(X_c, res_c, coords, 5.0)[1]
        se_c10 = conley_se_uniform(X_c, res_c, coords, 10.0)[1]
        t_c5 = beta / se_c5
        t_c10 = beta / se_c10
        p_c5 = 2 * (1 - stats.norm.cdf(abs(t_c5)))
        p_c10 = 2 * (1 - stats.norm.cdf(abs(t_c10)))
    else:
        se_c5 = se_c10 = t_c5 = t_c10 = p_c5 = p_c10 = np.nan

    # WCR Webb 6-pt, B=9999 — via wildboottest (needs DataFrame X + integer cluster ids)
    wcr_p = np.nan
    try:
        from wildboottest.wildboottest import wildboottest
        m_for_wcr = sm.OLS(y, X_df)
        cluster_codes = pd.Categorical(df["sido_code"].values).codes.astype(np.int64)
        res = wildboottest(
            model=m_for_wcr,
            cluster=cluster_codes,
            B=9999,
            param="z_x_std",
            weights_type="webb",
            bootstrap_type="11",
            show=False,
            parallel=False,
        )
        if isinstance(res, pd.DataFrame):
            cand_cols = [c for c in res.columns if "p" in c.lower()]
            if "pvalue" in res.columns:
                wcr_p = float(res["pvalue"].iloc[0])
            elif "p-value" in res.columns:
                wcr_p = float(res["p-value"].iloc[0])
            elif cand_cols:
                wcr_p = float(res[cand_cols[-1]].iloc[0])
            else:
                wcr_p = float(res.iloc[0, -1])
        else:
            wcr_p = float(res)
    except Exception as e:
        print(f"[WARN] wildboottest failed for {label}: {e}")
        # Manual WCR Webb 6-pt fallback
        wcr_p = manual_wcr_webb(y, X_df.values, df["sido_code"].values, B=9999, seed=42)
        print(f"[INFO] manual WCR Webb fallback for {label}: p={wcr_p:.4f}")

    rows = [
        (label, "HC1 (White 1980)", se_hc1, t_hc1, p_hc1, beta, len(df), G),
        (label, "Cluster-province CR1 (G=16, t-dist)", se_cl, t_cl, p_cl_t, beta, len(df), G),
        (label, "AKM-proper (ADM 2019 exposure design)", se_akm, t_akm, p_akm, beta, len(df), G),
        (label, "Conley 5 km (uniform kernel)", se_c5, t_c5, p_c5, beta, len(df), G),
        (label, "Conley 10 km (uniform kernel)", se_c10, t_c10, p_c10, beta, len(df), G),
        (label, "WCR Webb 6-pt (B=9,999)", np.nan, np.nan, wcr_p, beta, len(df), G),
    ]
    return rows, beta, m_hc1


def build_panel(iv_df, label, e_h_col):
    """Build long-difference panel. e_h_col selects which denominator column to keep."""
    mort = pd.read_parquet(MORT)
    cent = pd.read_csv(CENT, dtype={"h_code": str})
    mort["h_code"] = mort["h_code"].astype(str)
    iv_df = iv_df.copy()
    iv_df["h_code"] = iv_df["h_code"].astype(str)
    cent["h_code"] = cent["h_code"].astype(str)

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
        ld.merge(iv_df[["h_code", "z_x_per_worker", e_h_col]], on="h_code", how="inner")
        .merge(cent[["h_code", "lat", "lng"]], on="h_code", how="left")
        .dropna(subset=["d_log", "z_x_per_worker", e_h_col])
    )
    df["sido_code"] = df["h_code"].str[:2]
    sd = df["z_x_per_worker"].std(ddof=1)
    df["z_x_std"] = (df["z_x_per_worker"] - df["z_x_per_worker"].mean()) / sd
    print(f"[panel/{label}] n = {len(df)}, G_sido = {df['sido_code'].nunique()}, "
          f"σ_z = {sd:.4f}")
    return df, sd


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 80)
    print("Phase 4 — Drop-top-3 (Rotemberg α_k) robustness, native long-difference")
    print("=" * 80)

    shares = pd.read_parquet(SHARES)
    expo = pd.read_parquet(EXPOSURE)
    denom = pd.read_parquet(DENOM)
    shares["h_code"] = shares["h_code"].astype(str)
    denom["h_code"] = denom["h_code"].astype(str)

    # ============================================================
    # 1) Rotemberg α_k weights
    # ============================================================
    print("\n[Step 1] Rotemberg α_k weights")
    expo_map = expo.set_index("ksic9_2digit")["dM_2000_2010"].to_dict()
    # ||s_k||² = Σ_h s_{h,k}² for each industry k
    sk2 = (
        shares.assign(sk2=lambda x: x["share"] ** 2)
        .groupby("ksic9_2digit")["sk2"]
        .sum()
        .reset_index()
    )
    sk2["dM"] = sk2["ksic9_2digit"].map(expo_map).fillna(0.0)
    sk2["alpha_num"] = (sk2["sk2"]) * (sk2["dM"] ** 2)
    total = sk2["alpha_num"].sum()
    sk2["alpha_k"] = sk2["alpha_num"] / total
    sk2 = sk2.sort_values("alpha_k", ascending=False).reset_index(drop=True)
    sk2["rank"] = np.arange(1, len(sk2) + 1)
    sk2["cum_alpha"] = sk2["alpha_k"].cumsum()
    print(sk2[["rank", "ksic9_2digit", "sk2", "dM", "alpha_k", "cum_alpha"]].to_string(index=False))

    top3 = sk2.head(3)["ksic9_2digit"].tolist()
    cum_top3 = sk2.head(3)["cum_alpha"].iloc[-1]
    print(f"\n  Top-3 industries: {top3}, cumulative α-share = {cum_top3:.4f}")

    sk2.to_csv(OUT_REG / "rotemberg_weights_native.csv", index=False, encoding="utf-8-sig")
    print(f"  [saved] rotemberg_weights_native.csv")

    # ============================================================
    # 2) Re-build z_x^{dropTop3} (primary: full E_h denominator)
    # ============================================================
    print("\n[Step 2] Rebuild z_x_h^{dropTop3} (primary: full E_h denominator)")
    bs2 = shares.copy()
    bs2["dM"] = bs2["ksic9_2digit"].map(expo_map).fillna(0.0)
    bs2["contrib"] = bs2["share"] * bs2["dM"]
    # drop top-3 rows from numerator
    bs2["contrib_drop"] = np.where(bs2["ksic9_2digit"].isin(top3), 0.0, bs2["contrib"])

    iv_drop = bs2.groupby("h_code")["contrib_drop"].sum().reset_index().rename(columns={"contrib_drop": "z_x"})
    iv_drop = iv_drop.merge(denom, on="h_code", how="left")
    iv_drop["z_x_per_worker"] = iv_drop["z_x"] / iv_drop["E_h_1994"].replace(0, np.nan)

    # Alternative: ¬top3 denominator (restrict E_h to non-top3 industries)
    Eh_no_top3 = (
        bs2[~bs2["ksic9_2digit"].isin(top3)]
        .groupby("h_code")["employment"]
        .sum()
        .reset_index()
        .rename(columns={"employment": "E_h_no_top3"})
    )
    iv_drop_alt = bs2.groupby("h_code")["contrib_drop"].sum().reset_index().rename(columns={"contrib_drop": "z_x"})
    iv_drop_alt = iv_drop_alt.merge(Eh_no_top3, on="h_code", how="left")
    iv_drop_alt["z_x_per_worker"] = iv_drop_alt["z_x"] / iv_drop_alt["E_h_no_top3"].replace(0, np.nan)
    # also propagate full E_h for AKM-proper formula on alt spec (denominator is local)
    iv_drop_alt = iv_drop_alt.merge(denom, on="h_code", how="left")

    print(f"  iv_drop (primary E_h): n={len(iv_drop)}, "
          f"mean z_x_pw={iv_drop['z_x_per_worker'].mean():.4f}")
    print(f"  iv_drop_alt (¬top3 E_h): n={len(iv_drop_alt)}, "
          f"mean z_x_pw={iv_drop_alt['z_x_per_worker'].mean():.4f}")

    # ============================================================
    # 3) Native long-difference panel — primary spec
    # ============================================================
    print("\n[Step 3] Native long-difference panel (despair_total, 1997-1999 ↔ 2018-2022)")
    df_primary, sigma_z_primary = build_panel(iv_drop, "primary", "E_h_1994")
    df_alt, sigma_z_alt = build_panel(iv_drop_alt, "alt_¬top3_E", "E_h_no_top3")

    # AKM-proper inputs — drop top3 from S and w (so they aren't in identifying variation)
    bs_pivot = shares.pivot(index="h_code", columns="ksic9_2digit", values="share").fillna(0)
    industry_cols_all = list(bs_pivot.columns)
    industry_cols_keep = [c for c in industry_cols_all if c not in top3]
    df_s = df_primary[["h_code"]].merge(bs_pivot.reset_index(), on="h_code", how="left").fillna(0)
    S_keep = df_s[industry_cols_keep].values
    w_keep = np.array([expo_map.get(c, 0.0) for c in industry_cols_keep])
    print(f"  AKM-proper inputs: S {S_keep.shape}, w {w_keep.shape}, "
          f"non-top3 industries={len(industry_cols_keep)}")

    df_s_alt = df_alt[["h_code"]].merge(bs_pivot.reset_index(), on="h_code", how="left").fillna(0)
    S_keep_alt = df_s_alt[industry_cols_keep].values

    # ============================================================
    # 4) Run 5-layer SE (+ WCR Webb)
    # ============================================================
    print("\n[Step 4] 5-layer SE + WCR Webb 6-pt B=9,999 — primary spec")
    rows_primary, beta_primary, _ = run_5layer(
        df_primary, "d_log", "Drop-Top-3 (primary E_h)",
        S_full=S_keep, w_full=w_keep, E_h_col="E_h_1994", sigma_z=sigma_z_primary,
    )
    for r in rows_primary:
        layer = r[1]; se = r[2]; t = r[3]; p = r[4]
        se_s = f"{se:.4f}" if not np.isnan(se) else "—"
        t_s = f"{t:+.3f}" if not np.isnan(t) else "—"
        p_s = f"{p:.4e}" if not np.isnan(p) and p < 1e-3 else (f"{p:.4f}" if not np.isnan(p) else "—")
        print(f"    {layer:<45s}  SE={se_s:>10s}  t={t_s:>8s}  p={p_s:>10s}")

    print(f"\n[Step 4b] 5-layer SE + WCR Webb 6-pt B=9,999 — alt spec (¬top3 E_h)")
    rows_alt, beta_alt, _ = run_5layer(
        df_alt, "d_log", "Drop-Top-3 (alt ¬top3 E_h)",
        S_full=S_keep_alt, w_full=w_keep, E_h_col="E_h_no_top3", sigma_z=sigma_z_alt,
    )
    for r in rows_alt:
        layer = r[1]; se = r[2]; t = r[3]; p = r[4]
        se_s = f"{se:.4f}" if not np.isnan(se) else "—"
        t_s = f"{t:+.3f}" if not np.isnan(t) else "—"
        p_s = f"{p:.4e}" if not np.isnan(p) and p < 1e-3 else (f"{p:.4f}" if not np.isnan(p) else "—")
        print(f"    {layer:<45s}  SE={se_s:>10s}  t={t_s:>8s}  p={p_s:>10s}")

    # ============================================================
    # 5) Compute attenuation cascade
    # ============================================================
    print("\n[Step 5] Attenuation cascade")
    beta_main = -0.127212387489216  # from main_native_5layer_2026-05-12.csv
    beta_dropC26 = -0.0756  # paper § 6.2 line 398 (archive HC1 spec)
    print(f"  β_main (1994 baseline, all industries):  {beta_main:+.4f}")
    print(f"  β_dropC26 (archive HC1 spec, paper):     {beta_dropC26:+.4f}")
    print(f"  β_dropTop3 (primary, native 5-layer):    {beta_primary:+.4f}")
    print(f"  β_dropTop3 (alt ¬top3 E_h, native):      {beta_alt:+.4f}")
    print(f"  attenuation: β_dropTop3 / β_main = {beta_primary/beta_main*100:.1f}%")

    # ============================================================
    # 6) Save final results CSV
    # ============================================================
    cols = ["spec", "layer", "SE", "t", "p", "beta", "n", "G"]
    out_df = pd.DataFrame(rows_primary + rows_alt, columns=cols)
    out_df.to_csv(OUT_REG / "drop_top3_5layer_native_2026-05-12.csv", index=False, encoding="utf-8-sig")
    print(f"\n[saved] drop_top3_5layer_native_2026-05-12.csv")

    # cascade table
    cascade = pd.DataFrame([
        {"spec": "β_main (1994, all industries)",         "beta": beta_main,    "ratio_to_main": 1.000},
        {"spec": "β_dropC26 (paper § 6.2, archive HC1)",  "beta": beta_dropC26, "ratio_to_main": beta_dropC26 / beta_main},
        {"spec": "β_dropTop3 (primary E_h, native)",       "beta": beta_primary, "ratio_to_main": beta_primary / beta_main},
        {"spec": "β_dropTop3 (alt ¬top3 E_h, native)",    "beta": beta_alt,     "ratio_to_main": beta_alt / beta_main},
    ])
    cascade.to_csv(OUT_REG / "drop_top3_attenuation_cascade.csv", index=False, encoding="utf-8-sig")
    print(f"[saved] drop_top3_attenuation_cascade.csv")

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
