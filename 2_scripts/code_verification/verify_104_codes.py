"""사망 raw 코드별 카운트 → KOSTAT 공식 사인별 통계 매칭으로 104 분류 라벨 자동 추출.

전략:
  1. 사망 raw 28년치에서 코드별 × 연도별 카운트
  2. KOSTAT 공식 사인별 사망 통계와 매칭
  3. 매칭률 95% 이상이면 라벨 확정

이 스크립트는 코드 102 검증 (이미 자살로 확정) + 다른 79 코드의 후보 식별.
"""
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import RAW_DIR, DERIVED_DIR


MORT_DIR = RAW_DIR / "mortality_kostat" / "사망사료 정리"


# KOSTAT 공식 주요 사인별 통계 (사용자 검증용 vintage 2010-2019)
# 출처: KOSTAT 사망원인통계 보도자료
KOSTAT_OFFICIAL = {
    # (사인, 연도): 사망자 수
    ("자살", 2010): 15566,
    ("자살", 2011): 15906,
    ("자살", 2012): 14160,
    ("자살", 2013): 14427,
    ("자살", 2014): 13836,
    ("자살", 2015): 13513,
    ("자살", 2019): 13799,
    # 추가: 폐암, 뇌혈관, 심장, 당뇨병, 폐렴 등 (사용자가 추후 보강)
    # ("폐암", 2010): 15323,  # KOSTAT 검증 후 추가
    # ("심장 질환", 2010): 26517,
}


def code_year_count(year: int) -> pd.Series:
    """주어진 연도의 코드별 카운트."""
    files = list(MORT_DIR.glob(f"{year}_*.csv"))
    if not files:
        return pd.Series(dtype=int)
    df = pd.read_csv(files[0], dtype=str, encoding='cp949',
                     usecols=['사망원인_104항목분류코드'])
    return df['사망원인_104항목분류코드'].value_counts()


def match_codes_to_kostat(year: int = 2010) -> pd.DataFrame:
    """주어진 연도의 raw 코드 카운트를 KOSTAT 공식 통계와 매칭."""
    counts = code_year_count(year)
    print(f"\n=== {year}년 raw 코드별 카운트 ===")
    print(f"총 행수: {counts.sum():,}")
    print(f"고유 코드 수: {len(counts)}")

    # KOSTAT 와 매칭 (자살 = 102 already known)
    print(f"\n=== KOSTAT 매칭 (year={year}) ===")
    rows = []
    for (cause, y), official in KOSTAT_OFFICIAL.items():
        if y != year: continue
        # 같은 카운트의 코드 찾기
        match = counts[counts == official]
        if len(match) > 0:
            for code, count in match.items():
                print(f"  {cause}({y}): {official:,} = 코드 {code} ✅")
                rows.append({"cause": cause, "year": y, "code": code,
                             "raw_count": count, "official": official, "match": "exact"})
        else:
            # 가까운 카운트 (±0.5%)
            tol = official * 0.005
            close = counts[(counts >= official - tol) & (counts <= official + tol)]
            for code, count in close.items():
                print(f"  {cause}({y}): {official:,} ≈ 코드 {code} ({count:,}, diff {abs(count-official)})")
                rows.append({"cause": cause, "year": y, "code": code,
                             "raw_count": count, "official": official, "match": "close"})
    return pd.DataFrame(rows), counts


def main():
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    # 여러 연도에서 검증
    all_matches = []
    code_counts = {}
    for year in [2010, 2011, 2015, 2019]:
        try:
            matches, counts = match_codes_to_kostat(year)
            all_matches.append(matches)
            code_counts[year] = counts
        except Exception as e:
            print(f"\n  ⚠️ {year}: {e}")

    if all_matches:
        df = pd.concat(all_matches, ignore_index=True)
        out = DERIVED_DIR / "code_verification_104.csv"
        df.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"\n매칭 결과 저장: {out}")
        print(f"\n매칭된 코드 수: {df['code'].nunique()}")
        print(df.groupby('cause')['code'].first())

    # 모든 연도의 top 20 코드 비교 (안정적 코드 식별)
    print("\n=== 2010년 Top 20 코드 ===")
    top20 = code_counts.get(2010, pd.Series()).head(20)
    print(top20)


if __name__ == "__main__":
    main()
