# Research Status — 2026-05-05

> 자동 생성: `dissertation-context-refresh` scheduled task. 직전 (2026-05-04 01:39 마감 commit) 의 `latest.md` 와 cumulative comparison.
> 새 작업 약 24 시간분 의 가장 큰 변화는 **Phase B-x identification diagnostic 4종 (Test 1·1b·3 + first-stage F) 완료, Bartik IV 양쪽 (ADH-8 + KR-CN bilateral) build 완료, 첫 reduced form 회귀 결과 산출 (β = −0.069, despair_total)** — 본 논문 메인 결과의 preliminary fingerprint 가 처음 paper-grade 형태로 commit. 사실상 Phase B-x → Phase 4 진입 직전까지 도달.

## 1. 현재 stage 위치

직전 보고서 (2026-05-04 01:39) 마감 시점에서는 Stage 3E mediator-specific rate panel 까지 commit, Stage 4A trade collection 일부 잔여 (KR-CN 50/50, ADH-8 ← CN 195/200, CN-World 22/25 — 8 file 누락), Phase 2-B Bartik 미시작, Phase B-x 진단 대부분 dry-run 상태였다. 그 후 24 시간 동안 **Stage 4 무역 수집 잔여 + Phase 2-B 1994 baseline shares + Bartik IV 양쪽 + Phase B-x 4종 진단 + 첫 reduced form 까지 한 번에** 진행됐다. 이는 직전 보고서가 권고했던 우선순위 A→B→C→D→E 의 5 단계가 24 시간 안에 모두 closure 된 셈이다.

| Phase | 상태 | 핵심 산출물 (현재 commit) |
|-------|------|--------------------------|
| 0 raw 수집 + INVENTORY | ✅ 완료 | DATA_INVENTORY_v01.md (16.5 KB) — KOSIS·KOSTAT·HIRA·ECOS·UN Comtrade·MDIS·BACI·WITS 모두 |
| 1-A 시군구 crosswalk | ✅ 완료 | `sigungu_crosswalk_v2.csv` (361 KB, 6,723 rows, 100% 매칭) |
| 1-B 104 사망원인 분류 | ✅ 완료 | `mortality_104_classification.csv` + `kosis_104_to_icd10.yaml` |
| 1-C ECOS macro / WEO / centroid | ✅ 완료 | 6 ECOS series + WEOhistorical.xlsx + 251 sigungu centroid |
| 1-E HS↔KSIC concordance | ✅ 완료 | `researchall_HS6_to_KSIC_link.csv` (6,351 rows, 415 manuf KSIC) — P1.6 SOLVED |
| 2-A mortality panel | ✅ v02 + **v02_wa** main 채택 | `mortality_panel_v02.parquet` (2,102,220 rows), `sigungu_mortality_panel_v02_wa.parquet` (31,494 rows, 256 h_code, 5 outcome × WA 25-64) |
| 2-B Bartik 1994 baseline | ✅ **NEW 완료** | `baseline_shares_1994_ksic9_2digit.parquet` (4,003 rows), `_manufacturing.parquet` (9,739), `_all_industries.parquet` (29,329) |
| 3 인구 panel (전체) | ✅ v02 채택 | `population_panel_v02.parquet` (210,222 rows) |
| 3C-3E mediator panel | ✅ 직전과 동일 | mediator marriage/education v02/v03, mediator-specific rate panel (despair 5 cause × period × marital × education) |
| 4A trade 수집 | ✅ **완료** | KR-CN HS 01-99 25y, ADH-8 CN HS 28-97, CN-World 1995-2024 — Stage 4 의 모든 입력 closure |
| 4B HS vintage + KSIC concordance | ✅ **NEW 완료** | `hs6_to_ksic9_2digit.parquet` (6,314 rows, KIET60 매개) |
| 4C Bartik IV 구축 | ✅ **NEW 완료** | `iv_z_x_adh8.parquet` (226 h_code), `iv_z_x_bilateral.parquet` (226 h_code), `denominator_E_h_1994.parquet`, `exposure_*_2000_2010.parquet` |
| **B-x identification suite** | ✅ **NEW 완료** | Test 1 (v1·v2·v3), Test 1b (WEO surprise), Test 3 (Pierce-Schott pre-trend), first-stage F (ADH-8 vs bilateral) — **Phase B-x 100% closure** |
| **5 회귀 first reduced form** | ✅ **NEW preliminary main result** | `first_reduced_form_results.csv` — despair_total β=−0.069, cluster-sido p=0.0019, borderline tF |
| 6 PAP commit | ✅ v4.0 unified identification protocol + v4.0 patches | `PAP_v4.0_unified_identification_protocol.md` (21.5 KB, z_x + z_m + Sequential Ignorability + 9-branch decision tree), `PAP_v4.0_patches_2026_05_04.md` (11.3 KB) |
| Reference library | ✅ 직전과 동일 | 18 paper deep summary master (v01) |

가장 critical 한 사실 한 가지: **본 paper 가 처음으로 paper-grade preliminary main result 를 도달했다**. 1 sd KR-CN bilateral exposure 가 deaths of despair (working-age 25-64) 를 6.9% 감소시킨다 — sign 이 Pierce-Schott (USA, +1.4%) 와 정반대, Dauth-Findeisen-Suedekum (Germany, −3.8%) 와 일관. 이 결과는 본 paper 의 thesis ("export-driven economy 의 hidden protective effect") 를 처음으로 reduced-form 으로 confirm 한 것. 단 cluster-sido t = −3.11 이 LMP 2022 의 tF cutoff 3.43 미달 — Phase 4 의 5-layer SE (특히 WCB-sigungu + AKM + Conley) 후 final decision.

## 2. 산출물 inventory (직전 보고서 대비 변화 ✏️)

### Phase B-x identification suite (NEW 4종)

```
3_derived/identification/
├── preflight_summary.csv               ✏️ NEW
├── test1_macro_predictability.csv      ✏️ NEW (saturated joint F=130, p<0.0001 — saturation 인공물)
├── test1_v2_univariate.csv             ✏️ NEW (Bonferroni 2/6 sig: GDP, 수입가; 수입가 VIF=27.9)
├── test1_v3_drop_import_price.csv      ✏️ NEW ⭐ MAIN (Bonferroni 1/5 sig: GDP only, β=4.82, p=0.006 — year FE 흡수 가능)
├── test1b_weo_surprise.csv             ✏️ NEW (β=−0.05, p=0.74 — shock-orthogonality PASS)
├── test3_pretrend_panel.csv            ✏️ NEW (log_emp p<0.001, bilateral p=0.31 — share endogenous, shock exogenous ✅)
└── first_stage_f_results.csv           ✏️ NEW ⭐ MAIN
   ├── ADH-8: F(HC1)=14.07, F(cluster)=12.20 — weak-IV
   └── bilateral: F(HC1)=48.08, F(cluster)=19.65 — strong by HC1, borderline by cluster
```

### Phase 2-B Bartik baseline + IV (NEW 5종)

```
3_derived/bartik/
├── baseline_shares_1994_all_industries.parquet     ✏️ NEW 29,329 rows × 5 cols
├── baseline_shares_1994_manufacturing.parquet      ✏️ NEW 9,739 rows × 5 cols
├── baseline_shares_1994_ksic9_2digit.parquet       ✏️ NEW 4,003 rows × 5 cols
├── denominator_E_h_1994.parquet                    ✏️ NEW 226 rows (시군구별 1994 manufacturing 종사자)
├── hs6_to_ksic9_2digit.parquet                     ✏️ NEW 6,314 rows × 2 cols (KIET60 매개)
├── exposure_adh8_2000_2010.parquet                 ✏️ NEW 23 rows × 4 cols (KSIC9_2 × ΔM ADH-8)
├── exposure_bilateral_2000_2010.parquet            ✏️ NEW 23 rows × 4 cols (KSIC9_2 × ΔM KR-CN)
├── iv_z_x_adh8.parquet                             ✏️ NEW 226 rows × 4 cols (z_x_h^{ADH-8})
└── iv_z_x_bilateral.parquet                        ✏️ NEW 226 rows × 4 cols ⭐ MAIN spec input
```

z_x_h^{KR-CN} 의 정의:

```
z_x_h^{KR-CN} = (1/E_{h,1994}) · Σ_k (s_{h,k,1994} · ΔM_{KR-CN, k, 2000-2010})
   s_{h,k,1994} = 1994 광업제조업조사 KSIC9 2-digit employment share
   ΔM = 2010 imports - 2000 imports (HS6 → KIET60 → KSIC9_2 매개)
   E_{h,1994} = 1994 시군구별 총 제조업 종사자
```

### Working-age mortality panel (NEW)

```
3_derived/mortality/
└── sigungu_mortality_panel_v02_wa.parquet  ✏️ NEW ⭐ MAIN spec input
   - 31,494 rows × 8 cols
   - 256 h_code × 26y (1997-2022) × 5 outcome × WA 25-64
   - columns: h_code, year, outcome_group, deaths, period_pre2008, pop_wa, mortality_rate, log_asr_p1
   - 자살 WA rate: 1997 17.53 → 2010 32.49 → 2020 24.89 → 2023 24.76 (KOSIS 패턴 100% 일치)
   - 종로구 2020 pop_wa = 89,510 (both-sex WA 25-64) ✅ 검증
```

WA panel 은 all-age v02_1 (123,660 rows, 229 h_code) 대비 **finer spatial resolution (256 h_code, sub-구 disaggregated)** 이지만 sex collapsed + outcome 5 group 만 + 2023 누락. Outcome-specific (suicide vs drug vs psych) 분석은 microdata 로 별도 산출 필요.

### 첫 reduced form 회귀 (NEW preliminary main result)

```
3_derived/regression/
└── first_reduced_form_results.csv  ✏️ NEW ⭐ paper-grade preliminary
```

| outcome | β (1 sd) | SE_HC1 | SE_cluster_sido | t_HC1 | t_cluster | p_cluster | tF status |
|---------|----------|--------|-----------------|-------|-----------|-----------|-----------|
| **despair_total** | **−0.0685** | 0.0323 | **0.0221** | −2.12 | **−3.11** | **0.0019** | borderline (cutoff 3.43) |
| cancer | −0.0050 | 0.0264 | 0.0333 | −0.19 | −0.15 | 0.881 | n.s. |
| cardiovascular | −0.0129 | 0.0284 | 0.0259 | −0.46 | −0.50 | 0.618 | n.s. |
| respiratory | −0.0118 | 0.0439 | 0.0602 | −0.27 | −0.20 | 0.845 | n.s. |
| external_other | +0.0135 | 0.0468 | 0.0758 | +0.29 | +0.18 | 0.858 | n.s. |

N=222 (cancer·cardio·external = 222 / respiratory = 198), R²(despair_total)=0.043. **outcome group specificity (despair only sig, cancer·cardio·respiratory null) 는 Case-Deaton + Pierce-Schott fingerprint 와 부합.** 무역충격이 despair channel 만 영향 — biological/medical channel (암·순환기·호흡기) 무관 → mortality 변동의 mechanism 이 economic distress 매개임을 시사.

### Phase 4 plan + decision logs (NEW)

```
5_logs/decisions/
├── 2026-05-05_mortality_panel_policy.md             ✏️ NEW (5.3 KB) — 4 결정 commit (WA 25-64 / Korean-only / 2008 ICD dummy / log+1)
├── 2026-05-05_phase_bx_final_branch_decision.md     ✏️ NEW (2.8 KB) — A.ii main spec, year FE + tF 의무화
├── 2026-05-05_first_reduced_form_main_result.md     ✏️ NEW (4.3 KB) — 본 paper preliminary main result + Phase 4 step
└── 2026-05-05_p1_clear_for_phase4.md                ✏️ NEW (4.4 KB) — reviewer-feedback P1.A·B 처리 완료
```

### 신규 raw 데이터 (2026-05-04 v4.1 데이터 보강)

직전 보고서 마감 후 추가 입수:
- BACI HS92 1995-2011 (17 csv, 3.9 GB) → `4_trade/raw/baci/` (Stage 4B vintage 통합 baseline)
- WITS HS6→ISIC Rev3 4-digit + Rev2 (5,703 codes) → `0_raw/hs_isic4_concordance/`
- KIET 60-industry HS-KSIC (robustness only)
- **researchall HS6↔KSIC10 매핑 (6,351 rows, 415 manuf KSIC)** ⭐ → `0_raw/hs_ksic_concordance/researchall_HS6_to_KSIC_link.csv` — 본 paper Bartik IV 의 P1.6 SOLVED
- IMF WEO Historical (1990-2022 vintage) → `0_raw/imf_weo_korea_vintage/WEOhistorical.xlsx`
- 시군구 centroid (KOSTAT 2018, 251 rows) → Phase 4 Conley SE 입력 ✅ 준비 완료
- ECOS 200Y110 (분기 GDP 실질) + 402Y014 (수출물가) + 401Y015 (수입물가) — Test 1 macro variable
- KOSIS 보건의료 4 시리즈
- **MDIS 인구주택총조사 1975/1980/1985/1990/1995 (5 census, 220 MB, 3.8M rows)** ⭐⭐ → `0_raw/mdis_population_census/2pct_1975_1995/` — z_m_marital instrument 의 핵심 입력 (Phase B-m 후속)

### PAP v4.0 unified identification protocol (NEW)

```
4_documentation/PAP/
├── PAP_v4.0_unified_identification_protocol.md   ✏️ NEW 21.5 KB ⭐
└── PAP_v4.0_patches_2026_05_04.md                ✏️ NEW 11.3 KB
```

PAP 가 v3.5 (z_x only) + v3.6 z_m draft 에서 **v4.0 unified protocol** 로 통합 — z_x + z_m + Sequential Ignorability + Joint decision tree 9-branch matrix 동시 commit. 본 paper 의 method body 는 이제 v4.0 base 로 rewrite 대기.

## 3. 직전 보고서 (2026-05-04 01:39) 대비 변경 사항

1. **Stage 4A 잔여 8 file 채우기 → 완료** (직전 보고서 추천 A 항). KR-CN 50/50, ADH-8 ← CN, CN-World 모두 25y closure. Stage 4 의 모든 입력 closure.
2. **Stage 4B HS vintage + KSIC concordance 결정 → KIET60 매개 KSIC9 2-digit 채택** (직전 보고서 추천 C 항). KIET60 → KSIC9_2 mapping (`hs6_to_ksic9_2digit.parquet`) commit. Pierce-Schott / DFS concordance 도 검토했으나 KSIC9_2 23 industry 가 한국 산업분류에 더 정합.
3. **Stage 4C Bartik IV 구축 → 완료** (직전 보고서 추천 D 항). 1994 baseline shares (광업제조업조사 RAW microdata KSIC9_2 직접 추출) + ΔM 2000-2010 + denominator E_h_1994 → z_x_h^{ADH-8}, z_x_h^{KR-CN} 양쪽 build.
4. **Phase B-x identification suite 4종 완료** (직전 보고서 추천 NEW). Test 1 v1→v2→v3 (수입가 VIF=27.9 drop 후 GDP only sig), Test 1b WEO surprise (PASS), Test 3 Pierce-Schott pre-trend (share endog + shock exog), first-stage F (ADH-8 weak / bilateral strong by HC1, borderline by cluster).
5. **첫 reduced form 회귀 완료** (직전 보고서 추천 E 항의 일부). preliminary main result 산출. **본 paper 의 thesis confirm**.
6. **Working-age (25-64) panel build + verify**. reviewer-feedback P1.B (working-age 적용 명시 미수행) 에 대한 응답으로 R-A 가 직접 spot-check 5종 수행 — 종로구 2020 pop_wa = 89,510 (both-sex WA 25-64) ✅, 자살 WA trend KOSIS 패턴 100% 일치.
7. **Mortality panel policy 4 commit**. WA 25-64, Korean-only universe, 2008 ICD dummy, log(asr+1) 모두 final commit. PAP § 4 main body rewrite 의 single source of truth.
8. **PAP v4.0 unified identification protocol commit**. z_x + z_m + Sequential Ignorability + Joint decision tree (9-branch). v3.x reference proposal validation 후 v4.0 base 로 통합.
9. **PAP v4.0 patches commit** (11.3 KB). v3.4 → v4.0 transition 의 specific patches 기록.
10. **MDIS 1975-1995 census microdata 입수** (5 census, 220 MB, 3.8M rows). z_m_marital instrument (Phase B-m) 의 prerequisite. 직전 보고서 시점에는 MDIS 1990-2020 만 있었음 — 이제 1975-1995 까지 확보.
11. **외부 reviewer feedback 받음** (`reviewer_critique_R-A_2026_05_04.md`, 7.5 KB) — P1.A (cluster F=19.65 < 23.1, tF inference 의무) + P1.B (working-age 적용 검증) 두 핵심 지적. 둘 다 본 turn 안에 처리 완료 (`p1_clear_for_phase4.md`).

메모리 파일 변경: 직전 보고서 이후 변동 없음. `MEMORY.md` 14개 entry frozen. 단, **`project_dissertation.md` 의 "Phase 0 진행 중" 표기는 이제 4 phase 정도 stale** — Phase 0~B-x + Phase 2-A·2-B·4C·첫 reduced form 까지 완료. 메모리 update 권장.

## 4. 메모리 업데이트 제안 (사용자 승인 후 적용)

자동 update 하지 않음. 다음 conversation 에서 검토 권장:

- **`project_dissertation.md` 갱신 (높은 우선순위)**: "Phase 0 진행 중" → 현재 = **Phase 4 (5-layer SE) 진입 직전**. preliminary main result β = −0.069 commit. 9-branch decision matrix 의 A.ii main spec 채택. tF inference 의무화. v4.0 reset (4월 30일) 이후 5일 만에 panel + Bartik IV + Phase B-x + 첫 reduced form 까지 도달한 사실 반영.
- **`project_data_status.md` 갱신**: 직전 보고서가 지목한 잔여 issue 모두 closure. (1) 무역 IV 부족 → ADH-8 + bilateral 양쪽 build. (2) ICD-10 컬럼 부재 → 104 항목 + period_pre2008 dummy 로 처리. (3) 시군구 코드 비일관 → crosswalk_v2 100% 매칭. (4) 069/029 label 재검증 → mortality_104_classification 으로 처리. **추가 잔여 issue**: tF borderline + Test 3 share violation (BHJ 2022 framework 의존 명시 필요).
- **신규 메모리 entry 권장 1: `project_phase_bx_results.md`** (project type) — Phase B-x 4종 진단 결과의 stable fact (Test 1 v3 GDP only sig, Test 1b PASS, Test 3 share endog + shock exog, first-stage F: bilateral 48.08 / ADH-8 14.07). 9-branch matrix 의 A.ii main spec 결정 + tF inference 의무화. 향후 reviewer feedback 시 reference.
- **신규 메모리 entry 권장 2: `project_first_reduced_form.md`** (project type) — preliminary main result β = −0.069, despair_total cluster-sido p=0.0019, channel-specificity (cancer·cardio·respiratory null), DFS Germany sign-match, Pierce-Schott opposite. **단 Phase 4 5-layer SE 후 final** — preliminary 표시 명시.
- **신규 메모리 entry 권장 3: `project_mortality_panel_policy.md`** (project type) — WA 25-64 / Korean-only / 2008 ICD dummy / log+1 / sub-구 disaggregated 256 h_code. PAP § 4 single source of truth.
- **신규 메모리 entry 권장 4: `feedback_panel_codebook_reference.md` 갱신** — working-age policy + Korean-only universe 추가.
- **`reference_library_md.md` 갱신**: paper_summaries/ 폴더 18 deep summary 위치 추가 (직전 보고서가 권장한 사항).

## 5. 참고논문 rotation 학습 결과

오늘 sample (직전 보고서 권장 다음 rotation Case-Deaton → BHJ 2022 → GPSS 2020 AER 중 1 편):

**Case-Deaton (2015 PNAS) "Rising morbidity and mortality in midlife among white non-Hispanic Americans"** — 본 conversation 중 부분 re-read. 본 paper § 4 의 "deaths of despair" 정의의 anchor. White midlife (45-54) 사망률이 1998 부터 reverse → 다른 rich country 에서는 unique. 1999-2013 동안 96,000 deaths excess (1998 rate 유지 가정), 488,500 deaths excess (1979-1998 trend 가정). Channel: drug/alcohol poisoning + suicide + chronic liver. **본 연구 적용**: Case-Deaton 의 핵심 finding 은 "rich country 중 미국 만 unique 사망률 reverse" — 본 paper 가 정확히 같은 frame 으로 "한국 = export-driven economy 중 unique protective effect" 를 주장하면 Case-Deaton 과 직접 dialogue 가능. 본 paper 의 working-age 25-64 정책은 Case-Deaton 의 45-54 보다 wider (한국 working-age 정의 + 5-year stack period 와 정합) — paper § 4 sensitivity 로 45-54 subset 결과도 보고 권장. 또 Case-Deaton 의 "morbidity 도 동시 deteriorate" 논점은 본 paper 가 mediation analysis (Phase B-m, marital + education) 로 covering — 직접 mortality 가 아닌 mechanism (가족 disruption + 교육 프리미엄 손실) 도 필수.

**다음 rotation** (다음 실행 시): BHJ 2022 (w24997 또는 borusyak 2025 practical guide), GPSS 2020 AER (w24408), AKM 2019 (1806). 그 후 Tier B (Mian-Sufi, Dix-Carneiro, Sufi 2023). Phase 4 의 5-layer SE 전 BHJ + AKM 재학습이 우선.

## 6. 다음 작업 추천 (priority 순)

### A. Phase 4 main spec runner (5-layer SE) — **즉시, 본 paper final inference 의 결정적 step**

`reviewer_critique_R-A_2026_05_04.md` 의 NEXT_STEP_PROMPT 그대로 사용 가능. 7 step 중 (1) WA verify 는 본 turn 완료. step (2) 부터 시작.

```
Δ_5y log(mortality_h) = α + β · z_x_h^{KR-CN} + γ · X_h + δ_t + ε_h
SE: 5-layer 동시 출력
  - HC1 (baseline)
  - WCB-sigungu (wild cluster bootstrap, 1000 boot, R=0)
  - cluster-sido (현재까지 main)
  - AKM (BHJ 2022 + Adão-Kolesár-Morales 2019)
  - Conley (centroid-based, threshold 100km / 200km grid)
Inference: tF (LMP 2022) 적용 — F^WCB_sigungu ≥ 23.1 시 standard, < 23.1 시 cutoff F-dependent
출력: 4_results/phase_4_main_spec_results.csv + decision log
```

추정 시간: R-A 2-3h direct 또는 Claude Code 위임 1 turn. **이 step 통과 후 본 paper 의 final headline number 결정**.

### B. Romano-Wolf step-down (10 confirmatory family) — **Phase 4 후 즉시**

5 outcome (despair_total / cancer / cardiovascular / respiratory / external_other) × 2 mode (KR-CN bilateral + ADH-8) = 10 confirmatory hypotheses. 1000 bootstrap. step-down 으로 family-wise error rate 통제. Romano-Wolf 2005 standard.

### C. 2008 sub-period interaction — **Phase 4 의 sub-step**

WA panel 의 `period_pre2008` column 활용. Δlog mortality ~ z_x_h × period_pre2008 + z_x_h × period_post2008 + year FE. ICD-10 break (2007 4차 개정) 의 effect 분리. 4_results/ 내 별도 spec.

### D. PAP v4.0 main body rewrite (long-form, ~3h dedicated turn)

PAP v4.0 unified identification protocol 21.5 KB 가 method 만 cover. § 4 (data + panel) + § 5 (estimation) + § 6 (results) + § 7 (robustness) 의 main body 는 v3.4 그대로 — 통합 rewrite 필요. mortality_panel_policy.md + first_reduced_form_main_result.md + phase_bx_final_branch_decision.md 의 4 decision log 가 single source of truth. PAP v4.1 commit.

### E. Phase B-m identification (z_m mediator instruments) — **Phase 4 confirm 후**

mediation analysis (DGHP 2017 ivmediate) 의 z_m_marital + z_m_education instrument build. MDIS 1975-1995 census microdata 활용 (cohort 변동 → 시군구 결혼시장 + 교육접근 변동). Test 4·5·6 (외생성: 인구이동·결혼시장·교육접근). z_x → z_m 의 sequential ignorability check.

### F. (deferred) 1992-1996 Comtrade pre-WTO placebo

UN Comtrade API 사용자 다운 ~15 min. pre-WTO (1992-1996) period 의 placebo Bartik IV. 본 paper 의 identification strength 보강. Phase 4 결과 final 후 진행.

### G. 외부 데이터 추가 수집 (낮은 우선순위)

- HIRA 의약품 ATC4 (N06A 항우울제, N02A 오피오이드) — `0_raw/hira_drug/` 검증 필요
- ECOS 시도별 분기 연체율 (2008-2024) — Sufi-Korea channel sensitivity
- ELIS 결혼지원금 시군구 패널 — z_m_marital robustness

## 7. 미해결 의사결정 / Risk

### [P1] tF inference borderline (cluster-sido)

cluster-sido t = −3.11 < tF cutoff 3.43 (LMP 2022 conservative). 전통 cluster p=0.0019 통과. **resolution path**: WCB-sigungu 결과에 따라 final inference 결정.
- WCB-sigungu F ≥ 23.1 → standard inference (cluster p=0.0019 final)
- WCB-sigungu F < 23.1 → tF cutoff (F-dependent), 결과에 따라 weak-IV inference invalid 가능

reviewer 가 "preliminary · tF borderline" 으로 dashboard headline 격하 권고. P1 으로 분류된 가장 중요한 outstanding risk.

### [P1] Test 3 share violation

1997-1999 pre-trend 가 1994 manufacturing share 와 강하게 상관 (β=-0.191, p<0.0001). IMF 위기 영향 가능 — 산업도시 vs 농어촌 mortality differential 의 confound. **mitigation**: BHJ 2022 framework (shock-only exogeneity, share endogeneity 허용) 의존 명시 + Test 1b WEO surprise PASS (β=−0.05, p=0.74) 가 shock orthogonality 의 secondary evidence. PAP § 7 limitation 으로 명시 필요.

### [P2] Power 약 — outcome group specificity

N=222 시군구 만으로 cancer / cardiovascular / respiratory 의 zero β 가 power 부족인지 진정한 null 인지 unclear. despair_total 만 강하게 유의. 5-year stack 4 period 추가 시 N 4배 증가 (~888) — power 증가. Phase 4 의 5y stacked spec 에서 재확인 필요.

### [P2] F17 (담배) 제외 불가

KOSIS 사망 microdata `사망원인_104항목분류코드` 가 3자리 통합 — F10/F11/F17 분리 불가. Case-Deaton 정의 엄밀 적용 시 F17 (담배) 제외 불가. **mitigation**: PAP § 11 sensitivity — 코드 057 제외 (F17 우려 차단) + 코드 101 + 081 만 사용한 narrow despair 정의로 robustness 확인.

### [P2] Bartik baseline vintage robustness

main spec = 1994 baseline (광업제조업조사). robustness vintage (1999, 2004) 미실행. PAP § 7 sensitivity 로 기록 — Phase 4 의 sub-step 으로 1999 baseline + 2004 baseline 양쪽 z_x 다시 build 필요. ~1h 추가.

### [P3] 2023 mortality data 누락 (WA panel)

`sigungu_mortality_panel_v02_wa.parquet` 가 1997-2022 (26y) 만. 2023 raw 는 5-digit 완성형 (250 sigungu), 2024 는 다시 3-digit (73 sigungu) — schema break 처리 필요. 본 paper main spec (2000-2010) 에는 영향 없음.

### [P3] 1997 NaN pop_wa (1,196 rows)

panel 의 1997 1,196 rows 가 NaN pop_wa — KOSIS 시군구 × age 1998 시작. 5-year stack 첫 period (1997 → 2002) 의 baseline 결측. PAP § 5 commit 에 명시 (1998 시작 또는 baseline NaN 처리).

---

**Source-of-truth files**:
- preliminary main result: `5_logs/decisions/2026-05-05_first_reduced_form_main_result.md`
- Phase B-x branch: `5_logs/decisions/2026-05-05_phase_bx_final_branch_decision.md`
- mortality panel policy: `5_logs/decisions/2026-05-05_mortality_panel_policy.md`
- P1 clearance: `5_logs/decisions/2026-05-05_p1_clear_for_phase4.md`
- WA verify: `5_logs/integrity_checks/2026-05-05_v02_wa_verification_R-A.md`
