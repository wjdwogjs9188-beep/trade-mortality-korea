"""사망 microdata 28 시점 (1997-2024) parse + cleaning + standardization.

목적: mediator-specific mortality numerator 산출 위한 cleaned panel build.
  → 11b (marital crosstab) + 11c (education crosstab) 의 입력으로 사용

처리 단계:
  1. 28 csv (1997-2024) cp949 read, chunk 단위 (메모리 효율)
  2. 시군구 코드 정규화 (자릿수 통일):
     - 일반 (1997-2022, 2024): 시군구 = 3자리 (예: 010)
     - 2023 anomaly: 시군구 = 5자리 (시도 prefix 포함, 11200) → 시도 strip 후 3자리
     - h_code = 시도(2) + 시군구(3) = 5자리
  3. age band 매핑 (사망연령5세단위코드 → "00-04", "05-09", ..., "85+")
  4. 한국인 filter (사망자국적구분코드 = 1, 1997-2007 변수 부재 시 전체 keep)
  5. 혼인 코드 1-4 only (9 미상 drop)
  6. 교육 코드 → 3 카테고리 매핑 (모든 시점 align):
       NoHS (1,2,3), HS (4), College+ (5,6,7), 9=미상 drop
  7. cause_104 사망원인 그대로 keep
  8. 표준 column 명 으로 rename
  9. 통합 parquet save

산출:
  3_derived/mortality/mortality_microdata_cleaned_v01.parquet
    columns: year, h_code, sex_code, age_band, marital_code, education_band,
             cause_104, weight (=1 per row), national_filter_pass

선행:
  pip install pandas pyarrow --break-system-packages

실행:
    cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
    python 2_scripts\\data_collection\\11a_mortality_microdata_parse.py
"""
from __future__ import annotations
import sys
import re
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = Path(r"C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리")
OUT_DIR = ROOT / "3_derived" / "mortality"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────────────────
# Code mapping
# ────────────────────────────────────────────────────────

VALID_MARITAL = {"1", "2", "3", "4"}  # 1미혼 2배우자 3사망 4이혼 (9=미상 drop)

# 교육 3 카테고리 (1997-2024 모든 시점 align)
EDU_3CAT = {
    "1": "1.NoHS",     # 무학
    "2": "1.NoHS",     # 초등
    "3": "1.NoHS",     # 중학
    "4": "2.HS",       # 고등
    "5": "3.College+", # 1997-2007: 대학통합. 2008+ 미사용
    "6": "3.College+", # 2008+: 4년제
    "7": "3.College+", # 2008+: 대학원
    # 9 = 미상 drop
}

# 사망연령5세단위코드 → age band string
# (코드집 기반, 사용자 메모리 의 cause_104 코드북 build 시 verify 됨)
AGE_BAND_MAP = {
    "1":  "00-04",
    "2":  "05-09",
    "3":  "10-14",
    "4":  "15-19",
    "5":  "20-24",
    "6":  "25-29",
    "7":  "30-34",
    "8":  "35-39",
    "9":  "40-44",
    "10": "45-49",
    "11": "50-54",
    "12": "55-59",
    "13": "60-64",
    "14": "65-69",
    "15": "70-74",
    "16": "75-79",
    "17": "80-84",
    "18": "85+",     # 사용자 codebook verify: 18=85+
    "19": "85+",     # 일부 시점 90+ 도 18 또는 19. 안전 차원 85+ 통합
    "20": "85+",
    "21": "85+",
    "22": "85+",
    # 99 = 미상 drop
}

# Keyword-based fuzzy column mapping (column 명 미세 차이 robust)
# (column name 의 일부 substring 만 일치하면 매핑)
COL_KEYWORD_MAP = [
    # (canonical_name, [substring_keywords])
    ("sido_raw",          ["주소행정구역시도", "주소지행정구역시도"]),
    ("sigungu_raw",       ["주소행정구역시군구", "주소지행정구역시군구"]),
    ("sex_code",          ["성별코드"]),
    ("age_5y_code",       ["연령5세", "사망연령"]),
    ("marital_code_raw",  ["혼인상태"]),
    ("education_code_raw",["교육정도"]),
    ("cause_104",         ["104항목"]),
    ("national_code",     ["국적구분"]),
    ("year_str",          ["연도"]),
]


def build_column_map(actual_columns: list[str]) -> dict[str, str]:
    """actual column list 에서 keyword 매칭으로 rename map 생성."""
    out = {}
    for canonical, keywords in COL_KEYWORD_MAP:
        for col in actual_columns:
            if any(kw in col for kw in keywords):
                out[col] = canonical
                break
    return out


# ────────────────────────────────────────────────────────
# Functions
# ────────────────────────────────────────────────────────

def normalize_sigungu(sido: str, sigungu_raw: str) -> str:
    """시군구 자리수 정규화 → 5자리 h_code (시도 2 + 시군구 3).

    Cases:
      - sigungu_raw = '010' (3자리, 일반) → '11' + '010' = '11010'
      - sigungu_raw = '11200' (5자리, 2023 anomaly) → strip 시도 → '200' (잘못된 매핑)
        실제로 11200 = 사실 시군구 코드 200 (= 동작구 if sido=11). 시도 prefix 중복.
        → 처리: 5자리면 첫 2자리 == sido 면 strip, 아니면 그대로
      - sigungu_raw = '20' (2자리, 1990 등) → '11' + '020' (zfill) = '11020'
    """
    sido = str(sido).strip().zfill(2)
    sg = str(sigungu_raw).strip()

    if len(sg) == 5:
        # anomaly: 시도 prefix 중복
        if sg[:2] == sido:
            sg = sg[2:]  # → 3자리
        else:
            # 알 수 없는 경우 raw 그대로 사용 (5자리 자체가 h_code)
            return sg
    elif len(sg) == 4:
        # 4자리 = 1990 식 (시도 prefix + 시군구 2자리)
        if sg[:2] == sido:
            sg = sg[2:].zfill(3)
    elif len(sg) <= 3:
        sg = sg.zfill(3)
    else:
        sg = sg[:3]

    return sido + sg


def parse_one_csv(csv_path: Path, chunksize: int = 200_000) -> pd.DataFrame:
    """단일 csv parse + cleaning."""
    print(f"\n[parse] {csv_path.name}")

    # year 추출
    m = re.search(r"(\d{4})_사망", csv_path.name)
    year = int(m.group(1)) if m else None

    # ──────────────────────────────────────────────────────────
    # Position-based parse (column 명 차이 무시, 1997-2024 모두 18 col 동일 position)
    # verify_*.py inspect 확인:
    #   [0]=연도, [4]=시도, [5]=시군구, [10]=혼인, [11]=교육,
    #   [12]=성별, [13]=age_5y, [14]=국적, [16]=cause_104
    # ──────────────────────────────────────────────────────────
    df_raw = pd.read_csv(csv_path, encoding="cp949", dtype=str,
                         header=0, low_memory=False)
    print(f"  raw rows: {len(df_raw):,}, cols: {len(df_raw.columns)}")
    print(f"  col header sample: {df_raw.columns.tolist()[:6]}...")

    if len(df_raw.columns) < 17:
        print(f"  [SKIP] column 수 부족 ({len(df_raw.columns)} < 17)")
        return pd.DataFrame()

    # Position 직접 매핑 (column name 무시)
    COL_POS = {
        "year_str":            0,
        "sido_raw":            4,
        "sigungu_raw":         5,
        "marital_code_raw":   10,
        "education_code_raw": 11,
        "sex_code":           12,
        "age_5y_code":        13,
        "national_code":      14,
        "cause_104":          16,
    }
    new_data = {tgt: df_raw.iloc[:, idx].values for tgt, idx in COL_POS.items()}
    df = pd.DataFrame(new_data)
    print(f"  after position-based parse: cols = {df.columns.tolist()}")
    print(f"  age_5y_code sample 5: {df['age_5y_code'].head(5).tolist()}")
    print(f"  age_5y_code non-null: {df['age_5y_code'].notna().sum():,}/{len(df):,}")

    # year column
    if "year_str" in df.columns:
        df["year"] = pd.to_numeric(df["year_str"], errors="coerce").astype("Int64")
    else:
        df["year"] = year

    # 한국인 filter — 외국인 ("2") 만 drop, 나머지 (1/NaN/빈값) 모두 keep
    # 1997-2007: 변수 부재 (모두 NaN) → 전체 keep (한국인 간주)
    # 2008+: "1" = 한국인, "2" = 외국인
    if "national_code" in df.columns:
        before = len(df)
        df = df.copy()
        df["national_code"] = df["national_code"].astype(str).str.strip()
        # "2" 만 drop (외국인). NaN/nan/"" 등 missing 은 한국인 간주
        df = df[df["national_code"] != "2"].reset_index(drop=True).copy()
        # flag: "1" 명시된 row 만 = 1, 나머지 (1997-2007 missing) = 0
        df["national_filter_applied"] = (df["national_code"] == "1").astype(int).values
        print(f"  national filter (외국인 drop): {before:,} → {len(df):,} ({100*len(df)/before:.1f}%)")
    else:
        df["national_filter_applied"] = 0

    # 시군구 정규화 → h_code
    df["h_code"] = df.apply(
        lambda row: normalize_sigungu(row.get("sido_raw", ""), row.get("sigungu_raw", "")),
        axis=1
    )

    # age band
    df["age_5y_code"] = df["age_5y_code"].astype(str).str.strip()
    df["age_band"] = df["age_5y_code"].map(AGE_BAND_MAP)
    n_age_missing = df["age_band"].isna().sum()
    if n_age_missing > 0:
        miss_codes = df[df["age_band"].isna()]["age_5y_code"].value_counts().head(5)
        print(f"  age 매핑 missing: {n_age_missing:,} (codes: {miss_codes.to_dict()})")
    df = df.dropna(subset=["age_band"])

    # 혼인 (9 = 미상 drop)
    if len(df) == 0:
        print(f"  [skip marital/edu] empty after age filter")
        return pd.DataFrame()
    df["marital_code_raw"] = df["marital_code_raw"].astype(str).str.strip()
    before = len(df)
    df = df[df["marital_code_raw"].isin(VALID_MARITAL)].copy()
    df["marital_code"] = df["marital_code_raw"]
    pct = 100*len(df)/before if before > 0 else 0.0
    print(f"  marital filter (1-4): {before:,} → {len(df):,} ({pct:.1f}%)")

    # 교육 → 3 카테고리 (9 = 미상 drop)
    if len(df) == 0:
        print(f"  [skip edu] empty after marital filter")
        return pd.DataFrame()
    df["education_code_raw"] = df["education_code_raw"].astype(str).str.strip()
    df["education_band"] = df["education_code_raw"].map(EDU_3CAT)
    before = len(df)
    df = df.dropna(subset=["education_band"])
    pct = 100*len(df)/before if before > 0 else 0.0
    print(f"  education filter (1-7 → 3 카테고리): {before:,} → {len(df):,} ({pct:.1f}%)")

    # sex code clean
    df["sex_code"] = df["sex_code"].astype(str).str.strip()
    df = df[df["sex_code"].isin(["1", "2"])].copy()

    # cause_104 keep
    df["cause_104"] = df["cause_104"].astype(str).str.strip()

    # weight = 1 per row (microdata = 1 사망 = 1 row)
    df["weight"] = 1

    # 최종 column 만 keep
    out = df[["year", "h_code", "sex_code", "age_band",
              "marital_code", "education_band", "cause_104",
              "weight", "national_filter_applied"]].copy()

    print(f"  cleaned rows: {len(out):,}")
    return out


def main() -> int:
    print("=" * 70)
    print("11a: 사망 microdata 28 시점 (1997-2024) parse + cleaning")
    print("=" * 70)

    csv_files = sorted(RAW_DIR.glob("*_사망_연간자료_B형_*.csv"))
    print(f"\n[input] {len(csv_files)} csv files")

    all_dfs = []
    for csv_path in csv_files:
        df = parse_one_csv(csv_path)
        if not df.empty:
            all_dfs.append(df)

    final = pd.concat(all_dfs, ignore_index=True)
    print(f"\n[concat] total rows: {len(final):,}")

    # Save
    out_path = OUT_DIR / "mortality_microdata_cleaned_v01.parquet"
    final.to_parquet(out_path, index=False)
    print(f"\n[save] {out_path}")
    print(f"  rows: {len(final):,}")
    print(f"  size: {out_path.stat().st_size / 1e6:.2f} MB")

    # Validation summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"\nyears: {sorted(final['year'].unique())}")
    print(f"unique h_code: {final['h_code'].nunique()}")
    print(f"\nmarital_code distribution:")
    print(final["marital_code"].value_counts(dropna=False).to_string())
    print(f"\neducation_band distribution:")
    print(final["education_band"].value_counts(dropna=False).to_string())
    print(f"\nage_band distribution:")
    print(final["age_band"].value_counts(dropna=False).to_string())
    print(f"\nsex_code distribution:")
    print(final["sex_code"].value_counts(dropna=False).to_string())
    print(f"\nyear별 row count:")
    print(final["year"].value_counts().sort_index().to_string())

    print("\n" + "=" * 70)
    print("완료. 다음:")
    print("  11b_mortality_marital_panel.py: marital_code × cause_104 cross-tab")
    print("  11c_mortality_education_panel.py: education_band × cause_104 cross-tab")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
