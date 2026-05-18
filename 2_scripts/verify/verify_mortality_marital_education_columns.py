"""사망 microdata 의 혼인 / 교육 column 존재 여부 verify.

목적: paper § 5.2 mediation 의 numerator 형식 결정
  - 존재 → individual-level mediation (DGHP 2017 strict)
    : numerator = 사망 microdata × marital_code/education_code cross-tab (시군구×시점×성×연령)
  - 부재 → ecological mediation
    : numerator = mortality_panel (전체) / denominator = mediator panel 비율 회귀

탐색 위치:
  C:\\Users\\82103\\Desktop\\지역별 자살 데이터
  C:\\Users\\82103\\Desktop\\지역별 자살 데이터\\사망사료 정리

작업:
  1. 모든 폴더의 csv/xlsx/dat 파일 inventory
  2. 각 파일 의 column header 추출 (encoding cp949/utf-8 시도)
  3. 혼인/교육/marital/education keyword search
  4. 발견 시 sample value distribution 보여주기

실행:
    python 2_scripts\\verify\\verify_mortality_marital_education_columns.py
"""
from __future__ import annotations
import sys
import csv
from pathlib import Path
from collections import Counter

import pandas as pd

# 사망 microdata 후보 폴더 (사용자 메모리 기반)
SEARCH_DIRS = [
    Path(r"C:\Users\82103\Desktop\지역별 자살 데이터"),
    Path(r"C:\Users\82103\Desktop\지역별 자살 데이터\사망사료 정리"),
    Path(r"C:\Users\82103\Downloads\trade_mortality_korea\0_raw\mortality_microdata"),
]

# Target keyword (혼인 + 교육 변수 후보 명)
KEYWORDS = {
    "혼인": ["혼인", "결혼", "marital", "marriage", "혼인상태"],
    "교육": ["교육", "학력", "education", "학교", "edu_", "교육정도"],
    "성별": ["성별", "성별코드", "sex"],
    "연령": ["만연령", "만나이", "age", "연령"],
    "지역": ["시도", "시군구", "행정구역", "h_code", "sido", "sigungu"],
    "사망원인": ["사망원인", "cause", "사인", "ICD", "icd", "원인"],
    "사망일자": ["사망", "사망일자", "사망연월", "death_date"],
}


def detect_encoding(file_path: Path, sample_bytes: int = 50_000) -> str | None:
    """encoding 자동 감지 (cp949 → utf-8 → utf-8-sig 순서)."""
    for enc in ("cp949", "utf-8", "utf-8-sig", "euc-kr"):
        try:
            with open(file_path, "r", encoding=enc) as f:
                f.read(sample_bytes)
            return enc
        except UnicodeDecodeError:
            continue
    return None


def inspect_csv(csv_path: Path) -> dict:
    """CSV header + 첫 row + line length 분석."""
    print(f"\n{'='*70}")
    print(f"FILE: {csv_path}")
    print(f"{'='*70}")
    print(f"  size: {csv_path.stat().st_size / 1e6:.2f} MB")

    enc = detect_encoding(csv_path)
    if enc is None:
        print(f"  [FAIL] encoding detection")
        return {}
    print(f"  encoding: {enc}")

    with open(csv_path, "r", encoding=enc, newline="") as f:
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

    # Print all columns + first value
    print(f"  All columns:")
    for i, col in enumerate(header):
        val = first_row[i] if i < len(first_row) else ""
        print(f"    [{i:3d}] {col} = '{val[:40]}'")

    # Keyword search
    print(f"\n  Target keyword search:")
    found = {}
    for cat, kw_list in KEYWORDS.items():
        matches = []
        for i, col in enumerate(header):
            for kw in kw_list:
                if kw.lower() in col.lower():
                    matches.append((i, col))
                    break
        found[cat] = matches
        if matches:
            for idx, name in matches:
                print(f"    {cat}: [{idx}] {name}")
        else:
            print(f"    {cat}: NOT FOUND")

    return {
        "file": str(csv_path),
        "encoding": enc,
        "header": header,
        "first_row": first_row,
        "found": found,
    }


def value_distribution(csv_path: Path, enc: str, col_idx: int, col_name: str,
                       n_sample: int = 50_000) -> None:
    """특정 column 의 value distribution 출력."""
    print(f"\n  ── Value distribution: [{col_idx}] {col_name} (sample {n_sample:,} rows) ──")
    try:
        df = pd.read_csv(csv_path, encoding=enc, dtype=str, nrows=n_sample,
                         usecols=[col_name], low_memory=False)
        vc = df[col_name].value_counts(dropna=False).head(15)
        print(vc.to_string())
    except Exception as e:
        print(f"  [skip distribution] {type(e).__name__}: {e}")


def main() -> int:
    print("=" * 70)
    print("사망 microdata 의 혼인 / 교육 column 존재 여부 verify")
    print("=" * 70)

    # Step 1: 폴더 inventory
    print("\n[STEP 1] 폴더 inventory")
    all_files = []
    for d in SEARCH_DIRS:
        if not d.exists():
            print(f"  [skip] {d} (not found)")
            continue
        print(f"\n  {d}:")
        for f in sorted(d.rglob("*")):
            if f.is_file() and f.suffix.lower() in (".csv", ".xlsx", ".xls", ".dat", ".txt"):
                size_mb = f.stat().st_size / 1e6
                print(f"    {f.relative_to(d)}: {size_mb:.2f} MB ({f.suffix})")
                all_files.append(f)

    if not all_files:
        print("\n[FAIL] no files found")
        return 1

    # Step 2: 각 file inspection
    print(f"\n[STEP 2] file inspection ({len(all_files)} files)")
    results = []
    for f in all_files:
        if f.suffix.lower() in (".csv",):
            res = inspect_csv(f)
            if res:
                results.append(res)
        elif f.suffix.lower() in (".xlsx", ".xls"):
            print(f"\n[skip excel — manual open] {f.name}")
        elif f.suffix.lower() in (".dat", ".txt"):
            print(f"\n[skip dat/txt — fixed-width unknown] {f.name}")

    # Step 3: 혼인/교육 발견된 file 의 value distribution
    print("\n" + "=" * 70)
    print("[STEP 3] 혼인 / 교육 column 발견 file 의 value distribution")
    print("=" * 70)
    for res in results:
        혼인_matches = res["found"].get("혼인", [])
        교육_matches = res["found"].get("교육", [])
        if not (혼인_matches or 교육_matches):
            continue
        print(f"\n[{Path(res['file']).name}]")
        for idx, name in 혼인_matches:
            value_distribution(Path(res["file"]), res["encoding"], idx, name)
        for idx, name in 교육_matches:
            value_distribution(Path(res["file"]), res["encoding"], idx, name)

    # Step 4: Summary
    print("\n" + "=" * 70)
    print("[STEP 4] SUMMARY — paper § 5.2 mediation framework 결정")
    print("=" * 70)

    n_with_marital = sum(1 for r in results if r["found"].get("혼인"))
    n_with_education = sum(1 for r in results if r["found"].get("교육"))
    print(f"  inspected files: {len(results)}")
    print(f"    혼인 column 보유: {n_with_marital}")
    print(f"    교육 column 보유: {n_with_education}")

    if n_with_marital > 0 and n_with_education > 0:
        print("\n  ► individual-level mediation 가능 (DGHP 2017 strict framework)")
        print("    numerator = 사망 microdata × marital/education code cross-tab")
        print("    11_mediator_mortality_rate.py 작성 진행")
    elif n_with_marital > 0 or n_with_education > 0:
        print(f"\n  ► partial individual-level mediation 가능")
        print(f"    혼인 only or 교육 only individual-level, 다른 하나는 ecological")
    else:
        print("\n  ► individual-level 불가 — ecological mediation")
        print("    numerator = mortality_panel (전체) / denominator = mediator 비율")
        print("    DGHP 2017 의 ecological version (시군구 단위 mediator share)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
