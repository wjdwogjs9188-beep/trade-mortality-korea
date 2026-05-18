# Phase 2-A — Population join fix v3 (incremental)
_2026-05-05_

## Mortality panel
- rows: 31,494, cols: ['h_code', 'year', 'outcome_group', 'deaths', 'mortality_rate', 'log_asr_p1', 'pop_wa', 'period_pre2008']

## Population panel raw
- rows: 516,750, cols: ['C1', 'C1_NM', 'C2', 'C2_NM', 'C3', 'C3_NM', 'year', 'population']

## Schema 진단
- C1 length dist: {5: 479808, 2: 36942}
- C1 first 10 unique: ['00', '11', '11010', '11020', '11030', '11040', '11050', '11060', '11070', '11080']
- C2 unique: {'0': 172250, '1': 172250, '2': 172250}
- C3_NM unique (top 30): ['계', '0 - 4세', '5 - 9세', '10 - 14세', '15 - 19세', '20 - 24세', '25 - 29세', '30 - 34세', '35 - 39세', '40 - 44세', '45 - 49세', '50 - 54세', '55 - 59세', '60 - 64세', '65 - 69세', '70 - 74세', '75 - 79세', '80세 이상', '80 - 84세', '85세 이상', '85 - 89세', '90 - 94세', '95 - 99세', '100세 이상']
- year range: 1993-2023

## Working-age filter
- pop_wa rows: 174,816
- after 5-digit C1 filter: 161,976
- raw_code distinct: 286
- C2 top value: '0' (frequency 53,992)
- after C2='0' filter: 53,992

## Crosswalk merge 진단
- crosswalk rows: 6,723
- crosswalk raw_code distinct: 362
- crosswalk year range: 1997-2023
- crosswalk raw_code first 10: ['11010', '11020', '11030', '11040', '11050', '11060', '11070', '11080', '11090', '11100']
- pop raw_code: 286, crosswalk raw_code: 362
- intersect: 277
- pop only (top 10): ['31010', '31020', '31040', '31100', '33010', '33040', '35010', '37010', '38110']
- cw only (top 10): ['21510', '22510', '23510', '23520', '26510', '31390', '31400', '31550', '31570', '31580']

## Merge result
- match rate: 51,152/53,992 (94.7%)
- after drop unmatched: 51,152

## pop_wa aggregate
- rows: 6,321
- pop_wa stats: mean=119,859, median=95,517
- 2010 전국 합: 29,755,304 (KOSIS expected ~30M)

## Mortality + pop join
- pop matched: 30,298/31,494 (96.2%)
- mortality_rate non-null: 30,298
- mortality_rate stats: mean=39.8, median=36.7

- saved: `3_derived\mortality\sigungu_mortality_panel_v02_wa.parquet`
- final shape: (31494, 8)

## External validation: despair_total WA rate 전국
```
 year deaths pop rate_per_100k
 2008 13042 29212265.5 44.645630
 2009 14419 29510983.0 48.859775
 2010 14336 29755304.0 48.179646
 2011 14370 29975310.0 47.939454
 2012 13211 30114866.0 43.868699
 2013 13477 30211641.5 44.608632
 2014 13250 30331147.5 43.684467
 2015 12636 30455381.0 41.490205
 2016 12332 30629559.0 40.261762
 2017 12111 30787215.5 39.337757
 2018 12741 30902286.0 41.229959
 2019 12430 30998423.0 40.098814
 2020 12395 31010297.0 39.970594
 2021 12075 30975063.5 38.982971
 2022 11807 30876416.5 38.239541
```
- KOSIS suicide WA 2010 ≈ 32-35/100k (despair = +drug+psych+liver, 약간 더 높을 것)