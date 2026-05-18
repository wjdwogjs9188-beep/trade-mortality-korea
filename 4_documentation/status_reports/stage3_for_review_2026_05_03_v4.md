# Stage 3 인구 Panel + 사망률 Panel 구축 — 외부 피드백용 상세 기록 (v4)

작성일: 2026-05-03 (v4: v3 외부 reviewer 1 + 2 통합 12가지 피드백 반영)
프로젝트: Trade Shock × Family Disruption × Deaths of Despair (Korea)
문서 목적: paper submission 직전 quality. v4 = v3 + 12가지 reviewer 피드백 (Critical 3 + Major 4 + Minor 5).

**v3 → v4 주요 변경**:
1. **§ 6-2 + 신규 § 6-4 PAP deviation 명시** (R2-1, Critical) — original PAP commit (despair_total main) vs final spec (component main) 의 post-data design change 명시
2. **§ 5-1 "잔여 risk 무시 수준" → 보다 정확한 framing** (R2-2, Critical) — verified 4 + N/A 7 (merge 자체 적용 안 됨, 다른 종류 risk 는 별도 issue)
3. **§ 7 시군구 단위 cross-check + 외국인 비율 group separate estimation 권고** (R2-3, Critical) — manufacturing 비중 × 외국인 비율 상관성 risk 명시
4. **§ 12 KSIC 4-digit (~200) 결정** (R2-K, Major) — 통계청 응답 무관 4-digit 으로 down/up-aggregate
5. **§ 11 답변 D = D-1 full (Demography 권고)** (R2-D, Major)
6. **§ 8 항목 5 both/and reframe** (R2-5, Major) — 한계 인지 + design motivation 둘 다
7. **§ 12 옵션 C Pierce-Schott concordance 다른 점 정당화** (R1-4, Major) — Section 4 narrative
8. **§ 5-1 children collapse 검증 narrative** (R1-1, Minor) — 경기 6개 시 children → parent baseline collapse 정상 작동
9. **§ 4 EX1 disjoint set 명시** (R1-5, Minor) — priority-based 가 아니라 disjoint set, priority 불필요 이유 narrative
10. **§ 4 EX1 재실행 PASS 명시** (R2-EX1, Minor) — validation log timestamp 2026-05-03 = OUTCOME_PRIORITY 변경 후 재실행 결과
11. **§ 5-1 청주시 33020 footnote** (R1-6, Minor) — 통합 청주 출범 2014 후 자치구 reporting 의 시기적 누락 추정

---

## 0. Stage 별 위치

```
Stage 1 (완료): Raw 수집·검증
Stage 2 v4 (완료): 사망 panel — mortality_panel_v01.parquet, 7,297,865 records, 9 검증 PASS
Stage 3 v1 (완료): 인구 panel + 연령 표준화 사망률 panel  ← 본 문서
Stage 4A (진행 중): UN Comtrade 무역 데이터 수집
Stage 4B/4C (예정): HS vintage concordance + KSIC4-HS6 + Bartik IV
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

| 파일 | 크기 | 행 수 |
|------|------|-------|
| `3_derived/population/population_panel_v01.parquet` | 640 KB | 210,222 |
| `3_derived/population/population_panel_validation.md` | 2.0 KB | — |
| `3_derived/mortality/mortality_rate_panel_v01.parquet` | 1.7 MB | 74,196 |
| `3_derived/mortality/mortality_rate_validation.md` | 2.4 KB | — |

---

## 4. 처리 단계 (9 + 검증 EX1-EX3)

### Step 1-8 요약

1. **KOSIS filter pipeline**: 516,750 → 229,466
2. **17 통합 age band** mapping
3. **Hybrid sigungu merge**: Phase A 217,396 + Phase B 2,754
4. **Population collapse + 1997 = 1998 proxy**: 210,222 rows
5. **Mortality age_band 통합**: 1,483,920 → 1,261,332 cells
6. **Join + rate**: coverage 100.0000%
7. **2010 한국 baseline 직접 표준화** (within-sex)
8. **Log 변환**: `ln(ASR + 1)`

### Step 9 — 검증 V1-V9 + EX1-EX3 (v4: EX1 narrative 강화)

| # | 검증 | 결과 | 비고 |
|---|------|------|------|
| V1 | 인구 합 보존 | PASS | pre = post = 1,292,773,441 |
| V2-V4 | sigungu/year/age band cover | PASS | 229 / 27 / 17 |
| V5 | KOSIS 한국 총인구 (5년) | PASS | 0.124% – 1.173% (§ 7) |
| V6 | Despair ASR 시계열 | PASS | 1997=58.8 → 2023=35.3 |
| V7 | Mortality join coverage | PASS | 100.0000% |
| V8 | Age band 매핑 무결성 | PASS | deaths 합 보존 |
| V9 | 표준화 weight 합 | PASS | Σw=1.0 per sex |
| **EX1** | **Outcome group mutually exclusive** ⭐ v4 강화 | **PASS** | **본 paper 의 outcome group 은 disjoint set 정의**: 각 cause_104 코드는 단 1개 outcome 에만 속함 (예: 102 → despair_total only). Priority-based assignment 가 아니라 disjoint set 이라 priority 불필요. Stage 2 v4 의 mortality_panel_validation.md 의 V2 PASS 결과는 OUTCOME_PRIORITY 변경 (101, 102 모두 external_other 에서 제외) 후 재실행 결과 (validation log timestamp = 2026-05-03 명시) — 추정이 아니라 재실행 PASS. |
| EX2 | Panel cell tuple unique | PASS | h × year × sex × age × outcome 모두 unique |
| EX3 | 5 outcome 합 + other = total | PASS | despair + cardio + cancer + resp + ext_other + other = 7,297,865 |

**v4 EX1 narrative 강화**:
- **Disjoint set vs priority-based 구분 (R1-5)**: 본 paper 의 cause_104 는 한 record 당 단 1 코드 (KOSTAT 사망 microdata 의 단일 cause-of-death 정의). 각 코드는 5 outcome group 중 단 1개에 속하도록 disjoint set 으로 정의됨. 즉 priority-based assignment 가 발동될 case (한 record 가 여러 group 에 속할 수 있음) 가 본 paper 에서 발생하지 않음. 따라서 OUTCOME_PRIORITY 라는 이름의 `Stage 2 코드` 변수는 **list of (group_name, code_set) tuples** 이지만 실질적으로 disjoint set definition 역할.
- **재실행 logging 확인 (R2-EX1)**: `mortality_panel_validation.md` 의 첫 줄 `Generated: 2026-05-03` + v4 changes 항목 (cancer 027-048→047, 2023 full file) 이 명시되어 있으므로 OUTCOME_PRIORITY 정의 후 panel 재실행 결과로 logging 됨. 추정이 아닌 재실행 PASS.

---

## 5. 핵심 설계 결정 4가지 + 학술적 정당화

### (1) Hybrid sigungu merge — 11개 분구 spot check (v4 framing 정확화)

**문제**: KOSIS 인구 vs KOSTAT 사망 코드 충돌 + 분구 시군구 parent/children 공존.

**해결**: Phase A (year-aware) + Phase B (year-agnostic fallback with `(year, h_code)` dedup).

#### Verified 4/11 (모두 0.000% 차이)

| h_code | 시 | 검증 연도 (sample) | 결과 |
|--------|-----|------|------|
| 31050 | 부천시 | 2000, 2005, 2010, 2015 | 4/4 모두 0.000% |
| 34010 | 천안시 | 2010, 2015 | 2/2 모두 0.000% |
| 35010 | 전주시 | 2000, 2005, 2010, 2015 | 4/4 모두 0.000% |
| 37010 | 포항시 | 2000, 2005, 2010, 2015 | 4/4 모두 0.000% |

**14 (year × sigungu) sample 모두 정확히 0.000% 차이** → KOSIS parent-children consistency 완벽 유지.

#### N/A 7/11 (merge 자체 적용 안 됨, v4 framing 정확화)

| h_code | 시 | 사유 | merge accuracy |
|--------|-----|------|---|
| 33020 | 청주시 | KOSIS raw 에 children 코드 (33021-33024) 미존재. **통합 청주 출범 2014 직후 자치구 reporting 의 시기적 누락 추정** (v4 R1-6 footnote) | N/A — parent-only, merge 적용 안 됨 |
| 41110 | 수원시 | KOSIS raw 에 parent 코드 (41110) 미존재. children 만 reporting | N/A — children-only, merge 적용 안 됨 |
| 41130, 41170, 41190, 41280, 41460 | 성남, 안양, 안산, 고양, 용인 | parent 미존재 (children 만 reporting) | N/A — children-only |

**v4 정확한 framing (R2-2)**:

> "검증된 4개 (부천·천안·전주·포항) 의 14 sample 에서 정보 손실 0.000%로 확인되었다. **나머지 7개 (경기 6개 시 + 청주시) 는 single reporting unit (parent-only 또는 children-only) 라 merge 자체가 적용되지 않으므로 merge accuracy 검증은 N/A 다.** 단, single-unit reporting 케이스에는 merge accuracy 와 다른 종류의 잔여 risk 가 존재한다 — children-only reporting 케이스에서 children 합이 분구 시점 전후로 일관되는가 (행정구역 개편 직전·직후 계측 단절 가능), 청주시의 경우 통합 청주 출범 (2014) 전후 parent 정의의 일관성 — 이는 별도 issue 로 § 8 limitation #6 에 명시한다."

**v4 children collapse 검증 narrative 추가 (R1-1)**:

> "경기 6개 시 (수원·성남·안양·안산·고양·용인) 의 children 데이터는 sigungu_crosswalk_v2 에 정의된 parent h_code 로 collapse 된다 (예: 41111 + 41113 + 41115 + 41117 → 41110 수원시). 이 collapse 가 baseline 229개 단위 분석에 정상 작동함을 Population Panel V1 (인구 합 보존, pre = post = 1,292,773,441) 으로 간접 확인했다. Direct 검증은 children 합 vs 분석 단위 인구 비교지만 분석 단위 (229) 가 children 합 = parent 정의이므로 V1 = direct 검증과 동일하다."

**Paper Appendix narrative (v4 정확화)**:

> "분구 시군구 11개 중 4개 (부천·천안·전주·포항) 의 parent vs children 합 비교에서 14개 sample 모두 0.000% 차이로 일치하여 KOSIS 의 parent-children consistency 가 직접 확인되었다. 나머지 7개는 KOSIS 가 single reporting unit (parent-only 또는 children-only) 만 발행하여 merge accuracy 검증은 N/A 다. Single-unit reporting 케이스의 별도 risk (분구 시점 전후 일관성 등) 는 § 8 limitation #6 에 명시한다."

### (2) 1997 인구 = 1998 proxy

(생략 — v3 와 동일)

### (3) 17 통합 age band

(생략 — v3 와 동일)

### (4) 2010 한국 baseline 직접 표준화 (within-sex)

(생략 — v3 와 동일)

---

## 6. ASR 시계열 패턴 + Paper Main Thesis 함의

### 6-1. Despair_total ASR

| 연도 | ASR |
|------|-----|
| 1997 | 58.8 |
| 2010 | 47.0 |
| 2023 | 35.3 |

### 6-2. Component Decomposition main outcome (Case-Deaton 비교 narrative 유지)

**Component 별 시계열 발산**:
- Suicide: 1997 (~13/100k) → 2010 (~31/100k) → 2023 (~27/100k) — **2배 증가**
- Liver: 1997 (~30/100k) → 2010 (급락) → 2023 (낮음) — **1/3로 감소**

**Case-Deaton 비교**:
> "Case-Deaton (2015) 은 미국 1999-2013 기간 자살, drug, 간질환 모두 동시 증가 추세였기에 합산 정의 'deaths of despair' 가 적절했다. 본 paper 한국 1997-2023 기간 component 발산 (자살 ↑ 2배, 간질환 ↓ 1/3) 하에서 합산 통계는 mechanism 을 가리는 효과 → component decomposition main, despair_total robustness."

### 6-3. 한국 간질환 1997 정점 historical context

(v3 와 동일 narrative — 1980-90년대 알코올 문화, B형간염, IMF 외환위기)

### 6-4. Original PAP commit vs final spec — Post-Data Design Change (v4 신규, R2-1 Critical)

**원 PAP commit (research_proposal.md, line 122)**:
> "5개 outcome group (절망사, 심혈관계, 암, 호흡기, 외인사 기타) 에 대해 각각 추정한다. **절망사가 main outcome이고**, 심혈관계와 암은 placebo다."

**Final spec change (v4 § 6-2)**:
- Original PAP main outcome = `despair_total` (절망사 합산 정의, Case-Deaton style)
- Final spec main outcome = **Component decomposition** (suicide / drug / psych / liver 분해)
- Despair_total 은 **robustness check** 로 위치 변경

**Disclosure narrative (Paper Section 1 + Section 4 일관 적용)**:

> "본 paper 의 final main outcome 은 component decomposition (suicide / drug / psych / liver) 이지만, internal working document (research_proposal.md, 2026 작성) 의 PAP 은 despair_total 합산 정의를 main outcome 으로 commit 했다 (line 122 인용). 이 deviation 은 panel 구축 단계에서 1997-2010 component-level divergence (자살 +2배 vs 간질환 −1/3, § 6-2 정량 보고) 를 관찰한 후 § 6-2 의 학술적 motivation 에 의한 **post-data design change** 다. 외부 registry (OSF / AEA RCT registry) 등록은 없으나 supplementary materials 에 PAP 원본 + dated change log 첨부하여 transparent disclosure 한다."

**Main result 표 구조 (Paper Table 1, v4 결정)**:

| Column | Outcome | 위치 | PAP 일치 여부 |
|--------|---------|------|:------------:|
| 1 | Suicide ASR | **Final main** | new |
| 2 | Drug overdose ASR | Final secondary | new |
| 3 | Psych disorder ASR | Final secondary | new |
| 4 | Alcohol-related liver ASR | Separate (sign expectation 정반대) | new |
| 5 | **Despair_total ASR** | **Robustness (PAP main)** | original PAP main 위치 보존 |
| 6 | Cardiovascular ASR | **Placebo** (PAP commit 유지) | PAP 일치 ✅ |
| 7 | Cancer ASR | **Placebo** (PAP commit 유지) | PAP 일치 ✅ |

**v4 결정 narrative**: 표 자체가 final spec (component main) 과 original PAP (despair_total main) 의 두 정의를 동시에 보여주는 비교 형태. Deviation 이 paper 의 **기여로 전환** (기존 합산 정의 vs 새로운 분해 정의의 한국 context-specific 차이 quantify) 됨.

---

## 7. KOSIS V5 Cross-Check (실측값) + 시군구 단위 cross-check 권고 (v4 추가, R2-3 Critical)

### 7-1. 시도 단위 (전국 합계)

| 연도 | KOSIS 공식 (천명) | Panel 합 (명) | 차이 % | 부호 |
|------|------------------:|--------------:|------:|:----:|
| 2000 | 47,008,000 | 47,534,117 | +1.119% | panel > official |
| 2010 | 49,410,000 | 49,879,812 | +0.951% | panel > official |
| 2015 | 51,015,000 | 50,951,719 | −0.124% ⭐ best | panel < official |
| 2020 | 51,836,000 | 51,349,259 | −0.939% | panel < official |
| 2023 | 51,753,000 | 51,145,884 | −1.173% ⚠️ worst | panel < official |

### 7-2. Sign 전환 패턴 + paper-level risk (v4 강화, R2-3)

**Sign 전환 해석**:
- 2000-2010 (+): KOSIS 추계가 panel 주민등록보다 보수적 (외국인 ~2%)
- 2020-2023 (−): 한국 외국인 비율 ~5% (2023) 로 증가 → panel (주민등록 only) 미포함 → official < panel

**v4 paper-level risk 명시 (R2-3 Critical)**:

> "외국인 비율은 시군구별로 매우 heterogeneous 하다. 안산·화성·시흥·인천·서울 일부 등이 외국인 비율 상위인데, 이 지역들은 정확히 본 paper 의 manufacturing employment 비중이 높은 지역과 겹친다 (제조업 노동시장 → 외국인 노동자 유입). 즉 인구 panel 의 measurement error 가 treatment 변수 (manufacturing trade exposure) 와 상관될 가능성이 있다. 시도 단위 ±2% cross-check 가 시군구 단위에서도 동일하다는 보장이 없다. 이는 attenuation bias 또는 differential measurement error risk 다."

### 7-3. v4 추가 권고 (paper submission 직전 처리, R2-3)

1. **시군구 단위 cross-check**: Manufacturing 비중 상위 10개 시군구 (예: 울산 동구·북구, 안산, 시흥, 화성, 거제, 창원 진해·성산, 광양, 군산) 에 대해 KOSIS 시군구별 공식 추계인구 vs panel 비교. Manufacturing-heavy + 외국인 high 지역의 measurement error 추정.

2. **외국인 비율 group separate estimation**: 시군구 외국인 비율 high (>4%) vs low (<2%) group 별 separate 회귀. 두 group 결과 일관하면 measurement error 가 attenuation bias 만 유발 (sign 보존). 발산하면 differential measurement error → identification 위협.

3. **Robustness section 명시**: 외국인 비율 시군구 panel (KOSIS 외국인 등록인구 1B040A26 또는 통계청 행정자료) 추가 수집 → main 분석 후 robustness 로 보고.

**Paper limitation v4 update**:

> "주민등록인구 panel 의 KOSIS 추계 대비 시도 단위 차이는 ±1.17% 이내라 학술 standard 부합한다. 다만 외국인 비율의 시군구별 heterogeneity 가 manufacturing 비중과 상관될 가능성이 있어 시군구 단위 cross-check 와 외국인 비율 group separate estimation 을 robustness 로 추가한다. Differential measurement error risk 는 § 7-3 에서 정량 평가 후 paper 본문에 보고한다."

---

## 8. 알려진 한계점 (v4: 7 항목, 항목 5 both/and reframe)

| # | 한계 | 영향 | 대응 |
|---|------|------|------|
| 1 | 1997 인구 = 1998 proxy | 매우 미미 (~0.5%/yr) | Paper Appendix |
| 2 | 외국인 미포함 (주민등록 only) | 2023 -1.173% + 시군구 heterogeneity (R2-3) | § 7-3 시군구 cross-check + 외국인 group separate estimation |
| 3 | 80+ 단일 band | KOSIS C3 340 한계 | 80+ aggregate + 65+ sub-analysis |
| 4 | 2010 baseline 만 main | 비교 가능성 | Sensitivity: WHO 2000 + 2020 한국 (D-1 full) |
| **5 (v4 both/and)** | **Despair_total 합산 통계의 1997 liver dominance** | **합산 통계가 mechanism 을 가리는 효과 (자살 ↑ + 간질환 ↓ 부분 상쇄)** | **§ 6-2 component decomposition main outcome 결정의 motivation. 한계 인지 + design 결정 둘 다 명시.** |
| 6 (v4 update) | Hybrid merge 의 single-unit reporting 7개 (경기 6개 시 + 청주) 의 별도 risk | merge accuracy N/A 지만 **분구 시점 전후 일관성 risk 별도 issue** | § 5-1 narrative 가 별도 issue 명시. Paper limitation 에 single-unit reporting 의 인구 계측 단절 가능성 inclusion. |
| 7 | Sigungu_crosswalk_v2 256 → 229 collapse | 일반시 자치구 단위 heterogeneity 분석 불가 | Paper 명시: "분석 단위 = 229. 자치구 32개 collapse." |

**v4 항목 5 both/and reframe (R2-5)**:

> "Despair_total 합산 통계는 한국 1997 시점 간질환 dominance 로 인해 1997-2010 component-level divergence 를 가린다는 한계가 있다. 본 paper 는 이 한계를 인지하고 § 6-2 의 component decomposition main outcome 결정으로 대응한다. Despair_total 은 robustness check 로 보고하여 한계 인지와 design 결정의 두 가지 함의를 명시한다."

---

## 9. 코드 / 산출물 폴더 구조

(v3 와 동일 — `1_codebooks/sigungu_crosswalk_v2.csv` single source of truth)

---

## 10. Paper Appendix A 변경 사항 누적

| Stage | 변경 |
|-------|------|
| Stage 1 | Sigungu baseline 256 → 229 |
| Stage 2 v4 | (a) Cancer 027-048 → 027-047 (KOSIS C00-C97 정합) |
| Stage 2 v4 | (b) external_other = {097, 098, 099, 100, 103, 104}. **101 (drug) + 102 (suicide) 모두 despair_total components 라 mutually exclusive 위해 external_other 에서 제외**. EX1 PASS = 재실행 결과 (validation log timestamp 2026-05-03). |
| Stage 2 v4 | (c) 2023 file partial → full replace |
| Stage 3 | (a) Hybrid sigungu merge |
| Stage 3 | (b) 1997 인구 = 1998 proxy |
| Stage 3 | (c) Age band 통합 (17 unified bands) |
| Stage 3 | (d) 직접 연령 표준화 (2010 한국, within-sex) |
| **Final spec (v4)** | **(post-data design change)** Main outcome: despair_total → component decomposition. Despair_total 은 robustness 위치. PAP supplementary materials + dated change log 첨부. |

---

## 11. 외부 피드백 6가지 (A-F) + 답변 통합

### A. Hybrid merge 학술적 정당성

**답변**: 11개 spot check (4 verified 0.000% + 7 N/A merge 적용 안 됨). § 5-1 정확한 framing.

### B. 1997 = 1998 proxy

**답변**: 27년 유지 권장 (IMF 직전 baseline 가치).

### C. Despair_total liver dominance — main outcome

**답변**: Component decomposition main, despair_total robustness. **§ 6-4 PAP deviation 명시.**

### D. 추가 baseline (v4: D-1 결정, R2-D Major)

**v4 결정**: **D-1 full (3 baseline 모두 main paper)**.

**근거**:
- Demography submission target. Main text 40-50p 허용 (충분한 분량).
- WHO 2000 standardization = international comparability 핵심. Demographer reviewer 가 자주 묻는 항목.
- D-2 (compact, WHO 2000 online appendix) 가면 desk-level "왜 international standard 안 썼나" 질문 가능성.

**Final spec**: Main = 2010 한국 baseline. Sensitivity = WHO 2000 + 2020 한국 (둘 다 main paper Appendix Table A.X).

### E. Log linear vs Poisson IV

**답변**: Main = ln(ASR + 1). Poisson = sensitivity.

### F. 80+ aggregate + 65+ sub-analysis

**답변**: KOSIS C3 340 한계 + 65+ sub-analysis 추가.

---

## 12. 다음 Stage 4 — KSIC4-HS6 concordance (v4: KSIC 4-digit 결정, R2-K Major)

### Stage 4A (진행 중)

UN Comtrade API 직접 호출. KR-CN HS 01-99 (50 파일 ✅) + ADH/CN-World HS 28-97. 4-key auto-rotation + HS2 chunked + resume.

### Stage 4B — KSIC level 결정 (v4: KSIC 4-digit 사전 commit)

**v4 결정 (R2-K Major)**: **본 paper 는 KSIC 4-digit (~200 산업) 사용**. 통계청 응답 무관 사전 commit.

**근거 표**:

| KSIC level | 산업 수 | 학술 정합성 | Variance / HHI risk | 결정 |
|----|---:|:--------:|:--------:|:----:|
| 2-digit | ~76 | ⚠️ Pierce-Schott (4-digit SIC) 와 정합 약함 | ⚠️ Rotemberg HHI 가 소수 산업 집중 → GPSS share exogeneity 검증 약화 | reject |
| **4-digit** | **~200** | ⭐⭐⭐ **Pierce-Schott 4-digit SIC + ADH 정합** | ⭐⭐⭐ **Variance 안정 + HHI 분산** | **adopt** ⭐ |
| 5-digit | ~1,196 | ⭐⭐ fine 하지만 thin | ⚠️ share variance 폭발 risk | reject |

**통계청 응답 처리**:
- 통계청이 4-digit 으로 매핑 발행 → 그대로 사용
- 2-digit 발행 → KSIC 4-digit 으로 up-aggregate (정보 추가 안 됨, 4-digit으로 commit 했지만 2-digit 만 사용)
- 5-digit 발행 → 4-digit 으로 down-aggregate (5-digit → 4-digit collapse)

### Concordance 옵션 (v4: 옵션 C narrative 추가, R1-4 Major)

| 옵션 | Source | 산업 분류 | 한국 정합성 | Status |
|------|--------|---|:----------:|:------:|
| A. 통계청 직접 매핑 | KOSIS / KSIC office | KSIC 4-digit (~200) target | ⭐⭐⭐ best | 응답 1-2주 대기 |
| **B. 한국은행 IO 380** | BOK 산업연관표 | 380 → KSIC 4-digit aggregate | ⭐⭐ 한국 base | **Fallback 1순위** |
| C. Pierce-Schott / DFS 표준 | DFS = ISIC4 base, Pierce-Schott = US SIC base | KSIC11-ISIC4 bridge → KSIC 4-digit | ⭐⭐ medium | Fallback 2순위 |

**v4 옵션 C 정당화 narrative (Section 4 일관 적용, R1-4)**:

> "Pierce-Schott (2020) 은 미국 SIC industry concordance 를 사용했고 본 paper 는 한국 KSIC 4-digit 기반 concordance 를 사용한다. 이는 본 paper 가 한국 산업 구조 (예: HS 84 기계, 85 전자가 한국 KSIC 4-digit 26 (전자부품) 으로 집중) 의 unique pattern 에 맞추기 위함이며, 미국 SIC 산업 분류 직접 적용은 한국 산업 정합성을 약화시킨다. 본 paper 는 한국은행 IO 380 → KSIC 4-digit aggregate 를 fallback 1순위, ISIC4 bridge → KSIC 4-digit 매핑을 fallback 2순위로 우선순위화한다. 이 결정은 § 5 (Identification Strategy) 의 share exogeneity (GPSS 2018) 검증과도 직접 연결된다 — 한국 산업 분포에 정합한 concordance 가 Rotemberg HHI 의 산업 집중도 검증을 더 robust 하게 만든다."

### Stage 4C / Stage 5

(v3 와 동일)

---

## v4 변경 요약 (one-page abstract)

본 v4 는 v3 외부 reviewer 1 + 2 통합 12가지 피드백을 반영한 paper submission 직전 quality 갱신본:

**Tier 1 (Critical)**:
1. **§ 6-4 PAP deviation 명시** — original PAP (despair_total main) vs final spec (component main) 의 post-data design change 명시 + supplementary materials disclosure + Table 1 구조 (component main + despair_total robustness 마지막 column)
2. **§ 5-1 framing 정확화** — verified 4 + N/A 7 (single-unit reporting, merge 자체 적용 안 됨, 별도 risk 는 § 8 #6 inclusion)
3. **§ 7-3 시군구 단위 cross-check + 외국인 비율 group separate estimation 권고** — manufacturing × 외국인 비율 상관 risk 명시 + Robustness section

**Tier 2 (Major)**:
4. **§ 12 KSIC 4-digit (~200) 사전 commit** — Pierce-Schott 4-digit SIC + ADH 정합 + variance/HHI 안정. 통계청 응답 무관 down/up-aggregate.
5. **§ 11 답변 D = D-1** — Demography submission, WHO 2000 international comparability 핵심.
6. **§ 8 #5 both/and reframe** — 한계 인지 + design motivation 둘 다.
7. **§ 12 옵션 C Pierce-Schott concordance 다른 점 정당화** — Section 4 narrative.

**Tier 3 (Minor)**:
8. **§ 5-1 children collapse 검증 narrative** — 경기 6개 시 children → parent baseline collapse 정상 작동 (V1 인구 합 보존으로 간접 확인).
9. **§ 4 EX1 disjoint set 명시** — priority-based 가 아니라 disjoint set, priority 불필요 이유.
10. **§ 4 EX1 재실행 PASS 명시** — validation log timestamp 2026-05-03, 추정 아닌 재실행.
11. **§ 5-1 청주시 33020 footnote** — 통합 청주 출범 2014 후 자치구 reporting 시기적 누락 추정.
12. **§ 12 옵션 A 산업 수 KSIC 4-digit (~200) 으로 통일**.

---

## v4 잔여 작업 (paper submission 직전)

- 통계청 KSIC-HS6 매핑 응답 도착 시 § 12 옵션 A level 확인
- 시군구 단위 KOSIS 추계 vs panel cross-check (manufacturing 상위 10개) — § 7-3 권고 항목, Stage 3 마무리 또는 Stage 5 robustness 시점
- 외국인 비율 시군구 panel 수집 (KOSIS 1B040A26 또는 행정자료)
- Stage 4A 다운로드 완료 후 Stage 4B concordance 실작업 (한국은행 IO 380 fallback 준비)
- Paper Section 1 + 4 + supplementary materials 의 PAP deviation narrative 일관 적용

---

작성: 정재헌 (가천대 경제학부 학부생, wjdwogjs9188@gmail.com)
프로젝트: SSCI mid-tier 단독 저자 paper 준비 중. Demography target.
연구주제: Trade Shock, Family Disruption, and Deaths of Despair: A Hidden Mechanism in Korea
