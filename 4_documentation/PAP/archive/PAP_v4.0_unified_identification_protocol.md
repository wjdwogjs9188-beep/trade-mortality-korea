# PAP v4.0 — Unified Identification Protocol (IV + Mediation)

**작성일**: 2026-05-04
**상태**: pre-commit (regression 실행 전 사전 등록)
**대체 대상**: PAP v3.4 § 4–§ 5.2, PAP v3.5 (z_x only), pap_v41_feedback.md § 2
**적용 위치**: stage5_regression_plan_v01.md § 4 + § 5.2 + § 7.5
**선행**: v3.5 가 z_x (trade IV) 만 다뤘고 z_m (mediator IV) 미정의 — 본 v4.0 이 그 gap 메움

---

## 0. 본 protocol 의 동기

### 0.1 두 개의 black hole

PAP v3.4 의 핵심 contribution 은 **DGHP 2017 + DFH 2020 ivmediate** 식 mediation 분해:
```
Total effect (trade → mortality)
  = Direct effect (trade → mortality | mediator)
  + Indirect effect (trade → mediator → mortality)
```

이 분해가 *식별*되려면 **두 개의 별개 instrument** 가 필요하다:
- **z_x** = trade exposure (X) 의 instrument
- **z_m** = mediator (M) 의 instrument

PAP v3.5 (2026-05-04 작성) 는 z_x 의 validity·strength 만 protocol 화했다. **z_m 은 v3.4 § 5.2 와 RESEARCH_PROGRESS_v01 § 6.2 에서 "candidate selection in progress" 로 비어 있다.** z_m 미정의 상태에서 ivmediate 를 돌리면 indirect effect 는 *non-identified*. 이 gap 이 본 paper 의 가장 큰 식별 risk.

### 0.2 본 v4.0 의 scope

| 구성 | 다루는 것 |
|------|-----------|
| § 1 | 두-instrument framework 의 식별 가정 명시 |
| § 2 | z_x protocol (= v3.5 의 reorganized 버전) |
| § 3 | z_m protocol (신규 — 본 v4.0 의 핵심) |
| § 4 | Sequential ignorability (ivmediate 의 추가 가정) |
| § 5 | Joint pre-commit decision tree (z_x + z_m 동시 통과 시 Stage 5 진입) |
| § 6 | Stage5_regression_plan / PAP main 에 들어갈 patch 텍스트 |
| § 7 | 실행 순서 (Phase A → B → branch decision) |
| § 8 | Honest reporting 가이드 |

---

## § 1. 두-instrument framework 의 식별 가정

### 1.1 ivmediate (DGHP 2017 + DFH 2020) 의 4 가정

원전 DGHP 2017 (NBER WP 23209) 와 DFH 2020 (Stata Journal 20(3): 613-626) 가 명시하는 가정은 다음 4개:

**A1. Relevance of z_x for X**: z_x 가 trade exposure (X) 의 first-stage 에서 충분한 강도. ⇒ § 4.1 first-stage F (OP 2013).

**A2. Exclusion of z_x from Y**: z_x 가 mortality (Y) 에 영향을 줄 수 있는 유일한 경로는 X (또는 X 를 통한 M) 뿐. ⇒ § 2 z_x protocol.

**A3. Relevance of z_m for M conditional on X**: z_m 이 mediator (M) 의 first-stage 에서 충분한 강도, **z_x 를 통제한 후에도**. ⇒ § 3.4 z_m first-stage.

**A4. Exclusion of z_m from Y conditional on X and M**: z_m 이 Y 에 영향을 줄 수 있는 유일한 경로는 M. ⇒ § 3 z_m protocol.

A2 와 A4 는 *별개의 명제*다. A2 만 만족해도 ivmediate 는 indirect effect 를 식별 못한다. A4 가 본 paper 의 *추가* 식별 부담이다.

### 1.2 두 instrument 의 *독립적* variation 요구

A1 + A3 가 동시에 만족되려면 z_x 와 z_m 이 *서로 다른 variation source* 를 가져야 한다. 예를 들어 둘 다 "lagged industry shares × shock" 식 Bartik 으로 만들어지면, z_m 은 z_x 의 산업변동을 mediator 차원으로 reweight 한 것에 불과하고, 두 instrument 가 collinear → mediation 분해 미식별.

따라서 z_m 의 variation 은 *trade-shock 과 별개의 외생적 요인* 에서 와야 한다. § 3.2 가 후보 변수를 제시한다.

---

## § 2. z_x Protocol (PAP v3.5 의 reorganized)

이 부분은 v3.5 와 동일. 요약만:

### 2.1 후보 IV 두 종류
- **ADH-8** (Australia, Denmark, Finland, Germany, Japan, New Zealand, Spain, Switzerland imports from China) — share-side validity 가 baseline.
- **KR-CN bilateral net exposure** — strength ↑, validity 검증 필요.

### 2.2 Bilateral validity 3 orthogonality tests
- **Test 1** (Romer-Romer style, ECOS-only): bilateral shock 이 lagged 한국 거시 실현치 (GDP 성장률, 환율 logreturn, 수출입 물가지수, CPI, BoK 기준금리) 로 예측되지 않음.
- **Test 1b** (WEO surprise robustness): bilateral 이 lagged WEO Korea forecast surprise 와 무상관.
- **Test 2** (pre-WTO lead): pre-2001 bilateral 이 post-WTO 한국 거시를 예측하지 않음.
- **Test 3** (Pierce-Schott pre-trend): pre-period (1995-1999) 사망률 trend 가 baseline industry shares × bilateral exposure 와 무상관.

### 2.3 Strength branch
- **Branch A**: F_ADH8 ≥ 23.1 → ADH-8 main, 5-layer 표준.
- **Branch B**: 10 ≤ F_ADH8 < 23.1 → ADH-8 main, AR + tF column 1 격상.
- **Branch C.i**: F_ADH8 < 10, bilateral validity pass → bilateral main, AR + tF.
- **Branch C.ii**: F_ADH8 < 10, bilateral validity reject → reduced-form 또는 FNS spillover framing.

상세는 v3.5 § 2–3 참조. 본 v4.0 에서 *변경 없음*.

---

## § 3. z_m Protocol (신규)

### 3.1 z_m 후보 선정 원칙

z_m 은 *mediator (marital share / education share) 를 외생적으로 변동시키되, mortality 에 직접 영향이 없어야* 한다. Korean 맥락에서 trade-shock 과 *별개*의 variation source 4 후보 검토:

#### 후보 그룹 A — Marital share 전용 z_m

| 후보 | 메커니즘 | 외생성 후보 사유 | 데이터 가용성 |
|------|---------|-----------------|--------------|
| **A1. 시군구별 출생 성비 cohort lag** | 1980s–1990s 한국 sex ratio at birth 의 강한 son preference 변동 (Park-Cho 1995). 25년 후 결혼시장에 진입 → 결혼율 영향. 사망률에 직접 영향 없음. | sex selective abortion 은 *과거* 의사결정 → 현재 노동시장과 분리 | KOSIS 출생성비 시군구 단위 1980+ ✅ |
| **A2. 시군구별 군 복무 cohort 비율 lag** | 한국 남성 의무 군복무 (24-30개월) → 결혼 시기 지연. 시군구별 입대율 변동 → 결혼시장. 사망률 직접 채널 없음. | 군 복무 의무는 외생적 정책 (예외 적음) | 병무청 시군구 입대 통계 — access 확인 필요 |
| **A3. 결혼장려 보조금 정책 timing 변동** | 지방자치단체별 신혼부부 주택지원·출산장려금 도입 시기 차이. 결혼율에 영향. 사망률 직접 영향 약함. | 지자체 정책 도입은 정치적 의사결정 → trade shock 과 분리 가능 | 지자체 정책 인벤토리 별도 수집 필요 (수기) |

#### 후보 그룹 B — Education share 전용 z_m

| 후보 | 메커니즘 | 외생성 후보 사유 | 데이터 가용성 |
|------|---------|-----------------|--------------|
| **B1. 시군구별 4년제 대학 거리** | Bound-Jaeger 1996 식 distance-to-nearest-college instrument. 대학 위치는 1960s–1970s 정부 결정으로 고정. 진학율 → education share. | 지리적 외생성 — 트레이드 충격과 분리 | 4년제 대학 위치 master + 시군구 centroid 거리 계산 ✅ |
| **B2. 1995 5일 수업제 시범도입 시군구** | 1995 한국 교육개혁의 5일 수업제는 시범지역 → 전국 확대. 시범지역 cohort 의 학업성취 영향 (Lee-Hong 2010). | 시범지역 선정은 정부 결정 → 외생적 | 교육부 정책 인벤토리 — access 확인 필요 |
| **B3. 정원배분 변동 (BK21 등)** | 1999 BK21 program 으로 시도별 4년제 정원 변동. 진학 cohort 차이 → education share. | 정원배분은 학술 평가 결과 → 노동시장과 분리 가능 | 교육부 정원배분 시계열 |

### 3.2 권고 후보 (실용성 우선)

- **z_m for marital**: **A1 (출생 성비 cohort lag)** 권장. 데이터 즉시 가용 (KOSIS), Korean academic literature 에 이미 외생성 변호 존재 (Park-Cho 1995, Edlund-Lee 2009).
- **z_m for education**: **B1 (distance-to-college)** 권장. Bound-Jaeger 1996 의 표준 instrument, US/Korea 양쪽 다수 사용례 (Currie-Moretti 2003 등).

A1 과 B1 은 *서로 다른 차원의 외생성* (인구학적 vs 지리적) 이라 Joint test 가능.

### 3.3 z_m exclusion restriction — 3 orthogonality tests (z_x 와 평행)

#### Test 4 — z_m 과 사망률의 *직접* 무상관 (lagged mediator 통제 후)

```
ΔY_{c, t→t+5}^{cause}  =  α  +  β · z_m_{c, t-10}  +  γ · M_{c, t-5}  +  δ_t  +  ε
```

- 종속: 5-year change in cause-specific log mortality rate (working-age 25-64).
- 우변 z_m: lagged sex ratio cohort (A1) 또는 distance-to-college (B1).
- M_{c, t-5}: lagged marital/education share (mediator 자체).
- 만약 β ≠ 0 → z_m 이 mediator 외 *다른 채널* 로 사망률에 영향 → A4 위반.
- H0: β = 0. 4-cause × 2-mediator = 8 specification 별 검정.

#### Test 5 — z_m 과 z_x 의 직교성

```
z_x_{c, t}  =  α  +  β · z_m_{c, t}  +  ε
```

- 두 instrument 가 같은 variation 을 잡으면 ivmediate decomposition 미식별 (§ 1.2).
- H0: β = 0. p > 0.10 이면 두 instrument 가 *독립적* variation 보유.
- p < 0.05 → z_m 후보 교체 또는 추가 control 로 직교화.

#### Test 6 — Mediator first-stage (A3)

```
M_{c, t}  =  α  +  β_x · z_x_{c, t}  +  β_m · z_m_{c, t}  +  γ · X_{c, t-5}  +  δ_t  +  ε
```

- z_m 이 z_x 통제 후에도 mediator 에 충분히 strong 한가.
- H0: β_m = 0 reject 필요. F_z_m for M (KP rk-Wald) ≥ 10 이상.
- 약하면 z_m 후보 교체.

### 3.4 z_m strength branch (z_x 와 평행)

z_x 의 § 2.3 와 동일한 구조:

- **Branch αm**: F_z_m ≥ 23.1 → z_m main, ivmediate 표준 inference.
- **Branch βm**: 10 ≤ F_z_m < 23.1 → ivmediate 의 mediator 단계에 weak-IV-robust inference 적용. AR CI for indirect effect.
- **Branch γm**: F_z_m < 10 → mediation analysis 를 *robustness only* 로 강등. Reduced-form (trade → mortality) 결과를 main 으로 보고.

**중요**: ivmediate 자체의 weak-IV inference 는 still developing 영역. Branch βm 진입 시 Anderson-Rubin region 으로 indirect effect CI 보고하되, point estimate 는 보고하지 *않음* (point estimate 가 weak IV 하에서 biased — Lee-Moreira-McCrary-Porter 2022).

---

## § 4. Sequential ignorability (추가 가정)

ivmediate 는 위 A1–A4 외에도 *Sequential Ignorability* 를 요구한다. Imai-Keele-Yamamoto (2010, Statistical Science) 에 의하면:

**SI**: M_{c, t} 의 잠재결과 (counterfactual) 는 trade exposure X_{c, t} 의 잠재결과와 *조건부 독립*. 즉 M 과 Y 사이의 unmeasured confounder 가 X 를 통제한 후에도 존재해선 안 됨.

### 4.1 Korean 맥락에서 SI 위험 변수

다음 변수가 unmeasured 면 SI 위반:

1. **시군구별 cultural conservatism** — 결혼 규범 강도가 *동시에* 고용·이혼·자살에 영향. 시군구 FE 가 일부 흡수하지만, *변화* 부분이 남을 수 있음.
2. **지역 종교 분포 변동** — 개신교 시간 변동 → 결혼·이혼 + 자살률 직접 영향 (보호효과).
3. **지역 의료 인프라 변동** — 의료자원 → 우울증 진단·치료 + 결혼시장 (정신건강 ↔ 결혼).

### 4.2 SI 검증 — 진행 가능한 sensitivity

**Imai-Yamamoto rho sensitivity**: ρ = corr(error term in M eq, error term in Y eq) 의 다양한 값에 대해 indirect effect 가 어떻게 변하는지 보고. Stata `medsens` (Imai 등 2010 R package 의 stata port) 또는 직접 implementation 가능.

PAP v4.0 사전 commit:
- Main result 외에 ρ ∈ {-0.3, -0.1, 0, 0.1, 0.3} 에 대한 sensitivity table 첨부.
- |ρ| 가 0.3 까지 가도 indirect effect 의 sign 이 변하지 않으면 robust.

### 4.3 SI 위반 시 대응

ρ sensitivity 에서 sign flip 발생 → mediation claim 강도 약화. 다음 두 옵션:
- (a) "indirect effect estimate is sensitive to ρ ∈ ..." 를 paper § 4 limitation 에 명시.
- (b) Imai-Keele-Tingley (2010) 의 *non-parametric* upper-lower bound 만 보고하고 point estimate 포기.

---

## § 5. Joint pre-commit decision tree

z_x 와 z_m 의 검증 결과를 *동시에* 본 후 다음 분기에 commit:

| z_x 결과 | z_m 결과 | 결정 |
|---------|---------|------|
| Branch A (강) | Branch αm (강) | ⭐ **Full ivmediate**, 5-layer SE 표준, ρ sensitivity 첨부 |
| Branch A | Branch βm (중) | ivmediate with AR CI on indirect, point estimate 비보고 |
| Branch A | Branch γm (약) | Reduced-form main, mediation 은 *exploratory appendix* |
| Branch B (z_x 중) | αm | ivmediate main, *both* AR CI on direct + indirect |
| Branch B | βm | Reduced-form main, mediation appendix only |
| Branch B | γm | Reduced-form main, mediation 폐기 |
| Branch C.i (z_x bilateral) | αm | bilateral-IV ivmediate 가능 (caveat 명시 — bilateral validity 약화 영향) |
| Branch C.i | βm/γm | Reduced-form bilateral, mediation 폐기 |
| Branch C.ii (z_x reject) | any | 전체 paper 재포지셔닝 (reduced-form 또는 spillover) |
| any | A4 reject (Test 4) | mediation 폐기 — z_m 이 다른 채널로 Y 영향 |
| any | A3 z_x-z_m collinear (Test 5) | z_m 후보 교체 또는 mediation 폐기 |

**Pre-commitment**: 위 표는 회귀 결과를 보기 *전* 확정. 결과를 본 후 표를 *고치는 것은 cherry-pick*.

---

## § 6. 패치 텍스트

### 6.1 stage5_regression_plan_v01.md § 4 patch (v3.5 patch 와 통합)

§ 4.2 와 § 4.3 사이에 신규 § 4.2a:

```markdown
### 4.2a Identification branch decision (pre-committed, PAP v4.0)

PAP v4.0 의 protocol 에 따라 다음 *모든* 진단을 회귀 결과 관찰 *전* 완료:
* z_x 진단: § 4.1 first-stage F (ADH-8, bilateral 각각), Test 1/1b (Romer-Romer + WEO),
  Test 2 (pre-WTO lead), Test 3 (Pierce-Schott pre-trend)
* z_m 진단: Test 4 (z_m 과 mortality 의 직접 무상관, A4), Test 5 (z_x ⊥ z_m), Test 6 (mediator first-stage F)

위 7 진단을 PAP v4.0 § 5 의 joint decision tree 에 입력해 분기 commit.
분기 결정은 5_logs/decisions/<date>_iv_branch_committed.md 에 timestamp.
post-hoc IV switching 또는 분기 변경 금지.
```

### 6.2 stage5_regression_plan_v01.md § 5.2 patch (mediation spec)

§ 5.2 ivmediate spec 다음에 추가:

```markdown
### 5.2.x z_m commit + sensitivity

* z_m for marital: 시군구 출생 성비 (1980–1995 cohort) × 25년 lag.
  Source: KOSIS 출생성비 시군구별.
* z_m for education: 시군구 centroid 와 1990 4년제 대학 list 의 거리 (km),
  cohort fixed.
  Source: 교육통계연보 + KOSTAT 시군구 행정구역 master.
* PAP v4.0 § 4 의 Sequential Ignorability sensitivity (Imai-Yamamoto ρ ∈ {-0.3, -0.1, 0, 0.1, 0.3}) 첨부.
* 위 진단이 § 4.2a Joint decision tree 에서 Full ivmediate (Branch A × αm) 통과한 경우만 § 5.2 main.
```

### 6.3 PAP main body § 5.2 footnote

```markdown
^* Identification of mediation analysis follows DGHP (2017) IV mediation framework
implemented via DFH (2020) ivmediate. Identification requires four assumptions
(A1–A4 in PAP v4.0 § 1) plus Sequential Ignorability (Imai-Keele-Yamamoto 2010).
Pre-committed orthogonality tests for z_x and z_m, and ρ sensitivity for SI,
are reported in Appendix [...]. Branch decisions follow PAP v4.0 § 5 prior to
second-stage estimation.
```

---

## § 7. 실행 순서

### Phase A — 데이터 prep (별도 prompt PHASE_A_data_prep.md 에 정의됨)
- ECOS 신규 시리즈 호출 (200Y007, 401Y014, 401Y015)
- WEO Korea vintage 추출
- bilateral / ADH-8 5-year stacked exposure 집계

### Phase B-x — z_x 진단 (Phase A 완료 후)
- Test 1 (Romer-Romer macro predictability)
- Test 1b (WEO surprise robustness)
- Test 2 (pre-WTO lead) — bilateral 1995-1999 도착 후
- Test 3 (pre-trend on shares)
- § 4.1 first-stage F (ADH-8, bilateral)

### Phase B-m — z_m 진단 (Phase A 완료 후, B-x 와 병렬)
**선행 데이터 수집**:
1. KOSIS 출생성비 시군구별 1980-1995 → `0_raw/kosis_birth_sex_ratio/`
2. 교육통계연보 4년제 대학 list 1990 → `0_raw/edu_university_list_1990/`
3. 시군구 centroid 좌표 (KOSTAT 행정구역 master) → `0_raw/sigungu_centroid/`

**진단 스크립트**:
- Test 4 (z_m → Y 직접 무상관, lagged M 통제) for marital and education each
- Test 5 (z_x ⊥ z_m)
- Test 6 (mediator first-stage F, with z_x partialled out)

### Phase B-SI — Sequential Ignorability sensitivity
- ρ ∈ {-0.3, -0.1, 0, 0.1, 0.3} 에 대한 indirect effect re-estimate

### Phase C — Joint branch commit
- 위 진단 결과를 PAP v4.0 § 5 표에 매핑
- 결정 → `5_logs/decisions/<date>_v4_branch_committed.md`

### Phase D — Stage 5 main regression
- Branch 에 따라 spec 실행

---

## § 8. Honest reporting (paper § 4–5 에 들어갈 텍스트)

### 8.1 Identification 단락

> "Identification of the mediation parameters follows DGHP (2017) and is implemented
> via DFH (2020). The framework requires (i) relevance and exclusion of z_x for
> trade exposure (§ 4.A), (ii) relevance and exclusion of z_m for the mediator
> conditional on trade exposure (§ 4.B), (iii) Sequential Ignorability of the
> mediator (Imai-Keele-Yamamoto 2010). Each assumption is examined empirically
> via the protocol committed in PAP v4.0 prior to estimation. The point estimates
> reported in Tables X–Y correspond to Branch [A × αm] of the joint decision tree;
> alternative branches are reported in Appendix [...] for transparency."

### 8.2 Limitations 단락

> "The mediation analysis rests on stronger identification assumptions than the
> reduced-form trade-mortality estimate. In particular, A4 (exclusion of z_m
> from Y conditional on M) cannot be tested directly; we provide indirect
> evidence via Test 4 (PAP v4.0 § 3.3) and Sequential Ignorability sensitivity
> (Imai-Yamamoto ρ ∈ ±0.3). Should the Branch decision land on Branch γm or
> A4-reject, the mediation results are reported as exploratory appendix only.
> The reduced-form trade-mortality coefficient remains the primary quantity of
> interest in such cases."

### 8.3 Branch 결정 결과 보고 (paper appendix)

논문 Appendix 에 다음 표 첨부:

| 진단 | 결과 | Branch 매핑 |
|------|------|------------|
| z_x first-stage F (ADH-8) | F = ___ | A / B / C |
| z_x first-stage F (bilateral) | F = ___ | (참고) |
| Test 1 p-value | ___ | bilateral validity |
| Test 1b p-value | ___ | (robustness) |
| Test 2 p-value | ___ | (pre-WTO) |
| Test 3 p-value | ___ | (pre-trend) |
| z_m first-stage F (marital) | F = ___ | αm / βm / γm |
| z_m first-stage F (education) | F = ___ | (per-mediator) |
| Test 4 p-value (per cause × per mediator) | 8 entries | A4 결과 |
| Test 5 p-value (z_x ⊥ z_m) | ___ | 직교성 |
| Test 6 p-value (M first-stage with z_x partialled) | ___ | A3 |
| **Final branch commit** | ___ | Section 5 spec 결정 |

---

## § 9. 사용자 review 체크리스트

본 v4.0 이 PAP main body / stage5 plan 에 commit 되기 전 확인:

- [ ] § 3.2 z_m 후보 (A1 출생성비 / B1 distance-to-college) 가 한국 데이터에서 가용한지 1차 확인 (KOSIS 검색, 교육통계연보 archive)
- [ ] § 4.1 SI 위험 변수 3개 (시군구 cultural conservatism / 종교분포 / 의료인프라) 중 *통제변수* 로 추가 가능한 것 결정
- [ ] § 5 joint decision tree 의 8 row 중 본인이 동의 안 하는 분기 있으면 명시
- [ ] § 6 patch 텍스트 (stage5 plan + PAP main footnote) 적용 시점 결정
- [ ] § 7 Phase B-m 의 데이터 3종 수집 우선순위 결정
- [ ] § 8.2 의 Branch γm / A4-reject 시나리오를 paper 에 명시 commitment 받아들일지 결정 — *큰 결정* (mediation 이 본 paper 의 contribution 인데 사전에 "appendix only 가능" 을 commit 한다는 의미)

---

## § 10. References

본 protocol 이 의존하는 핵심 논문 (stage5_regression_plan § 15 의 부분집합):

**z_x related** (v3.5 와 동일):
- Andrews, Stock, Sun (2019) — Annual Review of Economics 11
- Lee, Moreira, McCrary, Porter (2022) — Restud
- Olea, Pflueger (2013) — JBES 31(3)
- Stock, Yogo (2005) — Cambridge UP chapter
- Goldsmith-Pinkham, Sorkin, Swift (2020) — AER 110(8)
- Borusyak, Hull, Jaravel (2022) — RES 89(1)
- Borusyak, Hull, Jaravel (2025) — JEP
- Mertens, Ravn (2013) — AER 103(4)

**z_m + mediation related** (v4.0 신규):
- **Dippel, Gold, Heblich, Pinto (2017)** — NBER WP 23209 — IV mediation theoretical framework
- **Dippel, Ferrara, Heblich (2020)** — Stata Journal 20(3): 613-626 — ivmediate package
- **Imai, Keele, Yamamoto (2010)** — Statistical Science 25(1): 51-71 — Sequential Ignorability + sensitivity
- **Imai, Keele, Tingley (2010)** — Psychological Methods 15(4): 309-334 — non-parametric mediation bounds
- **Bound, Jaeger, Baker (1995)** — JASA — distance-to-college instrument
- **Currie, Moretti (2003)** — QJE 118(4): 1495-1532 — distance-to-college applied
- **Park, Cho (1995)** — Population and Development Review — Korean sex ratio at birth
- **Edlund, Lee (2009)** — NBER WP 14495 — sex ratio long-term consequences
- **Lee, Hong (2010)** — KDI WP — Korean 5-day school week reform

---

## § 11. v3.5 와의 비교 요약

| 항목 | v3.5 | v4.0 |
|------|------|------|
| 다루는 instrument 수 | 1 (z_x only) | 2 (z_x + z_m) |
| Decision tree 분기 | 4 (A/B/C.i/C.ii) | 30+ (z_x × z_m × SI) |
| Orthogonality tests | 3 (Test 1/2/3) | 6 (Test 1–6) + ρ sensitivity |
| Identification 가정 명시 | exclusion (z_x) | A1–A4 + SI |
| Mediation 다룸 | 안 다룸 | 핵심 |
| 사전 commit 범위 | 회귀 직전 | 회귀 직전 + ρ sensitivity 사후 |
| Honest reporting | paper § 4 한 단락 | paper § 4–5 + Appendix 표 |

v4.0 = v3.5 (z_x 부분) + § 3 (z_m) + § 4 (SI) + § 5 (joint tree) + § 8 (확장된 reporting).

---

_End of PAP v4.0 unified identification protocol. ~3,800 words._
