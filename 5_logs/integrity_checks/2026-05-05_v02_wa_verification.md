# v02_wa panel verification (P1.B clear)
_2026-05-05_

## panel
- shape: (31494, 8), cols: ['h_code', 'year', 'outcome_group', 'deaths', 'period_pre2008', 'pop_wa', 'mortality_rate', 'log_asr_p1']

## 종로구 (11010) 2020 spot-check (P1.B reviewer)
- pop_wa: **89,510**
- ✅ **working-age range (70-100k)** — WA filter 정상 적용

## outcome group 별 row count
```
outcome_group
cancer 6392
despair_total 6392
cardiovascular 6384
external_other 6380
respiratory 5946
```

## 2010 전국 despair_total — KOSIS suicide WA cross-check
- 전국 deaths: 14,336
- 전국 pop_wa: 29,755,304
- 전국 rate: 48.2 per 100k
- KOSIS suicide WA 2010 ≈ 32-35, despair = +drug+psych+liver → 약 45-50 expected
- ✅ external validation pass

## 종로구 (11010) despair_total time series
```
 year deaths pop_wa mortality_rate
 1997 60 NaN NaN
 1998 59 112978.5 52.222325
 1999 46 111738.0 41.167732
 2000 29 111600.5 25.985547
 2001 50 111244.5 44.946042
 2002 50 110211.5 45.367316
 2003 39 108410.5 35.974375
 2004 39 106489.5 36.623329
 2005 54 104402.0 51.723147
 2006 48 102515.0 46.822416
 2007 38 101711.5 37.360574
 2008 35 103200.5 33.914564
 2009 41 104514.0 39.229194
 2010 36 102993.0 34.953832
 2011 40 101345.0 39.469140
 2012 35 99575.0 35.149385
 2013 43 96793.5 44.424471
 2014 38 94116.0 40.375707
 2015 40 92340.0 43.318172
 2016 30 90994.0 32.969207
 2017 39 91089.0 42.815269
 2018 36 91451.0 39.365343
 2019 30 90465.5 33.161813
 2020 25 89509.5 27.929996
 2021 41 88422.0 46.368551
 2022 18 86982.0 20.693937
```

## panel coverage
- distinct h_code: 256
- year range: 1997-2022
- mortality_rate non-null: 30,298/31,494