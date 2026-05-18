"""Phase 2 sub-task 2.5c -- M5 university distance (z_m_education) ETL.

Source: 8_submission/paper_v01_submission/03_mediators/z_m_education_baseline_sensitivity.parquet
This file already contains 1985 / 1990 / 1995 baseline distances and z-scores
(produced in identification diagnostic). paper § 6.4 anchor: Pearson(1985, 1990) = 0.989,
Pearson(1990, 1995) = 1.000, Pearson(1985, 1995) = 0.989.

Output: m5_z_education_pre.parquet
"""
import io
import sys
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
DERIVED = PROJ / "3_derived"

def main:
 src = PROJ / "8_submission" / "paper_v01_submission" / "03_mediators" / "z_m_education_baseline_sensitivity.parquet"
 print(f"[step1] read {src.name}")
 df = pd.read_parquet(src)
 print(f" rows={len(df)}, columns={df.columns.tolist}")

 rename_map = {
 "nearest_dist_km_y1985": "dist_nearest_univ_1985",
 "nearest_dist_km_y1990": "dist_nearest_univ_1990",
 "nearest_dist_km_y1995": "dist_nearest_univ_1995",
 "z_m_edu_y1985": "z_m_education_1985",
 "z_m_edu_y1990": "z_m_education_1990",
 "z_m_edu_y1995": "z_m_education_1995",
 }
 out = df.rename(columns=rename_map)
 out["z_m_education"] = out["z_m_education_1985"]

 cols = [
 "h_code",
 "dist_nearest_univ_1985",
 "dist_nearest_univ_1990",
 "dist_nearest_univ_1995",
 "z_m_education_1985",
 "z_m_education_1990",
 "z_m_education_1995",
 "z_m_education",
 ]
 cols = [c for c in cols if c in out.columns]
 out_path = DERIVED / "m5_z_education_pre.parquet"
 out[cols].to_parquet(out_path, index=False)
 print(f"\n[step2] written: {out_path.name} (rows={len(out)})")

 print("\n[step3] sensitivity Pearson check")
 for a, b in [("1985", "1990"), ("1990", "1995"), ("1985", "1995")]:
 sub = out[[f"dist_nearest_univ_{a}", f"dist_nearest_univ_{b}"]].dropna
 r = sub.corr.iloc[0, 1]
 print(f" Pearson({a}, {b}) = {r:.4f} (expected >= 0.989)")
 for y in ("1985", "1990", "1995"):
 s = out[f"dist_nearest_univ_{y}"]
 print(f" mean nearest distance {y}: {s.mean:.2f} km (n={s.notna.sum})")
 print("\n=== M5 ETL complete ===")

if __name__ == "__main__":
 main
