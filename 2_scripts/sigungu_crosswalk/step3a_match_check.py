"""Step 3a: 사망 raw_code (step2) ↔ KOSTAT 코드집 (step1) 매칭률 점검.

매칭 안 되는 raw_code 를 연도별로 모두 출력. 시도-시군구 패턴 분석으로
도서·행정 변동·코드집 누락을 분리.
"""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(r"C:/Users/82103/Downloads/trade_mortality_korea")
DERIVED = ROOT / "3_derived" / "sigungu"
OUT = DERIVED / "step3a_match_report.md"

def main -> int:
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")

 cb = pd.read_csv(DERIVED / "step1_codebook_old.csv",
 dtype={"raw_code": str, "sido_code": str})
 raw = pd.read_csv(DERIVED / "step2_raw_sigungu_by_year.csv",
 dtype={"raw_code": str, "sido_raw": str, "sgg_raw": str})

 # 코드집 raw_code 도 5자리 zfill 통일 (이전 step1엔 짧은 코드도 있을 수 있어서)
 cb["raw_code5"] = cb["raw_code"].str.strip.str.zfill(5)
 raw_active = raw[~raw["is_missing"]].copy
 raw_active["raw_code5"] = raw_active["raw_code"].str.zfill(5)

 # year × raw_code 기준 left join
 merged = raw_active.merge(
 cb[["year", "raw_code5", "sido_name", "sigungu_name", "code_len"]],
 on=["year", "raw_code5"], how="left", indicator=True,
)

 matched = (merged["_merge"] == "both").sum
 unmatched = (merged["_merge"] == "left_only").sum
 total = len(merged)
 print(f"매칭: {matched:,} / {total:,} ({matched/total*100:.2f}%)")
 print(f"미매칭: {unmatched:,}")

 unmatched_df = merged[merged["_merge"] == "left_only"].copy
 print(f"\n--- 미매칭 raw_code 연도별 분포 ---")
 yearly = unmatched_df.groupby("year").agg(
 n_codes=("raw_code5", "nunique"),
 n_deaths=("n_deaths", "sum"),
).reset_index
 print(yearly.to_string(index=False))

 # 코드집의 5-digit 으로 변환된 raw_code 의 시도(앞 2자리) 와 mortality raw 의 sido_raw 일치 여부도 체크
 # 미매칭 raw_code 들 모두 살펴보기 (집계, 가장 사망자 많은 순)
 print(f"\n--- 미매칭 raw_code TOP 60 (n_deaths 합계) ---")
 top_unmatch = (unmatched_df.groupby(["raw_code5", "sido_raw", "sgg_raw"])
.agg(n_deaths=("n_deaths", "sum"),
 years=("year", lambda s: f"{s.min}-{s.max}"),
 n_years=("year", "nunique"))
.sort_values("n_deaths", ascending=False)
.reset_index
.head(60))
 print(top_unmatch.to_string(index=False))

 # 미매칭 코드 중 5자리 표준 패턴 (sido[2] + 하위[3]) 인지 점검
 print(f"\n--- 미매칭 코드의 시도 prefix 분포 ---")
 unmatched_df["prefix2"] = unmatched_df["raw_code5"].str[:2]
 print(unmatched_df.groupby("prefix2")["raw_code5"].nunique.sort_values(ascending=False).to_string)

 # 보고서 저장
 lines = 
 def w(s=""): lines.append(s)
 w("# Step 3a: Mortality raw_code ↔ Codebook 매칭 점검")
 w("")
 w(f"- 매칭률: **{matched:,} / {total:,} = {matched/total*100:.2f}%** (year×rawcode 단위 unique 행 기준)")
 w(f"- 미매칭 unique 행: **{unmatched:,}**")
 w("")
 w("## 연도별 미매칭")
 w(yearly.to_markdown(index=False))
 w("")
 w("## 미매칭 raw_code TOP 60 (사망자 합계)")
 w(top_unmatch.to_markdown(index=False))
 w("")
 OUT.write_text("\n".join(lines), encoding="utf-8")
 print(f"\n보고서 저장: {OUT}")

 return 0

if __name__ == "__main__":
 sys.exit(main)
