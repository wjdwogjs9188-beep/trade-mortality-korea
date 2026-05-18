"""
Phase 4 fixes — WCB direct bootstrap + pre_2008 sub-period diagnosis
=====================================================================
"""
from __future__ import annotations
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
MORT = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
IV = PROJ / "3_derived" / "bartik" / "iv_z_x_bilateral.parquet"
CW = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
OUT_REG = PROJ / "4_results" / "regression"
LOGS = PROJ / "5_logs" / "decisions"
TODAY = date.today.isoformat

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def wcb_pvalue(y, X, cluster, n_boot=1000, seed=42):
 """Direct wild cluster bootstrap (no numba)."""
 rng = np.random.default_rng(seed)
 cluster = np.asarray(cluster)
 unique_clusters = np.unique(cluster)

 # main estimate
 m = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": cluster})
 beta_hat = m.params[-1]
 se_hat = m.bse[-1]
 t_hat = beta_hat / se_hat

 # restricted residuals (impose null β=0 on z_x_std)
 X_rest = X[:,:-1] # drop last column (z_x_std)
 if X_rest.shape[1] == 0:
 # only constant
 beta_r = np.array([y.mean])
 e_r = y - X_rest @ beta_r if X_rest.shape[1] > 0 else y - y.mean
 else:
 m_r = sm.OLS(y, X_rest).fit
 e_r = y - X_rest @ m_r.params

 boot_t = 
 for b in range(n_boot):
 # Mammen weight per cluster
 u_per_cluster = rng.choice([-1, 1], size=len(unique_clusters))
 u_map = dict(zip(unique_clusters, u_per_cluster))
 u = np.array([u_map[c] for c in cluster])
 y_b = X_rest @ (m_r.params if X_rest.shape[1] > 0 else np.array([0])) + e_r * u
 try:
 m_b = sm.OLS(y_b, X).fit(cov_type="cluster", cov_kwds={"groups": cluster})
 t_b = m_b.params[-1] / m_b.bse[-1]
 boot_t.append(t_b)
 except Exception:
 continue
 boot_t = np.array(boot_t)
 if len(boot_t) == 0:
 return np.nan
 p = (np.abs(boot_t) >= np.abs(t_hat)).mean
 return p

def main:
 log = [f"# Phase 4 fixes — WCB direct + pre_2008 diagnosis\n_{TODAY}_\n"]

 mort = pd.read_parquet(MORT)
 iv = pd.read_parquet(IV)
 cw = pd.read_csv(CW, dtype=str)
 h_to_sido = cw.drop_duplicates("h_code")[["h_code", "sido_code"]]

 # ====================================================================
 # 1. WCB-sido (direct, no numba) for despair_total
 # ====================================================================
 log.append("## WCB-sido direct bootstrap (1000 boot)")
 sub = mort[(mort["outcome_group"] == "despair_total") & (mort["year"].isin([2000, 2010]))].copy
 pv = sub.pivot_table(index="h_code", columns="year", values="log_asr_p1", aggfunc="mean").reset_index
 pv["d_log"] = pv[2010] - pv[2000]
 df = (
 pv.merge(iv[["h_code", "z_x_per_worker"]], on="h_code", how="inner")
.merge(h_to_sido, on="h_code", how="left")
.dropna(subset=["d_log", "z_x_per_worker"])
)
 df["z_x_std"] = (df["z_x_per_worker"] - df["z_x_per_worker"].mean) / df["z_x_per_worker"].std
 X = sm.add_constant(df[["z_x_std"]]).values
 y = df["d_log"].values
 cluster = df["sido_code"].astype(str).values
 log.append(f"- N = {len(df)}, sido clusters = {len(np.unique(cluster))}")

 # baseline
 m = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": cluster})
 log.append(f"- baseline cluster-sido: β={m.params[-1]:+.4f}, t={m.params[-1]/m.bse[-1]:+.2f}, p={m.pvalues[-1]:.4f}")

 # WCB
 p_wcb = wcb_pvalue(y, X, cluster, n_boot=1000)
 log.append(f"- **WCB-sido p (1000 boot)**: {p_wcb:.4f}")
 if p_wcb < 0.05:
 log.append(f"- ✅ WCB significant — small-cluster correction 후에도 유의")
 elif p_wcb < 0.10:
 log.append(f"- ⚠️ WCB borderline")
 else:
 log.append(f"- ❌ WCB not significant — small cluster (15-17 sido) 가 SE 크게 inflate")

 # ====================================================================
 # 2. pre_2008 sub-period diagnosis (despair_total)
 # ====================================================================
 log.append(f"\n## pre_2008 sub-period diagnosis (despair_total)")
 pre = mort[(mort["outcome_group"] == "despair_total") & (mort["year"] <= 2007)].copy
 log.append(f"- pre_2008 rows: {len(pre)}")
 log.append(f"- year distribution: {pre['year'].value_counts.sort_index.to_dict}")
 log.append(f"- pop_wa NaN by year: {pre[pre['pop_wa'].isna].groupby('year').size.to_dict}")
 log.append(f"- log_asr_p1 NaN by year: {pre[pre['log_asr_p1'].isna].groupby('year').size.to_dict}")

 # try multiple windows
 for y0, y1 in [(1998, 2007), (2000, 2007), (1999, 2007), (1997, 2007)]:
 pv_s = pre[pre["year"].isin([y0, y1])].pivot_table(index="h_code", columns="year", values="log_asr_p1", aggfunc="mean").reset_index
 if y0 not in pv_s.columns or y1 not in pv_s.columns:
 log.append(f"- window {y0}-{y1}: pivot 컬럼 부재")
 continue
 pv_s["d_log_pre"] = pv_s[y1] - pv_s[y0]
 ds = (pv_s.merge(iv[["h_code", "z_x_per_worker"]], on="h_code", how="inner")
.merge(h_to_sido, on="h_code", how="left")
.dropna(subset=["d_log_pre", "z_x_per_worker"]))
 if len(ds) < 50:
 log.append(f"- window {y0}-{y1}: n<50 ({len(ds)}), skip")
 continue
 ds["z_x_std"] = (ds["z_x_per_worker"] - ds["z_x_per_worker"].mean) / ds["z_x_per_worker"].std
 X_s = sm.add_constant(ds[["z_x_std"]])
 m_s = sm.OLS(ds["d_log_pre"], X_s).fit(cov_type="cluster", cov_kwds={"groups": ds["sido_code"].astype(str)})
 log.append(f"- window {y0}-{y1}: N={len(ds)}, β={m_s.params['z_x_std']:+.4f}, t={m_s.params['z_x_std']/m_s.bse['z_x_std']:+.2f}, p={m_s.pvalues['z_x_std']:.4f}")

 # ====================================================================
 # 3. final summary
 # ====================================================================
 log.append("\n## 종합")
 log.append("- WCB-sido 가 전통 cluster-sido 보다 SE inflate → small-cluster (15) 영향 정량")
 log.append("- pre_2008 결과 (위 windows) → ICD artifact 검증")

 out = LOGS / f"{TODAY}_phase4_fixes.md"
 out.write_text("\n".join(log), encoding="utf-8")
 print(f"[OK] {out}")

if __name__ == "__main__":
 main
