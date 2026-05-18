"""용인 31460 panel 부재 + 고양 partial 추가 verify."""
import pandas as pd

# === 1. sigungu_crosswalk_v2 의 용인 매핑 ===
print("=" * 60)
print("1. sigungu_crosswalk_v2 용인 매핑")
print("=" * 60)
xw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\sigungu_crosswalk_v2.csv", dtype=str)
yongin_xw = xw[xw["h_code"] == "31460"]
print(f"31460 매핑 raw_codes: {sorted(yongin_xw['raw_code'].unique())}")
print(f"연도 범위: {yongin_xw['year'].min()} - {yongin_xw['year'].max()}")
print(f"총 매핑 행: {len(yongin_xw)}")
print()

# === 2. KOSIS 인구 raw 에서 31460 또는 용인 children 검색 ===
print("=" * 60)
print("2. KOSIS 인구 raw 에서 용인 검색 (31460 + children + h_name)")
print("=" * 60)
pop_raw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\0_raw\kosis_population\population_combined.csv", dtype=str)

print(f"KOSIS raw 에 31460 records: {len(pop_raw[pop_raw['C1'] == '31460'])}")
for child in ["31461", "31463", "31465", "31467", "31469", "31471"]:
    cnt = len(pop_raw[pop_raw["C1"] == child])
    if cnt > 0:
        print(f"  KOSIS raw 에 {child}: {cnt}")

# 용인 이름 검색
print("\n'용인' 이름 검색:")
yongin_name = pop_raw[pop_raw["C1_NM"].astype(str).str.contains("용인", na=False)]
if len(yongin_name) > 0:
    print(f"  '용인' 매칭 unique C1: {sorted(yongin_name['C1'].unique())}")
    print(f"  연도 범위: {yongin_name['year'].min()} - {yongin_name['year'].max()}")
else:
    print("  부재")

# === 3. 사망 microdata 에서 용인 검색 ===
print()
print("=" * 60)
print("3. 사망 microdata 의 용인 검색")
print("=" * 60)
micro = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_microdata_combined.parquet")
yongin_micro = micro[micro["h_code"] == "31460"]
print(f"microdata h_code=31460 records: {len(yongin_micro):,}")

# 용인 이름 검색
yongin_name_micro = micro[micro["h_name"].astype(str).str.contains("용인", na=False)]
if len(yongin_name_micro) > 0:
    print(f"  '용인' 이름 매칭 unique h_code: {sorted(yongin_name_micro['h_code'].unique())}")

# === 4. 229 sigungu 중 panel v01 부재 시군구 ===
print()
print("=" * 60)
print("4. 229 sigungu vs panel v01 cover")
print("=" * 60)
v01 = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_panel_v01.parquet")
panel_h = set(v01["h_code"].unique())
xw_h = set(xw["h_code"].unique())
missing = xw_h - panel_h
print(f"crosswalk h_code 총: {len(xw_h)}")
print(f"panel v01 h_code 총: {len(panel_h)}")
print(f"crosswalk 에 있고 panel v01 에 없는 h_code: {sorted(missing)}")
