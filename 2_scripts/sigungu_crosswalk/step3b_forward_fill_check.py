"""Step 3b: 2022·2023 raw_code 가 2021 코드집 forward-fill 로 매칭되는지 점검."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(r"C:/Users/82103/Downloads/trade_mortality_korea")
DERIVED = ROOT / "3_derived" / "sigungu"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

cb = pd.read_csv(DERIVED / "step1_codebook_old.csv",
                 dtype={"raw_code": str, "sido_code": str})
raw = pd.read_csv(DERIVED / "step2_raw_sigungu_by_year.csv",
                  dtype={"raw_code": str, "sido_raw": str, "sgg_raw": str})

cb["raw_code5"] = cb["raw_code"].str.zfill(5)
raw_active = raw[~raw["is_missing"]].copy()
raw_active["raw_code5"] = raw_active["raw_code"].str.zfill(5)

# 2021 코드집 lookup
cb_2021 = cb[cb["year"] == 2021].set_index("raw_code5")[["sido_name", "sigungu_name"]]
print(f"2021 코드집 unique raw_code: {len(cb_2021)}")

for y in [2022, 2023]:
    rc = set(raw_active[raw_active["year"] == y]["raw_code5"])
    print(f"\n--- {y} ---")
    print(f"  사망 unique raw_code: {len(rc)}")
    matched = rc & set(cb_2021.index)
    unmatched = rc - set(cb_2021.index)
    print(f"  2021 코드집과 매칭: {len(matched)}")
    print(f"  미매칭 ({len(unmatched)}개): {sorted(unmatched)}")
    if unmatched:
        # 2022 raw 데이터에서 미매칭의 sido 분포
        sub = raw_active[(raw_active["year"] == y) & raw_active["raw_code5"].isin(unmatched)]
        print(f"    n_deaths 합: {sub['n_deaths'].sum()}")
        print(sub[["raw_code5", "sido_raw", "sgg_raw", "n_deaths"]].to_string(index=False))

# 2021 코드집에는 있는데 2022/2023 사망 데이터엔 없는 코드 (drop된 시군구)
for y in [2022, 2023]:
    rc = set(raw_active[raw_active["year"] == y]["raw_code5"])
    only_cb = set(cb_2021.index) - rc
    print(f"\n{y} 사망에 없고 2021 코드집에만 있는 ({len(only_cb)}개):")
    if only_cb:
        sub = cb_2021.loc[list(only_cb)].reset_index()
        print(sub.to_string(index=False))
