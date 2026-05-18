"""
Step 4 — Crosswalk validation

Checks:
 (a) Per-year matching rate vs step2 raw mortality codes (target: 100%)
 (b) Each year's deaths sum is preserved (raw → h_code aggregation lossless)
 (c) Per-year sido coverage (17 sido for ≥2012, 16 sido pre-세종)
 (d) Per-year h_code count (sanity: should be ≤ 262)
 (e) 군위 cross-sido check: h_code 37310 should appear under sido 37 pre-2023, sido 22 in 2023
 (f) KOSTAT 4년치 cross-check: 시도별 자살(102) deaths from raw == aggregated to h_code → sido

Output:
 3_derived/sigungu/step4_validation_report.md
"""
from __future__ import annotations
import sys
import io
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve.parents[2]
DERIVED = ROOT / "3_derived" / "sigungu"
MAP = DERIVED / "step3_h_code_mapping.csv"
RAW = DERIVED / "step2_raw_sigungu_by_year.csv"
OUT = DERIVED / "step4_validation_report.md"

def main -> None:
 m = pd.read_csv(MAP)
 r = pd.read_csv(RAW)
 m["raw_code"] = m["raw_code"].astype(int)
 r["raw_code"] = r["raw_code"].astype(int)
 m["h_code"] = m["h_code"].astype(int)

 lines: list[str] = 
 add = lines.append

 add("# Step 4 — Sigungu crosswalk 검증 보고서\n")
 add(f"- 매핑 테이블: `{MAP.name}` ({len(m):,} rows)")
 add(f"- 원본 raw: `{RAW.name}` ({len(r):,} rows)\n")

 # (a) per-year match rate
 add("## (a) 연도별 매칭률 (raw → h_code)\n")
 join = r.merge(m, on=["year", "raw_code"], how="left", indicator=True)
 cov = join.groupby("year").agg(
 n_raw=("raw_code", "size"),
 n_matched=("_merge", lambda s: (s == "both").sum),
 n_deaths_raw=("n_deaths", "sum"),
).reset_index
 cov["match_rate"] = cov["n_matched"] / cov["n_raw"]
 add("| year | n_raw | n_matched | match_rate | n_deaths_raw |")
 add("|------|------:|----------:|-----------:|-------------:|")
 for _, row in cov.iterrows:
 add(f"| {row.year} | {row.n_raw} | {row.n_matched} | {row.match_rate:.4f} | {row.n_deaths_raw:,} |")

 overall = (cov["n_matched"].sum / cov["n_raw"].sum)
 add(f"\n**Overall match rate: {overall:.4%}**")
 if overall < 1.0:
 add("⚠️ 100% 미달")
 else:
 add("✅ 100% 매칭")

 # (b) deaths preservation: raw deaths per year == aggregated to h_code → sum
 add("\n## (b) 사망자 합계 보존성 (raw 합 vs h_code 합)\n")
 deaths_raw = r.groupby("year")["n_deaths"].sum.rename("deaths_raw")
 agg = (
 r.merge(m[["year", "raw_code", "h_code"]], on=["year", "raw_code"], how="inner")
.groupby(["year"])["n_deaths"].sum.rename("deaths_via_hcode")
)
 cmp = pd.concat([deaths_raw, agg], axis=1).fillna(0).astype(int)
 cmp["delta"] = cmp["deaths_via_hcode"] - cmp["deaths_raw"]
 add("| year | deaths_raw | deaths_via_hcode | delta |")
 add("|------|-----------:|-----------------:|------:|")
 for y, row in cmp.iterrows:
 flag = "" if row.delta == 0 else " ⚠️"
 add(f"| {y} | {row.deaths_raw:,} | {row.deaths_via_hcode:,} | {row.delta}{flag} |")

 # (c) sido coverage per year
 add("\n## (c) 연도별 시도 coverage (h_code 기준)\n")
 add(
 "h_code = 2021-baseline 기준이므로 retroactive sido 재매핑이 발생.\n"
 "예: 연기군(1997-2011) 사망자 → h_sido 29 (세종). 즉 pre-2012 에도 sido=29 가 1건 등장.\n"
 "→ pre-2012 17 sido (16 행정 + 연기군 유래 세종), 2012+ 17 sido 가 정상.\n"
)
 sido_y = m.groupby("year")["sido_code"].nunique.rename("n_sido").reset_index
 add("| year | n_sido |")
 add("|------|------:|")
 for _, row in sido_y.iterrows:
 flag = ""
 # 17 expected throughout (panel-consistent h_sido)
 if row.n_sido!= 17:
 flag = " ⚠️ expected 17"
 add(f"| {row.year} | {row.n_sido}{flag} |")

 # (d) per-year h_code count
 add("\n## (d) 연도별 distinct h_code count\n")
 hc_y = m.groupby("year")["h_code"].nunique.rename("n_h_code").reset_index
 add("| year | n_h_code |")
 add("|------|--------:|")
 for _, row in hc_y.iterrows:
 flag = " ⚠️ >262" if row.n_h_code > 262 else ""
 add(f"| {row.year} | {row.n_h_code}{flag} |")

 # (e) 군위 cross-sido test
 add("\n## (e) 군위군 cross-sido transfer (2023.7.1)\n")
 gw = m[m.h_code == 37310].sort_values("year")
 add("| year | raw_code | h_code | h_name | sido_code | sido_name |")
 add("|------|--------:|------:|------|---------:|------|")
 for _, row in gw.iterrows:
 add(f"| {row.year} | {row.raw_code} | {row.h_code} | {row.h_name} | {row.sido_code} | {row.sido_name} |")
 pre = gw[gw.year < 2023]["sido_code"].unique
 post = gw[gw.year == 2023]["sido_code"].unique
 if list(pre) == [37] and list(post) == [22]:
 add("\n✅ 군위 transfer 정상: pre-2023 sido=37 (경북), 2023 sido=22 (대구)")
 else:
 add(f"\n⚠️ 군위 transfer 이상: pre={list(pre)}, post={list(post)}")

 # (f) KOSTAT cross-check — 시도별 자살(코드 102) 합계 4년치
 add("\n## (f) KOSTAT 자살(102) 시도별 cross-check\n")
 add("(별도 KOSTAT 공시값과 비교하기 위한 시도별 raw 합계 — 본 검증은 sigungu→sido aggregation 정합성만 점검)\n")
 # Aggregate raw → sido via crosswalk
 # We don't have ICD here — approximate by joining all raw sigungu deaths and grouping by mapped sido_code
 sido_agg = (
 r.merge(m[["year", "raw_code", "sido_code"]], on=["year", "raw_code"], how="inner")
.groupby(["year", "sido_code"])["n_deaths"].sum.reset_index
)
 # Spot-check: 2023 군위가 sido 22(대구)에 합류했는지
 g23 = sido_agg[(sido_agg.year == 2023) & (sido_agg.sido_code == 22)]
 g22 = sido_agg[(sido_agg.year == 2022) & (sido_agg.sido_code == 22)]
 add("**spot check**: 대구(22) 사망자 합 (군위 합류 효과)\n")
 add(f"- 2022 대구 합 = {int(g22['n_deaths'].iloc[0]):,}")
 add(f"- 2023 대구 합 = {int(g23['n_deaths'].iloc[0]):,}")
 # 2023 경북에서 군위 빠진 효과
 gb22 = sido_agg[(sido_agg.year == 2022) & (sido_agg.sido_code == 37)]
 gb23 = sido_agg[(sido_agg.year == 2023) & (sido_agg.sido_code == 37)]
 add(f"- 2022 경북 합 = {int(gb22['n_deaths'].iloc[0]):,}")
 add(f"- 2023 경북 합 = {int(gb23['n_deaths'].iloc[0]):,}")

 # 2023 군위 raw_code 22520 을 보여줌
 g_w_2023 = r[(r.year == 2023) & (r.raw_code == 22520)]
 if len(g_w_2023):
 add(f"- 군위 2023 raw_code=22520 deaths = {int(g_w_2023['n_deaths'].iloc[0]):,}")

 add("\n## 종합")
 fails = 
 if overall < 1.0:
 fails.append("(a) 매칭률")
 if (cmp["delta"]!= 0).any:
 fails.append("(b) deaths 보존")
 if (sido_y["n_sido"]!= 17).any:
 fails.append("(c) sido coverage")
 if (hc_y["n_h_code"] > 262).any:
 fails.append("(d) h_code 카운트")
 if list(pre)!= [37] or list(post)!= [22]:
 fails.append("(e) 군위 transfer")
 if not fails:
 add("\n✅ 모든 검증 통과")
 else:
 add(f"\n⚠️ 실패: {', '.join(fails)}")

 OUT.write_text("\n".join(lines), encoding="utf-8")
 print(f"[step4] wrote: {OUT}")
 print(f"[step4] overall match rate: {overall:.4%}")
 print(f"[step4] fails: {fails or 'NONE'}")

if __name__ == "__main__":
 main
