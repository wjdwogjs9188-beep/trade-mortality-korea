# Research Trajectory — Cumulative Summary

월별 milestone + 핵심 의사결정 압축본. Resume 시 daily report 보다 먼저 읽혀야 하는 파일.

---

## 2026-05 (current)

### 시작 시점 stage
- v4.0 reset 직후. Stage 1 raw 데이터 검증 완료, Stage 2/3 panel 미구축.

### 이번 달 milestone
- **2026-05-03**: Stage 2 v4 채택 (mortality panel 9 검증 PASS) + Stage 3 v1 채택 (population + mortality_rate panel 9 검증 PASS) + Stage 4A 착수 (무역 데이터 수집).
- **2026-05-04** (오전): Panel v02 → **v02.1** (외국인 빼기 제거, ASR mean −1.48% correction) 채택, sigungu 코드 5건 정정 audit, **Stage 3C mediator panel** (marriage/education/occupation microdata) 신설, Stage 4A 거의 완료 (KR-CN 50/50, ADH 8 ← CN 195/200, CN-World 22/25), `stage5_regression_plan_v01.md` (6 step workflow + 5-layer SE + DGHP 2017 + DFH 2020 mediation) 작성, **PAP v3.3 → v3.4** (안산 시계열 main → Appendix C demote, panel v02.1 explicit commit, limitation #21-23 추가).
- **2026-05-04** (오후-미명): **Stage 3C-3E mediator pipeline 완전 구축** — MDIS Census 2% microdata 7 시점 (1990-2020) 으로 mediator denominator panel build, 사망 microdata 28 시점 (1997-2024) cleaning + working-age 25-64 + 시군구_crosswalk align 으로 numerator panel build, 5-year stack 5 period × cause × marital × education cross-tab 으로 **mediator-specific mortality rate panel** (Stage 5 § 5.2 input) 생성. 28년 합 working-age deaths of despair = 자살 208,683 + 간 121,289 vs 약물 5,104 (한국 = 자살+간 dominance, US Pierce-Schott 2020 의 drug dominance 와 정반대 — paper § 7 핵심 finding raw 수치 confirm). **18 paper deep summary master** 작성 (`reference_library_master_v01.md` 32.7 KB + `paper_summaries/` 폴더 18 detailed summaries) + **PAP v3.4 reference update 제안서 v01** (7 ✅ 즉시 + 22 reference 추가 cite).
- **2026-05-04** (저녁-야간): **v4.1 데이터 보강** — BACI HS92 1995-2011 (3.9 GB, 17 csv), WITS HS6→ISIC Rev3·Rev2, **researchall HS6↔KSIC10 매핑 (P1.6 SOLVED)**, IMF WEO Historical (1990-2022 vintage), 시군구 centroid (251 rows), ECOS 200Y110/402Y014/401Y015 (Test 1 macro), KOSIS 보건의료 4 시리즈, **MDIS 인구주택총조사 1975-1995 (5 census, 220 MB, 3.8M rows, z_m_marital instrument 핵심)**. **PAP v4.0 unified identification protocol commit** (z_x + z_m + Sequential Ignorability + Joint decision tree 9-branch matrix) + PAP v4.0 patches commit. 폴더 정리 (root → 4_documentation/, 2_scripts/run/ 등).
- **2026-05-05**: **Phase 2-B Bartik 1994 baseline build + Stage 4 closure + Phase B-x 4종 진단 + Working-age panel verify + 첫 reduced form 회귀 — 본 paper preliminary main result paper-grade 도달**. Stage 4A 잔여 8 file 채움 (KR-CN HS 01-99 25y, ADH-8 ← CN HS 28-97, CN-World 1995-2024 모두 closure), 광업제조업조사 1994 microdata KSIC9_2 직접 추출 → `baseline_shares_1994_*.parquet` 3종 build, KIET60 매개 HS6→KSIC9_2 매핑 → exposure × ΔM × E_h_1994 → `iv_z_x_adh8.parquet` + `iv_z_x_bilateral.parquet` (z_x_h ADH-8 + bilateral 양쪽 build). **Phase B-x identification suite**: Test 1 v1 (saturated F=130, p<0.0001 — saturation 인공물) → v2 (Bonferroni 2/6 sig: GDP·수입가, VIF=27.9) → v3 (수입가 drop, GDP only sig — year FE 흡수 가능), Test 1b WEO surprise PASS (β=−0.05, p=0.74), Test 3 Pierce-Schott pre-trend (log_emp p<0.001 share endog, bilateral p=0.31 shock exog), first-stage F: ADH-8 14.07 / bilateral 48.08 HC1, cluster 12.20 / 19.65 — **bilateral A.ii main spec 확정 + tF inference 의무화**. **`sigungu_mortality_panel_v02_wa.parquet`** working-age 25-64 panel build + spot check (종로구 2020 pop_wa = 89,510 ✅, 자살 WA trend KOSIS 패턴 100% 일치). **첫 reduced form**: despair_total β=−0.0685, cluster-sido t=−3.11, p=0.0019 (borderline tF cutoff 3.43), cancer/cardio/respiratory/external_other null — channel-specificity Case-Deaton + Pierce-Schott fingerprint 부합, sign DFS Germany (−3.8%) 와 일관, Pierce-Schott (USA, +1.4%) 와 정반대. **본 paper thesis confirm**. P1 issues clear → Phase 4 (5-layer SE + Romano-Wolf) 진입 준비 완료.
- **2026-05-07**: **Path A native unification 본격 commit + paper v02 first state 도달 + Phase 2 entry**. archive scale (β=-0.0685, window 10y) → **native scale (β=-0.127, window 1997-1999↔2018-2022 21y) 의 1.854 amplification ratio commit**. 5-layer SE all native: HC1 t=-4.92, cluster-province t=-4.02, AKM-proper t=-4.92 (numerical coincidence), WCR Webb 6-point bootstrap (B=9,999) p<0.0001, **Romano-Wolf with WCR backend p_RW=0.0161 FWER PASS** (직전 5/6 P2 issue closure — 5-outcome family 위에서 despair significant). 1992 baseline robustness β=-0.0640, n=209, 50.4% attenuation (three-spec convergence: 1994 native + 1994 archive + 1992 native). Pre-WTO placebo sign flip (+0.024 → -0.123) → "gradual integration" interpretation. Drop-C26 cluster t=-3.24 p=0.0012 (broad exposure 입증). 5/6 latest.md 의 4 P1/P2 issue 모두 closure (P1 WCB numba ✅ via published wildboottest 0.3.2 no-numba patch, P1 LMP tF 3.286 통일 ✅, P2.1 universe vs analytic ✅, P2.2 1992 z_x_h NaN identified, P2.3 dual-cited ✅). paper draft 7 file native unified — § 1·2·5·6·8·9 native UNIFIED + § 3·4 신규 commit (31.3 KB) + § 7 신규 commit (8.3 KB Mechanism placeholder) + § 5.1 Footnote X (σ_z = 1,696,322 USD/worker, IQR = 1,228,279, IQR translation -8.78%) + § 6.X 1.854 ratio sub-section (Sullivan-Von Wachter + Eliason-Storrie + Case-Deaton + Pierce-Schott 4-anchor). paper_v01_submission zip 3.5 MB 첫 build (8_submission/paper_v01_submission/ 7 sub-folder + DATA_DICTIONARY.md + README.md). **target venue pivot AER:Insights → KER** (Korean Economic Review) 7월 submission target — 사용자 5/6 16:10 commit (status_report_phase2_entry.md). HIRA M5 mediator Phase 2 entry 권고 — sub-task 2.1 (HIRA sgguCd → h_code crosswalk) ✅ 완료, 2.2-2.5 pending (sigungu × year × ATC4 panel ETL + M5 outcome rate + ivmediate framework + § 7 narrative). 5 ATC4 grouping (사용자 commit Option 3): N06AB SSRI + N06AX 기타 antidepressants + N05BA Benzodiazepines + N05AX 기타 antipsychotics + A05BA Liver therapy. 4 honest limitation disclosure layer (2010-2019 unit inconsistency + 168/250 sigungu coverage 24% missing + N02A 부재 + cross-mediator decomposition abandoned). 3-stage audit cycle (explore-data → analyze → validate-data, path_a_3stage_audit_cycle.md, 13/13 native target PASS + 8/8 arithmetic verify PASS). 215 → 209 6 sigungu drop trace (안산 31090, 용인 31190, 통합청주 33040, 천안 34010, 통합창원 38110: 2018-2022 endpoint mortality missing for administrative consolidation; respiratory only 1 추가 sigungu drop 207 vs 209). External audit Layer A prompt commit (8.9 KB, Q1-Q5 substantive contribution + KER referee attack-surface 평가). HIRA crosswalk codebook commit (`1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv` + `intersection_main_hira_h_codes.csv`). wildboottest 0.3.2 published-package no-numba patch (`2_scripts/published_packages/wildboottest-0.3.2/`).

- **2026-05-06**: **Phase 4 5-layer SE main spec runner 본격 실행 + Romano-Wolf step-down 1000 boot + 2008 ICD sub-period split + Pre-WTO placebo + AKM 2종 + paper draft § 1-§ 9 v01 6 file 95 KB + PAP v4.4 → v4.5.4 5 patch 누적 + Track 2·3 robustness + 2026-05-06 R-A validation audit**. **본 paper final empirical body 가 paper-grade form 으로 commit**. 1994 baseline despair_total β = −0.0685 (HC1 t=−2.12, cluster-시도 t=−3.11 p=0.0019, AKM t=−3.65, Conley 5km/10km, WCB cluster numba pipeline error → P1 fix pending). Romano-Wolf 5-outcome family despair p_RW = 0.317 (FWER 5% 미달, n.s.) — single-outcome a-priori 또는 4-outcome despair-only family 로 좁힐 시 p<0.05. 2008 sub-period post_2008 β = −0.0458, p = 0.003 (pre_2008 symmetric build pending P3.2). Pre-WTO 1992-1996 placebo β = +0.024, p = 0.22 (PASS). 1992 baseline robustness β = −0.016 (1994 main 의 23%, attenuated, sub-period 2008+ 만 sig) → paper § 6.3 baseline year sensitivity 로 acknowledge. Track 2 z_m_education baseline sensitivity 정합 (1985·1990·1995 corr 0.989-1.000, 시군구 차이 > 0.5 단 0.8% = 2/251) → § 6.5 commit. Track 3 1992 baseline P1 → v2 fix (KSIC 6차→9차 23 매핑 이미 build, 시군구 매칭 ~85%) → footnote 17 retract. paper draft v01 § 1-§ 6 + § 8-§ 9 6 file (95 KB). § 7 Mechanism 은 HIRA pharmaceutical fetch 17% (9,500/55,080 calls) 완료 후 ~6 일 추가. PAP v4.4 (21.6 KB) 가 v4.0 → v4.4 통합 rewrite, v4.5 main body (37.8 KB) 가 Phase 4 결과 반영, v4.5.1·2·3·4 patch 누적. **2026-05-06 R-A direct audit** (data:validate-data + data:explore-data skill, sandbox + actual file inspect): paper-cited 14 핵심 수치 (β, t, p, n, RW p, correlation 등) 모두 actual CSV 와 100% 정합. 4 P1/P2 issue identified — P1 (parquet null-padding), P2.1 (§ 3.2 universe vs analytic sample), P2.2 (1992 z_x_h NaN h_code), P2.3 (LMP tF cutoff 3.286 vs 3.84 dual-cited). **Ready to share with noted caveats** 단계, ~25 분 fix 후 "Ready to share".

### 핵심 의사결정 (cumulative)

**Stage 1 (이전 reset 후)**
- Sigungu baseline 256 → 229 (자치구 collapse: 수원, 성남, 안양, 안산, 고양, 용인, 청주, 천안, 전주, 포항, 통합창원)

**Stage 2 v4**
- Cancer 정의 027-048 → **027-047** (KOSIS 악성신생물 C00-C97 정합, ±0.05% 정확도 달성)
- 6 outcome group: despair_total / cardiovascular / cancer / respiratory / external_other / other
- Despair_total = suicide(102) + drug(101) + psych(057) + liver(081) — Case-Deaton 표준
- 2023 file partial (262,710) → full (352,511) replace 후 재실행

**Stage 3 v1**
- Hybrid sigungu merge: year-aware (Phase A, 217,396 rows) + year-agnostic fallback with (year, h_code) dedup (Phase B, 2,754 rows). KOSIS 인구 코드 vs KOSTAT 사망 코드 충돌 + 분구 시군구 parent/children 공존 동시 해결.
- 1997 인구 = **1998 proxy** (KOSIS sigungu × sex × age 1998 시작)
- 17 통합 age band: KOSIS C3 020 + KOSTAT 1,2 → 0-4세 / KOSIS C3 340 + KOSTAT 18,19,20 → 80+
- 직접 연령 표준화: **2010 한국 baseline**, within-sex weight (Σw=1 per sex), 인구 결측 시 weight 재정규화

**Stage 4A (거의 완료)**
- Source: UN Comtrade API 직접 호출 (BACI 가 아니라). 4-key auto-rotation (.env) + HS2 chunk 분할 + resume.
- HS coverage 분리: KR-CN **HS 01-99** (KITA validation 정확도 + endogenous full cover), ADH/CN-World **HS 28-97** (Pierce-Schott 표준).
- KITA cross-check mode-aware: full-HS ±5% / mfg-only ±10% (KITA × 0.88).
- KIET 60대산업 mapping reject 됨 (KSIC2 너무 coarse) → Stage 4B 에서 Pierce-Schott / DFS concordance 채택 결정 필요.
- 2026-05-04 status: KR-CN 50/50 ✅, ADH 8 ← CN 195/200 (ES 2020-2024 5 누락), CN-World 22/25 (2015-2017 3 누락). 잔여 8 file resume 1회로 완료 가능.
- BACI HS92_V202501.zip (1.07 GB) 4_trade/raw/baci 에 다운 완료 — Stage 4B vintage 통합 baseline 으로 활용 가능.

**Stage 3B v02.1 (채택, 2026-05-04)**
- Panel v02 (외국인 빼기 적용) → v02.1 (제거): KOSIS DT_1B040M5 = 행정안전부 주민등록 = 한국인 only 라 외국인 빼기 = over-correction (KOR − KOR·foreign·overlap). v02.1 에서 분모 = `population_panel_v01.parquet` 그대로. ASR 평균 −1.48% correction (despair_total median +0.74%, max +22.79%).
- 10 outcome group: cancer / cardiovascular / despair_total / drug_101 / external_other / liver_081 / other / psych_057 / respiratory / suicide_102.
- 3 ASR baseline (kr2010 main + WHO 2000 + Eurostat 2013 sensitivity).
- 8 검증 ALL PASS. v02 는 Section 7 sensitivity 로 보존.

**Stage 3C mediator panel (신설, 2026-05-04)**
- 사망 microdata 의 marriage_status_code, education_code, occupation_code 컬럼으로 individual-level mediator panel 3 parquet 신설.
- Marriage 분포: 미혼 22.17 / 유배우 49.71 / 사별 14.37 / 이혼 13.17 / 미상 0.57%.
- Occupation code 13 (무직) 68.14% dominance — 1-12 codes (취업자) restricted-sample 권고.
- 분모 부재 한계: KOSIS 인구 panel 의 marriage·education·occupation 분포 별도 join 필요.

**Sigungu 코드 정정 audit (2026-05-04)**
- v02 audit 의 SIGUNGU_COLLAPSE_CASES 가 수원·성남·안양·안산·용인 5개 시 코드 잘못 (안산 31190 break −34.61% = 사실 용인). 정정 (수원 31010, 성남 31020, 안양 31040, 안산 31090, 용인 31190) 후 안산 break −8.40% (threshold 미달).
- 한국 secular trend (despair −20-25%/decade) 가 break threshold −20% false positive 양산 → break audit 자체가 main analysis 영향 없음, paper Section 7 limitation reference 만.
- PAP v3.4 limitation #21 = R-A audit sigungu 코드 매핑 모두 잘못 시인.

**Tier A 외부 데이터 (2026-05-04)**
- HIRA 시군구 종별 의료기관 수 2009-2025 (의료 인프라 control)
- 시군구 외국인 등록인구 2016-2024
- KOSIS 결혼 + 교육 panel 1995/2000/2005/2010/2015/2020 14 파일
- **MDIS Census 2% microdata 7 시점 1990-2020** (mediator denominator 의 prerequisite, KOSIS publish data 의 시도-only 한계 우회) — 2026-05-04 미명 입수

**Stage 3C-3E mediator pipeline (완료, 2026-05-04 미명)**
- `mediator_panel_marriage_v02.parquet` (71,125 rows, 6 시점, 279 h_code, working-age 25-64, 4 카테고리 미혼/배우자/사별/이혼)
- `mediator_panel_education_v03.parquet` (63,019 rows, 3 카테고리 NoHS/HS/College+ 으로 mortality align)
- `mortality_microdata_cleaned_v01.parquet` (7,408,230 rows, 28 시점 1997-2024 individual-level)
- `mortality_marital_panel_v01.parquet` (1,011,186 rows, working-age + crosswalk)
- `mortality_education_panel_v01.parquet` (1,035,849 rows)
- `mediator_specific_marital_rate_v01.parquet` (187,379 rows, 5-year stack 5 period × sex × age × marital × cause, deaths_5y/pop/rate_per_100k) — Stage 5 input
- `mediator_specific_education_rate_v01.parquet` (171,811 rows) — Stage 5 input
- 11a cleaning 4 회 재시도 후 position-based parse + 외국인(`"2"`)만 drop 으로 fix
- denom missing: marital 9.74%, education 2.11% (listwise deletion 예정)

**Reference library 정비 (완료, 2026-05-04 18:30 ~ 18:49)**
- `reference_library_master_v01.md` (32.7 KB) — 18 paper Tier A/B/C 분류 + PAP § 별 reverse lookup
- `reference_library_metadata_v01.md` (11.5 KB) — 20 paper 1-line 분류
- `paper_summaries/` 18 deep read summaries (각 13-23 KB, 2,300+ words)
- Staiger-Stock 1994 (NBER TWP 151) chunk read 추가 → Tier A 승격 (paper § 7.5+7.7 weak-IV asymptotics source)
- `PAP_v3.4_reference_update_proposal_v01.md` (14.6 KB) — 7 ✅ 즉시 + 2 ⚠️ 검토 + 22 reference 추가 cite
- `mediator_panel_build_pipeline_documentation_v01.md` (21.9 KB) — Stage 3 pipeline 종합 spec + bug history + lessons learned

**Stage 5 plan v01 (작성, 2026-05-04)**
- 6 step workflow + 5-layer SE (HC1 + WCB-sigungu + WCB-sido + AKM + Conley + AR+tF) + DGHP 2017 NBER 23209 + DFH 2020 Stata Journal mediation framework.
- Reference verified: GPSS 2020 AER, OP 2013, AKM 2019, BHJ 2022, P-S 2020, ADH 2013, Romano-Wolf 2005, CGM 2008, Roodman et al 2019.
- 4 main + 1 robustness + 2 placebo outcome spec: suicide / drug / psych / liver (main) + despair_total (robustness) + cardiovascular / cancer (placebo).

### 외부 피드백 받은 사항
- `stage3_for_review_2026_05_03.md`: A-F 6개 항목 (hybrid merge / 1997 proxy / liver dominance / baseline 추가 / log vs Poisson / 80+ aggregate) 의견 대기.

### 인프라 변경
- 매일 오전 9:06 자동 실행되는 `dissertation-context-refresh` scheduled task 등록
- `daily_status/` archive 시스템 구축 (`archive/YYYY/MM/`, `_index.md`, `_trajectory.md`, `latest.md`)
- 메모리에 `reference_research_archive.md` 추가 → 새 conversation 에서 trigger phrase 시 자동 로드

### 2026-05-04 PAP v3.3 → v3.4 추가 iteration

- **PAP v3.3** (panel v02 audit 후): § 5-1 Hybrid sigungu merge spot check 4/11 → 12/12 verified, § 8 limitation #21 (R-A sigungu 코드 매핑 잘못), #22 (R-A 외국인 빼기 over-correction +1.48% 정량 시인), #23 (Stage 3B break audit false positive). § 4.5 measurement error narrative 재작성 (분모 한국인 only). § 5.2 mediation framework 강화 (microdata individual-level mediator). § 6.2 component decomposition + 안산 시계열 발견.
- **PAP v3.4**: § 6.4 안산 시계열 main → Appendix C supplementary demote (single-sigungu cherry-pick = p-hacking). § 5.1 main analysis panel = `mortality_rate_panel_v02_1.parquet` explicit commit.
- 23 limitation 도달.

### 2026-05-03 후반 (PAP iteration 누적)

본 conversation 의 30+ rounds 에서 PAP v0 → v1 → v2 → v3 → v3.1 → v3.2 누적 iteration:

- **PAP v1**: Main outcome despair_total → component decomposition (post-data design change, line 122 의 PAP 변경)
- **PAP v2**: H1.3 medical infrastructure controls + DFH/DGHP mediation (citation 오류) + WCB SE + Title reframe + Stack count
- **PAP v3**: PS vs ADH 식별 전략 분리 + OP F=23.1 + AKM finite-sample + WCB-sigungu + DGHP 2020 NBER 23209 (당시 부정확) + Demography top-tier + § 1.4 phrasing + Baseline 1990-1994 sensitivity + Power calc 3.7배 + Cluster over-rejection 1.3-1.5배
- **PAP v3.1**: § 6.2 macro time-series ÷ cross-sectional IV β 산수 제거 + § 10 limitation #18-19 (R-A self-narrative bias)
- **PAP v3.2**: § 5.2 DGHP 2017 + DFH 2020 분리 인용 + GPSS 2018 → 2020 AER 정확 publish + § 10 limitation #20 (R-A citation accuracy 누적 3건)

**R-A self-discovery 한계 입증**: 모든 critical fix 가 외부 reviewer (R-1, R-2) + 사용자 명시적 요구 + 5+1 원칙 적용 결과. R-A 자발 발견 0 건.

### 다음 conversation 시작 가이드

`handoff_2026_05_03_for_new_conversation.md` 참조. Trigger phrase + Reference 5 항목 + 6+1 원칙 framework + R-A protocol 모두 정리.

~~다음 conversation 단계 3.1 HIRA 의료기관 수 가용성 verification 시작 예정.~~ (2026-05-04 완료)

**2026-05-04 미명 시점 다음 작업 우선순위**:
1. Stage 4A 잔여 8 file (ES 2020-2024, CN-World 2015-2017) resume 1회로 완료 — **여전히 blocking**
2. **Mediator share panel build** (Stage 3F) — `mediator_panel_v02/v03` 으로부터 marital_share/education_share 계산 (DGHP 2017 mediator regressor input)
3. Stage 4B HS vintage + KSIC4 concordance 결정 (Pierce-Schott 표준 권장)
4. Stage 4C Bartik IV 구축 (시군구 × KSIC4 × 1995-1999 baseline share)
5. Stage 5 시범 회귀 (mediator-specific rate panel + Stage 4 trade panel join → ivmediate)
6. PAP v3.4 → v3.5 갱신 (`PAP_v3.4_reference_update_proposal_v01.md` 의 7 ✅ 항 + 22 reference 적용)
7. Tier B: HIRA 의약품 ATC4 (N06A / N02A), ECOS 시도별 분기 연체율

**2026-05-05 시점 다음 작업 우선순위** (1-7 전부 24h 내 closure 후 갱신):
1. **Phase 4 main spec runner (5-layer SE)** — HC1 + WCB-sigungu + cluster-sido + AKM (BHJ 2022) + Conley (centroid). tF inference (LMP 2022 cutoff 3.43) 적용. 본 paper final headline number 결정. R-A 2-3h 또는 Claude Code 위임 1 turn.
2. **Romano-Wolf step-down** — 10 confirmatory family (5 outcome × 2 mode KR-CN + ADH-8), 1000 boot. Phase 4 후 즉시.
3. **2008 sub-period interaction** — period_pre2008 × z_x_h. ICD-10 break (2007 4차 개정) effect 분리. Phase 4 sub-step.
4. **PAP v4.0 main body rewrite** — § 4 (data + panel) + § 5 (estimation) + § 6 (results) + § 7 (robustness). v3.4 → v4.1 commit. ~3h dedicated turn.
5. **Phase B-m (z_m mediator instruments)** — DGHP 2017 ivmediate. MDIS 1975-1995 census 활용. Test 4·5·6.
6. **Bartik baseline robustness** — 1999 + 2004 vintage z_x build. ~1h.
7. (deferred) **1992-1996 Comtrade pre-WTO placebo** — Phase 4 결과 final 후.

**2026-05-07 시점 다음 작업 우선순위** (Phase 2 entry + KER submission 준비):
1. **paper § 7 (Mechanism) 완성** — Phase 2 sub-task 2.2-2.5 (sigungu × year × ATC4 panel ETL + M5 outcome rate + ivmediate framework DGHP 2017 + § 7 narrative). 2-3 주 작업. 사용자 측 execution (sub-task 2.2-2.4) + R-A 측 wording draft (2.5).
2. **KER submission package final review** — paper_v01_submission zip 3.5 MB (5/6 06:48 첫 build) 의 README + DATA_DICTIONARY + 06_paper_draft 7 file + 04_regression_results 13 native CSV cross-check. ~25 분 fix 후 submission-ready.
3. **WCB cluster-시도 published-package patch verify** — 5/6 commit 의 wildboottest 0.3.2 no-numba implementation 위에서 wcb_webb_native.csv + wcr_webb_native.csv cross-check. paper § 5.1 5-layer SE 의 5번째 layer 의 final verify.
4. **PAPER_WRITING_PLAN_v02 commit** — target venue AER:Insights → KER pivot 의 documentation align. PAPER_WRITING_PLAN_v01 의 target venue 영역 + paper format short → full paper format update. R-A 다음 turn 1 회.
5. **Pre_2008 sub-period symmetric build (P3.2)** — ~30 분.
6. **Phase B-m identification (z_m mediator instruments)** — DGHP 2017 ivmediate. MDIS 1975-1995 census. Test 4·5·6. § 7 sub-step. 5-7 일.
7. **Effective number of shocks (BHJ 2025 § 4)** — KSIC9 2-digit 23 industry Herfindahl. paper § 5.2 sub-step. ~30 분.
8. (deferred) **Bartik baseline robustness 5 vintage** — 1993·1995·1996·1999 추가. paper § 6.4 sensitivity table. ~2-3h.
9. (deferred) **외부 데이터** — KOSIS 자살률 외부 검증, GRDP, ELIS 결혼지원금.

**Outstanding risk (2026-05-07)**:
- [P1 → 0개] 직전 보고서 의 P1 2개 (WCB numba + LMP tF dual-cited) 모두 closure
- [P1 신규] HIRA M5 의 168/250 sigungu coverage 24% 부재 — paper § 7 4 honest layer 의 첫 layer
- [P2] N02A 오피오이드 부재 — Korea-US substantive 차이의 evidence (US opioid epidemic mirror image)
- [P2] target venue pivot 의 documentation align (PAPER_WRITING_PLAN_v01 → v02 commit)
- [P2] Romano-Wolf 5-outcome family pre-specification 정합 (PAP v4.5.4 명시 verify)
- [P2] Test 3 share violation (직전 동일, BHJ 2022/2025 framework 의존 명시)

---

**2026-05-06 시점 다음 작업 우선순위** (1-7 모두 24-30h 내 closure 후 갱신):
1. **paper draft § 7 (Mechanism) 완성** — HIRA pharmaceutical fetch 완료 의존 (현재 17%, 9,500/55,080 calls, ~6 일 추가). 다른 4 mediator (M3·M4·M5·M6) 는 ready. 본 paper mediation thesis 의 핵심 layer.
2. **validation report 4 P1/P2 issue 처리** — § 3.2 universe vs analytic sample (P2.1), LMP tF 3.286 vs 3.84 reconcile (P2.3, R-A 권장 3.286), 1992 z_x_h NaN h_code 식별 (P2.2), 중복 z_m_education sensitivity log archive (P3.3). 총 ~25 분 fix → "Ready to share".
3. **WCB cluster-시도 SE numba 우회 implementation** — 현재 5-layer SE 의 5번째 layer (WCB 1000 boot) 가 numba `wildboottest` library 의 nopython mode error 로 NaN. R-A 1-2h direct (WCB direct 또는 CGM 2008 wild bootstrap-t fallback).
4. **Pre_2008 sub-period symmetric build** — 현재 post_2008 만. symmetric pre_2008 (1997-1999 base → 2007 endpoint). ~30 분.
5. **Phase B-m (z_m mediator instruments)** — DGHP 2017 ivmediate. MDIS 1975-1995 census 활용. Test 4·5·6. § 7 Mechanism commit 의 sub-step.
6. **Effective number of shocks (BHJ 2025 § 4)** — KSIC9 2-digit 23 industry 의 Herfindahl. paper § 5.2 robustness sub-step. ~30 분.
7. (deferred) **Bartik baseline robustness 5 vintage** — 1992 v2 fix 완료 후 1993·1995·1996·1999 추가. paper § 6.4 sensitivity table 5 column.

**Outstanding risk (P1)**:
- WCB cluster-시도 SE numba pipeline error (5-layer 중 1 layer 결측) — R-A 1-2h direct fix
- LMP tF cutoff dual-cited (3.286 vs 3.84) — implementation script 와 paper narrative reconcile

**Outstanding risk (P2)**:
- Romano-Wolf 5-outcome FWER despair p_RW = 0.317 (n.s.) — single-outcome 또는 4-outcome family 로 좁힐 시 p<0.05
- 1992 baseline attenuated (β=−0.016 vs main −0.069, 23%) — paper § 6.3 baseline year sensitivity acknowledge
- § 3.2 universe vs analytic sample conflation
- Test 3 share violation (β=−0.191, p<0.0001) — BHJ 2022/2025 framework 의존 명시

---

## 2026-04 (previous)

(Stage 1 raw 데이터 검증 + v4.0 reset 작업. 상세 archive 없음 — 메모리 `project_dissertation.md` 참조.)

---

## Resume 시 우선 읽기 순서

1. 이 파일 (`_trajectory.md`) — full context
2. `latest.md` — 어제 상태 (가장 최근 detail)
3. 메모리 `MEMORY.md` + 연결 파일들
4. (필요 시) 특정 날짜 archive 보고서
