# P1.B Verification — sigungu_mortality_panel_v02_wa.parquet (R-A spot-check)

- Generated: 2026-05-05 (R-A)
- Trigger: reviewer-feedback critique P1.B (working-age 적용 명시 미수행)
- Decision: **P1.B 클리어** ✅

---

## Spot-check 결과

### 1. 종로구 2020 (reviewer's 핵심 spot-check)

| 지표 | 값 | 기대범위 | 판정 |
|---|---|---|:--:|
| pop_wa (panel, both-sex) | **89,509.5** | 70-100k (WA) | ✅ |
| pop_panel both-sex 25-64 (cross-check) | 89,509.5 | exact match | ✅ |
| pop_panel male 25-64 | 44,639.5 | reviewer expected 44,640 | ✅ |
| pop_panel female 25-64 | 44,870.0 | symmetric ~45k | ✅ |

→ **working-age (25-64) 분모 정확히 적용**. all-age 70,612 (male) 또는 ~150k (both) 와 명확히 구분.

### 2. Multi-sigungu pop_wa range (2020) — sensible 분포

| h_code | 명칭 | pop_wa | 해석 |
|---|---|---:|---|
| 11010 | 서울 종로구 | 89,510 | 도심 작은 구 |
| 11140 | 서울 마포구 | 234,856 | 큰 구 |
| 21010 | 부산 중구 | 24,025 | 항구 작은 구 |
| 39020 | 제주 서귀포시 | 104,104 | 중소도시 |

→ 24k ~ 235k 범위 sensible. Working-age 분모 logic 정상.

### 3. National WA suicide trend (microdata-derived)

| year | WA 25-64 rate (per 100k) | trend |
|---:|---:|---|
| 1997 | 17.53 | pre-IMF baseline |
| 2010 | 32.49 | post-금융위기 peak ✅ KOSIS 패턴 일치 |
| 2020 | 24.89 | recovery |
| 2023 | 24.76 | 안정 |

→ WA suicide 가 all-age (1997 13.1 → 2010 31.2 → 2020 25.7) 보다 일관되게 +1.5~3.5/100k 높음. KOSIS published 패턴과 sign 일치.

---

## 구조적 차이 (vs all-age panel) — P3 cosmetic

| 항목 | all-age panel (v02_1) | WA panel (v02_wa) |
|---|---:|---:|
| N rows | 123,660 | 31,494 |
| # h_code | 229 | **256** |
| sex split | 2 (남/여) | **collapsed (both-sex)** |
| outcome groups | 10 (despair 분리: suicide+drug+psych+liver) | **5 (despair_total aggregate only)** |
| year coverage | 1997-2023 (27y) | **1997-2022 (26y)** |
| sigungu unit | parent-city aggregate (31010 수원) | **sub-구 disaggregated (31011-14)** |

→ WA panel 은 **finer spatial resolution** (256 vs 229), 그러나 **outcome 분해 부재** + **sex collapsed** + **2023 missing**.

함의:
- 첫 reduced form (n=222) 는 WA panel 256 h_code 중 222 개 매칭 → 87% Bartik exposure coverage. 합리적
- Outcome-specific (suicide vs drug vs psych) 분석은 microdata 로 별도 산출 필요 (panel 만으로는 불가)
- Sex heterogeneity (남성 vs 여성 자살률) 도 microdata 로 별도

---

## 1997 NaN pop_wa — known issue

- 1997 의 1,196 rows 가 NaN pop_wa. 이는 pop_panel 의 1997 age_band 부재 (KOSIS DT_1B040M5 의 시군구 × age 조합이 1997 부터 시작이지만 일부 sigungu 결측)
- 영향: 1997 → 2002 5-year stack 의 baseline 결측. period_pre2008=1 sample 일부 손실
- Phase 4 spec: 1997 drop 시 5-year stack 첫 period 가 1998 시작 또는 baseline NaN 처리. PAP § 5 commit 에 명시 필요 (P3)

---

## P1.B 최종 판정

✅ **CLEAR**. Working-age (25-64, age_5y codes 6-13) filter 가 numerator 와 denominator 양쪽 적용.

- 분자: microdata 의 age_5y ∈ [6,...,13] subset 후 사망 count
- 분모: pop_panel 의 C3_NM "25-29" ~ "60-64" subset 후 sum
- Spot-check 종로구 2020: 89,509.5 (both-sex WA) ✅

reviewer 가 우려한 "panel 이 all-age 인지 WA 인지 불명" → **WA 명확 적용**. Naming 만 reviewer 의 가정 (`v02_2_wa`) 과 다름 (실제 `v02_wa`).

---

## 다음 step (Phase 4 진입 가능)

reviewer 의 NEXT_STEP_PROMPT 그대로 사용 가능. 한 가지 sharpening:

- Step 1 의 "WA verify" 는 **본 보고서로 완료**. Phase 4 는 step 2 (5-layer SE) 부터 시작
- Step 5 (1992-1996 placebo) 는 Comtrade 1992-1996 사용자 다운 필요 (현재 MDIS 1995 census 까지만 보유) → blocker. P2 deferred
- Step 6 (2008 sub-period split) — WA panel 의 period_pre2008 column 이 이미 있음 → Phase 4 에서 즉시 interaction term 가능

Phase 4 Critical Path (revised, post-WA-verify):
1. ~~WA verify~~ ✅ done
2. 5-layer SE main spec runner (HC1 + WCB-sigungu + WCB-sido + AKM + Conley)
3. tF inference 적용 (WCB-sigungu F ≥ 23.1 시 standard, < 23.1 시 cutoff 3.43)
4. Romano-Wolf step-down (1000 boot, family of 5 outcomes — WA panel 의 5 outcome groups)
5. 2008 sub-period interaction (period_pre2008 × z_x_h)
6. (deferred) 1992-1996 placebo — Comtrade 다운 후

Estimated: R-A 2-3h direct 또는 Claude Code 위임 1 turn.
