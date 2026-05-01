# Methodology

**Last update:** 2026-05-01

이 문서는 본 연구의 방법론 결정과 각 결정의 근거를 기록합니다. 모든 결정은 `5_logs/decisions/` 에 별도 markdown 파일로도 보존됩니다.

---

## 1. 연구 질문

> 한국 같은 export-oriented 경제에서 중국과의 무역 노출이 시군구 단위 사망률에 미친 인과적 효과는 무엇인가?

기존 문헌과의 차별점:
- 미국(ADH, Pierce-Schott, Finkelstein NAFTA): import 충격 → manufacturing ↓ → mortality ↑
- 한국: 중국에 중간재 export → manufacturing 보존 가능성. mirror image?

---

## 2. 핵심 가설

### 가설 A — Hidden Protective Effect
중국 무역 노출이 한국 시군구 사망률을 **낮춘다**. Finkelstein-Notowidigdo-Shi (2026) 의 mirror image: 미국 manufacturing -1pp → mortality +1.4%; 한국 manufacturing +pp → mortality 감소.

### 가설 B — Two Opposing Forces
한국에는 두 힘이 동시에 작동:
- Bilateral force (한국-중국 양자): 한국 수출 dominant → 보호효과
- China-World force (중국 vs 세계): 한국이 제3시장에서 share 잃음 → adverse 효과

### 가설 C — Geographic Bifurcation
광역시는 미국식 import-competition 우세 (adverse), 도(지방)는 산업단지 export 우세 (protective). 전국 평균은 net.

### 가설 D — Cardiovascular Mechanism (not Mental Health)
한국 NHI 보편 + EI + 기초생활보장 → mental/suicide 채널 약화. 대신 manufacturing 보존 → 신체 부담 감소 → 심혈관 사망 ↓ dominant. (Pierce-Schott FEDS 2016 AMI -3.8% + Ruhm 1996 procyclical 정합)

⚠️ 가설 A-D는 사전 등록만, 실증 결과 따라 검증/기각.

---

## 3. 데이터 (모두 verified raw)

| 데이터 | 출처 | 기간 | 검증 |
|---|---|---|---|
| 사망 microdata | KOSIS DT_1B34E03 (MDIS) | 1997-2024 | KOSTAT ±1% |
| 시군구코드집 | 통계청 1997-2021 | 24개 (매년) | ✅ |
| 인구 | KOSIS DT_1B040M5 시군구×성×5세 | 2000-2024 | KOSTAT 전국합 |
| 사업체조사 | KOSIS (1995 전수, 2000+ 10인 이상) | 1994-2024 | 1995=2,771,068행 |
| Korea-China 무역 | UN Comtrade bilateral HS6 | 2000-2024 | 한국공식 ±0.1% |
| ADH 8-국 무역 | UN Comtrade | 2000-2024 | 호주·덴마크·핀란드·독일·일본·뉴질랜드·스페인·스위스 |
| China-World | UN Comtrade (China reporter) | 2000-2024 | $45,607B 25년 |
| Census 2% | 통계청 | 1990, 1995, 2000, 2005, 2010 | 5개년 |
| 자영업 | KOSIS DT_1ES3A07S 시군구별 | 2013-2025 | 137 시군구 |
| 가계부채 | BOK ECOS 시도 단위 | 1990-2025 | 시도 17 |
| Land price | KOSIS DT_1YL20881E 시군구 | 1987-2026 | ✅ |
| 복지 (수급권자) | 보건복지부 시군구 | 2012-2019 | 238 시군구 |
| KSIC 연계표 | 통계청 8/9/10/11차 | 공식 | ✅ |
| HS6 → KSIC | UN CPC21 매개 | 공식 | 31,384 매핑 |

**핵심 결정 (2026-04-30):** 사망 사인은 KOSIS 104항목 코드를 신뢰하지 않고 **ICD-10 raw에서 직접 추출**. 이전 v3.x에서 코드 069="drug" / 029="alcohol" 라벨 mislabel 확인됨.

---

## 4. 식별 전략 (Bartik IV)

### 4.1 Treatment
```
ΔIPW_r,t = Σ_j (L_rj,1995 / L_r,1995) × (ΔM_jt / L_j,1995)
```
- r: 시군구, j: KSIC 5-digit
- L_rj,1995: 1995 사업체조사 전수 (Bartik baseline)
- ΔM_jt: 한국의 산업 j 중국 수입 변화 (2005-2019)

### 4.2 Primary IV — Korea-China Bilateral
```
Z_r = Σ_j (L_rj,1995 / L_r,1995) × (ΔM_jt^OTH / L_j,1995)
```
8개국 중국 수입 (호주·덴마크·핀란드·독일·일본·뉴질랜드·스페인·스위스).

⚠️ **결정 (2026-04-29):** 한국에서는 표준 ADH 8-country IV가 weak (F<2). 이유: 한국 자체가 8국과 비슷한 경쟁국. → Korea-China bilateral 직접 IV 우선 사용 (F=8-16).

### 4.3 Alternative IV — China-World
```
Z_r^{CW} = Σ_j (L_rj,1995 / L_r,1995) × (ΔX_j^{CN→World} / L_j,1995)
```
중국이 제3시장으로 수출 확대 → 한국 산업이 제3시장에서 share 잃음 → adverse force.

### 4.4 BHJ 2025 JEP 7-step checklist 준수

1. ✅ Idealized experiment: China industry-level productivity 충격
2. ✅ Bridge: 8국 imports = China supply proxy
3. ⚠️ **Incomplete shares control**: manufacturing share + period × manufacturing interaction (BHJ 2025 권고)
4. ✅ Lag shares: 1995 baseline (analysis 시점 2000+ 보다 앞)
5. ✅ Effective number of shifts: KSIC 5-digit ≥ 50
6. ✅ Balance tests: industry-level (skill/wage/computer) + region-level (인구구성)
7. ✅ Exposure-robust SE: AKM 2019 + ssaggregate (BHJ 2022)

---

## 5. 통제변수

### 시군구 수준
- log 1995 인구
- log 1995 manufacturing 고용
- 1995 manufacturing density (BHJ incomplete share)
- **2013 자영업 비율** (한국 specific — 25.1%, 미국 10.6%·독일 10.2%의 2배)
- 시도 (sido) FE

### 시점
- Year FE
- Sido × year FE (heterogeneity check)

### 자영업 endogeneity 처리
- 2013-2019 자기상관 0.976 → structurally slow-moving
- Robustness: 2014/2015/2019 baseline + imputation으로 sensitivity

---

## 6. 추론 — 5-layer 동시 보고

| Method | Reference | 처리 |
|---|---|---|
| HC1 robust | White (1980) | heteroskedasticity |
| Cluster-sido | Cameron-Miller (2015) | within-sido 잔차 |
| AKM industry-cluster | Adão-Kolesár-Morales (2019) | sectoral composition |
| Conley spatial-HAC | Conley (1999) 50/100/200km | 지리적 상관 |
| AR weak-IV-robust | Anderson-Rubin (1949) | weak IV CI |
| **tF critical value** | Lee-McCrary-Moreira-Porter (2022) | F<10 시 1.96 → ≥3.43 |

**원칙:** 하나라도 유의성 잃으면 paper에 명시. 5개 모두 통과한 결과만 main result.

---

## 7. Robustness Battery (사전 등록)

1. Pre-trend placebo (1997-1999, 5 historical windows)
2. Outlier sensitivity (Cook's distance, top-5/10 |bartik|, 울산·여수 제외)
3. Sub-period (2000-2008 boom vs 2009-2019 post-GFC)
4. Sample cuts (광역시 vs 도, 137 SE-restricted vs 204 imputed)
5. Rotemberg (top 5 / KSIC 201 chemical 제외)
6. ssaggregate (BHJ 2022 industry-level)
7. Alternative IV (China-World, Asia-only, EU-only, North America-only)
8. Period × manufacturing share interaction (BHJ 2025)
9. Mechanism placebo (cancer, respiratory — long latency)
10. Self-employment 대안 (2014/2015/2019 + imputed)

---

## 8. 분석 phase

| Phase | 내용 | 출력 |
|---|---|---|
| 0 | 폴더 + raw 추출 + INVENTORY | 0_raw/, INVENTORY.csv |
| 1 | Codebook (ICD-10, KSIC, 시군구) | 1_codebooks/*.yaml |
| 2 | 모든 panel 구축 + KOSTAT cross-check | 3_derived/*.parquet |
| 3 | Bartik IV (4 gate) | bartik_iv.parquet |
| 4 | 회귀 + 5-layer 추론 | regression_log.csv |
| 5 | 이질성 + mechanism | by_geography.csv |
| 6 | Robustness battery | robustness_log.csv |
| 7 | 논문 v4.0 작성 | 7_paper/v4.0.md |

---

## 9. 결정 기록

방법론 결정은 모두 `5_logs/decisions/YYYY-MM-DD_*.md` 에 별도 기록.

주요 결정:
- 2026-05-01: ICD-10 raw 직접 추출 (104항목 신뢰 X)
- 2026-04-29: Korea-China bilateral IV (ADH 8국 weak)
- 2026-05-01: 5-layer SE 동시 보고
- (이후 추가)

---

## 10. Risk Register

| Risk | 영향 | 대응 |
|---|---|---|
| Weak IV (F<10) | 통계 약화 | tF + AR CI |
| Female pre-trend 유의 | identification | Female 별도, male primary |
| 자영업 endogeneity | 통제 정당성 | 자기상관 + Robustness |
| Mortality mislabel 재발 | 결과 무효 | ICD-10 직접 + KOSTAT cross-check 자동 |
| 시군구 코드 24년 변경 | 시계열 일관성 | 통합 sigungu_24years.yaml |
| Korea-China bilateral endogeneity | IV 약함 | China-World 대안 + balance test |

---

## 11. 학술 기여

### Empirical
- 27년 한국 사망 microdata 1.0M+ 시군구 × cause panel 첫 구축·공개
- Korea-China bilateral Bartik IV 강력한 first-stage demo
- ICD-10 직접 추출의 중요성 (이전 paper 의존성 risk 노출)

### Methodological
6 가지 비-U.S. ADH 권고:
1. Bilateral 측정
2. Country-specific labor controls (자영업)
3. Sub-period analysis
4. Geographic decomposition
5. Rotemberg ≠ LATE
6. 5-layer inference

### Theoretical
"Trade-mortality 관계의 sign은 무역 방향성과 manufacturing 반응에 의존" — Finkelstein 2026 framework의 한국 case.
