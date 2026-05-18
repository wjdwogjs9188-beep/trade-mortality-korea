# Phase 2-B Step 2 — Baseline shares 1994 build
_2026-05-05_

- raw rows: **2,518,454**
- sigungu match (1997 baseline): **2,396,419/2,518,454** (95.2%)
- 미매칭 raw_code distinct: 19
- 미매칭 top 10 raw_code: {'38031': 17821, '38032': 14429, '31100': 14295, '31420': 10221, '31410': 7771, '38023': 6851, '22080': 6188, '38024': 5942, '31430': 5939, '31440': 5729}
- after drop unmatched: 2,396,419

## Manufacturing (D) 만
- rows: **280,865** (전체의 11.7%)

## Cross-check: 종사자 컬럼 후보별 전국 sum
- emp_c14 전국 합 (D only): 2,568,889
- emp_c11 전국 합 (D only): 2,228,068
- *cross-check anchor*: 1995 한국통계연감 제조업 종사자 ≈ 2,900,000

- agg rows (h_code × KSIC4): 9,739
- distinct h_code: 226
- distinct KSIC4: 70
- share NaN rows: 0 (h_total=0 시군구)

- saved: `3_derived\bartik\baseline_shares_1994_manufacturing.parquet`
- saved: `3_derived\bartik\baseline_shares_1994_all_industries.parquet`
- all-industry rows: 29,329, distinct KSIC4: 188

## Top 20 KSIC4 (제조업, 종사자 sum)
```
ksic4 emp_c14
 D181 266198.0
 D289 128060.0
 D343 110992.0
 D291 109549.0
 D293 105813.0
 D281 96342.0
 D369 88933.0
 D252 87986.0
 D323 85426.0
 D154 85190.0
 D151 76383.0
 D172 74940.0
 D222 68915.0
 D179 68592.0
 D193 64425.0
 D174 62341.0
 D321 59858.0
 D271 58950.0
 D221 49126.0
 D361 49001.0
```

## 시도별 제조업 종사자 (cross-check with 1995 통계연감)
```
sido
11 647198.0
31 545070.0
38 255778.0
21 247829.0
23 207613.0
37 177333.0
22 168908.0
36 63369.0
35 53410.0
33 51441.0
34 47550.0
24 37910.0
25 32512.0
32 27321.0
39 5647.0
```
- 전국 합 (D only, col 14): **2,568,889**

## 결정 사항
- ✅ **col 14 = 종사자 수 확정** (전국 합 2,568,889 ≈ 1995 통계연감 290만)