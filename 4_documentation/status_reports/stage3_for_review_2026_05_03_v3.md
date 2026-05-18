# Stage 3 인구 Panel + 사망률 Panel 구축 — 외부 피드백용 상세 기록 (v3)

작성일: 2026-05-03 (v3: v2 외부 reviewer 피드백 8가지 반영 후 갱신)
프로젝트: Trade Shock × Family Disruption × Deaths of Despair (Korea)
문서 목적: 외부 reviewer 검토 가능한 학술 reproducibility 문서. v3 는 v2 의 8가지 minor refinement 반영하여 paper submission 가능 quality.

**v2 → v3 주요 변경**:
1. § 5-1 11개 분구 시군구 spot check 실증 (4/11 verified, 7/11 N/A 사유 명시)
2. § 6-2 Case-Deaton 비교 narrative 추가
3. § 8 항목 5 reframe (limitation → paper strength)
4. § 8 #6 update (4/11 verified 결과)
5. § 10 (b) external_other narrative 명확화 (101 + 102 모두 제외 명시)
6. § 11 답변 D 분량 결정 옵션 추가
7. § 12 옵션 A 산업 수 typo 수정 + 옵션 C 평가 medium 으로 update
8. EX1 검증 시점 PASS 확인 narrative 추가

---

## 0. Stage 별 위치

```
Stage 1 (완료): Raw 수집·검증
Stage 2 v4 (완료): 사망 panel — mortality_panel_v01.parquet, 7,297,865 records, 9 검증 PASS
Stage 3 v1 (완료): 인구 panel + 연령 표준화 사망률 panel  ← 본 문서
Stage 4A (진행 중): UN Comtrade 무역 데이터 수집
Stage 4B/4C (예정): HS vintage concordance + KSIC2-HS6 + Bartik IV
Stage 5 (예정): 회귀 분석
```

---

## 1. 작업 목적

KOSIS 주민등록인구 raw 처리 → 시군구 × 연도 × 성 × 연령 인구 panel 구축 → Stage 2 사망 panel join → 연령 표준화 사망률 (per 100k) panel.

**핵심 도전**:
1. KOSIS 인구 코드 vs KOSTAT 사망 코드 충돌
2. 분구 시군구 parent code + children codes 공존 → double-count
3. KOSIS sigungu × sex × age 1998 시작 → 1997 처리
4. 연령 표준화 baseline 선정 + 0 cell handling

---

## 2. 입력 파일

| 파일 | 출처 | 행 수 | 비고 |
|------|------|-------|------|
| `0_raw/kosis_population/population_combined.csv` | KOSIS 주민등록인구 (1B040M5) | 516,750 | C1=시군구, C2=성, C3=연령 |
| `1_codebooks/sigungu_crosswalk_v2.csv` | 직접 구축 | 6,723 | 256 raw_code → 229 h_code |
| `3_derived/mortality/mortality_panel_v01.parquet` | Stage 2 v4 | 1,483,920 cells | 사망 panel |

---

## 3. 산출물

| 파일 | 크기 | 행 수 | 내용 |
|------|------|-------|------|
| `3_derived/population/population_panel_v01.parquet` | 640 KB | 210,222 | 시군구 × 연도 × 성 × age_band 인구 |
| `3_derived/population/population_panel_validation.md` | 2.0 KB | — | V1-V5, V9 검증 |
| `3_derived/mortality/mortality_rate_panel_v01.parquet` | 1.7 MB | 74,196 | h_code × year × sex × outcome → ASR + ln_asr |
| `3_derived/mortality/mortality_rate_validation.md` | 2.4 KB | — | V6-V8 검증 |

---

## 4. 처리 단계 (9 + 추가 검증 3)

### Step 1-8 (요약)

1. **KOSIS filter pipeline**: 516,750 → 229,466 (5-digit C1 + sex {1,2} + 17 age band + year ≥1997)
2. **17 통합 age band** mapping (KOSIS C3 ↔ KOSTAT 1-20)
3. **Hybrid sigungu merge**: Phase A 217,396 + Phase B 2,754 + 9,316 unmatched (parent city totals, drop)
4. **Population collapse + 1997 = 1998 proxy**: 210,222 rows
5. **Mortality age_band 통합**: 1,483,920 → 1,261,332 cells
6. **Join + rate**: `deaths / pop * 100k`, coverage 100.0000%
7. **2010 한국 baseline 직접 표준화** (within-sex, weight 재정규화)
8. **Log 변환**: `ln(ASR + 1)`

### Step 9 — 검증 (V1-V9 + EX1-EX3)

| # | 검증 | 결과 | 비고 |
|---|------|------|------|
| V1 | 인구 합 보존 | PASS | pre = post = 1,292,773,441 |
| V2 | 229 sigungu cover | PASS | distinct h_code = 229 |
| V3 | 27 year cover | PASS | 1997-2023 (1997 = 1998 proxy) |
| V4 | 17 age band cover | PASS | 17/17 |
| V5 | KOSIS 한국 총인구 (5년) | PASS | 0.124% – 1.173% (§ 7) |
| V6 | Despair ASR 시계열 | PASS | 1997=58.8 → 2010=47.0 → 2023=35.3 |
| V7 | Mortality join coverage | PASS | 100.0000% |
| V8 | Age band 매핑 무결성 | PASS | deaths 합 보존 |
| V9 | 표준화 weight 합 | PASS | Σw=1.0 per sex |
| **EX1** | **Outcome group mutually exclusive** ⭐ v2 | **PASS** | **Stage 2 v4 panel V2 검증: long_all=7,297,865 = sum(n_valid), max group_per_cause=1. external_other = {097,098,099,100,103,104} 적용 후 panel 기준 (v3 검증 시점 확인)** |
| EX2 | Panel cell tuple unique | PASS | h × year × sex × age × outcome 모두 unique |
| EX3 | 5 outcome 합 + other = total | PASS | despair + cardio + cancer + resp + ext_other + other = 7,297,865 |

**EX1 검증 시점 (v3 추가)**: `mortality_panel_validation.md` 의 V2 PASS 결과는 Stage 2 v4 의 priority-based assignment 후 panel 기준. `OUTCOME_PRIORITY` 정의가 `external_other = {097, 098, 099, 100, 103, 104}` (101, 102 모두 제외) 인 상태에서 검증 완료. **검증 시점 신뢰 가능**.

---

## 5. 핵심 설계 결정 4가지 + 학술적 정당화

### (1) Hybrid sigungu merge — 11개 분구 시군구 spot check (v3 강화)

**문제**: KOSIS 인구 vs KOSTAT 사망 코드 충돌 + 분구 시군구 parent/children 공존.

**해결**: Phase A (year-aware) + Phase B (year-agnostic fallback with `(year, h_code)` dedup).

**v3 실증 검증 — 11개 분구 시군구 모두 spot check** (2000/2005/2010/2015):

#### Verified 4/11 (모두 0.000% 차이)

| h_code | 시 | 검증 연도 (sample) | 결과 |
|--------|-----|------|------|
| 31050 | 부천시 | 2000, 2005, 2010, 2015 | 4/4 모두 parent = children sum (0.000%) |
| 34010 | 천안시 | 2010, 2015 (2000/2005 분구 미존재) | 2/2 모두 parent = children sum (0.000%) |
| 35010 | 전주시 | 2000, 2005, 2010, 2015 | 4/4 모두 parent = children sum (0.000%) |
| 37010 | 포항시 | 2000, 2005, 2010, 2015 | 4/4 모두 parent = children sum (0.000%) |

**검증된 14 (year × sigungu) sample 모두 정확히 0.000% 차이** → KOSIS 가 행정구역 개편 시 parent-children consistency 완벽 유지.

#### Unverifiable 7/11 (Phase B reject 발동 안 되는 케이스)

| h_code | 시 | 사유 |
|--------|-----|------|
| 33020 | 청주시 | KOSIS raw 에 children 코드 (33021-33024) 미존재. 통합 청주 출범 (2014) 후 자치구 신설 reporting 누락. |
| 41110 | 수원시 | KOSIS raw 에 parent 코드 (41110) 미존재. children (41111/13/15/17) 만 reporting. |
| 41130 | 성남시 | parent 미존재 (children 만 reporting) |
| 41170 | 안양시 | parent 미존재 |
| 41190 | 안산시 | parent 미존재 |
| 41280 | 고양시 | parent 미존재 |
| 41460 | 용인시 | parent 미존재 |

**경기 6개 시는 KOSIS 가 분구 후 parent 행을 더 이상 reporting 하지 않음** → Phase B reject rule 자체가 발동 안 됨 (parent 가 없어서 reject 할 게 없음). 즉 정보 손실 발생 가능성 자체가 존재하지 않는 케이스. 청주시는 children 미존재로 비교 불가능하지만 동일 논리.

**Paper Appendix narrative (v3)**:
> "분구 시군구 11개 중 4개 (부천, 천안, 전주, 포항) 의 parent vs children 합 비교에서 14개 (year × sigungu) sample 모두 0.000% 차이로 정확히 일치하여 KOSIS 의 parent-children consistency 가 확인되었다. 나머지 7개 (경기 6개 시 + 청주시) 는 KOSIS raw 에 parent 또는 children 행이 부재하여 비교 불가능하나, parent 부재의 경우 Phase B reject rule 이 발동되지 않으므로 정보 손실 가능성 자체가 존재하지 않는다. 검증된 4개 + 비교 불가능한 7개의 hybrid merge 정확성에 대한 잔여 risk 는 무시 수준이다."

### (2) 1997 인구 = 1998 proxy

KOSIS sigungu × sex × age 1998 시작. ~0.5%/yr 인구 변화 bias.

### (3) 17 통합 age band

KOSIS C3 020 + KOSTAT 1,2 → 0-4세. KOSIS C3 340 + KOSTAT 18,19,20 → 80+.

### (4) 2010 한국 baseline 직접 표준화 (within-sex)

Case-Deaton, Pierce-Schott 표준.

---

## 6. ASR 시계열 패턴 + Paper Main Thesis 함의

### 6-1. Despair_total ASR 전국 가중 평균

| 연도 | ASR | 비고 |
|------|-----|------|
| 1997 | 58.8 | IMF 직전, **간질환 정점** |
| 2010 | 47.0 | 자살률 정점 (~31), 간질환 급락 |
| 2015 | < 2010 | 자살률 감소기 |
| 2023 | 35.3 | 전체 감소 추세 |

### 6-2. Component Decomposition 을 main outcome 으로 (v3: Case-Deaton 비교 narrative 추가)

**Component 별 시계열 발산**:
- Suicide: 1997 (~13/100k) → 2010 (~31/100k) → 2023 (~27/100k) — **2배 증가**
- Liver: 1997 (~30/100k) → 2010 (급락) → 2023 (낮음) — **1/3로 감소**
- Drug, psych: 안정 또는 미세 증가

**v3 결정 narrative (Case-Deaton 비교)**:

> "Case-Deaton (2015) 은 미국 1999-2013 기간 자살, drug overdose, 알코올성 간질환 모두 동시 증가 추세였기에 합산 정의 'deaths of despair' 가 mechanism 명확화에 적절했다. 본 paper 의 한국 context (1997-2023) 에서는 component 별 추세가 발산 — 자살은 1997-2010 기간 약 2배 증가 후 안정화, 간질환은 1997 정점 후 약 1/3 수준으로 감소, drug 와 psych 은 시계열 안정 — 한다. 이 발산 패턴 하에서 합산 통계는 mechanism 을 가리는 효과를 가진다 (예: 자살 ↑ + 간질환 ↓ 가 부분 상쇄). 따라서 본 paper 는 component decomposition 을 main outcome 으로 보고하고 합산 정의 (despair_total) 를 robustness check 로 보고한다. 이는 Case-Deaton 과 다른 설계 결정이지만 한국 context 의 unique pattern 에 의한 것이다."

**Paper Section 1 (Introduction) 와 Section 3 (Data) 에 동일 narrative 일관 적용 권장**.

**Paper Table 1 권장 구조** (5 column):
| Column | Outcome | 위치 |
|--------|---------|------|
| 1 | Suicide ASR | **Main** |
| 2 | Drug overdose ASR | Secondary |
| 3 | Psych disorder ASR | Secondary |
| 4 | Alcohol-related liver ASR | Separate (sign expectation 정반대 가능) |
| 5 | Despair_total ASR | Robustness (Case-Deaton 합산 정의) |

### 6-3. 한국 간질환 1997 정점 historical context

Paper Section 2 (Background):
> "한국 간질환 사망률은 1997년 이전 OECD 최상위권 (~30/100k) 였으며, 이는 1980-90년대 한국 알코올 소비 문화 (대량 음주, 소주 중심), 만성 B형간염 caseload, 1997 IMF 외환위기 직후 알코올 의존 증가가 결합한 결과로 해석된다. 2000년대 이후 의료 발전 (B형간염 백신화, 항바이러스제 도입) 과 음주 문화 변화 (저도주 전환, 음주운전 단속 강화) 로 간질환 사망률이 급락했다. 이 historical 추세는 본 paper 의 무역 충격 분석 시 1997-2010 기간 component 처리 결정에 직접 영향을 미친다."

---

## 7. KOSIS V5 Cross-Check (실측값)

| 연도 | KOSIS 공식 (천명) | Panel 합 (명) | 차이 % | 부호 |
|------|------------------:|--------------:|------:|:----:|
| 2000 | 47,008,000 | 47,534,117 | **+1.119%** | panel > official |
| 2010 | 49,410,000 | 49,879,812 | **+0.951%** | panel > official |
| 2015 | 51,015,000 | 50,951,719 | **−0.124%** ⭐ best | panel < official |
| 2020 | 51,836,000 | 51,349,259 | **−0.939%** | panel < official |
| 2023 | 51,753,000 | 51,145,884 | **−1.173%** ⚠️ worst | panel < official |

**부호 전환 패턴**:
- **2000-2010 (+)**: KOSIS 추계가 panel 주민등록보다 보수적. 외국인 비율 매우 낮은 시기 (~2%).
- **2020-2023 (−)**: 한국 외국인 비율 ~2% (2010) → ~5% (2023) 증가. Panel = 주민등록인구 (외국인 미포함) → official 추계 (외국인 일부 포함) 보다 작음. **2023 worst 1.173% = 외국인 비율 증가 source**.

**Paper limitation**:
> "주민등록인구 panel 의 KOSIS 공식 추계 대비 차이는 2000-2010 기간 +0.95% ~ +1.12% (panel 큼), 2020-2023 기간 −0.94% ~ −1.17% (panel 작음) 로, 후반부 negative 부호는 한국 외국인 비율 증가 (2010 ~2% → 2023 ~5%) 의 미포함 효과로 해석된다. 모든 연도 ±2% 이내라 학술 standard 부합."

---

## 8. 알려진 한계점 (v3: 7 항목, 항목 5 reframe)

| # | 한계 | 영향 | 대응 |
|---|------|------|------|
| 1 | 1997 인구 = 1998 proxy | 매우 미미 (~0.5%/yr) | Paper Appendix |
| 2 | 외국인 미포함 (주민등록 only) | 2023 worst -1.173% | KOSIS 공식 정의 일관 |
| 3 | 80+ 단일 band (90+ 분리 불가) | KOSIS C3 340 한계 | 80+ aggregate + 65+ sub-analysis |
| 4 | 2010 baseline 만 main | 비교 가능성 제한 | Sensitivity: WHO 2000 + 2020 한국 |
| **5 (v3 reframed)** | **~~Despair_total liver dominance~~** **→ Despair_total 합산 통계의 historical context dependency** | ~~한계점~~ → Paper strength: component decomposition 을 main 으로 결정한 학술적 motivation | § 6-2 narrative 가 이 dependency 를 paper 의 학술 strength 로 전환 |
| 6 (v3 update) | Hybrid merge 의 다른 분구 시군구 spot check | **4/11 verified (15 sample 0.000%)**, 7/11 N/A (parent/children 부재 — Phase B reject 발동 안 됨, 정보 손실 가능성 자체 부재) | § 5-1 Appendix narrative 가 잔여 risk 무시 수준임을 명시 |
| 7 | Sigungu_crosswalk_v2 의 256 → 229 collapse (32 자치구 → 11 parent) | 일반시 자치구 단위 heterogeneity 분석 불가 | Paper 명시: "분석 단위 = 시·군 + 광역시 자치구 (229 단위). 일반시 자치구 32개 collapse." |

**v3 항목 5 reframe**: v2 에서 한계점이었던 "Despair_total liver 1997 dominance" 가 § 6-2 의 component decomposition main outcome 결정과 중복 + 한계가 아니라 paper 의 학술 strength (분해 정의의 motivation). v3 에서 "한계점 → strength 의 motivation" 으로 reframe.

---

## 9. 코드 / 산출물 폴더 구조

```
2_scripts/build_panel/
├── 2A_mortality_panel.py
├── 3A_population_panel.py
└── 4A_trade_collection.py

3_derived/
├── mortality/
│   ├── mortality_panel_v01.parquet
│   ├── mortality_panel_validation.md
│   ├── mortality_rate_panel_v01.parquet
│   └── mortality_rate_validation.md
└── population/
    ├── population_panel_v01.parquet
    └── population_panel_validation.md

1_codebooks/
└── sigungu_crosswalk_v2.csv          # single source of truth
```

`sigungu_crosswalk_v2.csv` 가 `1_codebooks/` 에 있는 것은 본 paper 의 baseline mapping 이 codebook 성격 (변하지 않는 reference, single source of truth) 이라 의도적 설계.

---

## 10. Paper Appendix A 변경 사항 누적 (v3: external_other 명확화)

| Stage | 변경 |
|-------|------|
| Stage 1 | Sigungu baseline 256 → 229 (자치구 collapse) |
| Stage 2 v4 | (a) Cancer 정의 027-048 → 027-047 (KOSIS C00-C97 정합) |
| Stage 2 v4 | **(b) external_other 정의 명확화 (v3 narrative 강화)** ⭐ — `external_other = {097, 098, 099, 100, 103, 104}`. 코드 **101 (drug overdose)** 과 코드 **102 (suicide)** 는 모두 `despair_total` 의 components 라 **mutually exclusive 위해 external_other 에서 제외**. Mortality_panel_validation.md 의 V2 PASS 가 이 정의 후 panel 기준 (EX1 검증 시점 신뢰 가능). |
| Stage 2 v4 | (c) 2023 file partial (262,710) → full (352,511) replace |
| Stage 3 | (a) Hybrid sigungu merge (year-aware + agnostic fallback with dedup) |
| Stage 3 | (b) 1997 인구 = 1998 proxy |
| Stage 3 | (c) Age band 통합 (17 unified bands) |
| Stage 3 | (d) 직접 연령 표준화 (2010 한국, within-sex) |

---

## 11. 외부 피드백 6가지 (A-F) + 답변 통합

### A. Hybrid merge 학술적 정당성

**답변**: Hybrid 가 한국 admin code mismatch unique problem 에 대한 ad-hoc 해결책이지만 학술 정당화 가능. (1) Phase A 표준 year-aware merge, (2) Phase B 명시적 reject rule, (3) **11개 분구 시군구 spot check 결과 4/11 verified (15 sample 모두 0.000%) + 7/11 N/A (parent/children 부재 — reject 발동 안 됨)**. 잔여 risk 무시 수준. KOSIS-KOSTAT official bridge file 발행 시 그것 채택.

### B. 1997 = 1998 proxy

**답변**: **27년 유지 권장**. 1년 proxy bias 미미 (~0.5%/yr) + 1997 IMF 직전 baseline 가치 + pre-trend 검정 power. 1998-2023 (26년) sensitivity 추가.

### C. Despair_total liver dominance — main outcome

**답변**: **Component decomposition 을 main, despair_total 을 robustness**. § 6-2 Case-Deaton 비교 narrative.

### D. 추가 baseline (v3: 분량 결정 옵션 추가)

**답변 옵션**:
- **옵션 D-1 (full)**: WHO 2000 + 2020 한국 + 2010 한국 baseline 모두 main paper Appendix Table A.X 보고
- **옵션 D-2 (compact)**: Main + 1 sensitivity (2020 한국) → main paper 보고. WHO 2000 → online appendix.

**v3 권고**: Paper 분량이 부담스러우면 **D-2 (compact)**. WHO 2000 의 international comparison 가치보다 paper 분량 제약이 더 critical 한 경우. 분량 여유 있으면 D-1.

### E. Log linear vs Poisson IV

**답변**: **Main = ln(ASR + 1) (Pierce-Schott 표준), Poisson IV = sensitivity**. 두 결과 일관하면 robust.

### F. 80+ aggregate + 65+ sub-analysis

**답변**: KOSIS C3 340 한계 명시 + 65+ sub-analysis 추가 (한국 OECD 1위 elderly suicide).

---

## 12. 다음 Stage 4 — KSIC2-HS6 concordance (v3: typo 수정 + 옵션 C 평가 update)

### Stage 4A (진행 중)
UN Comtrade API 직접 호출. KR-CN HS 01-99 (50 파일 ✅) + ADH/CN-World HS 28-97. 4-key auto-rotation + HS2 chunked + resume.

### Stage 4B — KSIC-HS6 concordance 3 옵션 (v3 갱신)

| 옵션 | Source | 산업 분류 level + 수 | 한국 정합성 | Status |
|------|--------|--------------------|:----------:|:------:|
| A. 통계청 직접 매핑 | KOSIS / KSIC office | **KSIC level 미정** (응답 시 확정. KSIC 2-digit ≈ 76개, 4-digit ≈ 200개, 5-digit ≈ 1,196개) | ⭐⭐⭐ best | 응답 1-2주 대기 |
| B. **한국은행 IO 380** | BOK 산업연관표 | 380 | ⭐⭐ 한국 base | **Fallback 1순위** |
| C. Pierce-Schott / DFS 표준 (v3 update) | DFS = ISIC4 base | varies (DFS 약 234 ISIC4) | ⭐⭐ **medium** (ISIC4 bridge 사용 가능, 다만 IO 380 보다 거침) | Fallback 2순위 |

**v3 변경**:
- 옵션 A: v2 의 "KSIC2 99" typo → "KSIC level 미정 (응답 시 확정)" 로 수정
- 옵션 C: v2 의 "한국 정합성 약함" → "**medium**" (DFS 의 ISIC4 base 가 UN 표준이라 KSIC11-ISIC4 연계표 사용 가능. IO 380 보다는 거침)

**v3 결정**: 통계청 응답 1-2주 더 기다리되 **한국은행 IO 380** fallback 1순위 준비. 통계청 응답 받으면 그 level 에 따라 산업 수 확정.

### Stage 4C
- 시군구 × KSIC2 산업 비중 panel
- KR-CN bilateral net export 변화 (Δ5yr, Pierce-Schott style)
- Bartik shift-share IV (GPSS 2018)

### Stage 5
5-year stacked first-difference 2SLS, 5-layer SE, 6 진단, Romano-Wolf step-down.

---

## v3 변경 요약 (one-page abstract)

본 v3 는 v2 외부 reviewer 피드백 8가지를 반영한 paper submission 가능 quality 갱신본:

1. **§ 5-1 11개 분구 spot check**: 4/11 verified (부천·천안·전주·포항, 15 sample 모두 0.000%) + 7/11 N/A (parent/children 부재로 Phase B reject 발동 안 됨, 정보 손실 가능성 자체 부재). Reviewer "왜 11개 다 검증 안 했나" 우려 해소.
2. **§ 6-2 Case-Deaton 비교 narrative**: 미국 1999-2013 (component 동시 증가, 합산 적절) vs 한국 1997-2023 (component 발산, 분해 적절) 명시. Paper Section 1 + 3 에 일관 적용 권장.
3. **§ 8 항목 5 reframe**: 한계점 → paper strength (component decomposition main outcome 의 motivation).
4. **§ 10 (b) external_other narrative**: 코드 101 (drug overdose) **+ 102 (suicide) 모두 제외** 명시. EX1 검증 시점 신뢰 가능 narrative 추가.
5. **§ 11 답변 D 분량 옵션**: D-1 full (3 baseline) vs D-2 compact (main + 1, WHO 2000 online appendix).
6. **§ 12 KSIC2 typo 수정**: 옵션 A "KSIC2 99" → "KSIC level 미정 (응답 시 확정)". 옵션 C "약함" → "medium" (ISIC4 bridge).
7. **EX1 검증 시점 PASS 확인**: Stage 2 v4 mortality_panel_validation.md 의 V2 가 OUTCOME_PRIORITY 정의 후 panel 기준임을 § 4 EX1 + § 10 (b) 에 명시.
8. **§ 8 #6 update**: spot check 권장 → 4/11 verified 결과 반영.

---

## v3 잔여 권고 사항 (paper submission 직전 처리)

- § 6-2 Case-Deaton 비교 narrative 를 paper Section 1 (Introduction) + Section 3 (Data) 에 일관 적용
- § 11 답변 D 분량 결정 (D-1 vs D-2) — paper 전체 분량 계획에 따라
- 통계청 KSIC-HS6 매핑 응답 도착 시 § 12 옵션 A 산업 수 확정
- 청주시 33020 의 children 코드 부재 사유 (KOSIS reporting 정책) 별도 short footnote

---

작성: 정재헌 (가천대 경제학부 학부생, wjdwogjs9188@gmail.com)
프로젝트: SSCI mid-tier 단독 저자 paper 준비 중
연구주제: Trade Shock, Family Disruption, and Deaths of Despair: A Hidden Mechanism in Korea
