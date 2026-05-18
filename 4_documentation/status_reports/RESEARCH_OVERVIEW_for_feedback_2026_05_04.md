# Research Overview — Trade Shocks and Deaths of Despair in Korea
## *Self-contained brief for external feedback*

**저자**: 정재헌 (Jae-Heon Jeong, 가천대학교 경제학부 학부생, ORCID 0009-0009-9403-0940)
**작성일**: 2026-05-04
**상태**: PAP v4.0 unified identification protocol commit 직전
**Target**: SSCI Q1 — AEJ Applied / Journal of Health Economics / Health Economics
**문서 목적**: 외부 reviewer 가 본 paper 의 *연구방향 · 식별전략 · 데이터 · 한계* 를 한 번에 파악하고 P1/P2/P3 critique 가능하도록 작성.

---

## 0. Executive summary (1 페이지)

본 paper 는 **한국의 시군구별 무역 노출이 25-64세 working-age 사망률에 미치는 인과효과** 를 추정하고, 그 효과 중 **가족구조 mediator (혼인상태·교육수준 분포)** 를 통해 전달되는 부분을 분리한다.

### Three points

1. **Setting differential**: 미국 (Pierce-Schott 2020 AERI: drug 사망 +2-3/100K) 과 한국은 *deaths-of-despair 의 구성*이 다르다. 미국 = drug-overdose dominance, 한국 = **suicide + liver dominance** (drug 사망률은 미국의 1/13).

2. **Methodological novelty**: DGHP (2017) IV-mediation framework + DFH (2020) `ivmediate` Stata package 의 **첫 한국 적용**. 2-instrument joint identification protocol (PAP v4.0) 사전등록.

3. **Korean structural context**: 본 paper 는 ADH (2013) 식 import-shock 만으로는 한국이 잡히지 않는다는 가설 을 제기 — 한국은 *export-driven* 경제 (대중국 중간재 수출 비중 ↑). 따라서 KR-CN bilateral net exposure 를 보조 IV 로 사용. validity 사전 검정 protocol commit (Tests 1-3).

### Core finding (preliminary, descriptive only)

- 본 panel main 분석 cohort (working-age 25-64): suicide rate 1997-2001 23.2 → 2007-2011 *35.3 (peak)* → 2017-2021 29.6 (per 100K)
- liver disease: monotonic 57% decline (1997-2001 44.2 → 2017-2021 19.1)
- drug: 5.6 → 3.9 (안정적, 미국 50+ 의 1/13)
- 본 trade-shock 효과 *causal estimate 는 Stage 5 진입 후 보고 (현재 pre-registration commit 단계)*

---

## 1. Research question + 4 hypotheses

### 1.1 Main research question

한국 시군구별 *무역 충격* (특히 2001 China WTO 가입 + 2015 KR-CN FTA 의 충격) 이 *deaths of despair (자살 + 약물 + 정신활성물질 + 알코올성 간질환)* 에 미치는 *인과적 효과* 의 크기는? 그 중 *가족구조 mediator* (혼인상태·교육수준 분포) 를 통해 전달되는 부분의 비중은?

### 1.2 Hypotheses (H1-H4)

**H1 — Reduced-form trade effect**: 시군구 무역노출 (Bartik IV) 1 std 증가 → working-age 25-64 의 deaths of despair (102+101+057+081) 5년 누적 기준 **β** 변화.
- 부호 전망: H1.1 자살 +, H1.2 약물·정신활성 ?, H1.3 간질환 ±, H1.4 placebo (cardiovascular 067-070, cancer 027-047) = 0.

**H2 — Mediator first-stage strength**: 무역 노출 z_x 가 marital share (혼인·이혼) 와 education share (NoHS/HS/College+) 변동을 *통계적 유의* 하게 설명. Olea-Pflueger 2013 effective F > 23.1 (Stock-Yogo 2005 Cragg-Donald 5% TSLS bias threshold).

**H3 — Indirect effect (mediation)**: DGHP 2017 + DFH 2020 ivmediate 의 indirect effect (trade → mediator → mortality) 가 *통계적·경제적으로 유의*. Total effect 의 X% 가 mediation 으로 설명.
- 단 H3 가 *식별* 되려면 z_m_marital + z_m_education 의 validity (PAP v4.0 Tests 4-6) + Sequential Ignorability 가 사전 commit 되어야.

**H4 — Korea-US heterogeneity**: 한국의 *suicide + liver dominance* 는 미국 (Case-Deaton 2015) 의 *drug dominance* 와 inverse pattern. 가족 채널 비중이 한국에서 *더 큼* (미국 = unemployment 채널 dominant, Pierce-Schott 2020).

---

## 2. Theoretical framework — DGHP 2017 + DFH 2020 ivmediate

### 2.1 Mediation 분해 (DGHP 2017)

```
Total effect (Trade → Mortality)
  = Direct effect (Trade → Mortality | Mediator)
  + Indirect effect (Trade → Mediator → Mortality)
```

### 2.2 4 식별 가정 (PAP v4.0 § 1)

**A1 (z_x relevance for X)**: trade IV 가 trade exposure 의 first-stage 강함 (KP rk-Wald F ≥ 10).

**A2 (z_x exclusion from Y)**: trade IV 가 mortality 에 영향을 줄 수 있는 채널은 trade exposure (또는 X→M) 뿐. 본 paper 의 Test 1/1b/2/3 으로 검정.

**A3 (z_m relevance for M | X)**: mediator IV 가 z_x 통제 후 first-stage 강함 (Test 6).

**A4 (z_m exclusion from Y | X, M)**: mediator IV 가 mortality 에 영향을 줄 수 있는 채널은 mediator 뿐 (Test 4).

A2 와 A4 는 *별개의 명제*. ivmediate 는 **두 개의 독립적 instrument** 가 필요 (z_x + z_m). v3.4 까지는 z_m 미정의 상태였고, **v4.0 가 이 black hole 메움**.

### 2.3 Sequential Ignorability 추가 가정 (Imai-Keele-Yamamoto 2010)

mediator counterfactual 이 trade counterfactual 과 *조건부 독립*. unmeasured 한 mediator-outcome confounder (예: 시군구 cultural conservatism → 결혼규범 강도 + 자살 직접 영향) 가 X 통제 후에도 존재하면 SI 위배. **Imai-Yamamoto ρ-sensitivity** 로 검증 (PAP v4.0 § 4).

---

## 3. Identification strategy — PAP v4.0 protocol

### 3.1 z_x (trade IV) — two candidates

| 후보 | 정의 | strength | validity 위험 |
|------|------|----------|---------------|
| **ADH-8** | Australia·Denmark·Finland·Germany·Japan·New Zealand·Spain·Switzerland 의 imports from China (1997-2024) | 약함 (한국 제조업 산업 분포 ≠ ADH-8 평균) | strong (한국과 무관) |
| **KR-CN bilateral net exposure** | 한국의 對中 수입 - 對中 수출 | 강함 (F≈12-16) | 변호 필요 (한국 macro 와 동시결정) |

### 3.2 z_x validity tests (Tests 1-3)

**Test 1 — Romer-Romer style**: bilateral shock 이 *lagged 한국 거시 실현치* (분기 GDP 성장률, KRW/USD 환율, 수출입 물가지수, CPI, BoK 기준금리) 로 예측 가능한가? H0: β_j = 0 ∀ j (모든 macro 변수). p > 0.10 → 외생성 신호.

**Test 1b — WEO surprise robustness**: bilateral 이 IMF World Economic Outlook Korea forecast surprise 와 무상관.

**Test 2 — pre-WTO lead orthogonality**: pre-2001 bilateral 이 post-2001 한국 macro 를 예측하지 *않음* (single-direction causality 검정).

**Test 3 — Pierce-Schott pre-trend**: 1995-1999 시군구 mortality trend 가 baseline industry shares × bilateral exposure 와 무상관 (share-side validity).

### 3.3 z_x strength branch (사전 commit)

- **Branch A**: F_ADH-8 ≥ 23.1 → ADH-8 main, 5-layer SE 표준.
- **Branch B**: 10 ≤ F_ADH-8 < 23.1 → ADH-8 main, AR + tF column 1 격상.
- **Branch C.i**: F_ADH-8 < 10 + bilateral validity (Tests 1-3) PASS → bilateral main, AR + tF.
- **Branch C.ii**: F_ADH-8 < 10 + bilateral reject → reduced-form 또는 FNS spillover framing.

### 3.4 z_m (mediator IV) — two recommended instruments

본 paper 의 *진짜 contribution* — 2-instrument framework 의 z_m 후보:

**z_m_marital — 시군구별 출생 성비 cohort lag**:
- 1980s-1990s 한국 son preference (selective abortion, Park-Cho 1995) → 시군구별 *출생 성비* 변동 → 25년 후 *결혼시장* 진입 cohort 의 외생적 imbalance → marital share 변동.
- 외생성 변호: 1980s sex-selective abortion = *과거* 의사결정, 1997-2021 본 panel 의 노동시장 충격과 분리.
- **데이터**: MDIS 1995 census 의 시군구 × 0-9세 (= 1986-1995 출생 cohort) × 성별 인구. **본 paper 가 추출 완료**: 247 시군구 × 2 cohort = 494 rows, median sex ratio 111.75 (한국 1990s son preference 정상 시그널), 88 시군구 가 SR > 130 (extreme).

**z_m_education — distance-to-nearest-4-year-college (1990 baseline)**:
- Bound-Jaeger (1996) 식 distance instrument. 1960s-1970s 정부의 대학 위치 결정 → *지리적 외생성* → 시군구별 진학율 → education share.
- **데이터**: namuwiki "한국의 대학교 일람" 233 학교 → 4년제 + dedupe + h_code 매핑 → 175 학교 → centroid 부착 → **251 시군구 × pairwise distance**. **본 paper 가 추출 완료**: median distance 12.5 km, 같은 시군구 내 (≈0 km) 77 시군구, 14 시군구는 ≥ 50 km (대학 desert: 울릉군 180km, 옹진군 174km).

### 3.5 z_m validity tests (Tests 4-6)

**Test 4 (A4 exclusion)**: z_m 이 mortality 에 직접 영향을 줄 수 있는가 (M 통제 후)?
$$\Delta Y_{c,t→t+5}^{cause} = \alpha + \beta \cdot z_{m,c,t-10} + \gamma \cdot M_{c,t-5} + \delta_t + \varepsilon$$
H0: β = 0 (8 spec: 4 cause × 2 mediator).

**Test 5 (z_x ⊥ z_m)**: 두 instrument 가 같은 variation 잡으면 ivmediate 미식별.
$$z_x = \alpha + \beta \cdot z_m + \varepsilon$$
H0: β = 0. p > 0.10 → 독립적 variation.

**Test 6 (z_m first-stage with z_x partialled)**:
$$M_{c,t} = \alpha + \beta_x \cdot z_x + \beta_m \cdot z_m + \gamma \cdot X_{c,t-5} + \delta_t + \varepsilon$$
H0: β_m = 0 reject, KP F ≥ 10.

### 3.6 z_m strength branch (사전 commit)

- **Branch αm**: F_z_m ≥ 23.1 → z_m main, ivmediate 표준.
- **Branch βm**: 10 ≤ F_z_m < 23.1 → mediator 단계 weak-IV-robust (AR CI on indirect, point estimate 비보고).
- **Branch γm**: F_z_m < 10 → mediation = robustness only (reduced-form 이 main).

### 3.7 Joint pre-commit decision tree (PAP v4.0 § 5)

z_x × z_m × SI 의 12+ branch 매트릭스:

| z_x | z_m | 결정 |
|-----|-----|------|
| A (강) | αm (강) | ⭐ Full ivmediate, 5-layer SE 표준, ρ sensitivity 첨부 |
| A | βm | ivmediate with AR CI on indirect |
| A | γm | reduced-form main, mediation = appendix |
| B | αm | ivmediate main, AR CI on direct + indirect |
| B | βm/γm | reduced-form main |
| C.i | αm | bilateral-IV ivmediate (caveat 명시) |
| C.i | βm/γm | reduced-form bilateral, mediation 폐기 |
| C.ii | any | paper 재포지셔닝 (FNS spillover 또는 reduced-form 만) |
| any | A4 reject | mediation 폐기 |
| any | Test 5 collinear | z_m 후보 교체 |

**Pre-commitment**: 회귀 결과 본 *전* commit. post-hoc switching 금지.

---

## 4. Data inventory — current status

### 4.1 사망 데이터 (Stage 1-3 완료)

- **MDIS 사망 microdata 1997-2024** (28 년치, 7.4M rows, working-age 25-64 1.5M)
- 변수: 사망원인 104 코드 (KCD-8) + 시군구 (5-digit) + 성별 + 연령 + 혼인상태 + 교육수준 + 직업 + 사망일자
- 산출 main panel: `mortality_rate_panel_v02_1.parquet` (123,660 rows, 229 h_code × 27 year × 2 sex × 10 outcome group, 3 ASR baselines: 한국2010 + WHO2000 + Eurostat2013)

### 4.2 인구 (Stage 3, mediator 완료)

- **MDIS 인구주택총조사 1990/1995/2000/2005/2010/2015/2020** (7 시점) — 본 panel 의 mediator denominator
- **MDIS 1975/1980/1985/1990/1995 census** (5 시점, 220 MB, 3.8M rows) — z_m_marital cohort sex ratio 추출용 (사용자 본 turn 에서 발견)
- KOSIS 시군구 인구 1993-2024 (rate 분모 cross-check)

### 4.3 무역 (Stage 4)

- **Comtrade KR-CN bilateral 2000-2024** (50 file, HS6, ✅)
- **Comtrade ADH-8 ← China 2000-2024** (200 file, ✅)
- **Comtrade CN → World 2000-2024** (25 file, ✅)
- **BACI HS92 1995-2011** (17 csv, 3.9 GB) — clean·imputed bilateral trade
- **KR-CN bilateral 1995-1999** (Test 2 pre-WTO, 사용자 추가 수집 진행 중)

### 4.4 산업 분류 매핑

- **researchall.net HS6 ↔ KSIC10 매핑** (6,351 rows, 503 KSIC, 415 manufacturing) — 본 paper 의 P1.6 차단 항목 SOLVED
- **WITS HS6 → ISIC Rev 3 4-digit** (5,703 rows, 145 ISIC, 119 manuf) — robustness
- **KSIC chain 8→9→10→11 통합 lookup** (1,361 rows) — 시기별 광업제조업조사 호환

### 4.5 산업 baseline shares (Stage 4 진행 중)

- **광업제조업조사 microdata 1994-2024** (31 csv, 2.5M rows in 1994 alone, KSIC 4-digit + 시군구 5-digit) — Bartik baseline
- 산업 share 추출 : 다음 turn 에서 KSIC chain 활용

### 4.6 z_m instrument (사용자 본 turn 에서 작성 완료)

- **z_m_marital**: `cohort_sex_ratio_1995_v01.csv` — 247 시군구 × 2 cohort, median SR 111.75
- **z_m_education**: `distance_to_nearest_college_pre1990_v01.csv` — 251 시군구 × 175 학교, median 12.5 km

### 4.7 거시 (Test 1 macro predictability)

- **ECOS 200Y110 (분기 GDP, 실질, 원계열)** — 2,100 rows
- **ECOS 402Y014 (수출물가지수 총지수, 월별)** — 900 rows
- **ECOS 401Y015 (수입물가지수 총지수, 월별)** — 900 rows
- 기존 ECOS 11 시리즈 (731Y004 환율, 901Y009 CPI, 722Y001 BoK rate, 161Y001/006 M1·M2, 102Y002 본원통화, 132Y001/003 산업별 대출, 301Y015 지역경상수지, 403Y001/002 수출입)

### 4.8 외생적 변동 source (Test 1b)

- **IMF World Economic Outlook Historical Forecasts** — Korea 1990-2022 vintages (8.6 MB)

### 4.9 Sigungu 좌표 + 인구

- **시군구 centroid** (KOSTAT 2018 GeoJSON, 251 시군구) — distance 계산 base
- **sigungu_crosswalk** (1997-2023 6,723 rows, 256 h_code, 2021 baseline)

### 4.10 SI 통제 변수 (보조)

- HIRA 약물 panel (post-2010 sensitivity mediator)
- KOSIS 보건의료 4 시리즈 (보건기관 이용률 + 인플루엔자 접종률 + 일반건강검진 정상B/질환의심)
- ECOS 가계부채 (Sufi 2023 채널)

---

## 5. Empirical specification

### 5.1 Main 2SLS (Pierce-Schott 2020 base)

5-year stacked first-difference:
$$\Delta_5 \ln(\text{ASR}_{h,t})^{\text{cause}} = \beta \cdot \Delta_5 \text{Trade}_{h,t} + \gamma \cdot X_{h,t} + \delta_t + \varepsilon_{h,t}$$

- **h** = 시군구 (n = 229), **t** = 5 stack period (1997-2001, 2002-2006, 2007-2011, 2012-2016, 2017-2021).
- **outcome**: ln(age-standardized rate + 1), Korea 2010 weights (main).
- **treatment**: Bartik shift-share
$$\Delta_5 \text{Trade}_{h,t} = \sum_k s_{h,k,1995} \times \Delta_5 \text{Imports}_{k,t}$$
- **controls X**: baseline 제조업 share + 교육 + 도시화 + 65세 이상 비율 + 외국인 비율
- **fixed effects**: sido FE + period FE (16 sido × 5 period)

### 5.2 First stage (z_x 결정 후)

$$\Delta_5 \text{Trade}_{h,t} = \alpha + \gamma \cdot \Delta_5 IV_{h,t} + X + \delta_t + \nu$$

IV = ADH-8 또는 KR-CN bilateral (PAP v4.0 § 3.3 branch decision).

### 5.3 Mediation (DGHP 2017 + DFH 2020 ivmediate, branch A × αm 시)

```stata
ssc install ivmediate weakivtest boottest rwolf
foreach cause in suicide_102 drug_101 psych_057 liver_081 {
    foreach mediator in marital_share education_share {
        ivmediate rate_per_100k_`cause' ///
            (`mediator' = z_m_lag) ///
            (trade_exposure = z_x_bartik), ///
            vce(cluster h_code)
    }
}
```

Total / Direct / Indirect 분해 + Imai-Yamamoto ρ sensitivity.

### 5.4 5-layer SE

| Layer | Method | Reference |
|-------|--------|-----------|
| 1 | HC1 robust | textbook |
| 2 | Wild cluster bootstrap, sigungu (n=229) | Cameron-Gelbach-Miller 2008 |
| 3 | Wild cluster bootstrap, sido (n=16, secondary) | small-cluster bias 1.3-1.5x |
| 4 | AKM clustered SE (shift-share specific) | Borusyak-Hull-Jaravel 2022 |
| 5 | Conley spatial SE | Conley 1999, 100km radius |

### 5.5 Weak-IV robust inference

- **Olea-Pflueger 2013 effective F**: cutoff 23.1 (Stock-Yogo 2005 의 robust 확장).
- **Anderson-Rubin** + **Lee-Moreira-McCrary-Porter 2022 tF**: F < 23.1 시 main inference 격상.

### 5.6 Multiple testing

**Romano-Wolf 2005 step-down (1000 bootstrap iterations)**:
- 4 main outcome (자살·약물·정신활성·간) × 2 mediator + 2 placebo (cardiovascular·cancer) = 10 hypotheses family
- FWE control, heterogeneity 는 exploratory 분류

---

## 6. Outcome variables + groupings

### 6.1 4 main outcomes

| 코드 | KCD-8 / ICD-10 | label | H1 부호 전망 | rationale |
|------|---------------|------|--------------|-----------|
| **102** | X60-X84 | 자살 | **+** | 실업 → despair → 자살 (Pierce-Schott 2020 mechanism) |
| **101** | X40-X49 | 약물중독사 (불의의) | **?** | 한국 ≠ 미국 opioid culture, 약한 시그널 |
| **057** | F10-F19 | 정신활성물질 정신·행동장애 | **?** | F17 (담배) 분리 불가 — sensitivity test 필요 |
| **081** | K70-K77 | 알코올성 + 일반 간질환 | **±** | 알코올 ↔ 대처기제 (trade ↑ → 간 ↑) vs 수출지역 ↑ → 간 ↓ |

### 6.2 Composite + placebo

- **despair_total** = 102 + 101 + 057 + 081 (composite robustness)
- **cardiovascular** (067-070, placebo, β = 0 expected, H1.4)
- **cancer** (027-047, placebo, β = 0 expected, H1.4)

### 6.3 Mediator-specific rate panels (Stage 5 input)

- **`mediator_specific_marital_rate_v01.parquet`** (187K rows) — 4 marital × 2 sex × 8 age × 6 cause × 5 period
- **`mediator_specific_education_rate_v01.parquet`** (172K rows) — 3 education × 동일

---

## 7. Limitations + R-A self-critique

### 7.1 8 known limitations (PAP v3.3-v3.4)

1. **1997-2007 외국인 분리 불가** — `nationality_code` 컬럼 2008+ 만. 외국인 사망 0.5% 이내 over-counting 추정.
2. **혼인·교육 unknown (코드 9) drop** — MAR 가정 (1997-2000 missing 율 높음, 2.5%/7%).
3. **교육 1997-2007 카테고리 collapse** — 5 → 3 카테고리. 전문대 vs 4년제 분해 손실.
4. **2022-2024 incomplete period drop** — 5-year stack 미충족 (3 년만).
5. **MDIS 2% 표본 가중치 ±5% 오차** — 행안부 인구 cross-check ±3% 검증 완료.
6. **Mediator panel denominator 결손 9.74%** — 67 h_code (1990 sigungu placeholder 잔여 의심) listwise deletion. R-A pending.
7. **2024 sigungu_crosswalk 미커버 252 h_code** — main analysis 1997-2021 에 무관.
8. **R-A v3.x sigungu code mapping audit errors** — Ansan 31090 vs 41190 등 정정 완료 (microdata h_name 검증).

### 7.2 R-A self-critique (`pap_v41_feedback.md`, 7 critical issues)

1. **H1 net-export 변수 conflation** — export-gain vs import-loss 두 채널 섞임. H1a (export → despair ↓) + H1b (import → despair ↑) 분리 권고 (DFS 2014 식).
2. **KR-CN bilateral endogeneity** — 한국 자체 무역량은 macro 동시결정. ADH-8 main 권고, weak-F 는 AR + tF 로 처리.
3. **Sparse cell 문제** — 영양·봉화 같은 <50K 시군구 cause-specific 사망 0-2/year. 미국 county avg 100K+ 와 비교 안 됨. 권고: (a) 50K+ 시군구 sample restriction, (b) Poisson regression main, (c) Rotemberg weight 사전 검정 (HHI ≤ 0.20).
4. **Pre-period data 부재** — KOSTAT mortality 1997+. PAP § 5.3 의 1990-1996 pre-trend 표는 *placeholder*. 권고: pre-period = 1997-2001 (pre-WTO) 로 재정의.
5. **Multiple testing 약함** — main 5 + hetero 6 + robustness 8 = ~240 tests. ad hoc Bonferroni → Romano-Wolf step-down (1000 reps) 으로 통합.
6. **Spillover spec vague** — § 7.3 의 β_m vs β_n decomposition (FNS 2026) 의 W matrix 미명시. row-normalize, self-exclude, distance decay 명시 필요.
7. **Scenario B contribution 약함** — β ≈ 0 시 paper contribution 모호. H1a + H1b 사전 분리로 보강.

---

## 8. Position vs. 4 anchor papers

| Anchor | 연구 setting | outcome | mediation | 본 paper 의 *novel contribution* |
|--------|-------------|---------|-----------|----------------------------------|
| **Pierce-Schott 2020 AERI** | US county (PNTR) | drug 사망 +, suicide·ARLD 무유의 | 없음 | **한국** + **가족 mediation** + **DGHP 2017 ivmediate** 첫 적용 |
| **Finkelstein-Notowidigdo-Shi 2026 BFI WP** | NAFTA × all-cause | 모든 사망원인 합계 | 없음 | **cause-specific 4 outcomes** + family channel |
| **Case-Deaton 2015 PNAS** | US white non-Hispanic | despair 개념 정의 | 없음 | **한국 4-outcome adaptation** (suicide+liver dominance 의 inverse pattern) + **individual-level 혼인코드** in mediation |
| **Hanson 2018** | US 결혼시장 | 결혼가치 하락 (생태학적) | 함축 (개체수준 X) | **MDIS individual-level 혼인코드 (1/2/3/4)** + **DGHP strict framework** |

### Unique contributions

1. **첫 한국 trade × mortality × mediator 통합 분석**.
2. **첫 DGHP 2017 + DFH 2020 ivmediate 한국 적용** (원전 DGHP = 독일 trade × 정치투표).
3. **Korea-US dominance contrast** — 한국 suicide+liver vs 미국 drug, Case-Deaton 2015.
4. **Individual-level marital/education codes** in mediation (Hanson 2018 = 생태학적 only).
5. **Pre-committed 2-instrument framework** (PAP v4.0) — mediation 식별 가정 transparent.
6. **5-year stacked first-difference** (Pierce-Schott 2020 spec) on 229 시군구 panel.

---

## 9. Current progress + pending

### 9.1 ✅ 완료

- Stage 1-3 main outcome panel (123,660 rows × 229 h_code × 27 year × 10 outcome × 3 ASR baseline)
- Stage Mediator (5 parquet, marital + education panel build)
- Stage 4 partial: Comtrade KR-CN + ADH-8 + CN-World + BACI + researchall HS-KSIC + KSIC chain
- z_m_marital instrument (MDIS 1995 census, 247 시군구 cohort sex ratio)
- z_m_education instrument (namuwiki 233 → 175 학교, 251 시군구 distance)
- ECOS Test 1 macro 변수 + WEO Test 1b
- **PAP v4.0 unified identification protocol commit 직전**

### 9.2 ⏳ 진행 중 / 차단

- **Bartik 1990 baseline industry share** (광업제조업조사 1994 microdata 의 KSIC 4-digit 추출) — 다음 turn
- **Comtrade KR-CN 1995-1999** (Test 2 pre-WTO, 사용자 진행 중)
- **Stata 환경 verify** (가천대 license + 7 packages: ivmediate, weakivtest, boottest, rwolf, reg_ss, acreg, weakiv)
- **denom missing 67 h_code 진단** (R-A pending)
- **PAP v3.4 → v4.0 main body commit** (R-A 직접 작업 ~3h)

### 9.3 다음 4 phase (PAP v4.0 § 7)

- **Phase B-x**: z_x 진단 (Test 1, 1b, 2, 3 + first-stage F) — *다음 turn 즉시 시작 가능*
- **Phase B-m**: z_m 진단 (Test 4, 5, 6) — 데이터 ready, *다음 turn 즉시 시작 가능*
- **Phase B-SI**: Sequential Ignorability ρ ∈ ±0.3 sensitivity — Imai-Yamamoto medsens
- **Phase C**: Joint branch commit (PAP v4.0 § 5 표 매핑) — *결정 timestamp 후* Stage 5 진입
- **Phase D**: Stage 5 ivmediate 회귀 + 5-layer SE + Romano-Wolf

---

## 10. 외부 reviewer 에게 요청하는 feedback 항목

### P1 (식별·측정 자체가 흔들리는 이슈)

- z_x branch decision tree 의 분기 4 + z_m 분기 3 + SI 분기 = 12+ branches 가 *모두 사전 commit* 인 점이 reviewer 가 받아들일 만한가?
- z_m_marital (출생 성비 cohort lag) 의 *exclusion restriction* (sex ratio → marriage market → mortality 만) 변호가 충분한가? *다른 채널* (예: sex ratio → 폭력 발생률 → 자살·외상사 직접) 가능성 검토 필요.
- z_m_education (distance-to-college) 의 *외생성* 이 1990 baseline 으로 충분한가? 1990-2024 사이 신설 대학 89개 (KESS 196 vs yunbo 1990 107) 가 *trade-shock 시점 (2001 이후)* endogenous 인지 검토 필요.
- 4년제 175 학교의 시군구 매핑 32 매칭 실패 (안양시·수원시 등 통합시 보강 필요) — 이게 결과 영향 미치는가?
- PAP v3.4 main body 가 v4.0 protocol 과 *완전 정합* 되어 있는가? (commit 작업 미완)

### P2 (제출 전 보강)

- Net-export framing → H1a (export) + H1b (import) 분리 — 본 paper 의 *core contribution* (export 채널 보호효과 가설) 와 정합?
- Sparse cell 문제 — 50K+ 시군구 sample restriction main vs Poisson regression main 중 어느 쪽이 *학술적으로 표준*?
- Pre-period 1995-1999 (4 년) 가 Pierce-Schott 식 pre-trend test power 에 충분한가? 1997 IMF 위기 confound 처리?
- F17 (담배) 분리 불가 — 057 (F10-F19) 의 sensitivity test 가 *robustness items* 에 포함됐는가? (stage5_regression_plan § 9 의 11 항)
- Multiple testing — 4 main + 2 placebo 만 confirmatory family 로 두고 hetero 8 + robustness 6 은 exploratory 분리 정합?

### P3 (polish)

- 26-entry reference list 의 13 인용 정확성 (DFH 2020 vs DGHP 2017 NBER 번호 정정 완료, 추가 검토 필요)
- KSIC chain (8→9→10→11) 의 시기별 연결 (1994-2006 = 8차, 2007-2016 = 9차, 2017-2023 = 10차, 2024+ = 11차) 매핑 robust?
- 1995 census 만으로 z_m_marital main + 1985/1990 census robustness 가 *학술적으로 충분*?
- Section 1-8 본문 작성 시 *Korean+English bilingual* 전략? SSCI 제출 시 영문 only?

---

## 11. Reviewer feedback 작성 가이드

본 문서를 보고 다음 형식으로 critique 부탁드립니다:

1. **P1/P2/P3 분류** — 각 issue 의 우선순위
2. **위치 명시** — 어느 section / equation / table reference?
3. **근거** — 학술 reference 또는 본인 경험
4. **합리적 해결방향** — 단정적 결론 X, 옵션 제시

본 paper 는 **PAP v4.0 protocol pre-registration commit 직전** 상태이므로, *식별 가정* 과 *변수 정의* 의 사전 commit 이 가장 critical. *계량 결과* 는 아직 없습니다 (Stage 5 진입 전).

---

_Total: ~3,500 words. Audience: PhD-level labor·health economists, SSCI Q1 reviewers._

_저자: 정재헌 + R-A (Claude LLM, R-A 가 orchestration, R-A 가 코딩, 사용자가 실행)_
_작성: 2026-05-04_
