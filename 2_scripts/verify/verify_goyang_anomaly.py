"""고양 31100 children 매핑 anomaly 점검."""
import pandas as pd

pop_raw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\0_raw\kosis_population\population_combined.csv", dtype=str)

# KOSIS raw 의 311xx 모든 코드
print("=" * 60)
print("KOSIS raw 의 311xx 코드 (고양 자치구 가능성)")
print("=" * 60)
goyang_codes = sorted(pop_raw[pop_raw["C1"].astype(str).str.startswith("311")]["C1"].unique)
print(f"311xx codes: {goyang_codes}")
print

for code in goyang_codes:
 sample = pop_raw[(pop_raw["C1"] == code) & (pop_raw["C2"] == "0") & (pop_raw["C3"] == "000")]
 if len(sample) > 0:
 name = sample["C1_NM"].iloc[0]
 years = sorted(sample["year"].unique)
 print(f" {code} ({name}): years {years[0]}-{years[-1]}, count={len(sample)}")

# crosswalk 의 31100 매핑
print
print("=" * 60)
print("sigungu_crosswalk_v2 의 31100 매핑")
print("=" * 60)
xw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\sigungu_crosswalk_v2.csv", dtype=str)
goyang_xw = xw[xw["h_code"] == "31100"]
print(f"31100 매핑 raw_codes: {sorted(goyang_xw['raw_code'].unique)}")
print(f"연도 범위: {goyang_xw['year'].min} - {goyang_xw['year'].max}")
