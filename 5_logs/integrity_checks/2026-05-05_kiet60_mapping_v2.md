# Phase 2-B Step 5a-2 — KIET60 mapping v2 (robust)
_2026-05-05_

## KSIC 6차 → 9차 manual crosswalk
- saved: `1_codebooks\ksic6_to_ksic9_2digit.csv` (28 mappings)

## KIET60_to_KSIC_v2 inspection
- shape: (101, 5)
- columns: ['1레벨', '2레벨', '3레벨', '표준산업분류 10차', '표준산업분류 9차']

- KSIC 9차 leading code 파싱 결과:
 - non-null: 94/101
 - distinct 2-digit: 63
 - top: {'C26': 8, 'Non': 7, 'P85': 7, 'C28': 6, 'C20': 5, 'C23': 4, 'C31': 4, 'C24': 3, 'C29': 2, 'C22': 2, 'K65': 1, 'K66': 1, 'O84': 1, 'K64': 1, 'L68': 1}

- KIET 코드 추출:
 - kiet1 distinct: 8
 - kiet2 distinct: 8
 - kiet3 distinct: 60

## baseline_shares_1994_manufacturing
- rows: 9,739, distinct KSIC4 (6차): 70
- KSIC 6차 → 9차 (2-digit) 변환률: **9,739/9,739** (100.0%)
- 미매핑 6차 2-digit top 5: {}

## KSIC9 2-digit → KIET 그룹 매핑 (mode 기준)
```
ksic9_2digit kiet1 kiet2
 C10 NaN I34
 C11 NaN NaN
 C12 NaN NaN
 C13 NaN NaN
 C14 NaN NaN
 C15 NaN NaN
 C16 NaN NaN
 C17 NaN NaN
 C18 NaN NaN
 C19 NaN I33
 C20 NaN I32
 C21 I3 I31
 C22 NaN NaN
 C23 NaN NaN
 C24 NaN NaN
 C25 NaN NaN
 C26 NaN NaN
 C27 NaN NaN
 C28 NaN NaN
 C29 NaN NaN
 C30 NaN NaN
 C31 NaN NaN
 C32 NaN NaN
 C33 NaN NaN
 G45 I7 I71
 G46 NaN NaN
 G47 NaN NaN
 H49 NaN NaN
 H50 NaN NaN
 H51 NaN NaN
 H52 NaN NaN
 I55 NaN I74
 I56 NaN NaN
 J58 NaN I72
 J59 NaN NaN
 J60 NaN NaN
 J61 NaN NaN
 J62 NaN NaN
 J63 NaN NaN
 K64 NaN NaN
 K65 NaN NaN
 K66 NaN NaN
 L68 NaN NaN
 L69 NaN NaN
 M70 NaN NaN
 M71 NaN NaN
 M72 NaN NaN
 M73 NaN NaN
 N74 NaN NaN
 N75 NaN NaN
 Non I0 NaN
 O84 NaN I73
 P85 NaN NaN
 Q86 NaN NaN
 Q87 NaN NaN
 R90 NaN NaN
 R91 NaN NaN
 S94 NaN NaN
 S95 NaN NaN
 S96 NaN NaN
 T97 NaN NaN
 T98 NaN NaN
 U99 NaN NaN
```

- saved: `3_derived\bartik\baseline_shares_1994_ksic9_2digit.parquet`
- rows: 4,003, distinct h_code: 226, distinct KSIC9 2-digit: 22

## HS6 ↔ KIET60 매핑 (Comtrade input 준비)
- shape: (6909, 8)
- HS code 길이 distribution: {6: 6206, 5: 703}
- 레벨1코드 distinct: 5
- 레벨2코드 distinct: 4
- 레벨3코드 distinct: 40
- 레벨1코드 distribution: {'I3': 6314, 'I1': 395, 'I2': 122, 'I5': 63, 'I4': 1}

## 결정 사항 (다음 step 입력)
- ✅ KSIC 6→9 (2-digit) 변환률 100.0% → **KSIC9 2-digit 단위 Bartik 진행 권장**
- baseline: `baseline_shares_1994_ksic9_2digit.parquet` (h × KSIC9 2-digit)
- next: HS6 → KSIC9 2-digit 매핑으로 Comtrade 집계 (또는 KIET 2레벨 매개)

- aggregation level 옵션:
 - **KSIC9 2-digit (~24 industries)**: ADH 4-digit SIC 보다 coarse 하지만 robust ← 권장
 - KIET 3레벨 (~60 industries): ADH 와 동급 precision but KSIC 9차 4-digit 까지 변환 필요 (별도 turn)
 - KIET 2레벨 (~10 industries): too coarse, robustness only