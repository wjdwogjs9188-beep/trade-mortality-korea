# PAP v3.5 — IV Identification Protocol Addendum

**작성일**: 2026-05-04
**상태**: pre-commit (regression 실행 전 사전 등록)
**대체 대상**: PAP v3.4 § 4 (IV section), pap_v41_feedback.md § 2.3 권고 (확장)
**적용 위치**: stage5_regression_plan_v01.md § 4 (insertable patch는 아래 § 5)

---

## 0. 본 부록의 목적

`pap_v41_feedback.md` § 2 가 KR-CN bilateral IV 의 share·shock 동시 내생성 위험을 제기하고 § 2.3 에서 "ADH 8국 main 으로 유지, AR/tF inference 격상" 권고를 내렸다. 본 v3.5 는 이를 확장하여 (i) bilateral IV 의 외생성을 *empirically testable* 한 형태로 재정의하고 (ii) ADH-8 first-stage 강도에 대한 *사전 commit* decision tree 를 명문화한다.

이 addendum 의 핵심은 *결과를 본 뒤에 IV 를 갈아타지 않는다* 는 commitment 이다. 데이터를 본 뒤 main IV 를 결정하면 reviewer 가 cherry-pick 으로 의심한다 (Andrews-Stock-Sun 2019). 본 문서는 회귀 실행 전에 timestamp 된 protocol 을 남긴다.

---

## 1. Bilateral IV exclusion restriction — 이론적 변호

### 1.1 두 가지 외생성 명제 분리

Bartik IV 의 validity 는 두 명제 *중 하나* 를 통해 확보된다 (Goldsmith-Pinkham, Sorkin, Swift 2020):

- **(P1) Share exogeneity** — baseline 산업 share s_{c,k}(1997) 가 unobserved sigungu 특성과 직교
- **(P2) Shock exogeneity** — shifter g_k(t) 가 sigungu 단위 unobservable 과 직교 (Borusyak, Hull, Jaravel 2022 가 강조)

PAP v3.4 는 (P1) path 를 채택했지만, KR-CN bilateral 의 경우 share 와 shock 양쪽이 동시에 한국 거시환경의 함수가 될 가능성이 있어 (P1) 만으로 부족하다는 것이 v4.1 feedback 의 지적이다.

### 1.2 Bilateral IV 가 valid 할 수 있는 (제한적) 조건

KR-CN bilateral 충격 ΔM_t^{KR←CN} = (KR 수입 from CN at t) − (KR 수입 from CN at t−1) 은 다음과 같이 분해 가능:

```
ΔM_t^{KR←CN}  =  ΔS_t^{CN→world}      ←  중국 측 supply shift (외생 후보)
              +  ΔD_t^{KR}             ←  한국 측 demand shift (내생)
              +  Δτ_t^{KR-CN}          ←  양자 무역정책 변화 (혼합)
              +  잔차
```

본 paper 의 외생성 주장은 *오직 ΔS_t^{CN→world}* 를 분리해낼 수 있다는 가정에 의존한다. 이는 BHJ 2022 의 shock-level exogeneity narrative 와 동치이며, **empirically demonstrable** 하지 paper 에서 단순 주장으로 끝낼 사안이 아니다. § 2 가 이 demonstration 을 정의한다.

### 1.3 ADH-8 와의 비교

ADH-8 (`d_M_oct/L_init` where oct = 8 OECD countries) 은 ΔD_t^{KR} 항이 구조적으로 0 이다. 즉 (P2) shock exogeneity 가 baseline 으로 만족된다. 다만 first-stage 가 약할 수 있다 — Korean labor market 에 대한 8국 imports from China 의 직접 첫째-단계 영향력이 제한적이기 때문 (v4.1 PAP § 4.2 보고: bilateral F = 12-16, ADH-8 F 미보고).

본 protocol 은 두 IV 의 *trade-off* 를 명시적으로 받아들인다: ADH-8 = 외생성 ↑ / 강도 ↓. KR-CN bilateral = 강도 ↑ / 외생성 (validity) 검증 필요.

---

## 2. Bilateral validity — empirically testable orthogonality

### 2.1 Test 1 — Korean macro surprise residualization

bilateral 충격이 한국 거시 충격과 *예측 가능하게* 연동되면 ΔD_t^{KR} 가 0 이 아니라는 증거다. 다음 회귀:

```
ΔM_t^{KR←CN}  =  α  +  Σ_j β_j · KR_macro_surprise_{t−j}  +  γ·X_{t−j}  +  ε_t
```

- **종속변수**: 5-year stacked HS6 bilateral net trade exposure (industry × period level)
- **macro surprise**:
  1. GDP growth surprise = realized − BoK 분기 전망 (한국은행 ECOS)
  2. KRW/USD return shock = monthly residual from AR(1)
  3. KOSPI return surprise = realized − analyst consensus
  4. 수출가격지수 residual = realized − Hodrick-Prescott trend
  5. BoK base rate surprise = realized − OIS-implied expectation
- **lag**: j = 1, 2 (5-year stacked spec 에서 stack-내 한 period 이전)
- **귀무가설**: H0: β_j = 0 ∀ j, 모든 macro surprise 변수
- **검정**: 결합 Wald F-test, p > 0.10 → 외생성 신호. Anderson-Rubin 영역 보고 (Mertens-Ravn 2013 macro shock identification 관행).

### 2.2 Test 2 — Pre-2001 lead orthogonality

만약 bilateral shock 이 미래 한국 mortality 를 유발하는 *진짜 구조 충격* 이라면, **pre-WTO 시점 (1995–2000)** bilateral shock 은 post-WTO 한국 거시변수를 예측하지 *말아야* 한다 (single-direction causality).

```
KR_macro_t  =  α  +  Σ_j δ_j · ΔM_{t−5−j}^{KR←CN}  +  ε   for t ≥ 2002
```

- δ_j ≠ 0 → 거꾸로 한국 macro 가 bilateral shock 을 유발하는 채널 시사 → 외생성 의심.
- δ_j = 0 → bilateral shock 이 단방향 외생 변동을 담고 있다는 증거.

### 2.3 Test 3 — Sigungu pre-period mortality vs. baseline shares

share-side validity 의 사후 검정. Pierce-Schott (2020) 식 pre-trend test 를 share 자체에 적용:

```
Δmortality_{c, 1995-2000}  =  α  +  β · share_{c, 1997}^{exposed}  +  ε
```

- exposed share = manufacturing × bilateral 노출도 weighted average.
- β ≠ 0 → share 가 사망률 사전-trend 와 상관 → (P1) 위반.
- β = 0 → share 외생성 신호.

**참고**: 이는 stage5_regression_plan_v01.md § 4.5 (Pre-trend) 와 *동일한 spec* 이지만 본 protocol 에서 **bilateral validity 의 일부로 명시 등록** 한다.

### 2.4 Pass / Fail 기준 (사전 commit)

| 결과 | bilateral 처리 |
|------|---------------|
| 3개 테스트 모두 p > 0.10 | bilateral validity defensible — § 3 decision tree 에서 main candidate 자격 보유 |
| 어느 한 테스트 p < 0.05 | bilateral 은 robustness 만 — § 3 에서 ADH-8 만 main 후보 |
| 한 테스트 0.05 ≤ p ≤ 0.10 | borderline — 두 IV 모두 main 으로 보고, 결과의 공통 패턴만 해석 |

---

## 3. ADH-8 strength decision tree (사전 commit)

### 3.1 분기 기준

ADH-8 first-stage 의 OP 2013 effective F (`weakivtest`, τ = 0.10, single endogenous + single IV) 를 trigger 로 사용. Stock-Yogo 2005 의 5% TSLS bias threshold = 23.1.

### 3.2 세 갈래

**Branch A — F_ADH8 ≥ 23.1 (strong identification)**

- **Main IV**: ADH-8.
- **5-layer SE table** (stage5 § 6): column 1 = HC1, 2 = WCB-sigungu, 3 = WCB-sido, 4 = AKM, 5 = AR+tF (convergence check).
- **Bilateral KR-CN**: robustness only. Paper § 4 에 "alternative narrative IV; consistency check" 로 footnote.
- **Paper framing**: "results identified by 8-country exogenous variation in import competition from China."

**Branch B — 10 ≤ F_ADH8 < 23.1 (moderate weak IV)**

- **Main IV**: ADH-8.
- **5-layer SE table 재구성**: column 1 = AR + tF (main inference), columns 2–5 = HC1 / WCB-sigungu / WCB-sido / AKM (transparency, sub-asymptotic).
- **CI 보고**: Anderson-Rubin 95% CI 가 main, tF 는 Lee, Moreira, McCrary, Porter (2022) 조건 충족 시 보고 (sufficient F for tF validity).
- **Bilateral KR-CN**: robustness, narrative comparison.
- **Paper framing**: "results identified under ADH-8 with weak-IV-robust inference." Section 4 limitation 에 weak-IV 인정.

**Branch C — F_ADH8 < 10 (strongly weak IV)**

ADH-8 만으로 부족. § 2 bilateral validity 결과에 따라 두 sub-branch:

- **C.i — bilateral 3개 테스트 모두 통과**:
  - **Main IV**: KR-CN bilateral (F ≈ 12-16 가정 시 여전히 weak — Branch B-style inference 적용).
  - **Inference**: AR + tF main, HC1/WCB/AKM transparency.
  - **ADH-8**: robustness footnote — "ADH-8 cannot reject weak instrumentation; bilateral validity demonstrated by Appendix [Test 1-3]."
  - **Paper framing**: "primary identification via Korea-China bilateral exposure, validated against Korean macro surprise orthogonality (Appendix [...]). Inference uses weak-IV-robust methods."
- **C.ii — bilateral 어느 테스트라도 reject**:
  - **재포지셔닝 필수**. 두 옵션:
    - **(a) Reduced form only**: "Net export exposure correlates with mortality; we report reduced-form estimates and do not claim causal identification under conventional Bartik framework."
    - **(b) FNS spillover framing**: Finkelstein-Notowidigdo-Shi 2026 의 own/spillover 분해를 main result 로 격상 (β_m vs β_n decomposition); Korean structural context 강조; descriptive comparison primary.
  - **결정 자체는 § 2 결과 본 후 (a) vs (b) 중 선택** — 단, 둘 다 사전 등록된 옵션이라는 점이 중요.

### 3.3 Pre-commitment statement (paper § 4 에 들어갈 텍스트)

> "본 연구는 회귀 결과를 관찰하기 전 IV strength 와 validity 에 대한 protocol 을 사전 commit 하였다 (PAP v3.5, 2026-05-04). ADH-8 first-stage F 와 bilateral validity 검정 결과에 따라 main IV 와 inference 방식이 결정되며, 본 paper 에 보고된 main spec 은 [Branch X] 에 해당한다. 잔여 IV (robustness) 는 main 결정 *이후* 보고된다. 본 protocol 은 5_logs/decisions/ 에 timestamp 되어 있다."

---

## 4. 실행 순서 (사전 등록 보존)

1. **§ 2.1–2.3 orthogonality 테스트 실행** — 데이터: ECOS 거시 (이미 보유) + KR-CN bilateral (51 file 보유) + sigungu mortality pre-period (2A panel 보유). 즉시 실행 가능.
2. **§ 4.1 first-stage F 측정** (ADH-8 단독, bilateral 단독 각각). 데이터: 0_raw/comtrade_adh_china/ (201 file 보유) + 0_raw/comtrade_korea_china/ (51 file 보유). BACI 처리 *불필요* — Comtrade 만으로 충분.
3. 결과 → 다음 두 로그에 *2nd-stage 실행 전* 기록:
   - `5_logs/integrity_checks/<date>_iv_orthogonality.md` (Test 1-3 결과)
   - `5_logs/integrity_checks/<date>_first_stage_strength.md` (F-stat 결과)
4. branch 결정 → `5_logs/decisions/<date>_iv_branch_committed.md`. 결정 *이후* main 2SLS regression 진행.
5. 위 3개 로그가 git commit 되어야 main spec 결과가 honest pre-registration 자격 획득.

---

## 5. stage5_regression_plan_v01.md § 4 patch 텍스트

다음을 § 4.2 와 § 4.3 사이에 **§ 4.2a Identification branch decision** 로 신규 삽입:

```markdown
### 4.2a Identification branch decision (pre-committed)

PAP v3.5 § 3 의 protocol 에 따라 § 4.1 first-stage F 와 § 4.5 / PAP v3.5 § 2 의
orthogonality 결과를 받은 직후 다음 분기를 commit 한다:

* **Branch A** — F_ADH8 ≥ 23.1: ADH-8 main, 5-layer 표준.
* **Branch B** — 10 ≤ F_ADH8 < 23.1: ADH-8 main, AR + tF 가 column 1
  (main inference) 로 reorder.
* **Branch C.i** — F_ADH8 < 10 + bilateral validity 3-tests pass:
  bilateral main, AR + tF inference. ADH-8 robustness only.
* **Branch C.ii** — F_ADH8 < 10 + bilateral validity reject:
  paper 재포지셔닝 (reduced-form only OR FNS spillover framing).

본 분기는 main 2SLS 회귀 *실행 전* 결정되며, 결정은
`5_logs/decisions/<date>_iv_branch_committed.md` 에 기록한다.
post-hoc IV switching 은 금지된다.
```

또한 § 4.5 (Pre-trend) 의 마지막에 다음 한 줄 추가:

```markdown
* 본 pre-trend 결과는 PAP v3.5 § 2.3 (Test 3) 으로도 분류되어 bilateral
  share-side validity 검정의 일부로 등록된다.
```

---

## 6. Honest reporting (paper § 4 limitation)

분기와 무관하게 paper § 4 에 다음 단락 포함:

> "한국에서 ADH 식 IV 의 first-stage 강도는 미국 (Autor-Dorn-Hanson 2013) 이나
> 독일 (Dauth-Findeisen-Suedekum 2014) 보다 약할 가능성이 있다. 한국이
> import-competing 보다는 export-oriented 경제이고, 중국向 중간재 수출구조가
> 다른 OECD 국가의 import 패턴과 부분적으로만 공명하기 때문이다. 본 paper 는
> 이 한계를 인정하고, weak-IV-robust inference (Anderson-Rubin, tF) 를
> [main / 보조] 로 사용한다. KR-China bilateral exposure 는
> Korean structural context 에 더 적합한 IV 후보이지만, share·shock 동시 내생성
> 위험을 사전 검증 (Appendix [...]) 하였다."

---

## 7. References

본 protocol 이 의존하는 핵심 논문 (stage5_regression_plan § 15 의 부분집합):

- **Andrews, Stock, Sun (2019)** — Annual Review of Economics 11: 727-753 — pre-registration framing
- **Lee, Moreira, McCrary, Porter (2022)** — *Restud* — tF inference, weak-IV
- **Olea, Pflueger (2013)** — JBES 31(3): 358-369 — effective F
- **Stock, Yogo (2005)** — Cambridge UP chapter — F = 23.1 threshold
- **Goldsmith-Pinkham, Sorkin, Swift (2020)** — AER 110(8): 2586-2624 — share exogeneity path
- **Borusyak, Hull, Jaravel (2022)** — RES 89(1): 181-213 — shock exogeneity path
- **Borusyak, Hull, Jaravel (2025)** — JEP — practical guide
- **Mertens, Ravn (2013)** — AER 103(4): 1212-1247 — macro shock residualization
- **Pierce, Schott (2020)** — AERI 2(1): 47-64 — pre-trend test
- **Finkelstein, Notowidigdo, Shi (2026)** — BFI WP 2026-33 — own/spillover 재포지셔닝 옵션

---

## 8. 사용자 review 체크리스트

본 v3.5 가 PAP main body 와 stage5 plan 에 들어가기 전 확인:

- [ ] § 2.1 macro surprise 변수 5개 — 모두 ECOS 또는 KOSIS 에서 추출 가능한지 확인
- [ ] § 2.2 pre-WTO bilateral data — KR-CN 1995-2000 보유 여부 확인 (Comtrade 또는 KITA 대체)
- [ ] § 3.2 Branch C.ii 의 (a) vs (b) 사전 우선순위 — 본인 선호 명시 필요
- [ ] § 4.5 (stage5 § 4.5) 와 본 v3.5 § 2.3 의 통합 표기 일관성 확인
- [ ] PAP v3.4 § 4 와 본 v3.5 의 conflict 부분 (있다면) 명시적 supersede 표기

---

_End of PAP v3.5 IV protocol addendum. ~1,950 words._
