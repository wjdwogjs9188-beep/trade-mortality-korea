# Trade × Mortality Korea — Paper Writing Plan v01

**Author**: 정재헌 (가천대학교, 단독 저자)
**Date**: 2026-05-05
**Status**: Phase 4 publishable result 확보 완료, 27편 reference library 정비 완료, PAP v4.2 anchor reframing plan 완성
**Goal**: 박사논문급 single-authored 무역×사망 paper 의 first complete draft 까지 명확한 roadmap

---

## 1. 목표 venue 결정 (가장 중요한 첫 결정)

### Tier matrix

| Venue | Tier | 적합도 | 요구사항 |
|---|---|---|---|
| **KER (Korean Economic Review)** | T2 | ⭐⭐⭐⭐⭐ | 한국 영문 영문 review; 학부 단독저자 가능; 무역 + 사망 niche fit |
| **Health Economics (Wiley)** | T2 | ⭐⭐⭐⭐⭐ | Lang-McManus-Schaur 2018 가 published; F=19 weak-IV 통과 precedent |
| **EER (European Economic Review)** | T1 | ⭐⭐⭐⭐ | 무역 × 노동 broad fit; EU-anchored 비교 가능 |
| **JIE (Journal of International Economics)** | T1 | ⭐⭐⭐⭐ | McManus-Schaur, Colantone published; trade focus |
| **JHE (Journal of Health Economics)** | T1 | ⭐⭐⭐ | Eliason-Storrie 2009 sister; mortality outcome fit |
| **JEEA (Journal of European Economic Association)** | T0.5 | ⭐⭐ | 학부 단독 risk; reviewer harsh |
| **AER:Insights** | T0 | ⭐ | 학부 단독 + Korea data 의 AER:I 진입 어려움 |

### R-A 권장 dual-track strategy

**Track A (primary)**: **KER 또는 Health Economics (Wiley)** — first submission
- 이유: Lang 2018 의 F=18.77 published precedent. 본 paper 의 F=19.65 + Pre-WTO placebo PASS + Drop-C26 robust = 동등한 publishing case.
- 학부 단독 저자 risk 감안.
- 6-9개월 내 first decision 가능.

**Track B (rejected 또는 R&R 시)**: **EER 또는 JIE** — re-submission
- 한국이 export-driven economy 인 contribution 강조. DFS 2014 frame.
- Reviewer pushback (e.g., "F<23.1 reject") 에 LMP 2022 + Lang 2018 precedent 로 response.

**Track C (Track A R&R + LMP threshold 달성 시)**: **JEEA 또는 RES** — long-shot

### 결정 deadline
- **Now**: Track A target 잠정 결정
- **PAP v4.2 main body 완성 후**: 다시 evaluation
- **First draft 완성 후**: final 결정 + cover letter

---

## 2. Paper 구조 (AER-style, 30-40 page)

```
§ 1. Introduction (4-5 pp)
§ 2. Related Literature & Korean Context (3 pp)
§ 3. Data (3-4 pp)
§ 4. Identification Strategy (4-5 pp)
§ 5. Empirical Specification (3-4 pp)
§ 6. Descriptive Evidence (3-4 pp)
§ 7. Main Results (5-6 pp)
§ 8. Robustness (4-5 pp)
§ 9. Mechanism (3-4 pp)
§ 10. Limitations & Discussion (2-3 pp)
§ 11. Conclusion (1-2 pp)
References (3-4 pp, ~50-60 cites)
Appendix (Online, 15-20 pp)
```

**Total**: main 35-40 pp, online appendix 15-20 pp

---

## 3. 작성 순서 (results-first, AER convention)

### Stage A: Results 안정화 (먼저 완료)
**왜 이 순서**: 만약 § 5 spec 이 § 7 결과 와 align 안 하면 § 1 narrative 가 무너짐. Result-first 확정 후 narrative 작성.

1. **§ 7 Main Results** — Phase 4 publishable spec 의 master regression table
2. **§ 5 Empirical Specification** — § 7 의 spec 정확 기술
3. **§ 4 Identification Strategy** — § 5 spec 정당화
4. **§ 8 Robustness** — Drop-C26, Pre-WTO placebo, IV vs RF 모두 요약
5. **§ 9 Mechanism** — z_m_marital + z_m_education ivmediate (현재 진행 중)

### Stage B: Setup 작성
6. **§ 3 Data** — KOSTAT mortality, KOSIS population, 광업제조업조사, Comtrade
7. **§ 6 Descriptive Evidence** — figures (event-study, choropleth)
8. **§ 2 Related Literature** — 27편 reference library 의 narrative 통합

### Stage C: Wrapping (마지막)
9. **§ 1 Introduction** — main contribution + result preview (Stage A 완료 후 precise)
10. **§ 10 Limitations & Discussion**
11. **§ 11 Conclusion**

### Stage D: Polish
12. Online appendix
13. Bibliography
14. Cover letter
15. Response to reviewer (if R&R)

---

## 4. Section-by-section content plan

### § 1 Introduction (4-5 pp, write last)

**Para 1** (motivation): Trade × deaths of despair 의 stylized fact
- US: ADH 2019, Pierce-Schott 2020, Charles-Hurst-Schwartz 2019 — manufacturing decline → opioid/suicide
- EU: Colantone 2019 (UK GHQ), Eliason-Storrie 2009 (Sweden displacement)
- Mediator: Lang 2018 (mental), McManus-Schaur 2016 (injury), Sullivan-vW 2009 (displacement)

**Para 2** (puzzle): 한국은 다르다
- Export-driven economy (DFS 2014 의 독일 analog)
- KR-CN bilateral 가 ADH-style import-Bartik 와 다름
- Trade gain 가 mortality 에 protective 가설

**Para 3** (identification challenge):
- ADH-style IV first-stage F = 19.65 (Lang 2018 의 F=18.77 와 동등)
- Solution: LMP 2022 tF + BHJ 2022 ssaggregate + Pre-WTO placebo direct test

**Para 4** (3 contributions):
1. First mortality estimate for Korea
2. Reverse asymmetry in export-economy (mirror image of US/EU)
3. LMP 2022 + Pre-WTO placebo direct shock-only test 적용 한 첫 paper

**Para 5** (main result preview):
- β = −0.069 (RF 5y diff), HC1 t = −2.42
- Drop-C26 cluster-sido t = −3.24 (broad exposure)
- Pre-WTO placebo cluster p = 0.22 (PASS)
- 25→75 percentile shock → 6.5% mortality decline (vs Lang 2018 의 +7.8% mental health)

**Para 6** (paper organization)

### § 2 Related Literature (3 pp)

Subsections:
- **2.1** Trade × employment: ADH 2013, DFS 2014, PS 2016, CHS 2019
- **2.2** Trade × mortality: PS 2020, ADH 2019, FNS 2026, CHS 2019
- **2.3** Trade × health (mental, injury): Lang 2018, McManus 2016, Colantone 2019
- **2.4** Displacement → mortality: Sullivan-vW 2009, Eliason-Storrie 2009
- **2.5** Methodology: ADH 2013 IV, BHJ 2022, AKM 2019, GPSS 2020, LMP 2022

각 subsection 3-4문단. 본 paper 의 differentiation 명시.

### § 3 Data (3-4 pp)

**3.1** Mortality data
- KOSTAT 사망 microdata 27 csv (1997-2023, 28 if 2024)
- Working-age 25-64, Korean-only filter
- 5 outcome groups: despair_total (102 + 101 + 057 + 081), cancer, cardio, respiratory, external_other
- KOSIS 인구 panel (286 sigungu, 31 years)
- Age-standardized mortality rate per 100k → log_asr_p1

**3.2** Trade data
- Comtrade ADH-8 OECD imports from China (HS6, 2000-2010)
- Comtrade KR-CN bilateral imports
- 광업제조업조사 1994 baseline employment (KSIC9 2-digit)
- KIET3 (60-industry) 매개 hs6→ksic9_2 매핑

**3.3** Sigungu crosswalk
- 2021 KOSTAT baseline (256 h_code)
- 1997-2023 raw 100% 매칭

**3.4** Mediator data
- z_m_marital: MDIS 1975-1995 cohort sex ratio
- z_m_education: 233 학교 → 251 시군구 nearest distance

### § 4 Identification Strategy (4-5 pp)

**4.1** Bartik IV construction
```
z_x_h = Σ_k s_{h,k}^{1994} × ΔM_{KR-CN,k} / E_h^{1994}
```
- s_{h,k}^{1994}: industry k employment share in sigungu h, 1994 baseline
- ΔM_{KR-CN,k}: 2000-2010 KR-CN bilateral import growth in industry k

**4.2** Identification assumption (Goldsmith-Pinkham-Sorkin-Swift 2020 framework)
- Either: shares (s) exogenous (GPSS path)
- Or: shocks (ΔM) exogenous (BHJ 2022 path)

**4.3** BHJ 2022 shock-only exogeneity 검증
- ssaggregate transformation
- AKM SE
- **Pre-WTO placebo (1992-1996 shock × 1998-2000 mortality)**: cluster p=0.22 (PASS) — shock-only exogeneity 직접 입증

**4.4** Identification challenges
- First-stage F=19.65 (ADH-8) — Lang 2018 의 F=18.77 와 비교
- LMP 2022 cutoff 3.286 미달 → IV interpretation 보수적
- Solution: RF main spec, IV as robustness

### § 5 Empirical Specification (3-4 pp)

**5.1** Main reduced-form spec
```
Δ_5y log(mortality_h) = α + β·z_x_h + θ_t + ε_h
```
- 5-year long differences
- Year FE (decade indicators)
- z_x_h standardized

**5.2** 5-layer SE
- HC1
- Cluster-sigungu (WCB)
- Cluster-sido
- AKM (BHJ industry-mode)
- Conley (1km/5km/10km)

**5.3** Inference
- Conventional 5%: |t|=1.96 for HC1, WCB, cluster-sido
- LMP 2022 tF: cutoff 3.286 for IV (F=19.65)
- AR confidence set: backup for weak-IV

**5.4** Outcomes (Romano-Wolf step-down, 5-outcome family)
- despair_total (main)
- cancer, cardio, respiratory, external_other (FWER 통제)

### § 6 Descriptive Evidence (3-4 pp, figures-heavy)

**Figures**:
- F1: Korean trade with China 1990-2020 (export-driven evidence)
- F2: z_x_h choropleth (sigungu-level shock distribution)
- F3: Mortality time-series 1997-2024 by outcome group
- F4: First-stage scatter (z_x_h vs Δlog mortality)

**Tables**:
- T1: Summary statistics (sigungu × year × outcome)
- T2: Comparison with US/EU baseline (DFS 2014, ADH 2019)

### § 7 Main Results (5-6 pp)

**7.1** Master regression table
```
| Outcome | β (RF) | HC1 t | WCB | Cluster-sido | AKM | LMP tF |
|---|---|---|---|---|---|---|
| despair_total | -0.069 | -2.42 | p=0.041 | -2.12 | t=+1.51 | F=19.65, c=3.286 |
| cancer | ... |
| cardio | ... |
```

**7.2** Sub-period split (1997-2007 + 2008-2018)
- Sign 일치 검증
- 2008 ICD break dummy

**7.3** IV reporting (transparent weak-IV)
- ADH-8 IV: β, |t|, LMP cutoff
- AKM canonical (BHJ WLS): β=+0.890, t=+1.51 (n.s.)
- AR confidence set: [-0.50, +0.01]

**7.4** Magnitude
- 25→75 percentile shock → -6.5% despair mortality
- Comparison: ADH 2019 (+10% in US), Lang 2018 (+7.8% mental)

### § 8 Robustness (4-5 pp)

**8.1** Drop-C26 (전자부품·컴퓨터)
- cluster-sido t = -3.24, p = 0.0012 → broad exposure (NOT single-industry case study)

**8.2** Drop top-3 (C26 + C24 + C20)
- β = -0.0713, t = -2.08

**8.3** Pre-WTO placebo (1992-1996 × 1998-2000)
- β = +0.0238, cluster p = 0.22 (PASS) — BHJ shock-only exogeneity 직접 입증

**8.4** Alternative baseline year
- 1995 vs 1996 (이미 보유)
- 1989 / 1992 (KOSIS MDIS 신청 후 — 다음 turn)

**8.5** Alternative outcome definition
- Despair sub-decomposition: 102 (자살), 101 (약물), 057 (정신활성), 081 (알코올 간)

**8.6** Romano-Wolf step-down
- 5-outcome family FWER 통제

### § 9 Mechanism (3-4 pp)

**9.1** Marriage market channel (z_m_marital)
- 1975-1995 cohort sex ratio shift
- Frölich-Huber 2017 ivmediate framework
- ADH 2019 의 marriage market deterioration ↔ 본 paper 의 marriage market 보존

**9.2** Education channel (z_m_education)
- 251 시군구 × 233 4년제 대학 nearest distance
- Displacement protection 이론

**9.3** Direct mediator IV (별도 IV 두 개)
- z_x_h vs z_m_marital + z_m_education separation
- DGHP/DFH single-IV mediation 도 비교

### § 10 Limitations & Discussion (2-3 pp)

- IV first-stage F < OP 23.1: ADH-style IV 가 export-driven Korea 에서 약한 것은 자연스럽지만 AR-CI 가 0 포함 → IV interpretation 보수적
- Mental health micro data 부재 (NHIS 시도-level only): mediator 직접 측정 한계
- 1994 baseline 의 1997 IMF 위기 직전 호황 우려 — 1989/1992 sensitivity 추후
- Cross-sigungu migration: ADH 2019 와 같이 robust (assume away)

### § 11 Conclusion (1-2 pp)

- Three main contributions 재진술
- Policy implication: Korean labor market gain 가 mortality protection 으로 transmit
- Future research: NHIS individual data, displacement → mortality micro foundation

---

## 5. Figures & Tables 목록

### Main paper (8 figures + 7 tables 권장)

**Figures (academic-paper-tools:figure-export 활용)**:
- F1: Korea-China trade volume time-series 1990-2020
- F2: z_x_h sigungu choropleth
- F3: Mortality outcome time-series (5 group, 1997-2024)
- F4: First-stage scatter (z_x_h vs ΔlogE)
- F5: Reduced-form scatter + lowess
- F6: Event-study (pre-trends + post-period)
- F7: Forest plot (5-layer SE comparison)
- F8: Pre-WTO placebo plot (1992-1996 shock × 1998-2000 mortality null)

**Tables (academic-paper-tools:regression-table-xlsx 활용)**:
- T1: Summary statistics
- T2: Main regression — 5 outcomes × 5-layer SE
- T3: Sub-period split (1997-2007 + 2008-2018)
- T4: IV vs RF comparison
- T5: Drop-C26 sensitivity
- T6: Pre-WTO placebo
- T7: Mechanism (z_m × outcome)

### Online appendix (15+ tables, 10+ figures)

- Robustness tables (alternate baseline, alternate weights, alternate definitions)
- Heterogeneity tables (working-age 25-64 sub-decomposition)
- Romano-Wolf step-down detail
- AKM canonical full reporting
- Codebook + crosswalk validation

---

## 6. Timeline

```
이번 turn (2026-05-05): 본 plan 사용자 sign-off
다음 turn 1 (2026-05-06): PAP v4.2 main body 본격 재작성
다음 turn 2 (2026-05-07): § 7 + § 5 + § 4 작성 (Stage A 의 1-3)
다음 turn 3 (2026-05-08): § 8 + § 9 작성 (Stage A 의 4-5)
다음 turn 4 (2026-05-09): § 3 + § 6 + § 2 작성 (Stage B)
다음 turn 5 (2026-05-10): § 1 + § 10 + § 11 작성 (Stage C)
다음 turn 6 (2026-05-11): Online appendix + Bibliography 정비
다음 turn 7 (2026-05-12): Polish + Cover letter + 첫 submission ready
```

**총 7 turn = 1 주일 가능 (R-A side)**. 사용자 측 review/feedback 시간 별도 (3-5 turn 추정).

→ **현실적 timeline: 2-3 주 within complete first draft**.

---

## 7. Iteration / Reviewer feedback strategy

### Internal review (writing 중)
- 매 section 완성 시 R-A → 사용자 review → R-A revision (1-2 turn cycle)
- Critical sections (§ 1, § 7) 는 3+ revision

### External review (submission 후)
- KER R&R 시 expected: identification strict 확장, mechanism 보강 요청
- Track A 의 expected timeline: submission → first decision 6-9개월

### Defense for likely critiques

| Critique | R-A response anchor |
|---|---|
| F=19.65 < OP 23.1 | Lang 2018 published with F=18.77; LMP cutoff 3.286 |
| Single-industry case (C26) | Drop-C26 cluster-sido t=-3.24 (Round 2 정독) |
| BHJ shock-only violation | Pre-WTO placebo cluster p=0.22 PASS |
| Working-age 25-64 selection | Lang 2018 employed effect concentration |
| Korean-only filter | Foreign 노동자 비율 < 3% 0_raw 검증 |
| 1994 baseline endogeneity | 1995/1996/1989/1992 sensitivity |

---

## 8. Bibliography (~50-60 cites)

- 27편 reference library (19 existing + 8 new)
- 추가 fetch 권장 (선택):
  - Adda-Fawaz 2017 (US county trade × health)
  - Hummels-Jorgensen-Munch-Xiang 2014 (Denmark offshoring)
  - Korean 학자의 무역 × 노동 (KDI/KIEP) — domestic anchor
  - Anderson-Rubin 1949 (AR test 원전)
  - Stock-Yogo 2005 (weak IV)
  - Cameron-Gelbach-Miller 2008 (WCB)

---

## 9. Language strategy

**Single language: English** (저널 submission 기준)
- 박사논문 defense 시 한글 abstract / 목차 / 일부 chapter 가능 (선택)
- 모든 paper draft 는 English
- R-A 의 한글 narrative 는 internal documentation only

---

## 10. Tools & skills

| Tool | Use |
|---|---|
| `academic-paper-tools:paper-docx` | Final docx export |
| `academic-paper-tools:figure-export` | Publication-grade PDF + PNG |
| `academic-paper-tools:regression-table-xlsx` | esttab-style table |
| `academic-paper-tools:reference-extract-pdf` | Additional reference fetch |
| `dissertation:section-draft` | Single section draft |
| `dissertation:reviewer-feedback` | Internal review iteration |
| `trade-mortality-toolkit:reduced-form-5layer` | § 7 master regression runner |
| `trade-mortality-toolkit:phase-bx-runner` | § 4 identification diagnostics |

---

## 11. R-A 권장 즉시 다음 step

**Path 1 — recommended (immediate)**:
1. 사용자가 본 plan 검토 + sign-off
2. Track A target 결정 (KER vs Health Economics)
3. R-A 가 다음 turn 에 PAP v4.2 main body 작성 (Stage A 시작)

**Path 2 — if pivot needed**:
1. 사용자가 plan revision (예: target tier 변경, 작성 순서 변경)
2. R-A 가 plan v02 작성

**Path 3 — additional materials first**:
1. 사용자가 Adda-Fawaz / Korean anchor 추가 fetch
2. R-A 가 reference library 보강 후 plan 시작

---

## 12. Risk & Mitigation

| Risk | Mitigation |
|---|---|
| Reviewer "F<23.1 reject" | Lang 2018 published precedent + LMP 2022 |
| Reviewer "single-industry case study" | Drop-C26 robust (Round 2 정독 확인) |
| Mechanism weak (시도-level NHIS only) | z_m_marital + z_m_education direct mediator |
| 학부 단독저자 risk | KER 또는 Health Economics tier; advisor (가천대 교수) 추후 합류 가능 |
| Korean data 의 generalizability | DFS 2014 독일 analog frame |
| 작성 timeline 지연 | R-A 가 자동화 가능한 부분 maximize (regression table, figure export) |

---

## 13. Success metrics

**Phase 1 (이번 plan 종료)**: 본 plan sign-off
**Phase 2 (1-2 주 후)**: Complete first draft (35-40 pp main + 15-20 pp appendix)
**Phase 3 (3-4 주 후)**: Internal review 완료 + cover letter + ready to submit
**Phase 4 (6-12개월)**: First decision (Track A)
**Phase 5 (12-18개월)**: Published / R&R complete
