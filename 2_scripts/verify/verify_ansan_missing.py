"""의심 #2 — 안산 (41190) records 누락 진단."""
import pandas as pd

# === panel v01 에 안산 있는지 ===
v01 = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_panel_v01.parquet")
ansan_v01 = v01[v01["h_code"] == "41190"]
print(f"panel v01 안산 (41190) records: {len(ansan_v01):,}")

# panel v01 의 경기 (4xxxx) h_code list
print()
print("panel v01 경기 (4xxxx) h_codes:")
gg_v01 = sorted([h for h in v01["h_code"].unique() if str(h).startswith("4")])
print(gg_v01)

# === panel v02 비교 ===
print()
print("=" * 60)
v02 = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_rate_panel_v02.parquet")
print(f"panel v02 unique h_code 총 개수: {v02['h_code'].nunique()}")
print()
print("panel v02 경기 (4xxxx) h_codes:")
gg_v02 = sorted([h for h in v02["h_code"].unique() if str(h).startswith("4")])
print(gg_v02)

# 차이
missing_in_v02 = set(gg_v01) - set(gg_v02)
new_in_v02 = set(gg_v02) - set(gg_v01)
print()
print(f"v01 에 있고 v02 에 없는 경기 h_code: {sorted(missing_in_v02)}")
print(f"v02 에 새로 생긴 경기 h_code: {sorted(new_in_v02)}")

# === 안산 어디로 매핑됐는지 (전체 v02 에 41190 또는 children 있는지) ===
print()
print("=" * 60)
print("안산 관련 코드 (411xx, 4119x) v02 에서 검색:")
ansan_related = sorted([h for h in v02["h_code"].unique() if str(h).startswith("411") or str(h)[:4] == "4119"])
print(ansan_related)

# === 사용자 inventory 의 시군구 crosswalk 확인 ===
print()
print("=" * 60)
xw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\sigungu_crosswalk_v2.csv", dtype=str)
print(f"sigungu_crosswalk_v2 안산 매핑:")
ansan_xw = xw[xw["h_code"] == "41190"]
print(f"  41190 으로 매핑되는 raw_code 개수: {len(ansan_xw)}")
if len(ansan_xw) > 0:
    print(f"  raw_code 종류: {sorted(ansan_xw['raw_code'].unique())}")
    print(f"  연도 범위: {ansan_xw['year'].min()} - {ansan_xw['year'].max()}")
