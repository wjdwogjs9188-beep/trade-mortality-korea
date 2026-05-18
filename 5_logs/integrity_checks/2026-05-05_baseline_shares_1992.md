# 1992 광업제조업조사 baseline shares build
_2026-05-05_

- raw: `1992_연간자료_20260505_20424.csv`
- raw rows: **76,357**, cols: 101

## Schema verify
- 시도 distinct: 15
- 시군구 (raw_code) distinct: 274
- KSIC 대분류: {'29': 9302, '17': 8106, '18': 6573, '28': 6129, '15': 5044, '36': 4917, '26': 4405, '25': 4313, '22': 3406, '32': 3132, '31': 2993, '19': 2721, '34': 2392, '24': 2353, '21': 2309, '20': 2150, '27': 1835, '14': 1405, '33': 1345, '35': 638, '30': 428, '10': 261, '37': 91, '23': 77, '16': 20, '13': 12}
- 종사자 (col 14) 합: 53,189

## sigungu match (1997 baseline crosswalk)
- match: **68,105/76,357** (89.2%)
- ⚠️ 매칭률 95% 미달 — 1992 의 행정구역이 1997 baseline 과 다를 가능성 (안성·시흥·평택 시군구 변경 등)
- 미매칭 top 10: {'31450': 1335, '31100': 940, '31430': 772, '36510': 493, '38032': 447, '36490': 346, '34450': 294, '31420': 263, '35430': 245, '37450': 217}

## Manufacturing (D) only
- rows: **0**
- 종사자 합 (D only): **0**
- *cross-check anchor*: 1992 한국통계연감 제조업 종사자 ≈ 약 250-280 만 (구체 숫자 cross-check 필요)

## KSIC 6차 → 9차 변환 (매핑 file: `ksic_crosswalk_8_to_9.csv`)
- 매핑 rows: 1121
- 매핑 컬럼: ['KSIC8', 'KSIC9']
- ⚠️ 본 file 은 8차→9차 매핑 (6차→9차 직접 매핑 부재). 6차→8차 별도 매핑 필요
- 임시 처리: ksic6_2digit 의 letter 부분을 직접 KSIC9 2-digit 로 매핑 (D=C, 등 manual)

## KSIC9 2-digit (임시 manual) distinct: 0

## Baseline shares 1992 build 결과
- h_code distinct: 0
- ksic9_2digit distinct: 0
- (h × k) rows: 0

## 저장
- 3_derived\bartik\baseline_shares_1992_ksic9_2digit.parquet
- 3_derived\bartik\denominator_E_h_1992.parquet