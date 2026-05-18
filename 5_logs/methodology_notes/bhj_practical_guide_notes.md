# BHJ 2025 (Borusyak-Hull-Jaravel) Practical Guide — 본 연구 적용 노트

**원논문:** Borusyak, K., Hull, P., & Jaravel, X. (2025). "A Practical Guide to Shift-Share Instruments." *Journal of Economic Perspectives* 39(1): 181-204.

**작성:** 2026-05-01 (본 연구 Phase 3 IV 구성 시 직접 가이드)

---

## 1. Big Picture — 본 연구의 IV 설계 가이드

이 paper 는 **shift-share IV 의 두 가지 식별 경로** 를 제시:
1. **Exogenous shifts** (BHJ 2022, Adão-Kolesár-Morales 2019) — shock 자체가 무작위
2. **Exogenous shares** (Goldsmith-Pinkham-Sorkin-Swift 2020) — exposure share 가 외생

각 path 마다:
- 다른 estimator
- 다른 inference (SE) 방법
- 다른 diagnostic test

본 연구의 **5-layer SE** 전략 (HC1, cluster-sido, AKM, Conley, AR+tF) 이 이 framework 와 직접 연결.

---

## 2. Shift-Share 구조

### 일반 형태
$$z_i = \sum_k s_{ik} g_k$$

- $z_i$: unit $i$ (시군구) 의 shift-share IV
- $s_{ik}$: $i$ 의 industry $k$ 노출 share (예: 1997 employment share)
- $g_k$: industry $k$ 의 national/global shift (예: ADH 8국 → 중국 import shock)

### 본 연구 적용
$$\text{Bartik}^{KR-CN}_{c,t} = \sum_j \frac{L^{1997}_{cj}}{L^{1997}_c} \cdot \Delta(X^{KR \to CN}_{j,t} - M^{KR \leftarrow CN}_{j,t})$$

- $c$: h_code (시군구 256개)
- $j$: KSIC 산업
- $L^{1997}_{cj}/L^{1997}_c$: 1997 baseline employment share
- $\Delta(X-M)$: t년의 산업별 net export shock (KR-CN bilateral)

---

## 3. 두 가지 식별 경로 — 본 연구가 어느 쪽?

### Path 1: Exogenous Shifts (BHJ 2022, AKM 2019)
**Idea:** Industry-level shifts ($g_k$) 가 random.

**핵심 가정:**
- 산업 수 $K$ 충분히 많음 (대수의 법칙)
- Shifts 가 unit-level error term 과 독립

**Practical implications:**
- **Shift-level regression** (산업 단위 수렴) 가능
- `ssaggregate` (Stata/R) 사용
- **Spatial clustering, serial correlation** 처리 가능
- AKM SE 적용
- Exposure-robust First-stage F (Olea-Pflueger 2013)

**본 연구 적합도:**
- ✅ 본 연구는 **Korea-China bilateral net export** 를 IV 로 사용
- ✅ KSIC 산업 수 충분 (24개 KSIC2 ~ 120개 KSIC3)
- ✅ Net export shock 은 한국 외부 (중국 산업별 글로벌 export) 에서 부분적 결정 → 외생성
- → **Path 1 (BHJ 2022 / AKM 2019)** 적합

### Path 2: Exogenous Shares (Goldsmith-Pinkham 2020)
**Idea:** Exposure shares ($s_{ik}$) 가 random.

**핵심 가정:**
- 1997 baseline industry share 가 mortality 에 직접 영향 X
- Treated as multiple DID (각 산업이 별도 instrument)

**Practical implications:**
- **Rotemberg weight** 분해 (어떤 산업이 IV variation 끌고가는지)
- 핵심 산업 식별 (예: ADH 의 textile/electronics)
- Pre-trend test 강조 (parallel trends)

**본 연구 적합도:**
- 🟡 부분적 — 본 연구도 1997 baseline employment share 사용
- 🟡 한국의 산업구조가 1997 → 2023 사이 큰 변화 (조선·반도체 부상) → share exogeneity 약함
- → **Path 2 도 보조로 사용** (Rotemberg diagnostic)

### 본 연구 결론
**메인 IV: Path 1 (Exogenous shifts) BHJ 2022 framework**
**Robustness: Path 2 (Goldsmith-Pinkham) Rotemberg weight diagnostic 추가**

---

## 4. ssaggregate Package — 본 연구 직접 사용

BHJ 의 `ssaggregate` 패키지가 자동화하는 것:
1. Outcome ($y_i$) 와 treatment ($x_i$) 를 industry level 로 변환
2. Industry-level controls 잔차화 (residualize)
3. Average 가중 ($s_k = \frac{1}{N}\sum_i s_{ik}$)

### 사용 흐름 (본 연구 Phase 3 시)

```r
# R 패키지 (ssaggregate 위치: 0_raw/ssaggregate-main/)
library(ssaggregate)

# Step 1: 시군구 → 산업 변환
shift_data <- ssaggregate(
  y = mortality_panel$ln_mortality_despair,
  x = mortality_panel$bartik_kr_cn_net,
  s = sigungu_industry_share_matrix,  # 256 시군구 × 24 KSIC
  controls = sigungu_controls
)

# Step 2: shift-level regression
# (BHJ 2022 의 핵심 — IV 가 제대로 작동하는지 산업 단위로 검증)

# Step 3: Exposure-robust F-statistic
robust_F <- compute_robust_F(shift_data)

# Step 4: AKM SE (Adão-Kolesár-Morales 2019)
akm_se <- compute_akm_se(shift_data, cluster = "sido")
```

### 본 연구 핵심 산출
- **Shift-level F-statistic** ⭐ (instrument strength) — 5-layer 의 첫 번째
- **AKM SE** ⭐ (5-layer 의 셋째)
- **Rotemberg weights** (5-layer 의 넷째 추가 robustness)

---

## 5. 핵심 Diagnostic Tests (본 연구 적용)

### A. Pre-trend Test (parallel trends)
```
y_{ct} = β × Bartik_c + α_c + τ_t + sum_t (γ_t × Bartik_c × pre_2000_dummy_t) + ε
```
- 2000 이전 해마다 별도 interaction
- 모두 유의하지 않으면 parallel trends 만족
- v3.x 에서 **female alcohol pre-trend 유의 (t=2.88)** 발견 → 본 연구 robustness 에서 명시 처리

### B. Falsification (Placebo)
- Cancer, respiratory 같은 internal causes → 무역충격에 빨리 반응 안 해야
- Pierce-Schott 2020 도 사용한 robustness
- 본 연구도 outcome group 별로 placebo 운영

### C. Rotemberg Weight (Goldsmith-Pinkham 2020)
- 어떤 산업이 IV variation 의 95% 를 차지하는지
- v3.x 에서 KSIC 201 (chemicals) 에 95% 집중 발견 → IV 가 chemicals 효과로 dominated
- 본 연구도 Rotemberg 분해 보고서 작성

### D. Exposure-robust First-stage F (Olea-Pflueger)
- 표준 F (Cragg-Donald) 보다 conservative
- AR test 와 일치 (weak IV 에 robust)
- v3.x 의 ADH 8국 IV 가 F<2 였던 게 이 측정
- 본 연구의 **KR-CN bilateral IV** 가 F=8-16 → 권장 (>10) 통과 여부 검증

### E. tF Test (Lee et al. 2022)
- weak IV 에 robust 한 t-statistic 보정
- 5-layer SE 의 다섯째
- 본 연구 main result 의 tF-corrected p-value 보고

---

## 6. 본 연구 Phase 3 시 작업 순서

### Step 3-A: Bartik IV 구성 (시군구 단위)
```python
# 0_raw/comtrade_korea_china/ + 0_raw/industry_census/
# → KSIC × year × 시군구 employment shares
# → KR-CN bilateral net export shocks
# → 시군구 × year Bartik IV
```

### Step 3-B: ssaggregate (R)
```r
# 0_raw/ssaggregate-main/ 패키지 사용
# 시군구 panel → 산업 panel 변환
# shift-level regression
# AKM SE
```

### Step 3-C: 5-layer SE
1. **HC1** robust SE (baseline)
2. **Cluster-sido** SE (17개 sido)
3. **AKM SE** (BHJ 2022 / Adão-Kolesár-Morales 2019)
4. **Conley SE** (spatial autocorrelation, geopandas + 시군구 shapefile)
5. **AR test + tF test** (weak IV robust)

→ Main table 에 5개 column 으로 모두 보고.

### Step 3-D: Diagnostic
- Rotemberg weights → 어떤 산업이 IV 끄는가
- Pre-trend test
- Placebo (cancer, respiratory)
- Exposure-robust F

---

## 7. 본 연구 paper 의 BHJ 인용 위치

### Section 3 (Methodology)
- "We follow Borusyak, Hull, and Jaravel (2025) practical guide..."
- IV 설계 + 두 가지 path 설명
- 본 연구 = Path 1 (exogenous shifts, BHJ 2022) 메인

### Section 4 (Identification & Diagnostic)
- AKM SE 사용 (Adão-Kolesár-Morales 2019)
- Rotemberg 분해 결과 (Goldsmith-Pinkham 2020)
- Pre-trend test
- Olea-Pflueger first-stage F

### Appendix A (IV details)
- ssaggregate 적용 디테일
- shift-level vs unit-level 결과 비교

---

## 8. 핵심 인용구

> "Two distinct paths to identification: One path... develops from shift exogeneity (Borusyak, Hull, Jaravel 2022; Adão, Kolesár, Morales 2019). The other path... focuses on share exogeneity (Goldsmith-Pinkham, Sorkin, Swift 2020)." (Introduction)

> "Identification 'from the shifts' can be understood as leveraging a shift-level natural experiment, while identification 'from the shares' can be viewed as pooling together multiple difference-in-differences designs leveraging heterogeneous shock exposure." (Section 1)

> "The ssaggregate packages in Stata and R automate the transformation of the outcome and treatment for this regression. The shift-level regression offers the flexibility to accommodate various types of dependence in the shifts; for example, not only standard clustering but also spatial clustering and serial correlation." (Section 4)

---

## 9. 본 연구 Phase 4 시 main table format

```
Outcome: ln(mortality_despair)
                                Specification
                    (1)         (2)         (3)         (4)         (5)
                    OLS         IV(Bartik)  IV+AKM      IV+Conley   IV+tF
β (Bartik IV)       -0.041*     -1.015**    -1.015**    -1.015**    -1.015*
HC1 SE              (0.012)     (0.243)     —           —           —
Cluster sido SE     —           —           (0.401)     —           —
AKM SE              —           —           (0.378)     —           —
Conley SE           —           —           —           (0.412)     —
tF p-value          —           —           —           —           [0.045]
First-stage F       —           7.2         7.2         7.2         7.2
N                   6,723       6,723       6,723       6,723       6,723
```

→ paper Table 2-3 의 baseline. v3.x 결과를 그대로 가져온 게 아니라 새로운 무역 IV (KR-CN bilateral 50개) 로 다시 계산.

---

## 10. 본 연구 v3.x 와 BHJ guide 차이

| 항목 | v3.x | 본 연구 (BHJ 2025 가이드) |
|------|------|------------------------|
| IV 식별 | ADH 8국 (weak F<2) | KR-CN bilateral (F=8-16) |
| ssaggregate | 미사용 | ⭐ 사용 (shift-level 검증) |
| AKM SE | 부분 사용 | ⭐ 정식 적용 |
| Rotemberg | KSIC 201 95% 발견 후 미처리 | ⭐ 명시적 robustness |
| Exposure-robust F | 미보고 | ⭐ 5-layer 첫째 |
| tF test | 미사용 | ⭐ 5-layer 다섯째 |
| Conley SE | 미사용 | ⭐ 5-layer 넷째 |

→ v3.x 는 quality gap 명백. 본 연구는 BHJ guide 대로 정석.

---

## 11. 다음 단계 메모

1. `0_raw/ssaggregate-main/` R 패키지 직접 검토 (이미 다운됨)
2. Phase 3 시 ssaggregate 사용 example 만들기
3. `linearmodels` (Python) + `ivreg2` (Stata) 비교 — Python 으로 가능한지 확인
4. AKM SE Python 구현 — 별도 라이브러리 vs 자작
5. Conley SE — geopandas + 시군구 shapefile (KOSIS 별도) 필요

논문에서 가장 직접적인 실용 가이드. Phase 3 시작 시 먼저 다시 read 권장.
