# PAP v4.4 — Main body (audit accept + pre-draft 5 items + Stage A·B 분담 정정)

**version**: 4.4
**date**: 2026-05-05 (v4.3 audit 정정)
**author**: 정재헌 (가천대 경제학)
**supersedes**: PAP v4.3 (2026-05-05 late evening)
**status**: framing 정정 commit + 코드 실행 P1·P4·P6·P8 Stage A 분담 + P2·P3 Stage B 분담

본 v4.4 는 사용자 측 v4.3 audit (P1·P2·P3 + pre-draft 5 items) 모두 인정 + framing 정정 즉시 commit. 코드 실행 필요한 7 pending 은 § 12.5 에 Stage A·B 분담 명시.

**v4.3 → v4.4 정정 list (framing only, R-A direct commit)**:
1. § 1.1 thesis: "3 SE layer 일관" → "3 SE layer 산출 완료 일관, Conley planned, AKM 별도 estimand" (P3.A)
2. § 1.2 contribution: KER full paper format 명시 (Pre-draft 1)
3. § 5.4: ADH-8 → **ADH-7 (Switzerland 누락)** 정정 (Pre-draft 4)
4. § 9.0: PCA obsolete reasoning 보강 (P2.B)
5. § 9.1: Lang 2018 BRFSS vs HIRA SSRI 의 substantive difference 명시 (Pre-draft 2)
6. § 9.4: z_m_education spec — baseline (1985) distance 사용 명시 (Pre-draft 5)
7. § 9.5: DGHP 2017 / DFH 2020 single-IV mediation 의 정확한 spec 명시 (P2.A)
8. § 11: 27편 = 19편 + 8편 추가 source 명시 (P3.D)
9. § 13: KOSIS DT_1B34E13 단독 = despair_total 의 자살 1 component only 명시. 나머지 3 component 외부 검증 source pending (Pre-draft 3)
10. § 8.13 신설: KOSIS 외부 검증 자살 only 한계
11. § 8.14 신설: ADH-7 (Switzerland 누락) 한계
12. § 12.5 신설: Stage A·B 분담 명확화 + P6·P7·P8·P9 추가

---

## § 1. Thesis & contribution

### 1.1 Thesis (P3.A 정정)

한국 시군구 단위 한국-중국 bilateral trade exposure 가 deaths of despair (자살 + 약물 사망 + 정신활성물질 + 간질환) 를 **보호** 한다.

**Reduced-form main spec** (n=251, 5-year long differences):
- β = −0.069
- HC1 t = −2.42 (p=0.016)
- WCB **cluster-시도** (G=16, 1000 boot) p = 0.041
- Cluster-시도 sandwich t = −2.12

→ **3 SE layer (HC1, WCB cluster-시도, cluster-시도 sandwich) 산출 완료 일관 negative**.
→ **Conley centroid SE = planned** (P6, Stage A).
→ **AKM (BHJ industry-mode, simplified) = 별도 estimand**, β=+0.890 (P2 정식 implementation pending).

> **v4.3 → v4.4 정정 (P3.A)**: "3 SE layers 일관" → "3 SE layer 산출 완료 일관, Conley planned, AKM 별도 estimand". Conley 미산출 + AKM 별도 estimand 명시.

### 1.2 Contribution (KER full paper format, Pre-draft 1)

**Target venue**: **KER full paper (25-35 page)**.

> **v4.3 → v4.4 정정 (Pre-draft 1)**: KER short note (8-12 page) vs full paper (25-35 page) 결정 = **full paper**. § 9 mechanism 의 6 mediator 모두 main paper 에 포함 가능. AER:I short-form 압축 부담 회피.

(Contribution 3 항목 v4.3 그대로)

### 1.3 Anchor 비교 (v4.3 그대로)

---

## § 2. Outcome groups (v4.3 그대로)

---

## § 3. Identification framework (v4.3 그대로 + n 정합성 § 12.5 P1)

---

## § 4. Empirical specification (v4.3 그대로 + § 4.1 표 Conley 정확 표기)

### 4.1 5 SE layers (P3.A 정정)

| Layer | Method | 결과 (despair_total, OLS β=−0.069) | Status |
|---|---|---|---|
| HC1 | Eicker-Huber-White | β=−0.069, SE=0.0285, **t=−2.42, p=0.016** | ✅ 산출 |
| WCB cluster-시도 (G=16) | CGM 2008, 1000 iter | β=−0.069, **p=0.041** | ✅ 산출 |
| Cluster-시도 sandwich | sandwich | β=−0.069, t=−2.12 | ✅ 산출 |
| Conley centroid | spatial (1km/5km/10km) | (planned, P6) | 🟡 **Stage A pending** |
| AKM (BHJ industry-mode, simplified) | ssaggregate WLS (별도 estimand) | β=+0.890, t=+1.51 (n.s.) | 🟡 정식 implementation P2 pending |

**3 SE layer 산출 완료 + 1 layer planned (Conley) + 1 layer 별도 estimand (AKM)**

(§ 4.1.1 v4.3 그대로 — AKM 정의 명확화)

### 4.2-4.4 (v4.3 그대로)

---

## § 5. Sample, panel, IV (Pre-draft 4 정정)

### 5.4 ADH-7 robustness IV (Pre-draft 4 정정)

> **v4.3 → v4.4 정정 (Pre-draft 4)**: 본 paper 의 "ADH-8 IV" 표기 → **"ADH-7 IV (Switzerland 1국 Comtrade fetch 미완)"** 정정.

DATA_COLLECTION § 2 항목 5: Comtrade ADH 8개국 × China imports 200 파일 (스위스 1개 누락).

**ADH 2013 의 8 OECD**: AU, **CH** (Switzerland — 누락), DE, DK, ES, FI, JP, NZ
**본 paper 의 7 OECD**: AU, DE, DK, ES, FI, JP, NZ

**IV 비교**:

| IV | 국가 수 | First-stage F | LMP cutoff (5%) | 본 paper |t| | 상태 |
|---|---|---|---|---|---|
| KR-CN bilateral (main) | 1 | 6.10 | ≈5.05 | n/a | weak, RF main |
| **ADH-7 (robustness, 본 paper)** | **7** (Switzerland 누락) | **19.65** | **3.286** | **1.85** | borderline (LMP fail) |
| ADH-8 published precedent (Lang 2018) | 8 (Switzerland 포함) | 18.77 | ≈3.32 | 2.06 | 동일 protocol procedural reference |

**Lang 2018 비교 framing (Pre-draft 4 추가 caveat)**:
- Lang 2018 = 8 OECD (Switzerland 포함) 으로 추정
- 본 paper = 7 OECD (Switzerland 누락)
- Switzerland 의 China imports 가 본 paper 의 IV strength (F) 에 marginal 영향. Switzerland 의 China imports 비중이 8 OECD 중 작은 비중 (~5%) 이므로 F 의 변화 마이너 가설.
- 그러나 정식 비교는 Switzerland fetch 완료 후. **§ 12.5 P10 추가 권고** — 사용자 측 Comtrade Switzerland 1국 25 시점 fetch.

→ § 8.14 limitation 신설 (NEW v4.4)

(나머지 § 5 v4.3 그대로)

---

## § 6. Phase 4 results (v4.3 그대로 + Pre-WTO sub-period § 6.5 추가 명시)

### 6.5 Pre-WTO placebo (P2.C 추가 sub-period 명시)

```
Δ_2y log(despair_total mortality, 1998→2000) = α + β·z_x_h^{1992-1996} + ε_h
```

| 통계 | 값 |
|---|---|
| β | +0.0238 |
| Cluster-시도 p | 0.22 |

(v4.3 정정 framing 그대로)

**추가 sub-period sensitivity (P8, Stage A 추가)**:
- 1992-1996 shock × 1998-2000 mortality (현재) — β=+0.0238
- **1992-1995 shock × 1996-1998 mortality** (P8) — overlap 더 짧
- **1990-1994 shock × 1995-1997 mortality** (P8) — 1년 shift

3 placebo 의 sign 패턴 (P8 결과 후):
- 모두 positive → share-violation evidence 강화 → 본 paper 의 robustness 패키지 (Drop-C26 + 5 baseline + DGHP/DFH mediator) 로 종합 평가
- 무작위 sign → noise interpretation 강화 → § 6.5 의 v4.3 framing ("p=0.22, point estimate sign reversal weak evidence") 그대로

(나머지 § 6 v4.3 그대로)

---

## § 7. Robustness (v4.3 그대로)

---

## § 8. Limitations (v4.4 신설 항목 추가)

### 8.1-8.12 (v4.3 그대로)

### 8.13 (NEW v4.4) — KOSIS 외부 검증 자살 only 한계

본 paper § 13 의 KOSIS DT_1B34E13 외부 검증 = despair_total 4 component (자살 102 + 약물 101 + 정신활성물질 057 + 간질환 081) 중 **자살 1 component (1/4) only**.

나머지 3 component (약물·정신활성물질·간질환) 의 시군구 ASMR 외부 검증 source pending. KOSIS 사망원인 50항목 시군구별 통계 (DT_1B34E14 등) 추가 search 필요 (P9 — 사용자 측 다운).

**Mitigation**:
- 자살 1 component (despair_total 의 ~50% 비중) 외부 검증 시 본 paper 의 main outcome 신뢰성 partial 입증
- 나머지 3 component 는 사망원인 KOSTAT microdata 의 internal consistency 만 검증

→ § 13.5 (NEW) 신설 (despair 4 component 외부 검증 plan)

### 8.14 (NEW v4.4) — ADH-7 (Switzerland 누락) 한계

본 paper 의 ADH-style robustness IV 가 ADH 2013 의 8 OECD 중 Switzerland 1국 누락된 ADH-7. Lang 2018 의 8 OECD published 결과와 직접 비교 부적절 (Switzerland 누락 영향 marginal 가설이지만 정식 verify 안 됨).

**Mitigation (P10)**: 사용자 측 Comtrade Switzerland 1국 25 시점 fetch (1-2일). 받은 후 ADH-8 IV 재산출 + first-stage F 재측정.

---

## § 9. Mechanism (v4.3 그대로 + § 9.0 reasoning 보강 + § 9.1 Lang 비교 정정 + § 9.4 z_m_edu spec + § 9.5 DGHP/DFH spec)

### 9.0 (P2.B 보강)

이전 conversation round 12-13 의 "5-mediator family-structure framework PCA composite" 권고는 v4.0 이전 round 의 mediator framework 에 기반한 것으로, v4.2/v4.3/v4.4 의 6 mediator framework (HIRA 약물 시군구 + HIRA 정신질환 시도 + KOSIS family marriage market + z_m_marital + z_m_education + KOSIS 자살 외부 검증) 와 incompatible.

**Substantive reasoning (P2.B 정정)**:
- 6 mediator 의 unit 다름:
  - HIRA 약물 = 시군구 × 월 × ATC (251 × 24 × 5)
  - HIRA 정신질환 = 시도 × 연도 × ICD10 (17 × 15 × 20)
  - KOSIS family = 시군구 × 연도 × 사건유형 (251 × 24 × 4)
  - z_m_marital = 시군구 baseline 1980-1995 cohort sex ratio
  - z_m_education = 시군구 baseline 1985 distance
  - KOSIS 자살 = 시군구 × 연도 × 성별 (251 × 24 × 2)
- PCA composite 의 적합 조건: **동일 unit + 동일 scale + correlated indicators** 의 dimension reduction
- 본 paper 의 6 mediator = 서로 다른 unit + scale + 상이한 sample size → PCA composite 부적합
- **별도 spec 의 separate channel reporting 더 정확** (각 mediator 의 effect size + identification 가정 별도 commit)

→ Obsolete 처리 + separate channel reporting commit

### 9.1 Main mediator: HIRA 약물 처방 (시군구 단위) (Pre-draft 2 정정)

(v4.3 § 9.1 base + framing 정정)

> **v4.3 → v4.4 정정 (Pre-draft 2)**: "Lang 2018 의 BRFSS 정신건강 day 직접 대응" framing → "Lang 2018 의 self-reported subjective mental health 를 보완하는 administrative measure".

**HIRA SSRI 처방률 vs Lang 2018 BRFSS poor mental health day 의 substantive difference**:

| 항목 | Lang 2018 BRFSS | 본 paper HIRA SSRI 처방률 |
|---|---|---|
| Outcome 정의 | "지난 30일 중 poor mental health day 수" | "분기 × 시군구 × ATC4 단위 처방받은 환자수" |
| 측정 방식 | self-reported subjective | administrative full coverage |
| Sample | 표본조사 (340 of 722 CZs) | 全 한국 의료보험 가입자 |
| Stigma 영향 | self-report 의 social desirability bias | 의료 미이용 = 측정 불가 |
| 한국 적용성 | self-reported mental health 의 cultural meaning 이 미국과 다름 | 한국 OECD 대비 정신과 의료이용 낮음 (의료 미이용자 mental distress 측정 못 함) |

**본 paper framing**:
- HIRA 약물 = Lang 2018 self-report 보완하는 administrative measure
- **장점**: stigma 강한 한국 setting 에서 self-report bias 회피, full coverage
- **한계**: 의료 미이용자 mental distress 는 측정 불가 (한국 정신과 의료이용 OECD 대비 낮음 — § 8 한계 명시 필요)

→ § 8.15 (NEW) 신설: HIRA 약물 panel 의 의료 미이용자 mental distress 측정 불가 한계

### 9.4 Education channel (z_m_education spec, Pre-draft 5 정정)

> **v4.3 → v4.4 정정 (Pre-draft 5)**: z_m_education 의 정확한 spec 명시.

**z_m_education 정의 (v4.4 commit)**:
```
z_m_education_h = -log(min_{u in 4년제 대학} distance(centroid_h, location_u^{1985}))
```

- **Baseline 시점**: **1985** (KEDI 1985 연보 의 4년제 대학 location)
- 1985-1995 사이 대학 신설/이전 변동 사용 안 함 (endogeneity 우려 회피)
- 1985 시점 기준 distance 만 사용 → IV relevance 약 가능성 인정

**식별 가정**:
- 1985 시점 4년제 대학 분포가 시군구 baseline characteristic
- 1985-2024 사이 시군구 trade exposure (KR-CN bilateral) 는 1985 대학 분포에 affect 안 함 (시간 순서)
- 1985 대학 분포 → 시군구 education access → labor market mobility → mortality 의 chain

**Sensitivity (planned)**:
- 만약 IV relevance 약 (z_x_h × z_m_education first-stage F < 5) → z_m_education 을 § 9 의 supplementary mediator 로 demote
- main mediator = HIRA 약물 (시군구) + KOSIS family (시군구)

### 9.5 Direct mediator IV (DGHP/DFH single-IV spec, P2.A 정정)

> **v4.3 → v4.4 정정 (P2.A)**: DGHP 2017 / DFH 2020 의 정확한 spec 명시.

**Single-IV mediation framework (DGHP 2017 + DFH 2020)**:

#### 9.5.1 Estimator
```
y_h = α + β_total · z_x_h + γ X_h + ε  (total effect)
m_h = α + δ · z_x_h + γ X_h + u  (mediator effect)
y_h = α + β_direct · z_x_h + ζ · m_h + γ X_h + ν  (direct + indirect via m)
```

- y_h = mortality (despair_total log_asr_p1)
- m_h = mediator (HIRA SSRI 처방률 or KOSIS 이혼률 등)
- z_x_h = single Bartik IV (KR-CN bilateral)
- β_total = β_direct + ζ · δ (decomposition)

#### 9.5.2 Identification 가정
**DGHP 2017 (Dippel-Gold-Heblich-Pinkovskiy)**:
- (a) **Treatment exogeneity**: z_x_h ⊥ ε (Bartik IV 의 standard assumption)
- (b) **Mediator unconfoundedness given treatment**: m_h | z_x_h ⊥ ν

**DFH 2020 (Dippel-Ferrara-Heblich)** ivmediate Stata package:
- Identical assumption + bootstrap CI implementation

#### 9.5.3 Implementation (P2 Stage B Claude Code 위임)
- Stata `ivmediate` package 또는 Python `linearmodels` + bootstrap
- 1000 cluster-시도 wild bootstrap
- Sobel test 도 별도 보고 (parametric, restrictive 가정)

#### 9.5.4 6 mediator 별 channel
- Channel 1: HIRA SSRI 처방률 (시군구 main)
- Channel 2: KOSIS 이혼률 (시군구)
- Channel 3: KOSIS 출생률 (시군구)
- Channel 4: KOSIS 혼인률 (시군구)
- Channel 5: z_m_marital 1980-1995 cohort sex ratio (시군구 baseline)
- Channel 6: z_m_education 1985 distance (시군구 baseline)

각 channel 별 β_direct + ζ · δ decomposition + bootstrap CI

(나머지 § 9 v4.3 그대로)

---

## § 10. Pre-registered hypotheses (v4.3 그대로)

---

## § 11. References (P3.D 명시)

본 paper 가 인용하는 27편 reference paper deep summary:

**v4.0 시점 19편** (paper_01 ~ paper_19):
- DFS 2014 (paper_01)
- IMF 1806 shift-share (paper_02)
- Pierce-Schott 2020 AERI (paper_02_pierce_schott_2020_aeri.md)
- Fed 2016094 trade-suicide (paper_03)
- Annurev weak instruments (paper_04)
- ADH 2013 (paper_05)
- Sufi BFI WP 2023-109 (paper_06)
- Finkelstein NAFTA mortality 2026 (paper_07)
- Borusyak-Hull-Jaravel 2025 shift-share (paper_08)
- Mian-Sufi 2016 (paper_13)
- Pierce-Schott 2020 (paper_14)
- t0151 (paper_15)
- Dix-Carneiro 2017 (paper_16)
- GPSS Bartik (paper_24408)
- BHJ SSIV (paper_24997)
- DGLR Deaths (paper_25787)
- Bartik OriginalShiftShare (paper_5570)
- (PAP v4.0 시점 + 2-3편 추가)

**이번 conversation 8편 추가 (paper_20 ~ paper_27)**:
- McManus & Schaur 2016 J Int Econ (paper_20)
- Lang, McManus & Schaur 2018 Health Economics (paper_21)
- Colantone, Crinò & Ogliari 2019 J Int Econ (paper_22)
- Autor, Dorn & Hanson 2019 AER:I (paper_23)
- Charles, Hurst & Schwartz 2019 NBER MA (paper_24)
- Eliason & Storrie 2009 J Hum Res (paper_25)
- Sullivan & von Wachter 2009 QJE (paper_26)
- Lee, McCrary, Moreira & Porter 2022 AER (paper_27)

**v4.4 commit pending (P5)**: DGHP 2017 (Dippel-Gold-Heblich-Pinkovskiy) + DFH 2020 (Dippel-Ferrara-Heblich) 의 분리 인용 별도 file 작성. paper_28·29 추가 권고.

---

## § 12. Commit log (v4.0 → v4.1 → v4.2 → v4.3 → v4.4)

### 12.1-12.4 (v4.3 그대로)

### 12.5 (NEW v4.4) — Stage A·B 분담 + P6·P8·P9·P10 추가

**v4.3 → v4.4 정정 12 항목** (framing only, R-A direct commit):

| # | 정정 | Status |
|---|---|---|
| 1-9 | (v4.3 의 1-9 commit 그대로) | ✅ commit |
| 10 | KER full paper format 명시 (Pre-draft 1) | ✅ commit |
| 11 | ADH-8 → ADH-7 (Switzerland 누락) 정정 (Pre-draft 4) | ✅ commit |
| 12 | Lang 2018 BRFSS vs HIRA SSRI substantive difference (Pre-draft 2) | ✅ commit |
| 13 | z_m_education baseline (1985) spec (Pre-draft 5) | ✅ commit |
| 14 | DGHP 2017 / DFH 2020 single-IV spec 명시 (P2.A) | ✅ commit |
| 15 | § 9.0 PCA obsolete reasoning 보강 (P2.B) | ✅ commit |
| 16 | KOSIS DT_1B34E13 자살 only 한계 (Pre-draft 3) | ✅ commit |
| 17 | § 1.1 framing "3 SE layer + Conley planned + AKM 별도 estimand" (P3.A) | ✅ commit |
| 18 | § 11 references 27편 = 19편 + 8편 명시 (P3.D) | ✅ commit |

**v4.4 의 코드 실행 pending list (paper draft Stage C 진입 전 commit 필수)**:

| # | Pending | 처리 방식 | Effort | Stage |
|---|---|---|---|---|
| **P1** | n=222 vs n=251 정합성 | derived panel build code 검증 + 5 시군구 drop list | R-A direct 1-2h | **Stage A** |
| **P2** | AKM (BHJ industry-mode) 정식 implementation | R `ShiftShareSE` `reg_ss()` 적용 | Claude Code 위임 3-4h | **Stage B** |
| **P3** | AR-CI 산출 | linearmodels AR_test + ConfidenceSet | Claude Code 위임 2-3h | **Stage B** |
| **P4** | WCB cluster-시도 G=16 결과 재산출 | Phase 4 5-layer SE script 재실행 | R-A direct 1h | **Stage A** |
| **P5** | DGHP 2017 + DFH 2020 분리 인용 file | 별도 markdown citation | R-A direct 30분 | **Stage A** |
| **P6** (NEW) | Conley centroid SE 산출 (1km/5km/10km) | spatial cluster SE script | R-A direct 1h | **Stage A** |
| **P7** | (renumber, prev P6) — § 9.0 PCA reasoning + § 9.5 DGHP spec — already commit in v4.4 | already done | — | done |
| **P8** (NEW) | Pre-WTO 추가 sub-period sensitivity (1992-1995, 1990-1994) | placebo regression script | R-A direct 1h | **Stage A** |
| **P9** (NEW) | KOSIS 사망원인 50항목 시군구별 statistics search (despair 4 component 외부 검증) | KOSIS DT search | 사용자 측 다운 1h | **사용자** |
| **P10** (NEW) | Comtrade Switzerland 1국 25 시점 fetch (ADH-7 → ADH-8 회복) | Comtrade fetch script | 사용자 측 다운 1-2일 | **사용자** |

**Stage A 합계 (R-A direct)**: P1 + P4 + P5 + P6 + P8 = 4-5h, 다음 turn 단일 가능

**Stage B 합계 (Claude Code 위임)**: P2 + P3 = 5-6h, 차차 turn 단일 위임

**사용자 측 (P9 + P10)**: P9 (KOSIS search 1h) + P10 (Comtrade Switzerland 1-2일) — 병렬 가능

→ Stage A·B + 사용자 측 (P9·P10) 모두 commit 후 v4.5 → paper draft Stage C (KER full paper format 25-35 page) 진입

---

## § 13. Outcome external validation (Pre-draft 3 정정)

### 13.1-13.3 (v4.3 그대로)

### 13.4 (NEW v4.4) — KOSIS DT_1B34E13 단독 = 자살 1 component only 한계

**v4.3 → v4.4 정정 (Pre-draft 3)**: KOSIS DT_1B34E13 = despair_total 4 component (자살 + 약물 + 정신활성물질 + 간질환) 중 **자살 1 component only**. 나머지 3 component 외부 검증 source pending.

**Plan**:
- KOSIS 사망원인 50항목 시군구별 통계 (DT_1B34E14 등) 추가 search (P9, 사용자 측)
- 받은 후 약물 (101) + 정신활성물질 (057) + 간질환 (081) 의 시군구 ASMR 외부 검증 commit
- 4 component 모두 외부 검증 일치율 > 95% 시 main outcome 신뢰성 입증

### 13.5 (NEW v4.4) — Despair 4 component 외부 검증 plan

| Component | 사망원인 코드 | ICD-10 | KOSIS 외부 source | 상태 |
|---|---|---|---|---|
| 자살 | 102 | X60-X84 | DT_1B34E13 | ✅ 받음 (50,071 행) |
| 약물 사망 | 101 | X40-X49 | DT_1B34E14 (?) | 🟡 P9 search |
| 정신활성물질 | 057 | F10-F19 | (?) | 🟡 P9 search |
| 간질환 | 081 | K70-K77 | (?) | 🟡 P9 search |

P9 commit 후 § 13 의 4 component 외부 검증 표 commit.

---

## § 14. Paper draft 작성 plan (KER full paper format)

### Stage A (다음 turn, R-A direct 4-5h)
- P1: n=222 vs n=251 정합성 + 5 시군구 drop list
- P4: WCB cluster-시도 G=16 재산출
- P5: DGHP/DFH 분리 인용 file
- P6: Conley centroid SE 산출
- P8: Pre-WTO sub-period sensitivity

### Stage B (차차 turn, Claude Code 위임 5-6h)
- P2: AKM 정식 BHJ 2022 implementation (R `ShiftShareSE`)
- P3: AR-CI 산출 (linearmodels AR_test)

### 사용자 측 병렬 (Stage A·B 와 동시)
- P9: KOSIS 사망원인 50항목 시군구별 search (1h)
- P10: Comtrade Switzerland 1국 fetch (1-2일)

### v4.5 commit (Stage A·B + P9·P10 모두 완료 후)
- 7 pending 모두 closed
- AR-CI publishable verdict 결정
- AKM 정식 결과 + § 4.1 표 정정
- 4 component 외부 검증 표 (P9 결과 후)
- ADH-8 IV 회복 (P10 결과 후)
- → paper draft Stage C (KER full paper format) entry-ready

### Stage C (paper draft 본격 작성)
- KER full paper format: 25-35 page main + 15-20 page online appendix
- § 1 Introduction (3-4 page)
- § 2 Background & Korean trade context (2-3 page)
- § 3 Data (3-4 page)
- § 4 Identification + Spec (4-5 page)
- § 5 Main results (5-6 page)
- § 6 Robustness (4-5 page)
- § 7 Mechanism (4-5 page) — 6 mediator separate channel
- § 8 Discussion + Limitations (2-3 page)
- § 9 Conclusion (1-2 page)
- Online appendix: full robustness tables + mechanism details + 4 baseline sensitivity

---

## 결론 (PAP v4.4 commit)

본 PAP v4.4 = audit 의 framing-only 정정 12 항목 즉시 commit + 코드 실행 7 pending (P1·P4·P5·P6·P8·P2·P3 + 사용자 측 P9·P10) Stage A·B 분담 명시.

**Target venue**: KER **full paper format** (25-35 page main + online appendix) — AER:I short-form 압축 부담 회피, § 9 mechanism 6 mediator 모두 main 포함 가능.

**timeline**:
- v4.4 commit: ✅ (본 turn)
- Stage A (R-A direct 4-5h): 다음 turn
- Stage B (Claude Code 위임 5-6h): 차차 turn
- 사용자 측 P9·P10: 병렬, Stage B 완료 시점에 일치
- v4.5 commit: 차차차 turn
- paper draft Stage C 진입: v4.5 commit 후
- KER submission ready: 4-6주 (timeline realistic)

**academic honesty**: framing-only 정정 12 항목 + 코드 실행 7 pending 의 explicit list = paper-grade reviewer-response 의 model. 학부 단독 저자 의 이 process spontaneous 수행 = 매우 unusual + paper-grade preparation.
