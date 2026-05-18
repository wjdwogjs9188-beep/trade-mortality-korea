"""Phase 2 sub-task 2.5d -- M6 KOSTAT suicide validation ETL.

Source: 3_derived/mortality/mortality_rate_panel_v02_1.parquet
 Filter outcome_group == 'suicide_102' (KOSTAT 102, X60-X84).
 Sum across sex_code, then collapse 1997-1999 baseline + 2018-2022 endpoint.

Note: 8_submission/.../sigungu_mortality_panel_v02_wa.parquet does not split
out suicide-only -- it stores the despair_total composite. The
mortality_rate_panel_v02_1 derived file retains the per-code split.

Output: m6_suicide_panel.parquet with columns
 h_code, log_suicide_rate_baseline, log_suicide_rate_endpoint, delta_log_suicide
"""
import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
DERIVED = PROJ / "3_derived"

def main:
 src = PROJ / "3_derived" / "mortality" / "mortality_rate_panel_v02_1.parquet"
 print(f"[step1] read {src.name}")
 mr = pd.read_parquet(src)
 print(f" rows={len(mr)}, outcome_groups={mr['outcome_group'].unique.tolist}")
 sui = mr[mr["outcome_group"] == "suicide_102"].copy
 sui["year"] = sui["year"].astype(int)
 sui["h_code"] = sui["h_code"].astype(int)
 print(f" suicide_102 rows: {len(sui)} (sex_code, year, h_code panel)")

 print("\n[step2] aggregate across sex_code (sum deaths, sum population)")
 agg = (
 sui.groupby(["h_code", "year"], as_index=False)
.agg(deaths=("deaths", "sum"), population=("population", "sum"))
)
 agg["suicide_rate"] = agg["deaths"] / np.maximum(agg["population"], 1.0) * 100000.0
 agg["log_suicide_rate"] = np.log(agg["suicide_rate"] + 1e-3)

 print("\n[step3] long-difference 1997-1999 baseline vs 2018-2022 endpoint")
 base = (
 agg[agg["year"].isin(range(1997, 2000))]
.groupby("h_code", as_index=False)["log_suicide_rate"]
.mean
.rename(columns={"log_suicide_rate": "log_suicide_rate_baseline"})
)
 end = (
 agg[agg["year"].isin(range(2018, 2023))]
.groupby("h_code", as_index=False)["log_suicide_rate"]
.mean
.rename(columns={"log_suicide_rate": "log_suicide_rate_endpoint"})
)
 out = base.merge(end, on="h_code", how="outer")
 out["delta_log_suicide"] = out["log_suicide_rate_endpoint"] - out["log_suicide_rate_baseline"]

 out_path = DERIVED / "m6_suicide_panel.parquet"
 out.to_parquet(out_path, index=False)
 print(f"\n[step4] written: {out_path.name} (rows={len(out)})")
 print(f" delta_log_suicide: mean={out['delta_log_suicide'].mean:+.4f}, std={out['delta_log_suicide'].std:.4f}, n={out['delta_log_suicide'].notna.sum}")
 print("\n=== M6 ETL complete ===")

if __name__ == "__main__":
 main
