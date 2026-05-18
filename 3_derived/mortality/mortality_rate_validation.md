# Stage 3 — Mortality Rate Panel Validation (v1)

- Generated: 2026-05-03
- Inputs: `3_derived\mortality\mortality_panel_v01.parquet` + `3_derived\population\population_panel_v01.parquet`
- Output: `3_derived\mortality\mortality_rate_panel_v01.parquet` (74,196 rows)

## Pipeline

1. Mortality panel age_5yr_code (1-20) → unified age_band (17 bands; 1+2→0-4, 18+19+20→80+)
2. Collapse mortality to (h, year, sex, age_band, outcome) → deaths
3. Merge with population panel on (h, year, sex, age_band) → rate_per_100k
4. 2010 한국 인구 baseline → within-sex age weight (Σw=1 per sex)
5. Direct age-standardized rate ASR = Σ(rate × w) / Σ(w_available) per (h, year, sex, outcome)
6. ln_asr = log(asr + 1)

## Panel dimensions

- distinct h_code: 229
- year range: 1997-2023
- outcomes: ['cancer', 'cardiovascular', 'despair_total', 'external_other', 'other', 'respiratory']
- max cells: 229 × 27 × 2 × 6 = 74,196
- actual cells: 74,196
- ASR NaN count (no population): 0

## Validation

| check | result | detail |
|---|:---:|---|
| V6 despair ASR historical pattern (2015<2010, 2023<1997) | PASS | weighted ASR/100k by year: 1997=58.84, 2000=52.40, 2003=55.58, 2010=46.99, 2015=37.90, 2017=34.98, 2020=35.18, 2023=35.32 | despair=suicide+drug+psych+liver; 간질환 1997 정점 후 급락이 suicide 상승을 압도 → 전체 감소 추세 정상 |
| V7 mortality × pop join coverage > 99.5% | PASS | joined=1,261,332 / mort_band=1,261,332 = 100.0000% (pop_missing=0) |
| V8 age band 매핑 deaths 합 보존 | PASS | orig=7,297,865 band=7,297,865 |

## National despair_total ASR (population-weighted, /100k by year)

| year | weighted_asr |
|---:|---:|
| 1997 | 58.84 |
| 1998 | 65.59 |
| 1999 | 57.71 |
| 2000 | 52.40 |
| 2001 | 51.45 |
| 2002 | 53.23 |
| 2003 | 55.58 |
| 2004 | 54.01 |
| 2005 | 51.33 |
| 2006 | 44.91 |
| 2007 | 45.28 |
| 2008 | 44.73 |
| 2009 | 47.90 |
| 2010 | 46.99 |
| 2011 | 46.12 |
| 2012 | 41.81 |
| 2013 | 41.08 |
| 2014 | 39.11 |
| 2015 | 37.90 |
| 2016 | 36.50 |
| 2017 | 34.98 |
| 2018 | 36.67 |
| 2019 | 35.50 |
| 2020 | 35.18 |
| 2021 | 35.22 |
| 2022 | 34.55 |
| 2023 | 35.32 |

(despair_total = suicide+drug+psych+liver. 한국 자살률 단독 시 2010 ~31; despair 전체 ~45-50 예상)

**Overall (rate panel)**: ALL PASS