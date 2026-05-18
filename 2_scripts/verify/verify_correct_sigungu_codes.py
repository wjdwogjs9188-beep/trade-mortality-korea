"""정확한 11 분구 시군구의 h_code 매핑 verify."""
import pandas as pd

micro = pd.read_parquet(r"C:\Users\82103\Downloads\trade_mortality_korea\3_derived\mortality\mortality_microdata_combined.parquet")

print("=" * 60)
print("11 분구 시군구의 정확한 h_code (microdata 의 h_name 기반)")
print("=" * 60)

CITIES = ["수원", "성남", "부천", "안양", "안산", "고양", "용인",
          "청주", "천안", "전주", "포항", "창원"]

for city in CITIES:
    sub = micro[micro["h_name"].astype(str).str.contains(city, na=False)]
    if len(sub) == 0:
        print(f"\n{city}: 부재")
        continue
    print(f"\n--- {city} ---")
    # h_code 별 count + 이름
    grp = sub.groupby(["h_code", "h_name"]).size().reset_index(name="records")
    grp = grp.sort_values("records", ascending=False)
    for _, row in grp.iterrows():
        print(f"  h_code={row['h_code']}  h_name={row['h_name']}  records={row['records']:,}")

print()
print("=" * 60)
print("부산 / 대구 등 광역시 자치구 분포 (cross-verify)")
print("=" * 60)
for sido in ["서울 강남", "부산 해운대", "대구 달서"]:
    sub = micro[micro["h_name"].astype(str).str.contains(sido, na=False)]
    if len(sub) > 0:
        grp = sub.groupby(["h_code", "h_name"]).size().reset_index(name="records").head(3)
        print(f"\n{sido}:")
        for _, row in grp.iterrows():
            print(f"  h_code={row['h_code']}  h_name={row['h_name']}  records={row['records']:,}")
