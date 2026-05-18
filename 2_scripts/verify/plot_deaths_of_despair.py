"""Deaths of despair 시계열 시각화 — reviewer feedback 용 핵심 figure.

산출:
 4_documentation/figures/deaths_of_despair_timeseries.png
 4_documentation/figures/mediator_specific_rate_by_marital.png

input: mediator_specific_marital_rate_v01.parquet

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\verify\\plot_deaths_of_despair.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic' # 한글 표시
matplotlib.rcParams['axes.unicode_minus'] = False

ROOT = Path(__file__).resolve.parents[2]
RATE_PATH = ROOT / "3_derived" / "mortality" / "mediator_specific_marital_rate_v01.parquet"
FIG_DIR = ROOT / "4_documentation" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def main -> int:
 print("=" * 70)
 print("Deaths of Despair 시계열 visualization")
 print("=" * 70)

 df = pd.read_parquet(RATE_PATH)
 print(f"input: {len(df):,} rows")

 # ─── Figure 1: deaths of despair 4 outcome × 5 period ───
 dod = df[df["cause_group"].isin(["suicide", "drug", "psych", "liver"])].copy
 agg = (dod.groupby(["period", "cause_group"], observed=True)
.agg(deaths=("deaths_5y", "sum"), pop=("population", "sum"))
.reset_index)
 agg["rate_per_100k"] = agg["deaths"] / (agg["pop"] * 5) * 100_000
 pivot = agg.pivot(index="period", columns="cause_group", values="rate_per_100k")

 period_label = {1: "1997-2001", 2: "2002-2006", 3: "2007-2011",
 4: "2012-2016", 5: "2017-2021"}
 pivot.index = [period_label[p] for p in pivot.index]

 fig, ax = plt.subplots(figsize=(11, 6.5))
 colors = {"suicide": "#d62728", "liver": "#2ca02c",
 "psych": "#1f77b4", "drug": "#ff7f0e"}
 labels_kor = {"suicide": "자살 (102)", "liver": "간질환 (081)",
 "psych": "정신질환 (057)", "drug": "약물 (101)"}

 for cause in ["suicide", "liver", "psych", "drug"]:
 ax.plot(pivot.index, pivot[cause], marker='o', linewidth=2.5,
 markersize=10, label=labels_kor[cause], color=colors[cause])

 ax.set_xlabel("5-year stack period (Pierce-Schott 2020)", fontsize=11)
 ax.set_ylabel("Deaths per 100,000 person-year (annual)", fontsize=11)
 ax.set_title("Korea Deaths of Despair, Working-age 25-64\n(MDIS 사망 microdata + 인구 census)",
 fontsize=13, pad=15)
 ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
 ax.grid(True, alpha=0.3)

 # 자살 peak 강조
 ax.annotate("자살 peak\n(카드사태 2003 +\n글로벌 금융위기 2008-2010)",
 xy=("2007-2011", 35.27), xytext=("2017-2021", 42),
 fontsize=9, color="#d62728",
 arrowprops=dict(arrowstyle="->", color="#d62728"))
 ax.annotate("간질환 -57% 감소\n(B형 간염 백신 + 의료 발전)",
 xy=("2017-2021", 19.05), xytext=("2002-2006", 12),
 fontsize=9, color="#2ca02c",
 arrowprops=dict(arrowstyle="->", color="#2ca02c"))
 ax.annotate("약물 매우 낮음\n(US 의 1/10)",
 xy=("2017-2021", 3.86), xytext=("2002-2006", 1),
 fontsize=9, color="#ff7f0e",
 arrowprops=dict(arrowstyle="->", color="#ff7f0e"))

 plt.tight_layout
 out1 = FIG_DIR / "deaths_of_despair_timeseries.png"
 plt.savefig(out1, dpi=150, bbox_inches="tight")
 print(f"[save] {out1.name}")
 plt.close

 # ─── Figure 2: mediator-specific rate (by marital_code) ───
 mar_dod = (df[df["cause_group"].isin(["suicide", "drug", "psych", "liver"])]
.copy)
 mar_dod["marital_label"] = mar_dod["marital_code"].map({
 "1": "1.미혼", "2": "2.배우자", "3": "3.사별", "4": "4.이혼"
 })

 mar_agg = (mar_dod.groupby(["period", "marital_code", "marital_label", "cause_group"],
 observed=True)
.agg(deaths=("deaths_5y", "sum"), pop=("population", "sum"))
.reset_index)
 mar_agg["rate_per_100k"] = mar_agg["deaths"] / (mar_agg["pop"] * 5) * 100_000

 fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharex=True)
 causes = [("suicide", "자살 (cause=102)"), ("liver", "간질환 (cause=081)"),
 ("psych", "정신질환 (cause=057)"), ("drug", "약물 (cause=101)")]

 for ax, (cause, title) in zip(axes.flat, causes):
 sub = mar_agg[mar_agg["cause_group"] == cause]
 for label in ["1.미혼", "2.배우자", "3.사별", "4.이혼"]:
 grp = sub[sub["marital_label"] == label].sort_values("period")
 grp_idx = [period_label[p] for p in grp["period"]]
 ax.plot(grp_idx, grp["rate_per_100k"], marker='o', linewidth=2,
 markersize=8, label=label)
 ax.set_title(title, fontsize=12)
 ax.set_ylabel("Per 100K", fontsize=10)
 ax.legend(fontsize=9, loc='best', framealpha=0.9)
 ax.grid(True, alpha=0.3)
 ax.tick_params(axis='x', rotation=30)

 fig.suptitle("Mediator-specific Mortality Rate by Marital Status × Cause × Period\n"
 "(Working-age 25-64, Korea 1997-2021)", fontsize=13, y=1.00)
 plt.tight_layout
 out2 = FIG_DIR / "mediator_specific_rate_by_marital.png"
 plt.savefig(out2, dpi=150, bbox_inches="tight")
 print(f"[save] {out2.name}")
 plt.close

 # ─── Figure 3: 미혼 vs 배우자 자살 격차 (key mediation finding) ───
 suicide_mar = mar_agg[mar_agg["cause_group"] == "suicide"].copy
 pivot_s = suicide_mar.pivot(index="period", columns="marital_label",
 values="rate_per_100k")
 pivot_s.index = [period_label[p] for p in pivot_s.index]

 fig, ax = plt.subplots(figsize=(11, 6))
 for label in ["1.미혼", "2.배우자", "3.사별", "4.이혼"]:
 if label in pivot_s.columns:
 ax.plot(pivot_s.index, pivot_s[label], marker='o', linewidth=2.5,
 markersize=10, label=label)
 ax.set_xlabel("5-year stack period")
 ax.set_ylabel("자살 (cause=102) per 100K person-year")
 ax.set_title("자살률 by 혼인상태 × 시점 (Working-age 25-64)\n"
 "→ 본 paper § 5.2 mediation 의 marital channel 핵심 evidence",
 fontsize=12, pad=15)
 ax.legend(loc='upper left', fontsize=11, framealpha=0.95)
 ax.grid(True, alpha=0.3)
 plt.tight_layout
 out3 = FIG_DIR / "suicide_by_marital.png"
 plt.savefig(out3, dpi=150, bbox_inches="tight")
 print(f"[save] {out3.name}")
 plt.close

 print(f"\n총 3 figure 산출: {FIG_DIR}")
 return 0

if __name__ == "__main__":
 sys.exit(main)
