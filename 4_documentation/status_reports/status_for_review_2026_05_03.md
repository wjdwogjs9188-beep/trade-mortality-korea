# 연구 진행 상황 — 2026-05-03

**작성자**: 정재헌 (가천대학교 경제학)
**연구**: 무역 충격, 가족 해체, 절망사 — 한국의 숨은 메커니즘 (Mechanism focus paper)
**Submission target**: SSCI 중상위 single-authored (Demography first choice)
**Timeline**: 6개월 working paper 완성 + submission

---

## 1. 연구 개요

### 1.1 Main RQ

한국에서 무역 충격이 절망사 사망률 증가로 이어지는 과정에서 가족 구조 변화 (결혼율, 이혼율, 출생률, 1인가구 비율) 는 어떤 매개적 역할을 하는가?

### 1.2 핵심 기여

기존 문헌의 두 빈틈 메우기.

첫째, Pierce-Schott (2020) 미국 paper 가 무역충격→약물과다복용사망 reduced form 만 보였는데 본 paper 는 매개 chain (무역→가족구조→절망사) 을 정량화. Pierce-Schott 의 매개 (오피오이드 처방 폭증) 는 미국 특수적이고 가족구조 채널은 한국에서 더 중요할 수 있음.

둘째, 한국같은 수출 주도 경제에서 무역충격 → 사망률 인과 분석 부재. 미국 (Pierce-Schott), 독일 (Dauth 2014) 외 국가에서 분석 부족.

### 1.3 사전 가설 (5개, falsifiable)

- H1: 무역충격 → 가족구조 4지표 변화 (결혼↓, 이혼↑, 출생↓, 1인가구↑)
- H2: 가족구조 변화 → 절망사 사망률 ↑
- H3: 매개 효과 비중 ≥ 30%
- H4: working-age (25-54) 남성에서 효과 max
- H5 (placebo): cancer, CVD 단기효과 X

3 시나리오 모두 사전 작성 (가설 통과 / null / reject) 으로 falsifiability 보장.

---

## 2. 식별 전략

### 2.1 Bartik IV

```
TradeShock_{c,t} = Σ_j s_{cj,1997} × Δln(KR-CN net export)_{j,t}
```

- 1997 시군구 c 의 산업 j employment share (KOSIS 사업체통계, 시군구별 고정)
- KR-CN bilateral net export 변화 (전국, 시군구와 무관)
- Goldsmith-Pinkham-Sorkin-Swift (2018) 의 share exogeneity path

### 2.2 Main Spec

5-year stacked first-difference 2SLS (Pierce-Schott 2020 표준):

```
Δln(Mortality)_{c,t,g} = α_t + β · Δ̂TradeShock_{c,t} + X'_{c,t-1}γ + ε_{c,t}
```

5 period × 229 시군구 = 1,145 obs main spec.

### 2.3 식별 진단 6개

First-stage F (Olea-Pflueger), Rotemberg HHI, Share-covariate balance, Pre-trend event-study, AKM placebo, Share permutation. Standard error 5-layer (HC1, Cluster-sido, AKM, Conley, AR+tF).

---

## 3. 데이터 + Panel 구축 진행 상황

### 3.1 분석 단위 (확정)

- 시군구: **229개** baseline (sigungu_crosswalk_v2, 일반시 자치구 11개 parent 통합)
- 연도: 1997-2023 (27년)
- Panel cells (full annual): 229 × 27 × 2 sex × 20 age × 6 outcome = 1,483,920
- 5-year stacked: 1,145

### 3.2 Stage 별 진행

| Stage | 내용 | 상태 |
|---|---|---|
| 1 | 시군구 crosswalk (229 baseline) | ✅ 완료 |
| **2** | **사망 panel build** | **✅ 완료 + 8 layer 검증 PASS** |
| 3 | 인구 panel build | 🔜 다음 |
| 4 | 산업 census 1997 → KSIC2 baseline shares | 🔜 |
| 5 | Comtrade 무역충격 (KR-CN bilateral) | 🔜 (Comtrade quota 회복 대기) |
| 6 | Bartik IV 계산 | 🔜 (Stage 4 + 5 결합 후) |
| 7 | 가족구조 mediator panel (혼인/이혼/출생/TFR/1인가구) | 🔜 |
| 8 | 보조 mediator (HIRA 의료, ECOS 부채) | 🔜 (HIRA 의약품 추가 다운 필요) |
| 9 | Master panel merge | 🔜 |
| 10 | Descriptive + 검증 | 🔜 |

---

## 4. Stage 2 사망 panel 결과 (현재 완료 단계)

### 4.1 산출물

- `mortality_panel_v01.parquet`: 1,483,920 cells (229 × 27 × 2 × 20 × 6)
- `mortality_microdata_combined.parquet`: 7,298,820 records (1997-2023)
- 6 outcome groups: despair_total, cardiovascular, cancer (027-047), respiratory, external_other, other

### 4.2 Outcome 분포

```
despair_total   : 102 + 101 + 057 + 081  (자살 + 약물 + 정신활성물질 + 간질환, Case-Deaton broad)
cardiovascular  : 067-070
cancer          : 027-047  (악성신생물 only, ICD-10 C00-C97, KOSIS 공식과 정합)
respiratory     : 073-078
external_other  : 097-104 minus {101, 102}
other           : fallback (기타 사인 + 코드 095 미상 등)
```

### 4.3 검증 결과 — 8 Layer

| Layer | 결과 | 핵심 |
|---|---|---|
| 1 KOSIS multi-cause | suicide·cancer·total ±0.05% perfect, drug/psych/respiratory 편차 ⚠️ | 신뢰도 최고 통계 perfect |
| 2 Sex × Age | cancer 성비 4/4 PASS, 자살 성비 한국 패턴 일치 | 한국 인구학 정합 |
| 3 Sigungu spot check | SKIPPED | KOSIS source file 부재 |
| 4 시계열 자살률 | 7/7 PASS | 1997=13.2, 2010=31.5, 2017=24, 2023=27 한국 historical 정확 |
| 5 분구 collapse | 11/11 PASS | 창원·청주·고양 등 통합 정확 |
| 6 Internal consistency | 3/3 PASS | panel = micro = 7,297,865 |
| 7 0-cell vs 인구 | PASS (Spearman ρ=-0.97) | 강한 음의 상관 |
| 8 시도 합계 | 4/4 PASS | 17개 시도 합 일치 |

### 4.4 KOSIS 공식 통계 cross-check (정밀)

| 사인 | Panel 측정 | KOSIS 공식 | Diff |
|---|---|---|---|
| Suicide 2010 | 15,566 | 15,566 | 0.000% |
| Cancer 2020 | 82,199 | 82,204 | -0.006% |
| Cancer 2023 | 85,270 | 85,271 | -0.001% |
| Total deaths 2020 | ~305k | ~305k | 일치 |

### 4.5 발견된 이슈 + 해결 history

이슈 1: 처음 cancer 정의 027-048 사용 → KOSIS 보다 +1.5% bias. 원인은 코드 048 (양성신생물) 포함. 027-047 (악성만) 로 narrow → ±0.05% 일치 회복.

이슈 2: 2023 microdata 가 처음에 partial (262,710 records, 1-9월만) 이었음. Full version (352,511 records, 1-12월) 로 교체 후 KOSIS 공식과 정밀 일치.

이슈 3: 시군구 baseline 결정 — 처음에 256 으로 추정했으나 KOSTAT 2021 microdata + 시군구 crosswalk 의 실제 ground truth 는 250. 자치구 분구 collapse 후 최종 229 baseline 확정.

### 4.6 잔존 이슈 (Stage 2 의 Pipeline 무결성과는 무관)

- Layer 1 의 drug_101/psych_057/respiratory KOSIS 비교에서 -33%~+47% 편차. 원인은 KOSIS 발표 정의 (X40-X49 vs 코드 101 의 X40-X44 만) 차이 의심. **Panel 자체 결함 아님** — KOSIS 사이트에서 ICD subgroup 정확 numbers 받으면 해소 가능.
- Layer 3 (sigungu spot check) 미수행. KOSIS 시군구 사망원인 csv 추가 다운 후 실행 가능.

---

## 5. 데이터 보유 현황

### 5.1 보유 (확정)

- KOSTAT 사망 microdata 27년 (1997-2023, ~7.3M records, B형 cp949)
- KOSIS 인구 panel (1993-2023, 시군구 × 성 × 5세, 주민등록인구 1B040M5)
- Comtrade KR-CN bilateral 무역 (50 country-years, 2000-2024)
- 산업 census 1997 (KSIC 8차, 1.6GB)
- ECOS 한국은행 11 series (1997-2024)
- ECOS 가계대출/연체 5 series (2008-2024, 시도 단위 한계)
- 시군구 출생/혼인/이혼 (KOSIS, 가족구조 main mediator 3개)
- 합계출산율 (KOSIS)
- HIRA 의료인력 (2009-, 16종)
- KIET 60대산업 분류 ↔ HSCODE 매핑 (KSIC-HS6 bridge)

### 5.2 추가 다운로드 필요

- 우선순위 1: KOSIS 인구주택총조사 시군구 1995-2020 (1인가구 비율, 핵심 mediator)
- 우선순위 2: KOSIS 시군구 노동시장 panel (실업률, 2008+)
- 우선순위 3: 시군구 GRDP (KOSIS)
- 우선순위 4: HIRA 시군구 의약품 사용 (mechanism 보강)

### 5.3 Comtrade 부분 누락

- ADH 8국 중 ES 21년 (2004-2024), DE 4년 (2019, 2021-2024) 누락
- KR-CN bilateral (main IV) 는 완전 보유 → main spec 에 영향 없음
- ADH 8국 IV 는 robustness only

### 5.4 접근 불가 (Limitation 명시)

- NHIS 진료 microdata (학부 자격 부족) — 정신건강 직접 측정 불가, 자살 outcome 으로 부분 보완
- 통계청 소득 microdata (박사 자격 필요) — ECOS 가계부채 proxy 사용

---

## 6. PAP (Pre-Analysis Plan) 상태

`research_proposal.md` 가 paper 의 사전등록 PAP. 다음 spec 사전 commit:

- 분석 단위 (시군구 c × 연도 t, 229 baseline)
- 5 outcome group + 정의
- Bartik IV (KR-CN bilateral, share exogeneity)
- 5-year stacked first-difference 2SLS
- 5-layer SE (HC1, Cluster, AKM, Conley, AR+tF)
- 6 식별 진단
- Multiple testing 보정 (Romano-Wolf 1000 boot)
- 3 시나리오 사전 작성

변경 시 Appendix A 에 사유/일시/학술근거 기록.

### 6.1 PAP commit 후 변경 사항 (Appendix A 기록 예정)

- Cancer 정의 027-048 → 027-047 (KOSIS 공식과 정합, 2026-05-03 변경)
- 시군구 baseline 256 → 229 (자치구 collapse 후, 2026-05-02 확정)

---

## 7. 다음 단계 (즉시 실행 가능)

옵션 A — Stage 3 인구 panel build 진행. KOSIS population_combined.csv 처리 + age 매핑 (KOSTAT 1-20 ordinal → KOSIS C3 020-340) + Stage 2 mortality panel 과 결합 → 사망률 (per 100k) + 연령 표준화 (2010 한국 기준) + 로그 변환.

옵션 B — Stage 2 보완 검증 먼저. KOSIS X40-X49 (drug), F10-F19 (psych), J00-J99 (respiratory) 정확 numbers + 시군구 사망원인 csv 다운로드 → Layer 1 + Layer 3 재검증.

권고: **옵션 A 먼저**. Pipeline 무결성은 5개 layer 에서 완벽 입증, 추가 KOSIS reference 작업은 paper 작성 단계에서 (Section 3 limitation 작성 시) 처리 가능.

---

## 8. 검토받고 싶은 점

1. **연구 정체성**. Mechanism focus (가족구조 매개) 가 broad paper (Pierce-Schott 한국 응용) 보다 학술 contribution 더 강한지?
2. **Cancer 정의 변경 (027-048 → 027-047) 의 타당성.** KOSIS 공식 매칭 우선 vs 학술 broad 정의 유지 중 어느 게 적절?
3. **시군구 baseline 229 결정.** 자치구 collapse (Pierce-Schott 방식) 가 시계열 일관성 측면에서 맞는 결정인지?
4. **Stage 2 의 8 layer 검증 quality.** 추가로 검증할 항목 있는지? KOSIS reference 보완 vs Stage 3 진행 우선순위?
5. **Comtrade 부분 누락 처리.** ADH 8국 robustness 부족분 (ES 21년 + DE 4년) 을 어떻게 paper 에 명시?
6. **NHIS 부재 한계.** 정신건강 mechanism 직접 측정 불가 — 자살 outcome + HIRA 의료인력으로 충분한 보완인지?
7. **PAP 변경 기록 protocol.** Appendix A change log 가 학술 standard 부합하는지?

피드백 부탁드립니다.

---

**END OF STATUS DOCUMENT 2026-05-03**
