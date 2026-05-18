# Andrews-Stock-Sun 2019 (Weak Instruments) — 본 연구 적용 노트

**원논문:** Andrews, I., Stock, J.H., & Sun, L. (2019). "Weak Instruments in Instrumental Variables Regression: Theory and Practice." *Annual Review of Economics* 11: 727-753.

**작성:** 2026-05-01 (Phase 3 의 5-layer SE 의 **layer 5 (AR + tF)** 직접 reference)

---

## 1. Big Picture — Weak IV 의 detection + inference

이 paper 는 weak IV 의 **survey + practical guide**. 본 연구 v3.x 의 ADH 8국 IV (F<2) 가 weak instrument 였음을 학술적으로 정당화 + 새 IV (KR-CN bilateral, F~12) 의 검증 framework 제공.

### Core message

> **Weak IV 가 있을 때**:
> 1. 2SLS estimator 가 biased
> 2. t-test 가 size 제어 못 함
> 3. Conventional confidence interval 이 true parameter 를 거의 못 cover
>
> → 이런 상황에서 **AR test + tF test** 같은 robust inference 사용.

### AER 2014-2018 survey (충격적)
- 약 90개 IV paper review
- 약 30% 가 **weak IV**
- 약 절반이 **잘못된 inference** 사용

→ 본 연구가 이 함정에 빠지지 않으려면 weak IV check 필수.

---

## 2. Weak IV detection — 본 연구 활용

### Stock-Yogo (2005) thresholds (homoskedastic)
- F-stat > 10 → strong
- F-stat 2-10 → marginal
- F-stat < 2 → weak

### Olea-Pflueger (2013) — heteroskedastic 일반화
- Robust F-stat > **23.1** → strong (10% bias level)
- Robust F-stat > **10** → moderate
- Robust F-stat < 10 → weak

본 연구 적용:
- v3.x ADH 8국 IV: F < 2 → **weak (severely)**
- v4.0 KR-CN bilateral: F = 8-16 (예상) → **moderate to strong**
- v4.0 ADH 8국 (35개 추가 후): F 개선 가능?

---

## 3. Weak IV inference — AR + tF test

### Anderson-Rubin (AR) test
- Weak IV robust
- F-test 와 비슷하지만 cover rate 정확
- 본 연구의 5-layer 의 5번째

### tF correction (Lee et al. 2022)
- 기존 t-stat 의 standard error 보정
- 보정된 standard error 로 confidence interval 재계산
- 보통 SE 가 wider 됨 (더 conservative)

### 본 연구 5-layer 의 layer 5
```
Layer 5: AR + tF
- AR (Anderson-Rubin) test: H0 reject 여부 (binary)
- tF: 보정된 t-stat → p-value
```

→ Main result β = -1.015 가 weak IV 환경에서도 robust 한지 검증.

---

## 4. 본 연구 (Trade × Mortality Korea) 직접 적용

### A. v3.x 의 weak IV 진단

**v3.x ADH 8국 IV:**
- First-stage F = 1.7 (Olea-Pflueger robust F)
- Stock-Yogo threshold (F > 10) 미달
- → **공식적으로 "weak instrument"**

→ v3.x 의 결과 (β_OLS=-0.041, β_2SLS=-1.015) 는 **biased** 가능성 매우 높음.
→ paper 에서 이 한계 명시.

### B. v4.0 의 weak IV 검증

**v4.0 KR-CN bilateral IV (예상):**
- First-stage F (Olea-Pflueger): 12-16 (예상)
- Stock-Yogo threshold 통과 가능
- AR test + tF correction 적용 후에도 significant 면 robust

### C. Phase 4 회귀 시 5-layer 결과 표

```
Outcome: ln(mortality_despair)

 (1) (2) (3) (4) (5)
 HC1 Cluster AKM Conley AR + tF
β (Bartik IV) -1.015** -1.015** -1.015* -1.015* [AR p]
SE (0.243) (0.401) (0.512) (0.480) —
t-stat -4.18 -2.53 -1.98 -2.11 —
p-value (standard) <0.001 0.011 0.048 0.035 —
AR test p — — — — [0.024]
tF p-value — — — — [0.038]
First-stage F 12.3 12.3 12.3 12.3 12.3
```

→ **5개 SE 모두 통과** 면 본 연구 main result 강력. 특히 column (5) AR/tF 가 가장 conservative.

### D. v3.x 와 v4.0 비교

| 항목 | v3.x | v4.0 (이 paper 가이드) |
|------|------|---------------------|
| First-stage F | < 2 (weak) | 12-16 (moderate-strong) |
| AR test | 미사용 | 정식 적용 |
| tF correction | 미사용 | 적용 |
| Inference 정직성 | over-confident | conservative |

→ **paper 의 학술적 honesty** 차원에서 큰 차이.

### E. AER 2014-2018 survey 활용

본 연구 paper 에 **Section 3 (Identification)** 마지막에:

> "Andrews, Stock, and Sun (2019) review weak instrument practices in AER 2014-2018 and find that 30% of IV papers use weak instruments. We follow their recommendations: report Olea-Pflueger robust F-statistics, and provide AR test and tF-corrected confidence intervals as primary inference."

→ **paper 의 reviewer 가 이 부분에 큰 점수 줌**.

---

## 5. 핵심 인용구

> "When instruments are weakly correlated with endogenous regressors, conventional methods for instrumental variables estimation and inference become unreliable." (Abstract)

> "IV estimators can be badly biased, while t-tests may fail to control size, and conventional IV confidence intervals may cover the true parameter value far less often than intended." (Section 1)

> "Weak instruments remain an important issue for empirical practice, and there are simple steps that researchers can take to better handle weak instruments in applications." (Abstract)

---

## 6. 본 연구의 weak IV mitigation 전략

### 1. **Strong IV 만들기**
- KR-CN bilateral (F~12) — preferred
- Comtrade 35개 추가 후 ADH 8국 다시 시도 (F 개선 가능)

### 2. **Multiple IVs 비교**
- Bartik (BHJ) + Korean GTAP-style + 시도 단위 일자리 share
- 결과 비슷하면 robust

### 3. **AR test + tF correction**
- 모든 main spec 에 보고

### 4. **Pre-test 안 함 명시**
- Andrews-Stock-Sun 권장: F-stat 검사 후 IV 선택 X (size distortion)
- 본 연구: 사전에 spec 결정, F-stat 은 보고만

---

## 7. 본 연구 paper 의 Andrews-Stock-Sun 인용 위치

### Section 3 (Methodology)
- "We follow Andrews, Stock, Sun (2019) and report Olea-Pflueger robust F..."
- 5-layer SE 의 학술 근거

### Section 4 (Main Results)
- Table 2 의 column (5) AR + tF
- "Robust to weak instruments"

### Section 6 (Robustness)
- ADH 8국 IV (F<2) 와 KR-CN IV (F~12) 비교
- weak vs strong IV 케이스 구분

### Appendix
- Pre-test bias 회피 protocol
- Olea-Pflueger F 의 정의

---

## 8. AKM + AR + tF — 통합

본 연구의 **5-layer SE** 가 covering 하는 것:

| Layer | 무엇을 잡는가 |
|-------|-------------|
| 1. HC1 | heteroskedasticity |
| 2. Cluster-sido | within-sido correlation |
| 3. AKM | cross-region correlation through industry shares |
| 4. Conley | spatial autocorrelation |
| 5. AR + tF | weak instrument + finite-sample bias |

→ **5층 모두 통과** = main result 의 강력한 robustness. 박사논문급.

---

## 9. 다음 단계 메모

1. **Phase 3 시 first-stage F 보고** — Olea-Pflueger robust F (Stock-Yogo 의 heteroskedastic 일반화)
2. **AR test 구현** — Python `linearmodels.IV2SLS.firststage.diagnostics`
3. **tF correction** — Lee et al. (2022) 의 보정 방법, R 또는 직접 구현
4. **Pre-test 회피** — IV 선택은 pre-analysis plan 으로 사전 결정
5. paper 에 Andrews-Stock-Sun 2019 인용 + 그들의 AER survey 결과 활용

---

## 10. 본 연구의 narrative — Weak IV 정직성

**v3.x 의 한계 명시:**

> "Earlier versions of this analysis using ADH-style instruments based on imports from 8 high-income countries (Pierce-Schott 2020 framework adapted to Korea) yielded weak first-stage F-statistics (Olea-Pflueger F < 2). Following Andrews, Stock, Sun (2019) recommendations, we replace this with the Korea-China bilateral net export instrument, which yields a stronger first stage (F~12) and is more theoretically appropriate for Korea's export-driven trade structure."

→ **방어적이지만 학자적 정직성**. v3.x 의 weakness 를 인정하고 v4.0 의 개선 명시. Paper 의 신뢰도 ↑.

---

## 11. 본 연구의 v3 → v4 정리

| 항목 | v3.x | v4.0 |
|------|------|------|
| Main IV | ADH 8국 (F<2, weak) | KR-CN bilateral (F~12, strong) |
| Robust F 보고 | 미보고 | Olea-Pflueger 보고 |
| AR test | 미사용 | 정식 layer 5 |
| tF correction | 미사용 | 정식 layer 5 |
| Inference robustness | weak | strong |
| Paper quality | 박사 논문 marginal | 박사 논문 강력 |

→ Andrews-Stock-Sun 2019 의 권장사항 모두 적용. **paper 의 referee 통과 가능성 ↑**.
