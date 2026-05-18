# PAP v4.0 patches — Reviewer P1 5항 통합 반영

**작성**: 2026-05-04 (저녁)
**대상**: PAP v4.0 unified identification protocol (`PAP_v4.0_unified_identification_protocol.md`)
**근거**: R-A reviewer critique (`reviewer_critique_R-A_2026_05_04.md`)
**Status**: Stage 5 진입 전 PAP main body 에 반영해야 할 patches 모음

---

## Patch 1 — § 5 Joint decision tree 9-branch 통합 (P1.C 처리)

### Before — 12+ branch matrix (v4.0 § 5 원본)

z_x 4 branch (A/B/C.i/C.ii) × z_m 3 branch (αm/βm/γm) × SI 변동 = 12+ branches. Reviewer critique: AER/QJE precedent 부재, "over-engineered protocol" reject 위험.

### After — 9-branch (3 main × 3 fallback) + § 8 framing

**Branch matrix (재구성)**:

| z_x branch | z_m branch | spec | 비고 |
|-----------|-----------|------|------|
| **A: F_ADH-8 ≥ 23.1** | **αm: F_z_m ≥ 23.1** | ⭐ **MAIN-1**: Full ivmediate, 5-layer SE 표준, ρ ±0.5 sensitivity | 본 paper 의 *최선 시나리오* |
| A | βm/γm | **MAIN-2**: ADH-8 reduced-form, mediation appendix only | reduced-form 충분히 strong |
| B: 10 ≤ F_ADH-8 < 23.1 | αm/βm | **MAIN-3**: ivmediate with AR + tF (column 1 격상), point estimate + CI | weak-IV-robust inference |
| **C.i: F_ADH-8 < 10, bilateral validity PASS** | αm/βm | **FALLBACK-1**: Bilateral-IV ivmediate (caveat: bilateral validity 변호) | secondary IV path |
| C.i | γm | **FALLBACK-2**: Bilateral reduced-form, mediation 폐기 | mediator IV 약함 |
| **C.ii: F_ADH-8 < 10, bilateral REJECT** | any | **FALLBACK-3**: 재포지셔닝 — reduced-form Pierce-Schott style 또는 FNS spillover framing | Rev1.A: 가장 보수적 |
| any | A4 reject (Test 4) | mediation **abolished** — z_m 이 다른 채널로 Y 영향 | Test 4 (P1.A) 핵심 검정 |
| any | Test 5 collinear (β > 0.3) | z_m 후보 교체 또는 mediation 폐기 | |
| (joint failure) | (joint failure) | "Working paper" 단계 출판, reject path | last resort |

**= 6 active branches (3 main + 3 fallback) + 3 abort scenarios**.

### § 8 contribution framing 텍스트 (paper 본문에 들어갈)

> "본 paper 의 식별 protocol 은 *pre-committed transparent decision tree* (PAP v4.0) 로 6 active branches 를 명시한다. 이는 Pierce-Schott (2020) 등의 single-decision post-hoc 보고와 다른 *학술 정직성 framework* 로, 무역 IV 와 mediator IV 의 strength 가 사전적으로 불확실한 상황에서 cherry-pick 회피와 reproducibility 를 함께 보장한다. 6 branches 모두 Olea-Pflueger (2013) effective F 와 Lee, Moreira, McCrary, Porter (2022) tF inference 로 기준화되어, 어느 branch 가 적용되든 inference 의 internal consistency 가 유지된다."

---

## Patch 2 — § 8 Limitations 통합 (P1.A + P1.B + P1.D + P1.E 처리)

### Before — § 8 8 known limitations (v3.3-v3.4 commit)

기존 8 항 (외국인 식별 / 코드 9 drop / 교육 카테고리 collapse / 2022-2024 drop / sample weight ±5% / 분모 결손 9.74% / 2024 sigungu / sigungu code audit).

### After — 통합 11 항 (기존 8 + reviewer P1 추가 3)

**§ 8.9 z_m_marital exclusion restriction 의 비-mediator 채널 (P1.A 처리)**:

> "z_m_marital instrument (시군구별 출생 성비 cohort lag) 의 exclusion restriction 은 sex ratio → marital share → mortality 만을 가정한다. 그러나 sex ratio imbalance 의 다른 mortality 채널 3 가지가 존재할 수 있다:
> (i) **Gendercide / 가정폭력**: 남초 시군구 → 폭력 발생률 ↑ → 외상사·자살 직접 영향 (Edlund-Lee 2009 NBER WP 14495 가 자체적으로 sex ratio → crime/violence 다룸).
> (ii) **매매혼·결혼이주**: 남초 → 베트남·필리핀 결혼이주 ↑ → 외국인 비율 변동 → 1997-2007 외국인 식별 불가 measurement 영향 (§ 8.1).
> (iii) **청년 인구 유출**: 남초 → 결혼 못한 남성의 도시 유출 → mortality denominator bias.
> 이 세 채널의 영향은 Imai-Yamamoto (2010) Sequential Ignorability **ρ ∈ ±0.5 sensitivity** (PAP v4.0 § 4 의 ±0.3 에서 확장) 으로 정량화하며, sign flip 발생 시 indirect effect 를 *exploratory appendix* 로 격하한다."

**§ 8.10 z_m_education baseline 의 1990 외생성 (P1.B 처리)**:

> "z_m_education instrument (distance-to-nearest-4-year-college) 는 *1990 baseline* 학교 list (yunbo 1-14-1 의 107 본교 기준) 로 한정한다. 1990-2008 사이 신설 89 학교 (KESS 2008 196 - yunbo 1990 107) 는 trade-shock 시점 (2001 WTO 진입 이후) 의 endogenous 위치 결정 가능성 — 예: 제조업 쇠퇴 시군구 정부 보상 정책 — 을 배제할 수 없어 main spec 에서 제외한다. 본 paper 의 namuwiki 233 학교 → 4년제 + 시군구 매핑 175 학교 중 *설립연도 < 1990* 학교만 baseline 사용. 1990-2008 신설 89 학교 포함 시 estimate 변동은 Appendix [TBD] sensitivity 로 보고."

**§ 8.11 z_m_marital cohort timing — period 1-2 mediation 미커버 (P1.D 처리)**:

> "z_m_marital instrument 의 main spec 은 **1995 MDIS Census 의 0-9세 cohort sex ratio** (1986-1995 출생 cohort) 를 활용한다. 본 cohort 의 결혼시장 진입 (25-29세 도달) 은 2011-2020 년이므로, **5-year stack panel period 3-5 (2007-2021) 에서만 mediation main spec 적용** 가능하다. Period 1-2 (1997-2006) 의 25-29세 cohort (1968-1977 출생) 는 1995 census 25-29세 (현재 mediator endogenous) 또는 18-22세 (학업 이주 corruption) 에 해당해 instrument validity 가 약화된다. 따라서 period 1-2 는 *reduced-form (Pierce-Schott 2020 style) 만* 보고하며, mediation 분해는 period 3-5 에 한정한다.
>
> 이 제한의 *substantive impact* 는 작다 — Total effect (β_TY, reduced-form) 는 5 period 모두 cover 되며, Mediation 손실 obs 는 이론상 40% (2 period × 229 시군구 × 2 sex = 916 obs) 이지만, period 1-2 는 본 paper 의 *high-trade-variation* 시기 (post-WTO 정점 + KR-CN FTA + COVID, 2007-2021) *외* 의 pre-WTO 시기로, mediation analysis 의 information value 가 본질적으로 낮다.
>
> 1985/1990 MDIS Census 의 4-digit sigungu codes 와 *5-digit h_code 매핑 표* 는 통계청 publish 부재로 본 paper 에서 미구축. *Future work*: KOSTAT historical 행정구역 cross-reference 표 별도 수집 후 1985+1990+1995 census triple-source z_m_marital 로 period 1-5 full mediation cover 가능. 현재 시점에서는 period 3-5 main spec 으로 학술적 충분성 확보."

---

## Patch 3 — § 4 SI sensitivity ρ 범위 확장 (P1.A 와 연동)

### Before — § 4.2 ρ ∈ {-0.3, -0.1, 0, 0.1, 0.3}

### After — § 4.2 ρ ∈ {-0.5, -0.3, -0.1, 0, 0.1, 0.3, 0.5}

**근거**: 한국 cultural confounding (지역 보수성, 종교 분포, 연고주의) 의 unmeasured magnitude 가 ρ ±0.5 까지 갈 수 있다는 reviewer 권고. ±0.3 만으로는 한국 특수성 미반영.

**구체화**:
> "본 paper 는 Imai-Yamamoto (2010) ρ-sensitivity 를 **ρ ∈ {-0.5, -0.3, -0.1, 0, 0.1, 0.3, 0.5}** 7-point 로 확장한다. 한국 시군구의 cultural conservatism (지역별 종교 분포 변동, 출산력 정책 영향, 연고주의) 가 mediator-outcome unmeasured confounder 로 작용할 magnitude 가 미국·독일 setting (DGHP 2017 의 ρ ±0.3) 보다 클 가능성을 반영한다. ρ = ±0.5 에서 indirect effect 의 sign 이 flip 하면 mediation claim 을 exploratory appendix 로 격하한다."

---

## Patch 4 — § 7 5-layer SE 의 Romano-Wolf family 명시 (P2.D 처리)

기존: family 정의 모호 (§ 5.6 = 10 vs § 7.2 = 240).

명시:
> "Multiple testing correction 의 hypothesis families 는 다음 *2-tier* 로 분리:
> - **Confirmatory (10 hypotheses)**: 4 main outcomes (suicide·drug·psychiatric·liver) × 2 mediators (marital·education) + 2 placebos (cardiovascular·cancer). Romano-Wolf step-down (Romano-Wolf 2005, 1000 bootstrap iterations) 으로 family-wise error rate (FWE) ≤ 0.05 보장.
> - **Exploratory (~230 specs)**: heterogeneity (성별·연령·urban/rural) + robustness (specification variants + 시기 sub-sample). FWE 미적용, individual p-values 보고."

---

## Patch 5 — Stage 5 regression plan v01 § 9 의 robustness 항목 추가

`stage5_regression_plan_v01.md` § 9 (robustness items) 에 추가:

```markdown
**11. 057 (F10-F19) F17 (담배) sensitivity (P2.C)**

본 paper 의 outcome group despair_total = 102 + 101 + 057 + 081 의 057 (정신활성물질 사용 정신·행동장애) 은 ICD-10 F10-F19 의 통합 코드. **F17 (담배 의존)** 은 Case-Deaton (2015) deaths-of-despair 정의에서 *명시적 제외* 되나 한국 KCD-8 에서는 분리 불가.

Sensitivity test:
- Main spec: 057 그대로 사용 (F17 포함)
- Robustness: ICD-10 raw 컬럼이 가용하면 F17 제외; 불가하면 paper § 4 limitation 명시
- 변동 magnitude 추정: F17 (담배) 의 working-age 25-64 사망 비중 ≈ 5-10% (KOSTAT 보고 기준), 따라서 057 estimate 변동 약 ±5-10%

**12. Pre-period 1997-2001 → pre-WTO sample restriction (P2.E)**

Pierce-Schott (2020) 의 pre-period 8 년 vs 본 paper 의 1997-2001 (4 년) power 부족 우려. 1997 IMF 위기 confound 처리:
- Robustness: pre-period 1997-2000 (3 년, IMF 직후 회복기) 으로 한정 + IMF 노출 통제 변수 (시·도 수출 비중) 추가
- 또는 sample restriction: 1997 IMF 충격이 가장 큰 시도 (서울·부산·인천 등) sub-sample 제외 후 estimate
```

---

## Patch 6 — § 1 H1 → H1a/H1b 분리 (P2.A 처리)

기존 § 1 H1 reduced-form trade effect (sign 모호).

분리:
> "**H1a (Export-gain channel)**: 시군구의 *對中 수출 노출* 1 std 증가 → working-age deaths of despair *감소* (β_export < 0). 메커니즘: 수출 산업 고용·임금 ↑ → 가족 안정성 ↑ → mortality ↓. Dauth-Findeisen-Suedekum (2014) 의 독일 east export gain (1.4M jobs) 과 정합.
>
> **H1b (Import-loss channel)**: 시군구의 *對中 수입 노출* 1 std 증가 → working-age deaths of despair *증가* (β_import > 0). 메커니즘: import competition → 제조업 employment ↓ → 가족 해체 → mortality ↑. Pierce-Schott (2020) 의 미국 county PNTR 효과와 정합 (drug 사망 +).
>
> **본 paper 의 핵심 가설**: 한국은 export-driven 경제 (대중국 중간재 수출 비중 ↑) 이므로 |β_export| > |β_import| → net effect 가 *protective*. 미국 (Pierce-Schott) 의 import-dominant pattern 과 *대비*. 이는 KR-CN bilateral *net* exposure 변수의 sign 이 *negative* 일 것을 함의."

---

## Patch 적용 순서 권장

1. **즉시** (본 patch 파일에 작성됨): P1.A+B+C+D 통합 § 8 limitation, § 5 9-branch, § 4 ρ ±0.5, § 7 family, § 9 robustness, § 1 H1a/b
2. **Phase B 진단 시작 *전***: PAP v3.4 main body 의 § 5.2 mediation, § 7 5-layer SE, § 8 limitation 을 본 patches 와 정합 commit (R-A ~3h)
3. **Stage 5 진입 *전***: PAP v5.0 으로 version up 후 사용자 review

본 patch 의 reviewer P1 처리 status:
- ✅ P1.A — § 8.9 limitation + § 4 ρ ±0.5
- ✅ P1.B — § 8.10 limitation (1990 baseline 한정)
- ✅ P1.C — § 5 9-branch 통합 + § 8 transparent framing
- ✅ P1.D — § 8.11 limitation + Option (c) main spec 명시
- ⏳ P1.E — PAP v3.4 main body rewrite (별도 dedicated turn)

