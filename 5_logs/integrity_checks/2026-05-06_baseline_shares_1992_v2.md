# 1992 광업제조업조사 baseline shares build (v2)
_2026-05-06_

## v1 → v2 변경 사항
| Bug (v1) | Fix (v2) |
|----------|----------|
| col 2 'D' filter rows = 0 | col 2 'D' filter 정확히 작동 (97.8%) |
| col 14 (자영업주_월평균만 사용) | col 30 (종사자수합계_월평균) 사용 |
| 시군구 코드 결합 누락 | col 0 (시도) + col 1 (구시군) = 5-digit 결합 |
| KSIC 6→9 crosswalk 시도 (file 부재 오인) | 1_codebooks/ksic6_to_ksic9_2digit.csv 사용, 100% match |

## Schema audit
- raw rows: **76,357**
- D filter rows: **74,679** (97.8%)
- 시군구 5-digit distinct: **274**
- KSIC 6차 2-digit distinct: **23** (D + 23 codes)
- KSIC 9차 2-digit distinct (after crosswalk): **22**
- 종사자 합계 (D, col 30): **2,529,671**
 - 1992 한국통계연감 anchor: 약 250-280 만 → **정합** ✅

## Sigungu crosswalk match
- (h × k) match rate: **85.3%**
- denominator match rate: **81.3%**
- (h_code × k) final cells: **3,237**
- h_code distinct: **215**

### Unmatched top 15 (sigungu5 → 1997 h_code)
- 31430: 42,757 workers
- 38032: 30,450 workers
- 31450: 30,299 workers
- 37010: 27,997 workers
- 31420: 26,016 workers
- 38023: 18,461 workers
- 34450: 14,806 workers
- 31100: 12,989 workers
- 34440: 10,873 workers
- 36490: 8,240 workers
- 31440: 7,717 workers
- 38410: 5,979 workers
- 37450: 4,666 workers
- 35430: 4,075 workers
- 34410: 3,631 workers

## Output
- shares: `3_derived/bartik/baseline_shares_1992_ksic9_2digit_v2.parquet`
- denominator: `3_derived/bartik/denominator_E_h_1992_v2.parquet`

## Sample shares (top 10 h × k by share)
h_code ksic9_2digit E_hk_1992 E_h_1992 share_hk_1992
 31110 18 156.0 156.0 1.000000
 32350 23 846.0 846.0 1.000000
 32390 23 34.0 34.0 1.000000
 32400 23 54.0 54.0 1.000000
 33390 23 895.0 895.0 1.000000
 35370 10 329.0 329.0 1.000000
 37350 23 58.0 58.0 1.000000
 37360 23 286.0 286.0 1.000000
 38100 31 12981.0 12999.0 0.998615
 34370 23 882.0 932.0 0.946352

## Anchor
- ADH (2013): per-worker baseline shares 표준 spec
- BHJ (2025): shift-share IV identification
- Sufi (2023 BFI): 한국 trade-empirical 의 KIET 60-sector 매개