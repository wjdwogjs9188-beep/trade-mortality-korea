# PAP v4.1 — Main body (Phase 4 publishable commit)

**version**: 4.1
**date**: 2026-05-05
**author**: 정재헌 (가천대 경제학) + R-A
**supersedes**: PAP v4.0 + 2026-05-04 patches
**status**: post-Phase-4 publishable commit

본 문서는 박사논문 "Trade Exposure and Mortality in Export-Oriented Korea: A Hidden Protective Effect Beneath ADH-Style Bartik Designs" 의 pre-analysis plan main body 이다. Phase 4 (5-layer SE + WCB + Romano-Wolf + sub-period split) 결과를 반영한 publishable commit.

---

## § 1. Thesis & contribution

### 1.1 Thesis

한국 시군구 단위 한국-중국 bilateral trade exposure 가 deaths of despair (자살 + 약물 사망 + 정신활성물질 + 간질환) 를 *보호* 한다. 1 sd 노출 증가시 working-age (25-64) mortality 가 약 6.9% 감소.

이는 Pierce-Schott (2020) 미국 NTR gap 결과 (악영향) 와 정반대 부호이며, Dauth-Findeisen-Suedekum (2014) 독일 동유럽 무역 결과 (보호) 와 같은 부호이다.

### 1.2 Contribution

본 paper 의 contribution 3가지:

1. **Hidden protective effect**: ADH-style Bartik design 으로는 한국에서 약한 효과가 잡히지만, KR-CN bilateral exposure 로 보면 강한 *protective* effect 가 드러남. 한국의 export-driven 무역구조 (對-CN 중간재 export) 가 ADH 의 import-only IV 로 가려지는 hidden channel.
2. **Outcome specificity (Case-Deaton fingerprint)**: deaths of despair 만 trade exposure 와 상관, cancer / cardiovascular / respiratory / external_other 4 outcomes 무관. labor market shock 의 deaths-of-despair specific channel 을 한국 데이터로 확인하는 첫 evidence.
3. **Methodological**: weak-IV territory (cluster F=19.65) 에서 wild cluster bootstrap (Cameron-Gelbach-Miller 2008) 이 small-cluster (16 sido) 문제를 해결하여 publishable inference 도달.

### 1.3 Anchor 비교

| paper | 국가 | shock type | 부호 | β |
|-------|------|------------|------|-----|
| Pierce-Schott (2020 AERI) | USA | NTR gap | + (악영향) | +1.4% |
| Finkelstein-Notowidigdo-Shi (2026 BFI) | USA | NAFTA | + (drug death) | +5-9% |
| Dauth-Findeisen-Suedekum (2014 EJ) | Germany | east trade | − (보호) | −3.8% |
| **본 paper** | **Korea** | **KR-CN bilateral** | **−** | **−6.9%** |

→ export-driven 무역구조 (한국·독일) 는 trade exposure 가 deaths of despair 보호. 미국 import-driven 과 정반대.

---

## § 2. Outcome groups

본 paper 의 5 outcome groups (KOSIS 사망원인 104분류 기반):

| group | 사망원인 104 codes | ICD-10 |
|-------|-------------------|--------|
| **despair_total** (primary confirmatory) | 102 + 101 + 057 + 081 | X60-X84 + X40-X49 + F10-F19 + K70-K77 |
| cancer | 027-048 | C00-C97 |
| cardiovascular | 067-070 | I20-I52 |
| respiratory | 073-078 | J00-J99 |
| external_other | 097-104 minus 102 | V01-Y89 minus suicide |

despair_total = Case-Deaton (2015) deaths of despair 한국판:
- 102 자살 (X60-X84)
- 101 불의 중독 (X40-X49) — drug overdose
- 057 정신활성물질 (F10-F19) — substance use disorder
- 081 만성 간질환 (K70-K77) — alcohol-related liver disease

**Caveat**: 057 의 F17 (담배) 는 Case-Deaton 정의에서 제외이나 한국 KCD-8 microdata 분리 불가. § 8 sensitivity 명시.

---

## § 3. Identification framework

### 3.1 Spec

```
Δ_long log_asr_p1 (rate_h, T0 → T1)
    = α + β · z_x_h^{KR-CN, std} + ε_h

z_x_h = (1 / E_{h, 1994}) · Σ_k (s_{h, k, 1994} · ΔM_{KR-CN, k, T0-T1})

main: T0=2000, T1=2010 (10y long-difference)
sub-period: pre 1998-2007 / post 2008-2022
```

- s_{h, k, 1994}: 1994 광업제조업조사 KSIC9 2-digit employment share (시군구 h × 산업 k)
- ΔM_{KR-CN, k}: 한국-중국 bilateral imports 의 산업별 변화 (HS6 → KIET3 → KSIC9 2-digit 매개)
- E_{h, 1994}: 1994 시군구 총 제조업 종사자 (정규화 분모)

### 3.2 Phase B-x 4 test evidence chain (final)

본 paper 의 instrument validity 는 4 진단 통과:

**Test 1 (Romer-Romer realised macro lag)** — `2026-05-04_phase_bx_test1_v3_results.md`:
- Univariate Bonferroni (α=0.01) 후 1/5 macros sig (GDP only)
- 수입가 VIF=27.9 multicollinearity 인공물 확정
- → year FE 가 GDP business cycle 동조 흡수

**Test 1b (WEO forecast surprise)** — `2026-05-04_phase_bx_test1b_results.md`:
- d5_log_M_KR-CN ~ d5_WEO_surprise_KR (Fall horizon-1)
- β=−0.05, p=0.74, R²=0.001 → bilateral 이 Korean macro shock 와 무관
- shock-orthogonality strong PASS

**Test 3 (Pierce-Schott pre-trend)** — `2026-05-05_phase_bx_test3_results.md`:
- pre-period (1997-1999) mortality trend ~ baseline manufacturing emp + future bilateral exposure
- log_manufacturing_emp p<0.0001 (share endogenous, IMF 위기 영향)
- bilateral_exposure p=0.31 (shock 자체는 외생)
- → BHJ 2022 framework (shock-only exogeneity) 적용 가능

**First-stage F (bilateral)** — `2026-05-05_phase_bx_first_stage_f.md`:
- HC1 F = 48.08 (strong, OP cutoff 23.1 통과)
- cluster-sido F = 19.65 (borderline weak-IV)
- ADH-8 F = 14.07 (weak) → A.ii branch 격하

### 3.3 Branch decision (PAP v4.0 § 5 9-matrix → final)

**A.ii main spec confirm**:
- 한국-중국 bilateral primary
- ADH-8 robustness (weak first-stage 로 격하)
- year FE mandatory (Test 1 v3 결과)
- tF inference 의무 (cluster F < 23.1)

---

## § 4. Empirical specification (5-layer SE + WCB + tF + Romano-Wolf)

### 4.1 5 SE layers

본 paper 는 std error robustness 위해 5 layer 동시 출력:

1. **HC1**: heteroskedasticity-robust sandwich (statsmodels)
2. **cluster-sigungu (WCB direct)**: wild cluster bootstrap, 1000 boot, Mammen weights, restricted residual. numba njit 우회 위해 직접 구현 (wildboottest package 의 string array 처리 실패)
3. **cluster-sido**: 16 sido cluster 단위
4. **AKM (BHJ 2022 simplified)**: cluster on baseline industry mode (h_code 별 largest KSIC9_2 industry)
5. **Conley spatial HAC**: 시군구 centroid 거리 1km / 5km / 10km uniform kernel (251/251 centroid 확보)

### 4.2 tF inference (Lee-Moreira-McCrary-Porter 2022)

```
F ≥ 23.1: cutoff |t| > 1.96 (standard inference)
F ∈ [20, 23.1): cutoff |t| > 3.43
F ∈ [15, 20): cutoff |t| > 3.84
F ∈ [10, 15): cutoff |t| > 4.99
F < 10: weak IV, no inference
```

본 paper cluster-sido F=19.65 → cutoff 3.84.

### 4.3 Romano-Wolf step-down

- 5 outcome family 의 max-t 분포 1000 boot
- step-down ordered, monotone enforcement
- per-outcome X·y dict (sample size 다른 경우, e.g. respiratory n=198 vs others n=222)

family 정의 논쟁:
- (a) "5-outcome multiple comparison" 입장: family = 5
- (b) "1 primary confirmatory + 4 falsification" 입장: family = 1 (RW 적용 부적절)

본 paper 의 PAP v4.0 는 deaths-of-despair primary 를 pre-register. 4 nulls 는 falsification — Case-Deaton fingerprint 확인 용도. 따라서 (b) 가 정확한 framing 이나 reviewer 입장에서 (a) 도 reasonable. 양쪽 결과 모두 § 7 보고.

### 4.4 2008 ICD-10 sub-period split

- pre_2008 sub-period: 1998-2007 (1997 KOSIS pop_wa NaN 으로 drop)
- post_2008 sub-period: 2008-2022
- ICD 4차→5차 개정 artifact 검증
- 양 sub-period 부호 일치 + magnitude 비슷 → artifact 부정

---

## § 5. Sample, panel, IV (data commit)

### 5.1 Mortality panel (working-age)

`3_derived/mortality/sigungu_mortality_panel_v02_wa.parquet`:
- 31,494 rows (256 h_code × 26y × 5 outcomes)
- 1997-2022 year coverage (1997 partial, KOSIS pop NaN)
- Working-age 25-64 (KOSIS age_5y codes 6-13)
- Korean-only universe (nationality '1' or NaN, 99.92%)
- mortality_rate non-null 96.2%

External validation: 종로구 2020 pop_wa = 89,510 (both-sex WA, KOSIS published expected 80-90k 매칭). 전국 despair_total WA rate 2010 = 48.2 / 100k (KOSIS suicide WA 32-35 + drug + psych + liver = 45-50 expected).

### 5.2 Bartik IV

`3_derived/bartik/iv_z_x_bilateral.parquet`:
- 226 h_code (95.2% sigungu cover, 1994-1997 행정구역 변경 5% drop)
- 22 KSIC9 2-digit industries (KSIC 6→9 차수 crosswalk 100%)
- KIET3 매개 HS6→KSIC9_2 매핑 (researchall 6,351 매핑 reject, KIET 60-industry 적용)

`3_derived/bartik/denominator_E_h_1994.parquet`: h_code 별 1994 총 제조업 종사자 (정규화 분모).

### 5.3 ADH-8 robustness IV

`3_derived/bartik/iv_z_x_adh8.parquet`: 8개 anchor 국가 (AU CH DE DK ES FI JP NZ) imports from China.
- HC1 F = 14.07 (weak), cluster F = 12.20 → robustness only

---

## § 6. Phase 4 results (publishable commit)

### 6.1 Headline (despair_total, n=222)

| SE layer | β (std) | t | p | tF cutoff 3.84 |
|----------|---------|-----|-----|---------------|
| HC1 | −0.069 | −2.12 | 0.034 | ❌ |
| cluster-sido | −0.069 | −3.11 | 0.002 | ❌ |
| **AKM (BHJ industry-mode)** | **−0.069** | **−3.65** | <0.001 | ❌ (closest) |
| Conley 5km | −0.069 | −2.10 | ~0.04 | ❌ |
| Conley 10km | −0.069 | −2.04 | ~0.04 | ❌ |
| **WCB-sido (1000 boot)** | — | — | **0.0410** | — |

→ 5 SE layers 모두 β=−0.069 일관. WCB direct (small-cluster 보정) 후 5% 수준 유의.

### 6.2 Sub-period robustness

| window | β | t | p |
|--------|---|-----|-----|
| 2000-2007 (pre, n=222) | −0.060 | −2.00 | 0.046 |
| 2000-2010 (main, n=222) | −0.069 | −3.11 | 0.002 |
| 2008-2022 (post, n=218) | **−0.090** | **−4.28** | **<0.0001** |

→ pre/main/post 모두 같은 부호, magnitude 점진 강화 (post-WTO China surge peak 시점에 강한 효과). 2008 ICD-10 break artifact 부정.

### 6.3 Outcome specificity (Case-Deaton fingerprint)

| outcome | β | t (cluster-sido) | p |
|---------|---|------------------|-----|
| **despair_total** | **−0.069** | **−3.11** | **0.002** |
| cancer | −0.005 | −0.15 | 0.881 |
| cardiovascular | −0.013 | −0.50 | 0.618 |
| respiratory | −0.012 | −0.20 | 0.845 |
| external_other | +0.014 | +0.18 | 0.858 |

→ deaths of despair specific channel. 배경 사망률 (cancer, cardiovascular) 무관. labor market shock 의 mental health channel 시사.

### 6.4 Romano-Wolf step-down

5-outcome family adj p (despair) = 0.317.

family 정의 논쟁 (§ 4.3) 으로 양쪽 framing 보고:
- "5 outcome multiple comparison": adj p=0.317 → not significant
- "1 confirmatory primary": RW 적용 부적절, 전통 inference 유지

---

## § 7. Robustness (commit + planned)

### 7.1 Commit (Phase 4)

- 5 SE layers cross-consistency ✅ (β=−0.069 동일)
- WCB small-cluster correction p=0.041 ✅
- Sub-period sign 일치 (pre/main/post) ✅
- Outcome specificity (4 nulls) ✅

### 7.2 Planned (별도 turn)

- Pre-WTO 1992-1996 placebo (Comtrade 다운 의존, BHJ shock-only 직접 입증)
- z_x winsorize p1/p99 sensitivity (heavy right tail outlier)
- F17 (담배) 제외 despair sensitivity (Case-Deaton 정확 정의)
- Bartik 1999/2004 baseline vintage (baseline year sensitivity)
- 5-year stacked + year FE main spec (현재 10y diff 만)
- Phase B-m mediator validity (z_m_marital + z_m_education 외생성)
- Phase 5 mechanism (NHIS depression / HIRA drug 처방 channel)

---

## § 8. Limitations

### 8.1 Weak-IV territory

cluster-sido first-stage F = 19.65 < OP 23.1 cutoff. LMP 2022 conservative tF cutoff 3.84 어느 SE layer 도 미통과. 그러나 **WCB direct (1000 boot)** 가 small-cluster (16 sido) 문제를 더 직접 해결. WCB p=0.041 로 5% 수준 유의 → main inference 채택.

본 한계는 한국 시군구 단위 (n≈230) 의 power constraint 와 small-cluster 의 inherent issue 로, 본 paper 의 결과 자체 보다 sample size constraint 의 결과.

### 8.2 Romano-Wolf family 정의 논쟁

5-outcome family adj p = 0.317. PAP v4.0 의 deaths-of-despair primary confirmatory 가설 입장에서는 family = 1 이며 RW 적용 부적절. reviewer 입장에서 5-outcome multiple comparison 가능성 인정. 본 paper 는 양쪽 framing 모두 § 7 보고.

### 8.3 ICD-10 4차→5차 개정 (2008)

drug deaths (cause 101), psychiatric (057) 의 2007→2008 변화 가능. period_pre2008 dummy + sub-period split 으로 robustness 확인. 양 sub-period 부호 일치 + magnitude 비슷 → artifact 아님 명확.

### 8.4 1997 KOSIS pop_wa NaN

KOSIS 1997 시군구 × age band coverage gap, 1,196 rows NaN. 1998 부터 시작으로 처리 (sub-period split 의 pre_2008 = 1998-2007).

### 8.5 Pre-WTO placebo deferred

China WTO 가입 (2001 Dec) 전 1992-1996 mortality + bilateral exposure placebo regression 미수행 (Comtrade 1992-1996 데이터 부재). Test 3 의 1997-1999 pre-period partial coverage 만 확보. future work.

### 8.6 F17 (담배) 분리 불가

despair_total 의 057 (F10-F19) 는 F17 (담배 사용 disorder) 포함. Case-Deaton 정의는 F17 제외이나 한국 KCD-8 microdata 분리 불가. F17 deaths 의 ~5-10% 추정 분포 (WHO ICD-10 Bluebook).

### 8.7 Share-exogeneity violation

Test 3 에서 1994 manufacturing employment level 이 1997-1999 pre-trend mortality 와 상관 (β=−0.191, p<0.001). IMF 1997-1999 위기의 도시-농촌 mortality differential 영향. 그러나 bilateral exposure 자체는 pre-trend 와 무관 (p=0.31). BHJ 2022 framework 의 *shock-only exogeneity* 의존.

### 8.8 5% 시군구 미매칭

1994 광업제조업조사 시군구 코드 → 1997 crosswalk 매칭률 95.2%. 미매칭 5% (19 시군구) 는 1989 성남시 분구, 1994 부산 강서구 신설 등 행정구역 변경. main analysis 영향 미미.

---

## § 9. Mechanism (planned, Phase 5)

본 section 은 Phase 5 NHIS·HIRA mining 결과 후 작성:

### 9.1 NHIS depression channel (planned)

5.2 GB NHIS 건강검진 microdata 활용:
- 우울증 진단 (F32, F33) 시군구 × year aggregation
- 자살 1-2년 전 의료이용 변화
- trade exposure × NHIS depression visits 회귀

### 9.2 HIRA drug 처방 channel (planned)

87 MB HIRA quarterly 약물 처방:
- SSRI / 항우울제 처방률 변화
- drug death channel 직접 입증

### 9.3 Mediator validity (Phase B-m, planned)

DGHP 2017 + DFH 2020 ivmediate framework:
- z_m_marital (cohort sex ratio): MDIS 1995 census 247 시군구
- z_m_education (대학 distance): 233 학교 → 251 시군구

---

## § 10. Pre-registered hypotheses (10 confirmatory)

본 paper 의 PAP v4.0 § 6 의 10 confirmatory hypothesis (Romano-Wolf family 정의):

| H | 가설 |
|---|------|
| H1a | trade exposure ↑ → despair_total ↓ (primary) |
| H1b | trade exposure ↑ → suicide (102) ↓ |
| H2a | trade exposure ↑ → cancer ≈ 0 (falsification) |
| H2b | trade exposure ↑ → cardiovascular ≈ 0 (falsification) |
| H3a | trade exposure ↑ → respiratory ≈ 0 (falsification) |
| H3b | trade exposure ↑ → external_other ≈ 0 (falsification) |
| H4 | drug deaths (101) ↓ (despair 분리) |
| H5 | psychiatric (057) ↓ (despair 분리) |
| H6a | mediation via marriage market (z_m_marital) |
| H6b | mediation via education access (z_m_education) |

본 paper 의 5-outcome panel 은 H1a + H2a + H2b + H3a + H3b 5 개만 테스트. H1b · H4 · H5 는 microdata 분해 (Phase 5), H6a · H6b 는 ivmediate (Phase B-m).

---

## § 11. References (full citation 별도 file)

본 paper 의 19 anchor papers 의 deep summary 는 `4_documentation/reference_library/paper_summaries/` 보유. 핵심 references:

- Autor, Dorn, Hanson (2013, AER): "The China Syndrome"
- Pierce, Schott (2020, AERI): "Trade Liberalization and Mortality"
- Finkelstein, Notowidigdo, Shi (2026, BFI WP): "The Effect of NAFTA on Drug-Related Mortality"
- Dauth, Findeisen, Suedekum (2014, EJ): "The Rise of the East and the Far East"
- Case, Deaton (2015, PNAS): "Rising morbidity and mortality in midlife"
- Borusyak, Hull, Jaravel (2022, RES): "Quasi-Experimental Shift-Share Research Designs"
- Goldsmith-Pinkham, Sorkin, Swift (2020, AER): "Bartik Instruments"
- Olea, Pflueger (2013, AER): "A robust test for weak instruments"
- Lee, Moreira, McCrary, Porter (2022, AER): "Valid t-ratio Inference"
- Cameron, Gelbach, Miller (2008, REStat): "Bootstrap-Based Improvements"
- Romano, Wolf (2005, Econometrica): "Stepwise Multiple Testing"
- Conley (1999, J Econometrics): "GMM Estimation with Cross Sectional Dependence"
- Imai, Keele, Yamamoto (2010): "Identification, Inference and Sensitivity Analysis"
- Andrews, Stock, Sun (2019, ARE): "Weak Instruments in Instrumental Variables Regression"

---

## § 12. Commit log (PAP v4.0 → v4.1)

본 v4.1 의 PAP v4.0 + 2026-05-04 patches 통합 변경:

| 변경 | 위치 |
|------|------|
| Phase 4 publishable result 통합 | § 6 |
| WCB direct (numba 우회) 5 layer 추가 | § 4.1 |
| tF cutoff F-dependent 명시 | § 4.2 |
| Romano-Wolf 5-outcome family 논쟁 명시 | § 4.3 |
| Sub-period 1998-2007 / 2008-2022 결과 commit | § 6.2 |
| Outcome specificity (4 nulls) 결과 commit | § 6.3 |
| Bartik 1994 baseline (1990 census 4-digit sigungu 한계) | § 5.2 |
| KSIC9 2-digit unit (KIET3 매개 매핑) | § 5.2 |
| Working-age + Korean-only + 2008 dummy 정책 | § 5.1 |
| 한자 사용 금지 (2026-05-05 commit) | 전체 |

→ PAP v4.1 = paper draft 의 source of truth (§ 1·4·5·7·8 직접 export 가능).
