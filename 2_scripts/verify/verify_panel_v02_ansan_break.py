"""Panel v02 안산 31190 verify + break -34.6% 정밀 분석 + 5 추가 분구 spot check."""
import pandas as pd

# === 1. Panel v02 안산 31190 verify ===
print("=" * 60)
print("1. Panel v02 안산 31190 verify (sido prefix 정정)")
print("=" * 60)

v02 = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_rate_panel_v02.parquet")
print(f"v02 unique h_code 총: {v02['h_code'].nunique()}")
print(f"v02 sido prefix 분포:")
print(v02["h_code"].astype(str).str[:2].value_counts().sort_index())

ansan = v02[v02["h_code"] == "31190"]
print(f"\n안산 31190 records: {len(ansan):,}")
print(f"outcome_groups: {ansan['outcome_group'].unique()}")

# === 2. 안산 break -34.6% 정밀 분석 ===
print()
print("=" * 60)
print("2. 안산 31190 시계열 (외환위기 vs 분구 효과 분리)")
print("=" * 60)

for og in ["despair_total", "suicide_102", "liver_081", "cardiovascular"]:
    sub = ansan[ansan["outcome_group"] == og]
    if len(sub) == 0:
        print(f"\n{og}: no data")
        continue
    yearly = sub.groupby("year")["asr_kr2010_per_100k"].mean().sort_index()
    print(f"\n=== 안산 {og} (성평균 ASR) ===")
    for y in ["1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2010", "2015", "2020", "2023"]:
        if y in yearly.index:
            print(f"  {y}: {yearly[y]:>7.2f}/100k")
    pre = yearly.loc[[y for y in ["1997", "1998", "1999", "2000", "2001"] if y in yearly.index]].mean()
    post = yearly.loc[[y for y in ["2003", "2004", "2005", "2006", "2007"] if y in yearly.index]].mean()
    if pre > 0:
        print(f"  pre 1997-2001: {pre:.2f}, post 2003-2007: {post:.2f}, diff: {(post-pre)/pre*100:+.2f}%")

# 전국 평균 비교
print()
print("=" * 60)
print("3. 안산 vs 전국 평균 (despair_total)")
print("=" * 60)
nat = v02[v02["outcome_group"] == "despair_total"].groupby("year")["asr_kr2010_per_100k"].mean().sort_index()
ans_d = ansan[ansan["outcome_group"] == "despair_total"].groupby("year")["asr_kr2010_per_100k"].mean().sort_index()
print(f"{'year':<6}{'전국':>10}{'안산':>10}{'차이':>10}")
for y in ["1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007"]:
    if y in nat.index and y in ans_d.index:
        print(f"{y:<6}{nat[y]:>10.2f}{ans_d[y]:>10.2f}{ans_d[y]-nat[y]:>+10.2f}")

# === 3. 5 추가 분구 시군구 parent vs children 합 spot check ===
print()
print("=" * 60)
print("4. 5 추가 분구 시군구 spot check (수원/성남/안양/안산/고양)")
print("=" * 60)

import os, glob
xw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\sigungu_crosswalk_v2.csv", dtype=str)

# KOSIS 인구 raw csv 로 비교
pop_csv = r"C:\Users\82103\Downloads\trade_mortality_korea\0_raw\kosis_population\population_combined.csv"
pop_raw = pd.read_csv(pop_csv, dtype=str)

CASES = [
    ("31110", "수원", ["31111", "31112", "31113", "31114", "31115", "31116", "31117"]),
    ("31130", "성남", ["31131", "31132", "31133", "31134", "31135"]),
    ("31170", "안양", ["31171", "31172", "31173"]),
    ("31190", "안산", ["31191", "31192", "31193"]),
    ("31280", "고양", ["31281", "31282", "31285", "31287"]),
    ("31460", "용인", ["31461", "31463", "31465"]),
]

for parent, name, children in CASES:
    print(f"\n--- {name} parent={parent}, children={children} ---")
    for year in ["2000", "2005", "2010", "2015"]:
        # parent 인구 (C2='0' 계, C3='000' 계)
        parent_row = pop_raw[(pop_raw["C1"] == parent) & (pop_raw["year"] == year) &
                             (pop_raw["C2"] == "0") & (pop_raw["C3"] == "000")]
        # children 합
        children_rows = pop_raw[(pop_raw["C1"].isin(children)) & (pop_raw["year"] == year) &
                                (pop_raw["C2"] == "0") & (pop_raw["C3"] == "000")]
        if len(parent_row) == 0 and len(children_rows) == 0:
            print(f"  {year}: parent + children 모두 부재")
            continue
        parent_pop = float(parent_row["population"].iloc[0]) if len(parent_row) > 0 else None
        children_sum = children_rows["population"].astype(float).sum() if len(children_rows) > 0 else None
        if parent_pop is not None and children_sum is not None and children_sum > 0:
            diff = parent_pop - children_sum
            pct = diff / children_sum * 100 if children_sum > 0 else 0
            print(f"  {year}: parent={parent_pop:>10,.0f}  children_sum={children_sum:>10,.0f}  diff={diff:>+8,.0f} ({pct:+.4f}%)")
        elif parent_pop is not None:
            print(f"  {year}: parent={parent_pop:>10,.0f}  children=부재 (parent only reporting)")
        else:
            print(f"  {year}: parent=부재  children_sum={children_sum:>10,.0f} (children only reporting)")
