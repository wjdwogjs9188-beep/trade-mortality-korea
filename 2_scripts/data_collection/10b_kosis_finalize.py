"""population_combined.csv 마무리 — Unnamed 컬럼 drop, rename, 검증."""
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import RAW_DIR

OUT_DIR = RAW_DIR / "kosis_population"
src = OUT_DIR / "population_combined.csv"

print(f"읽는 중: {src}")
df = pd.read_csv(src, dtype=str)
print(f"shape: {df.shape}, 컬럼: {list(df.columns)}")

# Unnamed 컬럼 (trailing empty) drop
unnamed_cols = [c for c in df.columns if c.startswith("Unnamed:")]
if unnamed_cols:
    df = df.drop(columns=unnamed_cols)
    print(f"Unnamed 컬럼 drop: {unnamed_cols}")
print(f"이후 shape: {df.shape}, 컬럼: {list(df.columns)}")

# 위치 기반 rename
cols = df.columns.tolist()
if len(cols) == 8:
    rename_map = {cols[0]: "C1", cols[1]: "C1_NM",
                   cols[2]: "C2", cols[3]: "C2_NM",
                   cols[4]: "C3", cols[5]: "C3_NM",
                   cols[6]: "year",
                   cols[7]: "population"}
    df = df.rename(columns=rename_map)
    print(f"\n✅ rename 적용. 컬럼: {list(df.columns)}")
else:
    print(f"⚠️ 컬럼 수가 8 아님 ({len(cols)}). 수동 점검 필요.")
    sys.exit(1)

# year 정리
df["year"] = df["year"].str.extract(r"(\d{4})")[0]

# population 정리 (숫자 변환 — 인구수)
df["population"] = pd.to_numeric(df["population"], errors="coerce")

# 검증
print(f"\n=== 검증 ===")
print(f"총 행수: {len(df):,}")
print(f"연도 범위: {df['year'].min()} ~ {df['year'].max()}")
print(f"연도 수: {df['year'].nunique()}")
print(f"unique C1 전체: {df['C1'].nunique()}")
print(f"  └ 5자리 (시군구): {df[df['C1'].str.len() == 5]['C1'].nunique()}")
print(f"  └ 2자리 (시도/전국): {df[df['C1'].str.len() == 2]['C1'].nunique()}")
print(f"unique C2 (성별): {df['C2'].nunique()} → {sorted(df['C2'].unique())}")
print(f"unique C3 (연령): {df['C3'].nunique()}")
print(f"\npopulation 기본 통계 (시군구 X 연도 X 성별 X 연령):")
print(df['population'].describe())

# 샘플
print(f"\n--- 첫 3행 ---")
print(df.head(3).to_string())
print(f"\n--- 시군구 (5자리) 샘플 5개 ---")
print(df[df["C1"].str.len() == 5].head(5).to_string())

# 저장
out = OUT_DIR / "population_combined.csv"
df.to_csv(out, index=False, encoding="utf-8-sig")
print(f"\n✅ 정리 저장: {out}")
print(f"   size: {out.stat().st_size:,} bytes")

try:
    out_pq = OUT_DIR / "population_combined.parquet"
    df.to_parquet(out_pq, index=False)
    print(f"✅ Parquet: {out_pq}")
except Exception as e:
    print(f"⚠️ parquet 저장 (선택): {e}")
