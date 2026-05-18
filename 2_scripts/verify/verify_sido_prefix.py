"""sido prefix 41 vs 31 혼동 verify."""
import pandas as pd

v01 = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_panel_v01.parquet")

print(f"panel v01 unique h_code 총 개수: {v01['h_code'].nunique()}")
print()
print("panel v01 sido prefix 분포 (h_code 첫 2자리):")
sido_dist = v01["h_code"].astype(str).str[:2].value_counts().sort_index()
print(sido_dist)

print()
print("=" * 60)
print("KOSIS 표준: 31 = 경기, 41 = 강원 (?)")
print("행안부 표준: 41 = 경기, 42 = 강원")
print("=" * 60)

# 31xxx (경기 추정) h_code
print()
print("panel v01 31xxx h_codes (KOSIS 경기 가능성):")
gg = sorted([h for h in v01["h_code"].unique() if str(h).startswith("31")])
print(gg)

# 안산 = 31190 verify
print()
print("=" * 60)
ansan_31190 = v01[v01["h_code"] == "31190"]
print(f"panel v01 안산 31190 records: {len(ansan_31190):,}")
if len(ansan_31190) > 0:
    print("  → 안산 31190 으로 매핑됨 (KOSIS 표준 panel)")
    print(f"  연도 범위: {ansan_31190['year'].min()} - {ansan_31190['year'].max()}")
else:
    print("  → 31190 도 부재. 다른 코드 가능성")

# 수원 = 31110, 성남 31130, 안양 31170, 고양 31280, 용인 31460
print()
print("R-A 가 41xxx 로 commit 한 11 분구 시군구를 31xxx 로 재검색:")
for h_old, name in [
    ("31110", "수원"), ("31130", "성남"), ("31170", "안양"),
    ("31190", "안산"), ("31280", "고양"), ("31460", "용인"),
    ("31050", "부천"), ("33020", "청주"),
    ("34010", "천안"), ("35010", "전주"),
    ("37010", "포항"), ("38110", "통합창원"),
]:
    cnt = len(v01[v01["h_code"] == h_old])
    print(f"  {name} {h_old}: {cnt:>6,} records")

# 41xxx 도 확인
print()
print("panel v01 41xxx h_codes (만약 있다면):")
gg41 = sorted([h for h in v01["h_code"].unique() if str(h).startswith("41")])
print(f"  count: {len(gg41)}, sample: {gg41[:10]}")

# === sigungu_crosswalk_v2 의 31190 매핑 ===
print()
print("=" * 60)
xw = pd.read_csv(r"C:\Users\82103\Downloads\trade_mortality_korea\1_codebooks\sigungu_crosswalk_v2.csv", dtype=str)
print(f"sigungu_crosswalk_v2 안산 31190 매핑:")
ansan_xw = xw[xw["h_code"] == "31190"]
print(f"  raw_code 개수: {len(ansan_xw)}")
if len(ansan_xw) > 0:
    print(f"  raw_code 종류: {sorted(ansan_xw['raw_code'].unique())}")
    print(f"  연도 범위: {ansan_xw['year'].min()} - {ansan_xw['year'].max()}")
