"""
Phase 2-A — Population join fix v3 — incremental log + merge diagnostic.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
import traceback

import numpy as np
import pandas as pd

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
RAW_POP = PROJ / "0_raw" / "kosis_population" / "population_combined.csv"
CW = PROJ / "1_codebooks" / "sigungu_crosswalk.csv"
PANEL_IN = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
PANEL_OUT = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
LOGS = PROJ / "5_logs" / "integrity_checks"
LOGS.mkdir(parents=True, exist_ok=True)
TODAY = date.today.isoformat

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LOG_PATH = LOGS / f"{TODAY}_population_join_fix.md"
log_buf: list[str] = [f"# Phase 2-A — Population join fix v3 (incremental)\n_{TODAY}_\n"]

def flush:
 LOG_PATH.write_text("\n".join(log_buf), encoding="utf-8")

def log(msg: str):
 log_buf.append(msg)
 flush
 print(msg)

def main:
 # 1) load
 panel = pd.read_parquet(PANEL_IN)
 log(f"## Mortality panel\n- rows: {len(panel):,}, cols: {list(panel.columns)}")

 pop = pd.read_csv(RAW_POP, dtype=str)
 log(f"\n## Population panel raw\n- rows: {len(pop):,}, cols: {list(pop.columns)}")

 # 2) C1 / C2 / C3 진단 — schema 결정
 log(f"\n## Schema 진단")
 log(f"- C1 length dist: {pop['C1'].astype(str).str.len.value_counts.to_dict}")
 log(f"- C1 first 10 unique: {pop['C1'].dropna.unique[:10].tolist}")
 log(f"- C2 unique: {pop['C2'].astype(str).value_counts.head(10).to_dict}")
 log(f"- C3_NM unique (top 30): {pop['C3_NM'].dropna.unique[:30].tolist}")
 log(f"- year range: {pop['year'].min}-{pop['year'].max}")

 # 3) age band — working-age 25-64
 pop["__age_lo"] = pd.to_numeric(pop["C3_NM"].astype(str).str.extract(r"(\d+)").iloc[:, 0], errors="coerce")
 wa_lows = list(range(25, 65, 5)) # 25,30,35,40,45,50,55,60
 pop_wa = pop[pop["__age_lo"].isin(wa_lows)].copy
 log(f"\n## Working-age filter\n- pop_wa rows: {len(pop_wa):,}")

 # 4) C1 = 5-digit only (시도-only "11", "00" 전국 제외)
 pop_wa["raw_code"] = pop_wa["C1"].astype(str)
 pop_wa = pop_wa[pop_wa["raw_code"].str.len == 5].copy
 log(f"- after 5-digit C1 filter: {len(pop_wa):,}")
 log(f"- raw_code distinct: {pop_wa['raw_code'].nunique}")

 # 5) C2 — total only (가장 frequent value)
 c2_top = pop_wa["C2"].astype(str).value_counts.idxmax
 log(f"- C2 top value: '{c2_top}' (frequency {(pop_wa['C2'].astype(str) == c2_top).sum:,})")
 pop_wa = pop_wa[pop_wa["C2"].astype(str) == c2_top].copy
 log(f"- after C2='{c2_top}' filter: {len(pop_wa):,}")

 pop_wa["year"] = pd.to_numeric(pop_wa["year"], errors="coerce").astype("Int64")
 pop_wa["__pop"] = pd.to_numeric(pop_wa["population"], errors="coerce")

 # 6) crosswalk merge diagnostic
 cw = pd.read_csv(CW, dtype=str)
 cw["year"] = pd.to_numeric(cw["year"], errors="coerce").astype("Int64")
 cw_subset = cw[["year", "raw_code", "h_code"]].drop_duplicates
 log(f"\n## Crosswalk merge 진단")
 log(f"- crosswalk rows: {len(cw_subset):,}")
 log(f"- crosswalk raw_code distinct: {cw_subset['raw_code'].nunique}")
 log(f"- crosswalk year range: {cw_subset['year'].min}-{cw_subset['year'].max}")
 log(f"- crosswalk raw_code first 10: {cw_subset['raw_code'].unique[:10].tolist}")

 # 직접 intersect 확인
 pop_codes = set(pop_wa["raw_code"].unique)
 cw_codes = set(cw_subset["raw_code"].unique)
 log(f"- pop raw_code: {len(pop_codes)}, crosswalk raw_code: {len(cw_codes)}")
 log(f"- intersect: {len(pop_codes & cw_codes)}")
 log(f"- pop only (top 10): {sorted(pop_codes - cw_codes)[:10]}")
 log(f"- cw only (top 10): {sorted(cw_codes - pop_codes)[:10]}")

 # 7) merge
 pop_h = pop_wa.merge(cw_subset, on=["year", "raw_code"], how="left")
 n_match = pop_h["h_code"].notna.sum
 log(f"\n## Merge result\n- match rate: {n_match:,}/{len(pop_h):,} ({n_match/len(pop_h):.1%})")

 if n_match == 0:
 # year 없는 fallback — crosswalk h_code 가 시간 invariant 라고 가정
 log(f"\n[FALLBACK] year-less merge 시도 — h_code 가 시간 invariant 인 raw_code 만 사용")
 cw_invariant = cw_subset.drop_duplicates("raw_code")[["raw_code", "h_code"]]
 pop_h = pop_wa.merge(cw_invariant, on="raw_code", how="left")
 n_match = pop_h["h_code"].notna.sum
 log(f"- year-less match: {n_match:,}/{len(pop_h):,} ({n_match/len(pop_h):.1%})")

 pop_h = pop_h.dropna(subset=["h_code"])
 log(f"- after drop unmatched: {len(pop_h):,}")

 if len(pop_h) == 0:
 log("\n[FL] no rows after merge. mortality_rate 산출 불가.")
 return

 # 8) aggregate h_code × year → pop_wa
 pop_panel = pop_h.groupby(["h_code", "year"])["__pop"].sum.reset_index
 pop_panel.columns = ["h_code", "year", "pop_wa"]
 log(f"\n## pop_wa aggregate\n- rows: {len(pop_panel):,}")
 log(f"- pop_wa stats: mean={pop_panel['pop_wa'].mean:,.0f}, median={pop_panel['pop_wa'].median:,.0f}")
 sum_2010 = pop_panel.loc[pop_panel["year"] == 2010, "pop_wa"].sum
 log(f"- 2010 전국 합: {sum_2010:,.0f} (KOSIS expected ~30M)")

 # 9) join with mortality
 panel["year"] = panel["year"].astype("Int64")
 if "pop_wa" in panel.columns:
 panel = panel.drop(columns=["pop_wa"])
 if "mortality_rate" in panel.columns:
 panel = panel.drop(columns=["mortality_rate"])
 if "log_asr_p1" in panel.columns:
 panel = panel.drop(columns=["log_asr_p1"])

 merged = panel.merge(pop_panel, on=["h_code", "year"], how="left")
 n_pop_match = merged["pop_wa"].notna.sum if "pop_wa" in merged.columns else 0
 log(f"\n## Mortality + pop join\n- pop matched: {n_pop_match:,}/{len(merged):,} ({n_pop_match/len(merged):.1%})")

 if n_pop_match > 0:
 merged["mortality_rate"] = merged["deaths"] / merged["pop_wa"].replace(0, np.nan) * 100_000
 merged["log_asr_p1"] = np.log(merged["mortality_rate"] + 1)
 merged["period_pre2008"] = (merged["year"] <= 2007).astype(int)
 log(f"- mortality_rate non-null: {merged['mortality_rate'].notna.sum:,}")
 log(f"- mortality_rate stats: mean={merged['mortality_rate'].mean:.1f}, median={merged['mortality_rate'].median:.1f}")

 # save
 merged.to_parquet(PANEL_OUT, index=False)
 log(f"\n- saved: `{PANEL_OUT.relative_to(PROJ)}`")
 log(f"- final shape: {merged.shape}")

 # external validation
 log("\n## External validation: despair_total WA rate 전국")
 despair = merged[merged["outcome_group"] == "despair_total"]
 nat = despair.groupby("year").agg(deaths=("deaths", "sum"), pop=("pop_wa", "sum")).reset_index
 nat["rate_per_100k"] = nat["deaths"] / nat["pop"] * 100_000
 log("```")
 log(nat.tail(15).to_string(index=False))
 log("```")
 log("- KOSIS suicide WA 2010 ≈ 32-35/100k (despair = +drug+psych+liver, 약간 더 높을 것)")
 else:
 log("\n[FL] mortality + pop merge 0%. 별도 진단 필요.")

if __name__ == "__main__":
 try:
 main
 except Exception as e:
 log(f"\n[CRASH] {e}\n```\n{traceback.format_exc}\n```")
 raise
