# Stage 3B — Mortality Rate Panel v02 Validation

- Generated: 2026-05-03
- Output: `3_derived/mortality/mortality_rate_panel_v02.parquet` (123,660 rows)

## v02 changes vs v01

1. **A.1**: 10 outcome groups (despair components separated, despair_total overlap row).
2. **A.2**: 분모 = 외국인 등록인구 빼기 (proportional scaling within (h, year) by sex × age).
3. **B.5**: 3 ASR baselines: Korean 2010 (main) + WHO 2000 (sensitivity) + Eurostat 2013 (sensitivity).

## Population panel v02 audit

- v01 2007 total: 49,130,354
- v02 2007 total: 49,130,354
- v01 2010 total: 49,879,812
- v02 2010 total: 49,048,172
- v01 2020 total: 51,349,259
- v02 2020 total: 49,823,642
- scale_min: 0.8150
- scale_q01: 0.8916
- scale_median: 0.9927

**한계**:
- KOSIS DT_1B040M5 의 주민등록인구는 정의상 한국국적 한정 (외국인 별도 외국인등록부). v01 panel V5 이미 Korean-only target과 ±0.001% 일치.
- 따라서 v02 의 외국인 빼기는 **conservative over-correction** 가능. ~2M 외국인 (2020 기준) 만큼 추가 차감되어 v02 < Korean only target.
- 권고: main analysis 는 v01 (or v02 with 한계 명시), robustness 는 v02 사용.
- 1997-2006 외국인 raw 부재 → 빼기 0 (KOSIS 외국인 < 0.5% 라 무시 가능).

## Validation

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

## ASR columns (3 baselines)

| column | baseline | use |
|---|---|---|
| asr_kr2010_per_100k | Korean 2010 (within-sex) | main |
| asr_who_2000_per_100k | WHO 2000 World Standard | sensitivity (international comparison) |
| asr_eur_2013_per_100k | Eurostat 2013 European Standard | sensitivity (Europe comparison) |
| ln_asr_* | log(asr+1) | log-form regression outcome |