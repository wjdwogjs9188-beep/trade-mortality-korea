# Stage 3B — Mortality Panel v02 Validation

- Generated: 2026-05-03
- v02 changes vs v01:
  1. **A.1 Component decomposition**: 6 → 10 outcomes. despair_total split into suicide_102 / drug_101 / psych_057 / liver_081 (각각 separate row), despair_total 보존 (overlap row).
  2. **mutually exclusive 가 아님**: 한 record (예: 102 자살) 가 2 row 로 표시 (suicide_102 + despair_total).
  3. 회귀 spec 마다 다른 outcome 사용 (component 만 vs 합산만). panel cell 합 ≠ total deaths.
- Output: `3_derived/mortality/mortality_panel_v02.parquet` (2,102,220 rows)

## Outcome groups (10 total, despair_total overlap)

| group | cause_104 codes | n_codes | overlap with despair_total |
|---|---|---:|:---:|
| suicide_102 | ['102'] | 1 | YES |
| drug_101 | ['101'] | 1 | YES |
| psych_057 | ['057'] | 1 | YES |
| liver_081 | ['081'] | 1 | YES |
| despair_total | ['057', '081', '101', '102'] | 4 | = sum of 4 components |
| cancer | ['027', '028', '029', '030', '031', '032', '033', '034', '035', '036', '037', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047'] | 21 | — |
| cardiovascular | ['067', '068', '069', '070'] | 4 | — |
| respiratory | ['073', '074', '075', '076', '077', '078'] | 6 | — |
| external_other | ['097', '098', '099', '100', '103', '104'] | 6 | — |
| other | (fallback) | — | — |

## Outcome distribution (long_df, includes despair overlap rows)

| outcome_group | n_records |
|---|---:|
| suicide_102 | 323,833 |
| drug_101 | 9,353 |
| psych_057 | 26,330 |
| liver_081 | 220,258 |
| despair_total | 579,774 |
| cancer | 1,902,394 |
| cardiovascular | 1,561,216 |
| respiratory | 623,918 |
| external_other | 469,284 |
| other | 2,161,279 |

## Validation (V1-V14)

| check | result | detail |
|---|:---:|---|
| V1 27 yr cover | PASS | n_yrs=27, range=1997-2023 |
| V2 229 sigungu | PASS | n_h_code=229 |
| V3 17 age bands | PASS | bands=['01_02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18_19_20'] |
| V4 rate join coverage > 99.5% | PASS | 123660/123660 = 100.000% |
| V5 deaths sum (primary + other) = valid records | PASS | panel_sum=7,297,865 long_sum=7,297,865 |
| V10 despair_total = sum(suicide_102, drug_101, psych_057, liver_081) | PASS | despair=579,774 components=579,774 |
| V11 외국인 빼기 후 음수 cell 0 | PASS | n_negative=0 |
| V12 COVID-057 ratio post/pre 0.5–1.5 | PASS | ratio=1.20 → TYPO (mild increase, no COVID merge) |
| V13 primary partition + other = valid count | PASS | primary+other=7,297,865 valid=7,297,865 |
| V14 despair national ASR 2010 (KR2010 baseline) 30-60 | PASS | national despair ASR 2010 = 47.79/100k |

**Overall**: ALL PASS