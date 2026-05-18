"""Step 1 anomaly 점검:
(a) 1999-2021 매년 1개씩 등장하는 length=2 code 정체
(b) 1991→1992 4-digit→5-digit 전환 시 매핑 가능성
(c) 1994→1995 도농통합 효과
"""
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:/Users/82103/Downloads/trade_mortality_korea")
SRC = ROOT / "3_derived" / "sigungu" / "step1_codebook_old.csv"

df = pd.read_csv(SRC, dtype={"raw_code": str, "sido_code": str})

print("=== (a) length=2 sigungu rows (1999-2021) ===")
short = df[df["code_len"] == 2]
print(short.to_string(index=False))

print("\n=== (b) 1991 vs 1992 시군구 명칭 변화 (5-digit 전환) ===")
n91 = df[df["year"] == 1991].set_index("sigungu_name")
n92 = df[df["year"] == 1992].set_index("sigungu_name")
only91 = sorted(set(n91.index) - set(n92.index))
only92 = sorted(set(n92.index) - set(n91.index))
print(f" 1991만: {len(only91)}개 → {only91[:20]}{'...' if len(only91)>20 else ''}")
print(f" 1992만: {len(only92)}개 → {only92[:20]}{'...' if len(only92)>20 else ''}")

print("\n=== (c) 1994 vs 1995 시군구 명칭 변화 (도농통합) ===")
n94 = df[df["year"] == 1994].set_index("sigungu_name")
n95 = df[df["year"] == 1995].set_index("sigungu_name")
only94 = sorted(set(n94.index) - set(n95.index))
only95 = sorted(set(n95.index) - set(n94.index))
print(f" 1994만: {len(only94)}개")
for n in only94: print(f" - {n}")
print(f" 1995만 (신규): {len(only95)}개")
for n in only95: print(f" + {n}")

print("\n=== (d) 2013 vs 2014 (청주 통합 검증) ===")
n13 = df[df["year"] == 2013].set_index("sigungu_name")
n14 = df[df["year"] == 2014].set_index("sigungu_name")
only13 = sorted(set(n13.index) - set(n14.index))
only14 = sorted(set(n14.index) - set(n13.index))
print(f" 2013만: {only13}")
print(f" 2014만: {only14}")

print("\n=== (e) 세종 관련 모든 행 ===")
sj = df[(df["sido_name"].str.contains("세종", na=False)) | (df["sigungu_name"].str.contains("세종|연기", na=False))]
print(sj.to_string(index=False))
