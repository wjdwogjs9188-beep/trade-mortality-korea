"""
Verify v02_wa panel = working-age (reviewer critique).

Spot-check: 종로구 11010 2020 pop_wa 가 WA 범위 (80-90k both sex) 인지.
- All-age both sex 종로구 2020 ≈ 140k
- WA 25-64 both sex 종로구 2020 ≈ 80-90k (KOSIS published)

또한 5 outcome group 별 mortality_rate 분포 + 2010 외부 검증.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(r"C:\Users\82103\Downloads\trade_mortality_korea")
PANEL = PROJ / "3_derived" / "mortality" / "sigungu_mortality_panel_v02_wa.parquet"
LOG = PROJ / "5_logs" / "integrity_checks" / "2026-05-05_v02_wa_verification.md"

log = ["# v02_wa panel verification (clear)\n_2026-05-05_\n"]

df = pd.read_parquet(PANEL)
log.append(f"## panel\n- shape: {df.shape}, cols: {list(df.columns)}\n")

# spot-check: 종로구 11010 in 2020 (or most recent)
jongno = df[(df["h_code"] == "11010") & (df["year"] == 2020)]
log.append(f"## 종로구 (11010) 2020 spot-check (reviewer)")
if len(jongno) > 0:
 pop_wa = jongno["pop_wa"].iloc[0]
 log.append(f"- pop_wa: **{pop_wa:,.0f}**")
 if 70_000 <= pop_wa <= 100_000:
 log.append(f"- ✅ **working-age range (70-100k)** — WA filter 정상 적용")
 elif 130_000 <= pop_wa <= 160_000:
 log.append(f"- ❌ all-age range (130-160k) — WA filter 미적용. v3 rebuild 필요")
 else:
 log.append(f"- ⚠️ 예상 외 범위. KOSIS 발표 종로구 WA 2020 약 80-90k 와 비교 필요")
else:
 log.append("- ⚠️ 종로구 2020 data 없음")

# outcome group 별 row count
log.append(f"\n## outcome group 별 row count")
log.append("```")
log.append(df["outcome_group"].value_counts.to_string)
log.append("```")

# 2010 전국 + 종로구 mortality_rate (despair_total)
log.append(f"\n## 2010 전국 despair_total — KOSIS suicide WA cross-check")
d2010 = df[(df["year"] == 2010) & (df["outcome_group"] == "despair_total")]
nat_deaths = d2010["deaths"].sum
nat_pop = d2010["pop_wa"].sum
nat_rate = nat_deaths / nat_pop * 100_000
log.append(f"- 전국 deaths: {nat_deaths:,}")
log.append(f"- 전국 pop_wa: {nat_pop:,.0f}")
log.append(f"- 전국 rate: {nat_rate:.1f} per 100k")
log.append(f"- KOSIS suicide WA 2010 ≈ 32-35, despair = +drug+psych+liver → 약 45-50 expected")
if 40 <= nat_rate <= 55:
 log.append(f"- ✅ external validation pass")
else:
 log.append(f"- ⚠️ deviation from expected")

# 종로구 sample by year (despair)
log.append(f"\n## 종로구 (11010) despair_total time series")
jn_d = df[(df["h_code"] == "11010") & (df["outcome_group"] == "despair_total")][["year", "deaths", "pop_wa", "mortality_rate"]].sort_values("year")
log.append("```")
log.append(jn_d.to_string(index=False))
log.append("```")

# panel coverage
log.append(f"\n## panel coverage")
log.append(f"- distinct h_code: {df['h_code'].nunique}")
log.append(f"- year range: {df['year'].min}-{df['year'].max}")
log.append(f"- mortality_rate non-null: {df['mortality_rate'].notna.sum:,}/{len(df):,}")

LOG.write_text("\n".join(log), encoding="utf-8")
print(f"[OK] {LOG}")
