"""MDIS 인구주택총조사 5 시점 (2000-2020) column layout + 코드 정의 추출.

목적:
  1. 5 CSV 의 header (column 명) + 첫 row 추출
  2. description xlsx/.xls 의 항목정보 + 코드정보 sheet 전체 추출
  3. 혼인상태/교육정도/시군구/성별/연령 column 위치 + code 매핑 search
  4. 5 시점 column 일치성 verify

선행:
  pip install xlrd --break-system-packages
  pip install openpyxl --break-system-packages

산출:
  - stdout: 5 시점 column layout + 혼인/교육/시군구 code 정의
  - 0_raw/mdis_population_census/_layout/ 에 시점별 layout JSON 저장

실행:
    cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
    python 2_scripts\\data_collection\\07_mdis_population_columns_extract.py
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "0_raw" / "mdis_population_census"
LAYOUT_DIR = RAW_DIR / "_layout"
LAYOUT_DIR.mkdir(parents=True, exist_ok=True)

# 모든 description 폴더 (USRCNFRM_*) + 모든 데이터 폴더 (2%_표본_인구_*)
DESC_DIRS = sorted([p for p in RAW_DIR.glob("USRCNFRM_*") if p.is_dir()])
DATA_DIRS = sorted([p for p in RAW_DIR.glob("2%_표본_인구_*") if p.is_dir()])

print(f"DESC dirs ({len(DESC_DIRS)}):")
for d in DESC_DIRS:
    print(f"  {d.name}")
print(f"DATA dirs ({len(DATA_DIRS)}):")
for d in DATA_DIRS:
    print(f"  {d.name}")

# 우리가 mediator panel build 에 필요한 항목 (search keyword)
TARGET_KEYWORDS = {
    "시도": ["행정구역시도", "시도코드", "시도"],
    "시군구": ["행정구역시군구", "시군구코드", "시군구"],
    "성별": ["성별코드", "성별"],
    "연령": ["만연령", "연령"],
    "혼인상태": ["혼인상태", "혼인", "결혼"],
    "교육정도": ["교육정도", "교육수준", "학력"],
    "가구주관계": ["가구주관계", "가구주"],
}


def extract_csv_header(csv_path: Path) -> dict:
    """CSV header (column 명) + 첫 데이터 row 추출."""
    print(f"\n{'='*70}")
    print(f"CSV: {csv_path.name}")
    print(f"{'='*70}")

    with open(csv_path, "r", encoding="cp949", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print("  [FAIL] empty file")
            return {}
        try:
            first_row = next(reader)
        except StopIteration:
            first_row = [""] * len(header)

    print(f"  total columns: {len(header)}")
    print(f"  total data row sample: len={len(first_row)}")

    # 모든 column 출력 (number + name + first value)
    print(f"\n  All columns:")
    for i, col in enumerate(header):
        val = first_row[i] if i < len(first_row) else ""
        print(f"    [{i:3d}] {col} = '{val}'")

    # Target keyword search
    print(f"\n  Target column positions:")
    found = {}
    for target, keywords in TARGET_KEYWORDS.items():
        matches = []
        for i, col in enumerate(header):
            for kw in keywords:
                if kw in col:
                    matches.append((i, col))
                    break
        found[target] = matches
        if matches:
            for idx, name in matches:
                print(f"    {target}: [{idx}] {name}")
        else:
            print(f"    {target}: NOT FOUND")

    return {
        "file": csv_path.name,
        "n_columns": len(header),
        "header": header,
        "first_row": first_row,
        "target_columns": {k: v for k, v in found.items()},
    }


def extract_description_xls(xls_path: Path) -> dict:
    """description xlsx/.xls 의 항목정보 + 코드정보 sheet 전체 추출.

    sheet 구조 (사용자 paste 결과 기반):
      - 항목정보: 항목번호, 항목명, 길이, 타입, 코드정보, 특이사항
      - 코드정보: 코드번호, 항목명, 코드, 코드의미 및 단위, 특이사항
      - 행정구역코드 (있는 경우): 시도/시군구 매핑
    """
    print(f"\n{'='*70}")
    print(f"DESC: {xls_path.name}")
    print(f"{'='*70}")

    try:
        import pandas as pd
    except ImportError:
        print("  [skip] pandas not installed")
        return {}

    try:
        xl = pd.ExcelFile(xls_path)
    except Exception as e:
        print(f"  [FAIL] {type(e).__name__}: {e}")
        return {}

    print(f"  sheets: {xl.sheet_names}")
    out = {"file": xls_path.name, "sheets": {}}

    for sheet in xl.sheet_names:
        try:
            df = pd.read_excel(xls_path, sheet_name=sheet, dtype=str, header=None)
        except Exception as e:
            print(f"  [skip sheet '{sheet}'] {e}")
            continue

        print(f"\n  [sheet '{sheet}'] shape={df.shape}")
        # 항목정보 sheet 인 경우 전체 출력
        if "항목" in sheet or "정보" in sheet or "코드" in sheet:
            # head 60 row 출력 (대부분 항목 다 봄)
            print(df.head(80).to_string(max_cols=10, max_colwidth=30))
        else:
            print(df.head(20).to_string(max_cols=10, max_colwidth=30))

        out["sheets"][sheet] = df.values.tolist()

        # 혼인/교육/시군구 row search
        if "항목" in sheet or "코드" in sheet:
            print(f"\n  >>> Target keyword search in '{sheet}':")
            for col in df.columns:
                col_str = df[col].astype(str)
                for target, keywords in TARGET_KEYWORDS.items():
                    for kw in keywords:
                        mask = col_str.str.contains(kw, na=False, regex=False)
                        if mask.any():
                            indices = df.index[mask].tolist()
                            for idx in indices[:3]:  # 첫 3 row 만
                                row_str = " | ".join(str(v)[:30] for v in df.iloc[idx].tolist()[:8])
                                print(f"    {target} ({kw}): row {idx}: {row_str}")

    return out


def main() -> int:
    print("=" * 70)
    print("MDIS 인구주택총조사 5 시점 column layout + 코드 정의 추출")
    print("=" * 70)

    # 1. CSV header 추출
    print("\n" + "#" * 70)
    print("# PART 1: CSV header (column 명) 추출")
    print("#" * 70)

    csv_layouts = {}
    all_csvs = []
    for ddir in DATA_DIRS:
        all_csvs.extend(sorted(ddir.glob("*.csv")))
    print(f"\n[total CSV files] {len(all_csvs)}")

    for csv_path in all_csvs:
        # 파일명에서 시점 추출 (2000_2%_표본... → 2000)
        year = csv_path.name.split("_")[0]
        try:
            yr_int = int(year)
        except ValueError:
            yr_int = None
        layout = extract_csv_header(csv_path)
        if layout and yr_int:
            csv_layouts[yr_int] = layout
            # JSON save
            with open(LAYOUT_DIR / f"csv_layout_{year}.json", "w", encoding="utf-8") as f:
                json.dump({k: v for k, v in layout.items() if k != "first_row"},
                          f, ensure_ascii=False, indent=2)

    # 2. Description xls/xlsx 추출
    print("\n" + "#" * 70)
    print("# PART 2: Description (파일설계서/코드집) 항목정보 + 코드정보")
    print("#" * 70)

    desc_layouts = {}
    desc_files = []
    for ddir in DESC_DIRS:
        desc_files.extend(sorted(ddir.glob("*파일설계서*.xls*")))
        desc_files.extend(sorted(ddir.glob("(파일설계서*.xlsx")))
    desc_files = sorted(set(desc_files))  # dedup
    print(f"\n[total description files] {len(desc_files)}")

    for xls_path in desc_files:
        layout = extract_description_xls(xls_path)
        if layout:
            desc_layouts[xls_path.name] = layout

    # 3. Cross-year column 일치성 verify
    print("\n" + "#" * 70)
    print("# PART 3: 5 시점 column 일치성 verify")
    print("#" * 70)
    if csv_layouts:
        all_years = sorted(csv_layouts.keys())
        print(f"  years: {all_years}")
        for target in TARGET_KEYWORDS:
            print(f"\n  {target}:")
            for yr in all_years:
                matches = csv_layouts[yr].get("target_columns", {}).get(target, [])
                if matches:
                    print(f"    {yr}: {[(i, n) for i, n in matches]}")
                else:
                    print(f"    {yr}: NOT FOUND")

    print()
    print("=" * 70)
    print(f"완료. layout JSON: {LAYOUT_DIR}")
    print("다음 단계:")
    print("  - 위 결과 paste → 08_*_parse_and_crosstab.py 작성")
    print("  - 시군구 (시도+시군구) × 성 × 연령 × 혼인 × 교육 cross-tab")
    print("  - mortality_rate_panel_v02_1 의 분모 형식과 동일하게 align")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
