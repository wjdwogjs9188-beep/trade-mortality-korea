"""정확한 11 분구 시군구 코드로 break + spot check 재실행."""
import pandas as pd

CASES = {
    "31010": ("수원", ["31011", "31012", "31013", "31014"]),
    "31020": ("성남", ["31021", "31022", "31023"]),
    "31050": ("부천", ["31051", "31052", "31053"]),
    "31040": ("안양", ["31041", "31042"]),
    "31090": ("안산", ["31091", "31092", "31093"]),  # 안산 정확
    "31100": ("고양", ["31101", "31102", "31103"]),
    "31190": ("용인", ["31191", "31192", "31193"]),  # 용인 정확
    "33040": ("청주", ["33041", "33042", "33043", "33044"]),
    "34010": ("천안", ["34011", "34012"]),
    "35010": ("전주", ["35011", "35012"]),
    "37010": ("포항", ["37011", "37012"]),
    "38110": ("창원", ["38111", "38112", "38113", "38114", "38115"]),
}

# === 1. panel v02 안산 31090 break 재분석 ===
print("=" * 60)
print("1. 안산 31090 break 재분석 (정확한 코드)")
print("=" * 60)
v02 = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_rate_panel_v02.parquet")
ansan = v02[v02["h_code"] == "31090"]
print(f"안산 31090 records: {len(ansan):,}")

for og in ["despair_total", "suicide_102", "liver_081", "cardiovascular"]:
    sub = ansan[ansan["outcome_group"] == og]
    if len(sub) == 0:
        continue
    yearly = sub.groupby("year")["asr_kr2010_per_100k"].mean().sort_index()
    pre = yearly.loc[[y for y in ["1997","1998","1999","2000","2001"] if y in yearly.index]].mean()
    post = yearly.loc[[y for y in ["2003","2004","2005","2006","2007"] if y in yearly.index]].mean()
    print(f"  {og}: pre={pre:.2f}, post={post:.2f}, diff={(post-pre)/pre*100:+.2f}%" if pre > 0 else f"  {og}: pre=0")

# === 2. 11 분구 시군구 spot check 재실행 ===
print()
print("=" * 60)
print("2. 11 분구 시군구 parent vs children spot check (정확한 코드)")
print("=" * 60)
pop_raw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\0_raw\kosis_population\population_combined.csv", dtype=str)

verified = 0
na_count = 0
for parent, (name, children) in CASES.items():
    print(f"\n--- {name} parent={parent} ---")
    has_data = False
    for year in ["2000", "2005", "2010", "2015"]:
        parent_row = pop_raw[(pop_raw["C1"] == parent) & (pop_raw["year"] == year) &
                             (pop_raw["C2"] == "0") & (pop_raw["C3"] == "000")]
        children_rows = pop_raw[(pop_raw["C1"].isin(children)) & (pop_raw["year"] == year) &
                                (pop_raw["C2"] == "0") & (pop_raw["C3"] == "000")]
        parent_pop = float(parent_row["population"].iloc[0]) if len(parent_row) > 0 else None
        children_sum = children_rows["population"].astype(float).sum() if len(children_rows) > 0 else None

        if parent_pop and children_sum and children_sum > 0:
            diff = parent_pop - children_sum
            pct = diff / children_sum * 100
            print(f"  {year}: parent={parent_pop:>10,.0f}  children={children_sum:>10,.0f}  diff={pct:+.4f}%")
            has_data = True
        elif parent_pop:
            print(f"  {year}: parent={parent_pop:>10,.0f}  (children only KOSIS 부재)")
        elif children_sum:
            print(f"  {year}: parent 부재 children={children_sum:>10,.0f}")
        else:
            print(f"  {year}: parent + children 모두 부재")
    if has_data:
        verified += 1
    else:
        na_count += 1

print()
print(f"=== Summary: verified={verified}/{len(CASES)}, single-unit reporting={na_count}/{len(CASES)} ===")

# === 3. 안산 vs 전국 비교 (정확) ===
print()
print("=" * 60)
print("3. 안산 31090 vs 전국 평균 (despair_total)")
print("=" * 60)
nat = v02[v02["outcome_group"] == "despair_total"].groupby("year")["asr_kr2010_per_100k"].mean().sort_index()
ans = ansan[ansan["outcome_group"] == "despair_total"].groupby("year")["asr_kr2010_per_100k"].mean().sort_index()
print(f"{'year':<6}{'전국':>10}{'안산31090':>12}{'차이':>10}")
for y in ["1997","1998","1999","2000","2001","2002","2003","2004","2005","2010","2015","2020","2023"]:
    if y in nat.index and y in ans.index:
        print(f"{y:<6}{nat[y]:>10.2f}{ans[y]:>12.2f}{ans[y]-nat[y]:>+10.2f}")
