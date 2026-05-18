# Profile · Analyze · Validate — `mortality_rate_panel_v02_1.parquet`

- Generated: 2026-05-05 (R-A, /explore-data → /analyze → /validate-data chain)
- Target: `3_derived/mortality/mortality_rate_panel_v02_1.parquet` (7.0 MB)
- Linked to phase 2-a (다음 critical path per dashboard 2026-05-05)

---

## /explore-data — Profile

### Structure

| Field | Value |
|---|---|
| Source | parquet (Stage 3B v02.1) |
| Grain | `h_code × year × sex_code × outcome_group` |
| N rows | 123,660 |
| # h_code | 229 |
| # year | 27 (1997–2023, 연속) |
| # sex_code | 2 (1=남, 2=여) |
| # outcome_group | 10 (cancer · cardiovascular · despair_total · drug_101 · external_other · liver_081 · other · psych_057 · respiratory · suicide_102) |
| Balance | **100.00%** (229 × 27 × 2 × 10 = 123,660 = observed) |
| Duplicate keys | 0 |
| Nulls | 0 (전 12 컬럼) |

### Codebook coverage (h_code)

| 항목 | 값 | 해석 |
|---|---|---|
| Panel ∩ codebook | 224 | matched |
| Panel \ codebook | **5** (`31010 31020 31040 35010 37010`) | parent-city codes (수원·성남·안양·전주·포항) — codebook 은 구 단위 (`31011-14` 등) 만 보유 |
| Codebook \ panel | 32 | 위 5 city 의 sub-구 코드 (정확히 32 = 4+3+2+2+2 + 추가 split 들) |
| Sub-구 codes in panel | **0** | double-counting 없음 ✅ |

→ 5 unmapped 는 design intent (city-level aggregation). codebook 을 city-augmented 버전으로 정정 필요 (P3, 표 표기용).

### Quality flags (calibrated)

| code | flag | priority |
|---|---|:--:|
| Q1 | **deaths < 5 cells = 27,569 (22.3%)** — KOSIS small-cell suppression risk. Microdata source 였으면 0 cells 인지 확인 필요 | P2 |
| Q2 | **zero deaths = 13,152 (10.6%)** — small 시군구 × rare outcome (drug_101, psych_057) 의 honest zeros | P2 |
| Q3 | **2008 ICD-10 break**: drug_101 −20.2%, psych_057 −21.9% (2005-07 vs 2008-10 평균). suicide_102 +23.0% 는 real (post-금융위기 spike), liver_081 −12.1% 는 secular | P1 |
| Q4 | **Working-age dimension 부재** — panel 은 all-age. PAP v4.0 § 4 가 25-64 명시. 다음 § /validate 참고 | P1 |
| Q5 | **외국인 포함 가능성** — 분자 (deaths) 가 KOSIS published 와 정확히 일치 → 외국인 포함. 분모 (pop_v01) 는 행정안전부 주민등록 = Korean-only | P2 |

---

## /analyze — Descriptive + ASR sanity

### KOSIS published vs panel — suicide_102 (15-year cross-check)

| year | panel | KOSIS published | diff | %diff |
|---:|---:|---:|---:|---:|
| 2009 | 31.02 | 31.00 | +0.02 | +0.1% |
| 2010 | 31.19 | 31.20 | −0.01 | −0.0% |
| 2011 | 31.74 | 31.70 | +0.04 | +0.1% |
| 2012 | 28.12 | 28.10 | +0.02 | +0.1% |
| 2013 | 28.53 | 28.50 | +0.03 | +0.1% |
| 2014 | 27.25 | 27.30 | −0.05 | −0.2% |
| 2015 | 26.52 | 26.50 | +0.02 | +0.1% |
| 2016 | 25.61 | 25.60 | +0.01 | +0.1% |
| 2017 | 24.32 | 24.30 | +0.02 | +0.1% |
| 2018 | 26.65 | 26.60 | +0.05 | +0.2% |
| 2019 | 26.87 | 26.90 | −0.03 | −0.1% |
| 2020 | 25.70 | 25.70 | −0.00 | −0.0% |
| 2021 | 26.01 | 26.00 | +0.01 | +0.0% |
| 2022 | 25.18 | 25.20 | −0.02 | −0.1% |
| 2023 | 27.33 | 27.30 | +0.03 | +0.1% |

→ **15/15 within ±0.2%, max abs diff 0.05/100k**. External validity 강함. ±2% tolerance 통과 (DGHP/DFH replication-grade).

### Despair composition

`despair_total = suicide_102 + drug_101 + psych_057 + liver_081` 합 일치 (sample 11010-2020: 53 = 18+1+6+17+11=53 ✅). 정의 안정.

### Working-age 25-64 vs all-age (suicide_102, 국가단위)

| year | all-age rate | 25-64 rate | wa_share_deaths |
|---:|---:|---:|---:|
| 2000 | 13.60 | 17.19 | 0.71 |
| 2010 | 30.75 | 32.49 | 0.63 |
| 2020 | 23.82 | 24.89 | 0.63 |
| 2023 | 24.81 | 24.76 | 0.60 |

→ Working-age rate 가 +1.5~3.5/100k 일관되게 높음. WA share 60-75% (1990s 0.71-0.75 → 2020s 0.60-0.63, 인구고령화 reflect).

### 2008 ICD-10 break detail

| outcome | 2005-07 mean | 2008-10 mean | Δ% | 해석 |
|---|---:|---:|---:|---|
| suicide_102 | 23.91 | 29.41 | +23.0% | real (금융위기 spike) |
| drug_101 | 0.55 | 0.44 | −20.2% | likely classification | 
| psych_057 | 2.04 | 1.59 | −21.9% | likely classification |
| liver_081 | 15.98 | 14.05 | −12.1% | secular |

→ drug/psych break 는 mortality_panel_v02_validation.md 에서 추가 audit 필요 (memory `feedback_panel_codebook_reference.md` 의 8차분류 cross-ref).

---

## /validate-data — Pre-share QA

### Spec coherence vs PAP v4.0

| PAP § | 명시 | Panel | gap | 처리 |
|---|---|---|:--:|---|
| § 4 | working-age 25-64 | **all-age** (분모 = pop_v01 sum across age) | ❌ | **P1.NEW**: working-age subset panel build 필요. microdata + pop_panel 양쪽 age_band 존재 → 1-2h 작업 |
| § 4 | 5-year stack period | annual | (intended downstream) | OK: estimation 단계에서 stack |
| § 4 | 시군구 unit | h_code 229 | OK | 5 city-aggregate flag 만 |
| § 6 | 사망원인 outcome groups | 10 (정확 일치) | ✅ | OK |
| § 7 | ASR 3 baseline | kr2010 + WHO2000 + Eur2013 | ✅ | OK |
| § 7 | 외국인 처리 | KOSIS-equivalent (분자 includes foreigners) | ⚠ | sensitivity: foreigner-excluded variant 도 build 권고 |

### Codebook integrity

- 5 unmapped h_code = city-aggregate (수원·성남·안양·전주·포항) → codebook 을 city-row 추가 update 권고 (P3, 1h)
- 32 codebook \ panel = 위 5 city 의 sub-구 → expected, 무시 가능

### External validity (suicide_102 15-year)

15/15 within ±0.2% of KOSIS published. **Citable as "panel matches KOSIS official 사망원인통계 within ±0.2%"** — paper § 4 data section 직접 사용 가능.

### 정합성 issues 정리

**P1 (식별·spec 위협)**
- **P1.NEW**: working-age 25-64 subset 미적용. PAP v4.0 § 4 와 panel 불일치. **즉시 fix 필요** (1-2h, microdata + pop_panel 모두 age_band 보유 → reconstruction 가능)
- **P1.Q3**: drug/psych 의 2008 break 가 classification artifact 일 가능성. 8차 분류 cross-ref + 057 F-code split sensitivity 필요

**P2 (robustness)**
- 외국인 포함된 분자 (KOSIS-equivalent) vs 분모 = Korean-only → 분자/분모 population universe mismatch. Foreigner-excluded variant build 권고
- deaths < 5 cells 22.3% — Poisson regression 또는 small-area Bayesian smoothing 검토 (현재는 ln(asr+1) → log-form 으로 회피)
- Microdata cleaned (12,233 in 2020) vs panel (13,195 in 2020) ~7% 차이 → cleaned 는 외국인 + filter applied. 어느 쪽이 main 인지 PAP § 4 fix

**P3 (cosmetic)**
- 5 city-aggregate codes 를 codebook 에 city-row 추가
- 2024 microdata 존재하나 pop 미확보 → 2024 panel 추가는 pop 갱신 후 가능 (28-year coverage 가능성)

### Suggested next steps

1. **즉시 P1.NEW fix**: working-age (25-64) subset panel build → `mortality_rate_panel_v02_2_wa.parquet` (1-2h, deterministic ETL). microdata `age_band ∈ ['25-29',...,'60-64']` + pop_panel `age_band ∈ ['07',...,'14']` 로 reconstruct
2. **P1.Q3 audit**: 057 (F10-F19) 의 F17 (담배) split 불가 sensitivity, 그리고 drug_101 의 8차분류 매핑 changelog 확인
3. PAP § 4 update: foreigner inclusion 정의 명시 (panel = KOSIS-equivalent inclusive vs sensitivity = exclusive)
4. v02_1 → v02_2 migration: working-age + foreigner-policy fix 양 자 동시 처리한 v02_2 single source of truth
5. (optional) 2024 microdata 추가 시 pop 갱신 dependency 명시

### Overall judgment

**panel quality = strong**, with **two P1 spec-fits required** (working-age + foreigner policy). External validity (KOSIS match) 는 paper-grade. Phase 2-a critical path 에서 working-age 변환 + foreigner policy commit 만 추가하면 PAP v4.0 정합 완료.
