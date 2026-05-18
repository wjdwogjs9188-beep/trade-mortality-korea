"""MDIS 인구주택총조사 7 시점 microdata → mediator panel cross-tab.

산출 2 panel (mortality_rate_panel_v02_1 분모와 동일 형식):
  3_derived/population/mediator_panel_marriage_v01.parquet
    columns: h_code, year, sex_code, age_band, marital_code, population
  3_derived/population/mediator_panel_education_v01.parquet
    columns: h_code, year, sex_code, age_band, education_code, population

dimension:
  - h_code (5자리 시도+시군구): 2000-2020 직접 결합. 1990 은 sigungu 2자리 → 3자리 zfill placeholder
  - year (1990/1995/2000/2005/2010/2015/2020 7 시점)
  - sex_code (1=남, 2=여)
  - age_band (5세 단위, 0-4, 5-9, ..., 80-84, 85+)
  - marital_code (1=미혼, 2=배우자있음, 3=사별, 4=이혼) — 5 시점 일치 가정
  - education_code (1=무학, ..., 8=박사) — 시점별 코드 다를 수 있음 (paper § sensitivity 차원 verify)

가중값 적용: microdata 1 row = weight 명 모집단. sum(weight) = 모집단 추정.

산출 사용:
  - paper § 5.2 mediation analysis 의 mediator-specific population denominator
  - mortality numerator (microdata 의 marital/education code) / 이 panel = mediator-specific mortality rate

선행:
  - 06_*_unzip 완료
  - 07_*_columns_extract 완료 (layout JSON 산출)
  - pip install pandas pyarrow --break-system-packages

실행:
    cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
    python 2_scripts\\data_collection\\08_mdis_population_parse_crosstab.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "0_raw" / "mdis_population_census"
DATA_DIR_43590 = RAW_DIR / "2%_표본_인구_20260430_43590_데이터"  # 1990/1995/2000/2005/2010
DATA_DIR_65001 = RAW_DIR / "2%_표본_인구_20260504_65001_데이터"  # 2000/2005/2010/2015/2020 (column 정확)
OUT_DIR = ROOT / "3_derived" / "population"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────────────────
# Per-year column name mapping (CSV header 기반)
# ────────────────────────────────────────────────────────
# 2000-2020: 65001 batch 사용 (43590 batch 의 column header broken)
# 1990, 1995: 43590 batch only

YEAR_COLUMN_MAP: dict[int, dict] = {
    # ---- 1990 (43590) ----
    # 1990 시군구 = 2자리. 분리 mapping 필요. 일단 zfill(3) placeholder
    1990: {
        "csv_dir": DATA_DIR_43590,
        "csv_name": "1990_2%_표본_인구_20260430_43590.csv",
        "sido_col": "행정(시^도)",
        "sigungu_col": "행정(시군구)",
        "sex_col": "성별",
        "age_col": "만나이",
        "marital_col": "혼인상태",
        "education_col": "교육 학력",
        "weight_col": "가중치",
        "national_filter": None,  # 1990 출생국적 변수 부재
        "sigungu_digit": 2,
    },
    # ---- 1995 (43590) ----
    1995: {
        "csv_dir": DATA_DIR_43590,
        "csv_name": "1995_2%_표본_인구_20260430_43590.csv",
        "sido_col": "행정구역(시도)",
        "sigungu_col": "행정구역(구시군)",
        "sex_col": "성별",
        "age_col": "만나이",
        "marital_col": "혼인상태",
        "education_col": "교육(학력)",
        "weight_col": "가중치",
        "national_filter": None,
        "sigungu_digit": 3,
    },
    # ---- 2000 (65001) ----
    2000: {
        "csv_dir": DATA_DIR_65001,
        "csv_name": "2000_2%_표본_인구_20260504_65001.csv",
        "sido_col": "행정구역시도코드",
        "sigungu_col": "행정구역시군구코드",
        "sex_col": "성별코드",
        "age_col": "만연령",
        "marital_col": "혼인상태코드",
        "education_col": "교육정도코드",
        "weight_col": "가중값",
        "national_filter": None,  # 2000 출생국적 변수 부재
        "sigungu_digit": 3,
    },
    # ---- 2005 (65001) ----
    2005: {
        "csv_dir": DATA_DIR_65001,
        "csv_name": "2005_2%_표본_인구_20260504_65001.csv",
        "sido_col": "행정구역시도코드",
        "sigungu_col": "행정구역시군구코드",
        "sex_col": "성별코드",
        "age_col": "만연령",
        "marital_col": "혼인상태코드",
        "education_col": "교육정도코드",
        "weight_col": "가중값",
        "national_filter": None,
        "sigungu_digit": 3,
    },
    # ---- 2010 (65001) ----
    2010: {
        "csv_dir": DATA_DIR_65001,
        "csv_name": "2010_2%_표본_인구_20260504_65001.csv",
        "sido_col": "행정구역시도코드",
        "sigungu_col": "행정구역시군구코드",
        "sex_col": "성별코드",
        "age_col": "만연령",
        "marital_col": "혼인상태코드",
        "education_col": "교육정도코드",
        "weight_col": "가중값",
        # 2010+ 출생시국적 변수 존재 → 한국인 only filter
        "national_filter": ("출생시국적_대한민국여부", "1"),
        "sigungu_digit": 3,
    },
    # ---- 2015 (65001) ----
    2015: {
        "csv_dir": DATA_DIR_65001,
        "csv_name": "2015_2%_표본_인구_20260504_65001.csv",
        "sido_col": "행정구역시도코드",
        "sigungu_col": "행정구역시군구코드",
        "sex_col": "성별코드",
        "age_col": "만연령",
        "marital_col": "혼인상태코드",
        "education_col": "교육정도코드",
        "weight_col": "인구가중값",
        "national_filter": ("출생시국적_대한민국여부", "1"),
        "sigungu_digit": 3,
    },
    # ---- 2020 (65001) ----
    2020: {
        "csv_dir": DATA_DIR_65001,
        "csv_name": "2020_2%_표본_인구_20260504_65001.csv",
        "sido_col": "행정구역시도코드",
        "sigungu_col": "행정구역시군구코드",
        "sex_col": "성별코드",
        "age_col": "만연령",
        "marital_col": "혼인상태코드",
        "education_col": "교육정도코드",
        "weight_col": "인구가중값",
        "national_filter": ("출생국적_대한민국여부", "1"),  # 2020 = "출생국적" (시 빠짐)
        "sigungu_digit": 3,
    },
}

# Age band (5세 단위, 0-4, 5-9, ..., 80-84, 85+)
AGE_BINS = list(range(0, 90, 5)) + [200]
AGE_LABELS = [f"{b:02d}-{b+4:02d}" for b in range(0, 85, 5)] + ["85+"]


# ────────────────────────────────────────────────────────
# Functions
# ────────────────────────────────────────────────────────

def read_csv_chunked(csv_path: Path, needed_cols: list[str], chunksize: int = 200_000) -> pd.DataFrame:
    """대용량 CSV 를 chunked 로 읽어 필요 column 만 keep."""
    chunks = []
    for ch in pd.read_csv(csv_path, encoding="cp949", dtype=str,
                          usecols=needed_cols, chunksize=chunksize, low_memory=False):
        chunks.append(ch)
    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()


def build_year(year: int, cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """단일 시점의 marriage + education panel build."""
    csv_path = cfg["csv_dir"] / cfg["csv_name"]
    if not csv_path.exists():
        print(f"  [SKIP {year}] not found: {csv_path}")
        return pd.DataFrame(), pd.DataFrame()

    print(f"\n[{year}] reading {csv_path.name}")

    needed = [cfg["sido_col"], cfg["sigungu_col"], cfg["sex_col"],
              cfg["age_col"], cfg["marital_col"], cfg["education_col"],
              cfg["weight_col"]]
    if cfg.get("national_filter"):
        needed.append(cfg["national_filter"][0])
    needed = list(dict.fromkeys(needed))  # dedup

    df = read_csv_chunked(csv_path, needed)
    print(f"  rows: {len(df):,}, cols: {df.columns.tolist()}")

    # Rename
    rename_map = {
        cfg["sido_col"]: "sido_code",
        cfg["sigungu_col"]: "sigungu_code",
        cfg["sex_col"]: "sex_code",
        cfg["age_col"]: "age_int",
        cfg["marital_col"]: "marital_code",
        cfg["education_col"]: "education_code",
        cfg["weight_col"]: "weight",
    }
    df = df.rename(columns=rename_map)

    # National filter (한국인 only, 2010+ 만 가능)
    if cfg.get("national_filter"):
        col, val = cfg["national_filter"]
        before = len(df)
        df = df[df[col] == val].copy()
        after = len(df)
        print(f"  국적 filter ({col}={val}): {before:,} → {after:,} rows ({100*after/before:.1f}%)")

    # h_code 결합
    df["sido_code"] = df["sido_code"].astype(str).str.strip().str.zfill(2)
    df["sigungu_code"] = df["sigungu_code"].astype(str).str.strip().str.zfill(cfg["sigungu_digit"])

    if cfg["sigungu_digit"] == 2:
        # 1990 special: 2자리 → 3자리 placeholder (zfill 앞 0)
        # 실제 mortality panel 의 5자리 코드와 매핑은 별도 작업 (1990 행정구역코드표 기반)
        df["h_code"] = df["sido_code"] + df["sigungu_code"].str.zfill(3)
    else:
        df["h_code"] = df["sido_code"] + df["sigungu_code"]

    # Numeric cast
    df["age_int"] = pd.to_numeric(df["age_int"], errors="coerce")
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    # 비수치 weight drop
    df = df.dropna(subset=["age_int", "weight"])
    df = df[df["weight"] > 0]
    df["age_int"] = df["age_int"].astype(int)

    # Age band
    df["age_band"] = pd.cut(df["age_int"], bins=AGE_BINS, right=False, labels=AGE_LABELS)

    # Year
    df["year"] = year

    # Sex code clean
    df["sex_code"] = df["sex_code"].astype(str).str.strip()
    df = df[df["sex_code"].isin(["1", "2"])]

    print(f"  cleaned: {len(df):,} rows, weighted population: {df['weight'].sum():,.0f}")

    # ─── Marriage panel ───
    mar = df.dropna(subset=["marital_code"]).copy()
    mar["marital_code"] = mar["marital_code"].astype(str).str.strip()
    mar = mar[mar["marital_code"].notna() & (mar["marital_code"] != "")]
    marriage = (mar.groupby(["h_code", "year", "sex_code", "age_band", "marital_code"], observed=True)
                ["weight"].sum().reset_index().rename(columns={"weight": "population"}))
    print(f"  marriage panel: {len(marriage):,} cells")

    # ─── Education panel ───
    edu = df.dropna(subset=["education_code"]).copy()
    edu["education_code"] = edu["education_code"].astype(str).str.strip()
    edu = edu[edu["education_code"].notna() & (edu["education_code"] != "")]
    education = (edu.groupby(["h_code", "year", "sex_code", "age_band", "education_code"], observed=True)
                 ["weight"].sum().reset_index().rename(columns={"weight": "population"}))
    print(f"  education panel: {len(education):,} cells")

    return marriage, education


def main() -> int:
    print("=" * 70)
    print("MDIS 인구주택총조사 → mediator panel cross-tab build")
    print("=" * 70)

    all_mar, all_edu = [], []
    for year in sorted(YEAR_COLUMN_MAP.keys()):
        cfg = YEAR_COLUMN_MAP[year]
        mar, edu = build_year(year, cfg)
        if not mar.empty:
            all_mar.append(mar)
        if not edu.empty:
            all_edu.append(edu)

    # Concat
    final_mar = pd.concat(all_mar, ignore_index=True) if all_mar else pd.DataFrame()
    final_edu = pd.concat(all_edu, ignore_index=True) if all_edu else pd.DataFrame()

    # Save parquet
    mar_out = OUT_DIR / "mediator_panel_marriage_v01.parquet"
    edu_out = OUT_DIR / "mediator_panel_education_v01.parquet"

    if not final_mar.empty:
        final_mar.to_parquet(mar_out, index=False)
        print(f"\n[save marriage] {mar_out}")
        print(f"  rows: {len(final_mar):,}")
        print(f"  years: {sorted(final_mar['year'].unique())}")
        print(f"  unique h_code: {final_mar['h_code'].nunique()}")
        print(f"  marital_code values: {sorted(final_mar['marital_code'].unique())}")
        print(f"  total weighted pop sum: {final_mar['population'].sum():,.0f}")

    if not final_edu.empty:
        final_edu.to_parquet(edu_out, index=False)
        print(f"\n[save education] {edu_out}")
        print(f"  rows: {len(final_edu):,}")
        print(f"  years: {sorted(final_edu['year'].unique())}")
        print(f"  unique h_code: {final_edu['h_code'].nunique()}")
        print(f"  education_code values: {sorted(final_edu['education_code'].unique())}")
        print(f"  total weighted pop sum: {final_edu['population'].sum():,.0f}")

    # Validation summary (7 시점 cell count, h_code coverage 비교)
    print("\n" + "=" * 70)
    print("VALIDATION (per-year inventory)")
    print("=" * 70)
    if not final_mar.empty:
        print("\nMarriage panel — per-year:")
        for yr, sub in final_mar.groupby("year"):
            print(f"  {yr}: {len(sub):,} cells, {sub['h_code'].nunique()} h_code, "
                  f"pop sum {sub['population'].sum():,.0f}")
    if not final_edu.empty:
        print("\nEducation panel — per-year:")
        for yr, sub in final_edu.groupby("year"):
            print(f"  {yr}: {len(sub):,} cells, {sub['h_code'].nunique()} h_code, "
                  f"pop sum {sub['population'].sum():,.0f}")

    print("\n" + "=" * 70)
    print("완료. 다음 단계:")
    print("  1. 1990 sigungu 코드 (2자리 → 3자리) mapping 작성 (mortality panel 과 align)")
    print("  2. mortality_rate_panel_v02_1 의 numerator (혼인/교육 코드별 사망)")
    print("     와 join 하여 mediator-specific mortality rate panel build")
    print("  3. paper § 5.2 mediation analysis 진행")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
