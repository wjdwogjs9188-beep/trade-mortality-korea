# Phase 2-B Step 5b — Bartik IV build
_2026-05-05_

## baseline shares
- rows: 4,003, h_code: 226, KSIC9_2: 22
- denominator (E_h, 1994): 226 h_codes, mean=11367, median=4142

## HS6 → KIET3 → KSIC9_2 매핑 build
- HS6_to_KIET3 rows: 6,909, distinct HS6: 6909, distinct KIET3: 40
- KIET3 → KSIC9_2 mapping rows: 60 (after dedup)
- distinct KIET3: 60, distinct KSIC9_2: 42
- HS6 → KSIC9_2 combined: 6,314 rows, 6314 HS6, 23 KSIC9_2
- saved: `3_derived\bartik\hs6_to_ksic9_2digit.parquet`

## Comtrade ADH-8 aggregation (2000 vs 2010)
- ADH csv files: 201
- ADH aggregated rows: 41,526, countries: 8, years: [np.int64(2000), np.int64(2010)]
- ADH summed pivot rows: 5,292
- ADH HS6 매칭률: 4,852/5,292 (91.7%)
- ADH by KSIC9_2: 23
```
ksic9_2digit       M_2000       M_2010  dM_2000_2010
         C26 2.114231e+10 6.601133e+10  4.486902e+10
         C29 4.683628e+09 1.331249e+10  8.628860e+09
         C20 4.158712e+09 1.014142e+10  5.982709e+09
         C14 2.456772e+10 2.991845e+10  5.350726e+09
         C28 5.667689e+09 1.045744e+10  4.789754e+09
         C25 3.916131e+09 7.880958e+09  3.964827e+09
         C30 9.121248e+08 4.824466e+09  3.912341e+09
         C32 2.116470e+09 5.994357e+09  3.877887e+09
         C22 3.320758e+09 6.751997e+09  3.431239e+09
         C24 2.264027e+09 5.046155e+09  2.782128e+09
         C13 4.111452e+09 5.776073e+09  1.664621e+09
         C27 4.773413e+09 6.246569e+09  1.473156e+09
         C23 2.051849e+09 3.425997e+09  1.374148e+09
         C17 4.516240e+08 1.812478e+09  1.360854e+09
         C31 1.358225e+09 2.505128e+09  1.146902e+09
         C15 8.363111e+09 9.309503e+09  9.463919e+08
         C10 7.648100e+09 8.487807e+09  8.397075e+08
         C18 1.653352e+08 4.574859e+08  2.921507e+08
         C19 6.838167e+08 9.684259e+08  2.846091e+08
         C16 1.878192e+09 2.139929e+09  2.617370e+08
         C21 1.026808e+09 1.214712e+09  1.879037e+08
         C12 3.288542e+07 7.033267e+07  3.744725e+07
         C33 1.210165e+10 1.139216e+10 -7.094931e+08
```

## Comtrade KR-CN bilateral aggregation (2000 vs 2010)
- KR-CN by KSIC9_2: 23
```
ksic9_2digit       M_2000       M_2010  dM_2000_2010
         C26 2755400084.0 2.259254e+10  1.983714e+10
         C24 1232128211.0 8.138598e+09  6.906469e+09
         C20  748419498.0 5.132428e+09  4.384008e+09
         C28  946153357.0 5.162711e+09  4.216558e+09
         C25  150601890.0 3.289373e+09  3.138771e+09
         C29  215199287.0 2.979396e+09  2.764197e+09
         C30   65768981.0 2.220684e+09  2.154915e+09
         C14  900657047.0 2.929021e+09  2.028364e+09
         C23  177626423.0 1.990219e+09  1.812593e+09
         C31   49447126.0 1.745392e+09  1.695945e+09
         C10  810405182.0 2.412646e+09  1.602240e+09
         C27  147952406.0 1.426930e+09  1.278978e+09
         C15  298312840.0 1.435060e+09  1.136748e+09
         C13 1103087120.0 2.233801e+09  1.130714e+09
         C22   96944160.0 1.112238e+09  1.015294e+09
```

## Bartik IV: z_x_h = Σ_k s_{h,k} × ΔM_k / E_{h, 1994}

### ADH-8 IV summary
- h_code: 226, z_x mean=3990522925, sd=3863162098
- z_x_per_worker mean=1381684.1935, sd=2036146.2788
- top 5 most exposed: [{'h_code': '33390', 'z_x_per_worker': 16642083.010658046}, {'h_code': '23040', 'z_x_per_worker': 15232932.587082297}, {'h_code': '35330', 'z_x_per_worker': 8706114.332067637}, {'h_code': '37340', 'z_x_per_worker': 7564863.206986949}, {'h_code': '32340', 'z_x_per_worker': 7193528.002350901}]
- saved: `iv_z_x_adh8.parquet`

### KR-CN bilateral IV summary
- h_code: 226, z_x mean=2423886375, sd=1630743186
- z_x_per_worker mean=1148274.5189, sd=1683331.7434
- top 5 most exposed: [{'h_code': '37340', 'z_x_per_worker': 9773987.988992076}, {'h_code': '35330', 'z_x_per_worker': 9581133.999301447}, {'h_code': '33390', 'z_x_per_worker': 7759722.34412756}, {'h_code': '37330', 'z_x_per_worker': 7306760.401366429}, {'h_code': '32340', 'z_x_per_worker': 6963583.989245563}]
- saved: `iv_z_x_bilateral.parquet`

## 다음 step: 2-B.8 first-stage F + Test 3 final
- script 25 (first-stage F) — 이번에는 dry-run 아닌 실제 계산
- script 24 (Test 3) — Phase 2-A mortality panel build 후 실행 (cross-blocked)
- d5_log_employment_2000_2010 (LHS) — Phase 2-A 의존 (별도 turn)