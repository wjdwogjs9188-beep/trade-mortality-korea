# Stage 2-A — Mortality Panel Validation (v4, cancer narrowed to 027-047 + 2023 full file)

- Generated: 2026-05-03
- v4 changes vs v3:
  1. Cancer 정의 027-048 → 027-047 (KOSIS 공식 C00-C97 악성신생물과 정합. 048 양성/불명 → 'other' 흡수)
  2. 2023 microdata partial(262,710) → full(352,511) 교체
  3. V8 KOSIS cancer cross-check + V9 2023 record count 추가
- Source: `0_raw/mortality_kostat/사망사료 정리/` (27 cp949 CSVs)
- Crosswalk: `1_codebooks/sigungu_crosswalk_v2.csv` (229 h_codes, 27 years)
- Outputs:
  - `3_derived/mortality/mortality_microdata_combined.parquet` (7,298,820 rows; full incl. foreign/unmapped)
  - `3_derived/mortality/mortality_panel_v01.parquet` (1,483,920 rows)
  - `3_derived/mortality/unmatched_mortality.parquet` (0 unique foreign/unmapped raw_codes)

## Outcome groups (mutually exclusive, priority order)

| priority | group | cause_104 codes | n_codes | n_records | % |
|---:|---|---|---:|---:|---:|
| 1 | despair_total | ['057', '081', '101', '102'] | 4 | 579,774 | 7.94% |
| 2 | cardiovascular | ['067', '068', '069', '070'] | 4 | 1,561,216 | 21.39% |
| 3 | cancer | ['027', '028', '029', '030', '031', '032', '033', '034', '035', '036', '037', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047'] | 21 | 1,902,394 | 26.07% |
| 4 | respiratory | ['073', '074', '075', '076', '077', '078'] | 6 | 623,918 | 8.55% |
| 5 | external_other | ['097', '098', '099', '100', '103', '104'] | 6 | 469,284 | 6.43% |
| 6 | other | (fallback) | — | 2,161,279 | 29.62% |

**Note**: 101 (drug poisoning) and 081 (liver) → `despair_total` (not `external_other`/digestive). Priority order: despair > cardio > cancer > respiratory > external > other.

## Per-year processing summary

| year | n_in | foreign | unmapped(dom) | sex_drop | age=99 | cause_drop | n_valid | suicide(102) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1997 | 244,693 | 0 | 0 | 0 | 114 | 0 | 244,579 | 6,125 |
| 1998 | 245,825 | 0 | 0 | 0 | 83 | 0 | 245,742 | 8,698 |
| 1999 | 247,734 | 0 | 0 | 0 | 37 | 0 | 247,697 | 7,134 |
| 2000 | 248,740 | 0 | 0 | 0 | 20 | 0 | 248,720 | 6,522 |
| 2001 | 243,813 | 0 | 0 | 0 | 18 | 0 | 243,795 | 6,968 |
| 2002 | 247,524 | 0 | 0 | 0 | 21 | 0 | 247,503 | 8,664 |
| 2003 | 246,463 | 0 | 0 | 0 | 22 | 0 | 246,441 | 10,973 |
| 2004 | 246,220 | 0 | 0 | 0 | 10 | 0 | 246,210 | 11,568 |
| 2005 | 245,874 | 0 | 0 | 0 | 9 | 0 | 245,865 | 12,096 |
| 2006 | 244,162 | 0 | 0 | 0 | 8 | 0 | 244,154 | 10,736 |
| 2007 | 246,482 | 0 | 0 | 0 | 3 | 0 | 246,479 | 12,249 |
| 2008 | 246,113 | 0 | 0 | 0 | 7 | 0 | 246,106 | 12,858 |
| 2009 | 246,942 | 0 | 0 | 0 | 48 | 0 | 246,894 | 15,402 |
| 2010 | 255,405 | 0 | 0 | 0 | 70 | 0 | 255,335 | 15,558 |
| 2011 | 257,396 | 0 | 0 | 0 | 18 | 0 | 257,378 | 15,906 |
| 2012 | 267,221 | 0 | 0 | 0 | 49 | 0 | 267,172 | 14,159 |
| 2013 | 266,257 | 0 | 0 | 0 | 36 | 0 | 266,221 | 14,426 |
| 2014 | 267,692 | 0 | 0 | 0 | 42 | 0 | 267,650 | 13,834 |
| 2015 | 275,895 | 0 | 0 | 0 | 41 | 0 | 275,854 | 13,510 |
| 2016 | 280,827 | 0 | 0 | 0 | 42 | 0 | 280,785 | 13,092 |
| 2017 | 285,534 | 0 | 0 | 0 | 41 | 0 | 285,493 | 12,461 |
| 2018 | 298,820 | 0 | 0 | 0 | 43 | 0 | 298,777 | 13,670 |
| 2019 | 295,110 | 0 | 0 | 0 | 71 | 0 | 295,039 | 13,793 |
| 2020 | 304,948 | 0 | 0 | 0 | 27 | 0 | 304,921 | 13,195 |
| 2021 | 317,680 | 0 | 0 | 0 | 25 | 0 | 317,655 | 13,352 |
| 2022 | 372,939 | 0 | 0 | 0 | 18 | 0 | 372,921 | 12,906 |
| 2023 | 352,511 | 0 | 0 | 0 | 32 | 0 | 352,479 | 13,978 |
| **TOTAL** | **7,298,820** | **0** | **0** | **0** | **955** | **0** | **7,297,865** | **323,833** |

## Validation

| check | result | detail |
|---|:---:|---|
| V1 dtype: cause_104 string preserved | PASS | all 27 files read with dtype=str |
| V2 mutual exclusivity (each death exactly one outcome_group) | PASS | long_all=7,297,865 = sum(n_valid)=7,297,865; max group_per_cause=1 |
| V3 coverage all 27 years have deaths>0 | PASS | 1997-2023 all positive |
| V4 domestic sigungu unmapped < 1% | PASS | domestic_unmapped=0 of 7,298,820 = 0.0000%; foreign=0 (0.0000%) |
| V5 KOSTAT suicide cross-check ±2% | PASS | 2010: ours=15,558 official=15,566 diff=-0.051%; 2011: ours=15,906 official=15,906 diff=+0.000%; 2015: ours=13,510 official=13,513 diff=-0.022%; 2019: ours=13,793 official=13,799 diff=-0.043% |
| V6 deaths trend 1997 < 2010 < 2020 | PASS | 1997=244,579 2010=255,335 2020=304,921 |
| V7 outcome distribution (other < 50%) | PASS | other=29.62%  | despair_total=579,774(7.94%)  cardiovascular=1,561,216(21.39%)  cancer=1,902,394(26.07%)  respiratory=623,918(8.55%)  external_other=469,284(6.43%)  other=2,161,279(29.62%) |
| V8 KOSIS cancer cross-check ±0.5% (C00-C97, codes 027-047) | PASS | 1998: ours=51,283 official=51,291 diff=-0.016%; 2000: ours=58,195 official=58,197 diff=-0.003%; 2005: ours=65,529 official=65,529 diff=+0.000%; 2010: ours=72,047 official=72,048 diff=-0.001%; 2015: ours=76,854 official=76,855 diff=-0.001%; 2020: ours=82,199 official=82,204 diff=-0.006%; 2023: ours=85,270 official=85,271 diff=-0.001% |
| V9 2023 record count ~352,511 (full file) | PASS | n_in_2023=352,511 expected=352,511 diff=+0.0000% |

**Overall**: ALL PASS

## Top 10 cause_104 codes inside `other` group

- 095 (달리 분류되지 않은 증상, 징후와 임상 및 검사의 이상 소견): 831,558
- 053 (당뇨병(Diabetes mellitus)): 282,463
- 087 (나머지 비뇨생식계통 질환): 137,437
- 062 (나머지 신경계통 질환): 120,134
- 058 (나머지 정신 및 행동 장애): 112,973
- 082 (나머지 소화계통 질환): 105,553
- 061 (알츠하이머병(Alzheimer's disease)): 94,541
- 012 (패혈증(Septicaemia)): 74,530
- 005 (호흡기 결핵(Respiratory tuberculosis)): 61,750
- 084 (근골격계통 및 결합조직의 질환): 47,821

## Unit consistency vs KOSIS population panel (Stage 3 join prep)

### sigungu code format

- KOSTAT raw_code (5-digit) sample: `['11010', '11020', '11030', '11040', '11050']`
- KOSIS C1 (5-digit) sample: `['11010', '11020', '11030', '11040', '11050']`
- KOSIS C1 length distribution: `{5: 479808, 2: 36942}` (5-digit = sigungu, 2-digit = sido aggregate)
- **Match**: KOSTAT raw_code 형식 == KOSIS C1 5-digit. 직접 join 가능 (단 KOSIS 의 시-합계 / 시도-합계 행은 사전에 필터링 필요).

### sex code format

- KOSTAT sex_code unique: `['1', '2']` (1=남, 2=여)
- KOSIS C2 unique: `['0', '1', '2']` (['계', '남자', '여자']) — 0=계 + 1=남자 + 2=여자
- **Match**: 1/2 정확히 일치. KOSIS 의 C2='0'(계) 행은 사용 안 하면 됨.

### age 5-yr code format

- KOSTAT age_5yr_code unique (21): `['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '99']` (1-20 ordinal + 99 미상)
- KOSIS C3 unique (24): `['000', '020', '050', '070', '100', '120', '130', '150', '160', '180', '190', '210', '230', '260', '280', '310', '330', '340', '360', '370', '380', '410', '430', '440']`
- KOSIS C3_NM 일부: `['0 - 4세', '10 - 14세', '100세 이상', '15 - 19세', '20 - 24세', '25 - 29세', '30 - 34세', '35 - 39세', '40 - 44세', '45 - 49세'] ...`
- **MISMATCH**: KOSTAT 는 1..20 ordinal (예: 3=5-9세), KOSIS 는 020/050/070/... 시작연령*10 형식. **Stage 3 join 전에 mapping dict 필요**.
  - 또한 KOSTAT 코드 1 (0세) + 2 (1-4세) → KOSIS 020 (0-4세) 합산 필요.
  - KOSIS 의 80+ vs 80-84 vs 85+ vs 85-89 등 multi-bucket 처리 정책도 별도 결정.

### KOSIS year coverage

- range: 1993-2023 (KOSTAT 사망 panel 1997-2023 전부 포함)
- KOSIS C1 distinct: 304 (시군구 + 시도 합계 + 전국)

## Top 20 unmatched raw_codes (foreign + domestic_unmapped)

(none — KOSTAT B형은 모두 국내 거주자, 0% unmapped)
