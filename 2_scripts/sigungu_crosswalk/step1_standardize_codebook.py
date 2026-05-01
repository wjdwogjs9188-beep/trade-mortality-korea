"""Phase 1-A Step 1 표준화: KOSTAT 코드집 → long format.

입력: 0_raw/mortality_kostat/usrcnfrm/시군구코드집(공공용)_..._1999.xlsx
      (1997/1998/1999 SHA256 동일 — 캐논 historical 코드집, 1981-2021 wide)

구조:
  행 0: 연도 헤더 (col 2~42 = 2021, 2020, ..., 1981)
  행 1: '사망원인통계' 메타 라벨 (skip)
  행 2+: 데이터
      - 시도 행: col 0 = 시도명, code = 2자리 (예: 11)
      - 시군구 행: col 0 = 시군구명, code = 5자리 (~1996 4자리)
      - "-" = 해당 연도 미존재

출력: 3_derived/sigungu/step1_codebook_old.csv
컬럼: year, sido_code, sido_name, raw_code, sigungu_name, code_len
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(r"C:/Users/82103/Downloads/trade_mortality_korea")
SRC = ROOT / "0_raw" / "mortality_kostat" / "usrcnfrm" / \
      "시군구코드집(공공용)_사망원인통계_사망_연간자료_B형(제공)_1999.xlsx"
OUT_DIR = ROOT / "3_derived" / "sigungu"
OUT = OUT_DIR / "step1_codebook_old.csv"


def _norm(v) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    return str(v).strip()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = pd.read_excel(SRC, sheet_name=0, header=None, dtype=object)
    print(f"입력: {SRC.name}")
    print(f"shape: {raw.shape}")

    # 연도 헤더 (행 0, col 2~)
    year_row = raw.iloc[0]
    year_cols: dict[int, int] = {}
    for c in range(2, raw.shape[1]):
        v = year_row.iat[c]
        if pd.notna(v):
            try:
                y = int(v)
                if 1980 <= y <= 2030:
                    year_cols[c] = y
            except (TypeError, ValueError):
                pass
    print(f"연도 컬럼 {len(year_cols)}개: {min(year_cols.values())}~{max(year_cols.values())}")

    records: list[dict] = []
    current_sido_name: str | None = None
    current_sido_code: str | None = None
    sido_count = 0
    sigungu_count = 0
    skipped_meta = 0

    for r in range(2, raw.shape[0]):
        name = _norm(raw.iat[r, 0])
        if not name:
            continue

        # 시도/시군구 구분: 모든 연도 코드 중 최대 길이로 판정
        codes_per_year: dict[int, str] = {}
        max_len = 0
        for c, y in year_cols.items():
            v = _norm(raw.iat[r, c])
            if v and v != "-":
                codes_per_year[y] = v
                if len(v) > max_len:
                    max_len = len(v)

        if not codes_per_year:
            # 코드가 한 개도 없으면 메타/구분행
            skipped_meta += 1
            continue

        if max_len <= 2:
            # 시도 행
            sido_codes = set(codes_per_year.values())
            if len(sido_codes) > 1:
                # 시도 코드 변경 (없을 가능성 높음) — 가장 최신 코드 사용
                latest_y = max(codes_per_year.keys())
                current_sido_code = codes_per_year[latest_y]
            else:
                current_sido_code = next(iter(sido_codes))
            current_sido_name = name
            sido_count += 1
            continue

        # 시군구 행
        if current_sido_name is None:
            print(f"  ⚠ 행 {r} '{name}' — 시도 정보 없음. skip", file=sys.stderr)
            continue

        for y, code in codes_per_year.items():
            records.append({
                "year": y,
                "sido_code": current_sido_code,
                "sido_name": current_sido_name,
                "raw_code": code,
                "sigungu_name": name,
                "code_len": len(code),
            })
        sigungu_count += 1

    print(f"\n시도 행 {sido_count}, 시군구 행 {sigungu_count}, 메타/skip {skipped_meta}")
    print(f"long 레코드 수: {len(records)}")

    df = pd.DataFrame(records)
    df = df.sort_values(["year", "sido_code", "raw_code"]).reset_index(drop=True)
    df.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"\n저장: {OUT}")

    print("\n--- 연도별 unique 시군구 수 ---")
    yearly = df.groupby("year")["raw_code"].nunique().reset_index(name="n_sigungu")
    print(yearly.to_string(index=False))

    print("\n--- 시도 목록 (최신 연도 기준) ---")
    latest = df["year"].max()
    sidos = df[df["year"] == latest][["sido_code", "sido_name"]].drop_duplicates()
    print(sidos.to_string(index=False))

    print("\n--- code_len 분포 (연도×길이) ---")
    cross = df.groupby(["year", "code_len"]).size().unstack(fill_value=0)
    print(cross)

    return 0


if __name__ == "__main__":
    sys.exit(main())
