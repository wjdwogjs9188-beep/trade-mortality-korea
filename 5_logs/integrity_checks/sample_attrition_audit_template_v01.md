# Phase A.1 Sample Attrition Table Cascade — Audit Log Template v01

**Date**: 2026-05-06
**Author**: R-A (audit-only mode)
**Plan**: Option (1) standardized β=-0.0685 main + 9-단계 cascade ground truth
**Cross-reference**: paper § 3.2 Table A (Sample Universe Cascade)
**Status**: R-A 측 verify 가능 정보 (sandbox) + 사용자 측 build log 필요 정보 분리 template

---

## 9-단계 cascade ground truth audit

| # | n | Transition + drop reason | R-A verify status | 사용자 build log 필요 정보 |
|---|---|--------------------------|-------------------|-------------------------|
| 1 | **256** | KOSIS 286 sigungu codes minus 30 supra-sigungu municipal aggregates → 256 h_codes (KOSTAT 2021 baseline) | ✅ **R-A verified**: `1_codebooks/sigungu_crosswalk.csv` 의 unique h_code = 256 (sandbox 직접 query) | (없음 — R-A verified) |
| 2 | **251** | 256 h_codes minus 5 with insufficient mortality panel coverage 1997-2023 | ⚠️ **R-A partial**: mortality panel 의 unique h_code = 256 (sandbox query). 즉 mortality panel 자체에는 256 모두 cover. 그러나 paper § 3.2 narrative 는 251 main. 즉 사용자 측 build 의 specific filter (long-difference 1997-1999 + 2018-2022 valid 양 시점 모두 non-NA?) 적용 결과 251 추출. R-A 가 sandbox 에서 reproduce 시 235 (5 outcome) 가 산출 — 251 과 mismatch | **사용자 측 build log 필요**: 어느 R/Python script 의 어느 line 에서 256 → 251 의 5 sigungu drop 발생? 5 sigungu list (h_code) + drop 이유 (each h_code 별) |
| 3 | **226** | 251 h_codes intersect 1994 KOSTAT industrial census coverage | ✅ **R-A verified**: `3_derived/bartik/baseline_shares_1994_ksic9_2digit.parquet` 의 unique h_code = 226 (sandbox 직접 query). 251 - 226 = 25 sigungu (1994 baseline 부재) | (없음 — R-A verified) |
| 4 | **226** | placebo (Section 6.1 Pre-WTO) — 226 sigungu given different pre-period sample availability | ⚠️ **R-A partial**: paper § 3.2 의 "226" 단계가 placebo sample 인지, 또는 main sample 의 intermediate 단계인지 paper § 3.2 narrative 와 사용자 build 의 정확한 매핑 필요 | **사용자 측 build log 필요**: 226 단계의 정확한 spec (main 1994-baseline coverage vs placebo Pre-WTO sample) |
| 5 | **222** | 226 minus 4 sigungu (insufficient 1994 census + crosswalk join failures) → main analytic sample | ⚠️ **R-A partial**: 226 - 222 = 4 sigungu drop. R-A sandbox 에서 어느 4 sigungu 인지 reconstruct 어려움 (사용자 측 long-difference build 의 specific filter). | **사용자 측 build log 필요**: 4 sigungu list + drop 이유 (insufficient census coverage / crosswalk join failure / both) |
| 6 | **218** | 222 minus 4 sigungu with sparse post-2008 mortality cells → § 5.4 sub-period | ⚠️ **R-A partial**: small-cell suppression criterion 정확 threshold 사용자 측 build 에 의존 | **사용자 측 build log 필요**: 4 sigungu list + suppression threshold (e.g., deaths < 5? cells > 80% missing?) |
| 7 | **215** | 251 minus 36 sigungu (insufficient 1992 baseline coverage, 1995-1997 administrative reorganization) → § 6.3 1992 baseline | ✅ **R-A verified**: `3_derived/bartik/baseline_shares_1992_ksic9_2digit_v2.parquet` 의 unique h_code = 215 (sandbox 직접 query). 251 - 215 = 36 sigungu | (없음 — R-A verified). 다만 *어느 36 sigungu* 인지 list 는 사용자 build 에 dependent |
| 8 | **210** | 215 minus 5 sigungu with zero 1992 manufacturing employment (e.g., h_code 35330 = 전라북도 무주군) | ⚠️ **R-A partial**: 35330 무주군 verified ✅. 나머지 4 sigungu list 사용자 측 build log 필요 | **사용자 측 build log 필요**: 5 sigungu list (35330 + 4 others) + 각 zero-employment 검증 |
| 9 | **206** | 210 minus 4 sigungu sparse 1992-baseline post-2008 cells | ⚠️ **R-A partial** | **사용자 측 build log 필요**: 4 sigungu list + suppression criterion |
| 10 | **198** | 222 main minus 24 sigungu sparse respiratory mortality cells → § 5.3 respiratory outcome | ⚠️ **R-A partial**: 222 - 198 = 24 sigungu drop. respiratory specific suppression 사용자 측 build 의존 | **사용자 측 build log 필요**: 24 sigungu list + respiratory suppression threshold |

---

## 새 native build sample 패턴 (Option (1) 채택 시 footnote 처리)

native build (Round 31) 의 sample 패턴이 기존 9 단계와 부분 mismatch:

| Native sample | 위치 | 9-단계 cascade 와의 차이 | R-A 권고 |
|--------------|------|------------------------|---------|
| **221** | 4 outcome (despair/cancer/cardio/external_other) of native build | 222 - 1 = 221 (1 sigungu drop) | 222 main + footnote: "External-package replication uses n=221 due to differing inner-join policy on long-difference panel build" |
| **219** | respiratory of native build | 198 + 21 = 219 (21 sigungu added) | 198 main + footnote: "External-package replication of respiratory outcome uses n=219 due to relaxed small-cell suppression threshold" |
| **210** native winsorized | 1992 baseline despair (winsorized) | 210 ✅ matches main cascade | 209 (winsorized) vs 210 (main): 1 sigungu winsorize-drop footnote |
| **209** | 1992 baseline 4 outcome (winsorized) | 210 - 1 = 209 | 작은 차이 footnote |
| **207** | 1992 baseline respiratory (winsorized) | 198 1992 base post-2008 = 206. 207 = 206 + 1 | 사용자 build log 필요 |

**R-A 권고 (audit 영역)**: 9-단계 main cascade 그대로 + native sample 패턴은 § 3.2 Table A 의 footnote (또는 별도 Table B "External-package robustness sample sizes") 로 분리 reporting.

---

## R-A 측 sandbox query 결과 정리 (verify 완료)

```
[R-A sandbox query 결과 — 2026-05-06]

Step 1 ✅ sigungu_crosswalk.csv unique h_code = 256
Step 3 ✅ baseline_shares_1994_ksic9_2digit.parquet unique h_code = 226
Step 7 ✅ baseline_shares_1992_ksic9_2digit_v2.parquet unique h_code = 215

Step 2 ⚠️ mortality panel raw unique h_code = 256 (256 → 251 의 5 sigungu drop 은 사용자 측 build filter)
Step 5 ⚠️ 226 → 222 의 4 sigungu drop list = 사용자 측 build log 필요
Step 6 ⚠️ 222 → 218 의 4 sigungu drop list = 사용자 측 build log 필요
Step 8 ⚠️ 215 → 210 의 5 sigungu (35330 verified, 4 others 필요)
Step 9 ⚠️ 210 → 206 의 4 sigungu drop list = 사용자 측 build log 필요
Step 10 ⚠️ 222 → 198 (respiratory) 24 sigungu drop list = 사용자 측 build log 필요
```

---

## 사용자 측 build log 필요 정보 list (총 6 transition)

R-A 가 audit log template 채우기 위해 사용자 측 R/Python build script 또는 console output 에서 추출 필요한 정보:

### 1. Step 2 (256 → 251)
- 어느 R script 또는 Python script 의 어느 line 에서 5 sigungu drop?
- 5 sigungu h_code list
- 각 drop 이유 (e.g., mortality 1997-2023 27 년 모두 NA / partial NA / population panel mismatch / 등)

### 2. Step 5 (226 → 222 main)
- 4 sigungu h_code list
- 각 drop 이유 (1994 baseline coverage / crosswalk join failure / additional filter)

### 3. Step 6 (222 → 218 post-2008 sub-period)
- 4 sigungu h_code list
- Small-cell suppression threshold (e.g., deaths < 5 in 2008 baseline?)

### 4. Step 8 (215 → 210 1992 main)
- 5 sigungu h_code list (35330 무주군 + 4 others)
- 각 zero-employment 또는 partial coverage 이유

### 5. Step 9 (210 → 206 1992 post-2008)
- 4 sigungu h_code list
- Suppression criterion

### 6. Step 10 (222 → 198 respiratory)
- 24 sigungu h_code list
- Respiratory specific suppression threshold

---

## Audit cycle continuation

사용자가 위 6 transition 의 build log 정보 추출 후 paste 또는 별도 file 로 R-A 에 제공 → R-A 가:

(a) 9-단계 cascade 의 ground truth 완성 (R-A verified + 사용자 build log 통합)
(b) paper § 3.2 Table A 의 row-by-row narrative audit
(c) Native sample (221, 219) footnote 의 정합 audit
(d) paper 본문 모든 "n=221" 또는 "n=222" reference 가 cascade 와 정합한지 grep verify

R-A 는 paper 본문 update 안 함. (a)-(d) 의 audit 결과만 산출 → 사용자가 paper 본문 commit.
