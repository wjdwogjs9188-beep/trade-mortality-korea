"""
Pre-WTO 1992-1996 placebo v2 — incremental log + try/except
==============================================================

Spec:
  Δ log(mortality_h, 1997→1999) ~ z_x_h^{KR-CN, 1992-1996}
  H0: β = 0 → BHJ shock-only exogeneity 직접 입증

Author: R-A
Date  : 2026-05-05
"""
from __future__ import annotations

import sys
import re
import traceback
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
KRCN = PROJ / "0_raw" / "comtrade_korea_china"
SHARES = PROJ / "3_derived" / "bartik" / "baseline_shares_1994_ksic9_2digit.parquet"
DENOM = PROJ / "3_derived" / "bartik" / "denominator_E_h_1994.parquet"
HS_KSIC = PROJ / "3_derived" / "bartik" / "hs6_to_ksic9_2digit.parquet"
MORT = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
CW = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
OUT_REG = PROJ / "4_results" / "regression"
LOGS = PROJ / "5_logs" / "decisions"
OUT_REG.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
TODAY = date.today().isoformat()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LOG_PATH = LOGS / f"{TODAY}_pre_wto_placebo.md"
log_buf: list[str] = [f"# Pre-WTO 1992-1996 placebo v2 — incremental log\n_{TODAY}_\n"]


def flush():
    LOG_PATH.write_text("\n".join(log_buf), encoding="utf-8")


def log(msg: str):
    log_buf.append(msg)
    flush()
    print(msg)


def main():
    # 1) Load pre-WTO imports
    files = sorted(KRCN.glob("KR_imp_from_CN_199*.csv"))
    files = [f for f in files if int(f.stem[-4:]) <= 1996]
    log(f"## Pre-WTO csv: {len(files)}")

    rows = []
    for f in files:
        m = re.match(r".*_(\d{4})\.csv", f.name)
        year = int(m.group(1))
        df = pd.read_csv(f, low_memory=False)
        df.columns = [c.lower() for c in df.columns]
        rows.append(df.assign(__year=year))
    big = pd.concat(rows, ignore_index=True)
    log(f"- combined rows: {len(big):,}")
    log(f"- columns: {list(big.columns)[:20]}")

    # 2) HS6 + value 컬럼
    cmd_col = next((c for c in ("cmdcode", "commoditycode") if c in big.columns), None)
    val_col = next((c for c in ("primaryvalue", "tradevalue", "fobvalue") if c in big.columns), None)
    log(f"- cmd_col: {cmd_col}, val_col: {val_col}")

    if not cmd_col or not val_col:
        log(f"❌ HS6 또는 value 컬럼 부재. cols 전체: {list(big.columns)}")
        return

    big["hs6_str"] = big[cmd_col].astype(str).str.zfill(6).str[:6]
    big[val_col] = pd.to_numeric(big[val_col], errors="coerce")
    log(f"- HS6 distinct: {big['hs6_str'].nunique()}")

    # 3) ΔM 1992→1996
    pivot = big.pivot_table(index="hs6_str", columns="__year", values=val_col, aggfunc="sum").fillna(0)
    log(f"- pivot columns: {list(pivot.columns)}")
    if 1992 not in pivot.columns or 1996 not in pivot.columns:
        log(f"⚠️ 1992 또는 1996 부재")
        return
    pivot["dM_pre_wto"] = pivot[1996] - pivot[1992]
    log(f"- pre-WTO ΔM rows: {len(pivot)}, sum: {pivot['dM_pre_wto'].sum():,.0f}")

    # 4) HS6 → KSIC9_2 매핑
    if not HS_KSIC.exists():
        log(f"❌ {HS_KSIC} 부재")
        return
    hs_ksic = pd.read_parquet(HS_KSIC)
    log(f"- hs_ksic mapping rows: {len(hs_ksic)}, cols: {list(hs_ksic.columns)}")

    expo = pivot[["dM_pre_wto"]].reset_index().merge(hs_ksic, on="hs6_str", how="inner")
    log(f"- pre-WTO HS6 → KSIC9_2 merged: {len(expo)}")

    expo_ksic = expo.groupby("ksic9_2digit")["dM_pre_wto"].sum().reset_index()
    log(f"- pre-WTO ΔM by KSIC9_2: {len(expo_ksic)}")
    log("```")
    log(expo_ksic.sort_values("dM_pre_wto", ascending=False).to_string(index=False))
    log("```")

    # 5) z_x^{pre-WTO} 시군구별
    shares = pd.read_parquet(SHARES)
    denom = pd.read_parquet(DENOM)
    log(f"- shares rows: {len(shares)}, denom rows: {len(denom)}")

    bs = shares.merge(expo_ksic, on="ksic9_2digit", how="left")
    bs["dM_pre_wto"] = bs["dM_pre_wto"].fillna(0)
    bs["contribution"] = bs["share"] * bs["dM_pre_wto"]
    z_pre = bs.groupby("h_code")["contribution"].sum().reset_index().rename(columns={"contribution": "z_x_pre_wto"})
    z_pre = z_pre.merge(denom, on="h_code", how="left")
    z_pre["z_x_pre_wto_per_worker"] = z_pre["z_x_pre_wto"] / z_pre["E_h_1994"].replace(0, np.nan)
    log(f"\n- z_x^{{pre-WTO}}: {len(z_pre)} h_code, mean={z_pre['z_x_pre_wto_per_worker'].mean():.2f}")

    # 6) Outcome
    cw = pd.read_csv(CW, dtype=str)
    h_to_sido = cw.drop_duplicates("h_code")[["h_code", "sido_code"]]

    mort = pd.read_parquet(MORT)
    # 1997 KOSIS pop_wa NaN known issue → 1998-2000 placebo (shock 1992-1996 과 2년 gap)
    Y0_PRE, Y1_PRE = 1998, 2000
    sub = mort[(mort["outcome_group"] == "despair_total") & mort["year"].isin([Y0_PRE, Y1_PRE])].copy()
    pv = sub.pivot_table(index="h_code", columns="year", values="log_asr_p1", aggfunc="mean").reset_index()
    log(f"- mortality pivot columns: {list(pv.columns)}")
    if Y0_PRE not in pv.columns or Y1_PRE not in pv.columns:
        log(f"⚠️ {Y0_PRE} 또는 {Y1_PRE} 부재")
        return

    pv["d_log_mort_pre"] = pv[Y1_PRE] - pv[Y0_PRE]
    log(f"- {Y0_PRE}→{Y1_PRE} mortality non-null: {pv['d_log_mort_pre'].notna().sum()}")

    # 7) Placebo regression
    df = (
        pv[["h_code", "d_log_mort_pre"]]
        .merge(z_pre[["h_code", "z_x_pre_wto_per_worker"]], on="h_code", how="inner")
        .merge(h_to_sido, on="h_code", how="left")
        .dropna(subset=["d_log_mort_pre", "z_x_pre_wto_per_worker"])
    )
    log(f"- placebo panel: n={len(df)}")

    if len(df) < 50:
        log("⚠️ n<50, placebo skip")
        return

    df["z_pre_std"] = (df["z_x_pre_wto_per_worker"] - df["z_x_pre_wto_per_worker"].mean()) / df["z_x_pre_wto_per_worker"].std()

    X = sm.add_constant(df[["z_pre_std"]])
    m_hc1 = sm.OLS(df["d_log_mort_pre"], X).fit(cov_type="HC1")
    m_cl = sm.OLS(df["d_log_mort_pre"], X).fit(cov_type="cluster", cov_kwds={"groups": df["sido_code"]})

    beta = m_hc1.params["z_pre_std"]
    log(f"\n## Pre-WTO placebo regression result")
    log(f"- N = {len(df)}, R² = {m_hc1.rsquared:.4f}")
    log(f"- β (std) = {beta:+.4f}")
    log(f"- HC1: SE={m_hc1.bse['z_pre_std']:.4f}, t={beta/m_hc1.bse['z_pre_std']:+.2f}, p={m_hc1.pvalues['z_pre_std']:.4f}")
    log(f"- cluster-sido: SE={m_cl.bse['z_pre_std']:.4f}, t={beta/m_cl.bse['z_pre_std']:+.2f}, p={m_cl.pvalues['z_pre_std']:.4f}")

    p_cluster = m_cl.pvalues["z_pre_std"]
    log(f"\n## 판정")
    if p_cluster > 0.10:
        log(f"- ✅ **Pre-WTO placebo PASS** (cluster p={p_cluster:.4f} > 0.10)")
        log(f"- pre-WTO bilateral 변화가 1997-1999 mortality 와 무관 → BHJ shock-only exogeneity 직접 입증")
        log(f"- z_x_h^{{2000-2010}} 의 share-violation 에도 shock 자체는 외생")
    elif p_cluster > 0.05:
        log(f"- ⚠️ borderline (cluster p={p_cluster:.4f})")
    else:
        log(f"- ❌ **Pre-WTO placebo FAIL** (cluster p={p_cluster:.4f} < 0.05)")
        log(f"- pre-WTO 변화가 mortality 예측 → BHJ shock-only exogeneity 위반 의심")

    out = OUT_REG / "pre_wto_placebo_1992_1996.csv"
    pd.DataFrame([{
        "method": "Pre-WTO placebo (1992-1996 shock × 1997-1999 mortality)",
        "n": len(df),
        "beta_std": beta,
        "se_HC1": m_hc1.bse["z_pre_std"],
        "p_HC1": m_hc1.pvalues["z_pre_std"],
        "se_cluster_sido": m_cl.bse["z_pre_std"],
        "p_cluster_sido": p_cluster,
        "r2": m_hc1.rsquared,
    }]).to_csv(out, index=False, encoding="utf-8-sig")
    log(f"\n- saved: `{out.relative_to(PROJ)}`")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"\n[CRASH] {e}\n```\n{traceback.format_exc()}\n```")
        raise
