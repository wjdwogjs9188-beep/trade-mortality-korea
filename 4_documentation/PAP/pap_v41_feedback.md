# PAP v4.1 Expanded 종합 피드백

## Trade Exposure and Mortality in Export-Oriented Korea (정재헌 v4.1)

**작성 목적:** 본 PAP에 대한 학술적 피드백을 하나의 문서로 정리한다. 이 문서는 학습 차원에서 작성되며, 본인이 mechanism focus paper로 전환한 이후에도 broad PAP의 약점을 어떻게 식별하고 보완할 수 있는지의 reference로 사용한다.

**검토 시점:** 2026-05-02
**검토 대상:** PAP v4.1 expanded (1312 lines, v4.0의 § 5 상세화 + Appendix D, E 추가 버전)

---

## 0. 전체 평가

먼저 본 PAP의 학술적 quality부터 짚을게요. 본 PAP는 학부생 수준을 한참 넘는 진지한 학술 문서다. Pierce-Schott 2020을 한국에 응용하는 broad한 paper의 PAP로서 다음과 같은 강점을 가진다.

식별 전략의 명시성이 매우 강하다. Bartik IV의 share exogeneity 가정을 명시적으로 채택하고, 6개 식별 진단(First-stage F, Rotemberg HHI, share-covariate balance, pre-trend event-study, AKM random shifters placebo, share permutation)을 사전에 명시했다. 학부생이 이만큼 식별 진단을 깐 PAP는 거의 없다.

표준오차 처리의 다층성이 인상적이다. HC1, cluster-sido, AKM, Conley, AR+tF의 5-layer SE를 모두 사전에 약속했다. Over-rejection 문제에 대한 정직한 자세를 보여준다.

3 시나리오 (A 가설 통과, B null, C 가설 reject) 모두에 대한 해석을 사전에 작성한 falsifiability 자세가 학술적으로 진지하다.

코드 sketch와 Appendix B (AKM SE), Appendix D (Rotemberg implementation), Appendix E (figure 사양)까지 포함된 detail은 박사 1-2년차 working paper 수준의 기술적 깊이를 보여준다.

이러한 강점에도 불구하고 본 PAP에는 본 paper가 SSCI 중상위 단독 저자 publishable 수준이 되기 위해 보완해야 할 7개 핵심 이슈가 있다. 이슈들을 큰 것부터 순서대로 정리한다.

---

## 1. 가장 큰 이슈 — H1의 이론적 기반과 net export 변수의 한계

### 1.1 문제 정의

본 PAP의 핵심 가설 H1이 "대중국 net export 증가 → despair 사망률 감소"라고 단방향 protective effect를 예측한다. 학술 근거로 Dauth 2014 (독일 export → 고용 ↑)를 들었는데, Dauth는 사망률 paper가 아니다. 고용 효과를 사망률 효과로 직접 외삽하는 것은 비약이다.

더 큰 문제는 한국이 단순히 "수출 받는 쪽"이 아니라는 사실이다. 같은 산업 안에서도 어떤 시군구는 수출 효과를 보고(반도체 제조 공장 있는 곳), 어떤 시군구는 중국 저가품 수입에 노출된다(저부가가치 의류·신발·가구 제조). Net export로 묶으면 이 두 효과가 시군구별로 다르게 작동하면서 평균 효과가 영에 가깝게 나올 가능성이 매우 크다.

구체적인 mechanism을 짚으면 이렇다. 수원시는 반도체 비중이 높고 net export가 양수다. 수원의 보호 효과가 산출된다. 반면 대구 일부 시군구는 의류 비중이 높고 net export가 음수다. 대구의 파괴 효과가 산출된다. 회귀가 양 효과의 가중평균을 추정한다. 한국 전체에서 두 효과가 평균내지면 작은 음수, 0, 작은 양수 어느 쪽으로든 나올 수 있다.

### 1.2 위험성

이 문제가 paper의 main thesis 자체를 위협한다. § 9.2 시나리오 B(β ≈ 0)가 가장 가능성 높은 결과인데, 이때 paper의 contribution이 약해진다. "Korea's export-led structure may offset" 라는 추상적 해석으로는 Pierce-Schott 한국 응용 paper로서의 가치가 부족하다.

또한 시나리오 B 해석이 잘못된 결론으로 이어진다. 사실은 두 효과(수출 보호 + 수입 파괴)가 다 있는데 평균하면 0인 거지, 효과가 없는 게 아니다. Net export 변수로는 이 두 효과를 분리해서 검출할 수 없다.

### 1.3 권고

H1을 두 개로 쪼갠다. H1a는 "수출 충격이 큰 시군구에서 절망사 사망률이 감소한다 (β_export < 0)". H1b는 "수입 충격이 큰 시군구에서 절망사 사망률이 증가한다 (β_import > 0)". 두 가설이 함께 검증되어야 한국에서 무역의 사망률 효과를 정확히 이해한다.

회귀 spec도 수정한다. Bartik IV를 export shock과 import shock 두 개의 endogenous variable로 분리한다. Export Bartik은 1997 산업 비중과 산업별 한국 수출 증가율의 곱이다. Import Bartik은 1997 산업 비중과 산업별 한국 수입 증가율의 곱이다. 각각을 별도의 instrument로 처리하는 다중 endogenous variable 2SLS가 된다.

이는 본인이 PAP § 12에서 인용한 Dauth, Findeisen, Suedekum 2014가 정확히 한 일이다. Dauth는 독일이 중국·동유럽에서 받은 import shock과 동시에 동유럽으로 보낸 export 효과를 분리했고, 두 효과가 부호 반대였다. 이게 그 paper의 핵심 발견이다. 본 PAP가 Dauth를 인용하면서 정작 net export로 가는 것이 모순이다.

추가로 두 변수의 collinearity 진단이 필요하다. Export Bartik과 import Bartik이 시군구별로 강하게 상관될 가능성이 있다. PAP에 condition number를 보고하고 5-10 이하 확인하는 진단을 추가한다. 너무 강하게 상관되면 separate regression으로 fallback 한다는 것을 미리 명시한다.

---

## 2. 두 번째 이슈 — KR-CN bilateral IV의 식별 위협

### 2.1 문제 정의

본 PAP § 4.2에서 v3 → v4 변경의 정당화로 KR-CN bilateral IV의 first-stage F가 12-16으로 개선된다는 점을 든다. 다만 이는 도구변수가 강해진 것이지 더 valid해진 것이 아니다.

ADH 8국 IV의 핵심은 "한국 시군구 노동시장과 무관한 충격"을 잡는 것이다. 다른 선진국들이 중국한테서 받는 충격은 한국 노동공급과 분리되어 있다. 이게 IV의 외생성을 보장한다.

KR-CN bilateral로 바꾸면 한국이 수입하는 양 자체가 한국 노동시장 상태에 영향을 받는다. 한국 노동시장이 약해지면 임금이 하락하고 한국 기업이 수입을 줄인다. 또는 한국 경기가 좋아지면 수입이 늘어난다. 이게 정확히 Goldsmith-Pinkham이 경고한 share·shock 동시 내생성이다.

### 2.2 위험성

PAP가 share exogeneity path (GP 2018)를 채택한다고 명시했지만, KR-CN bilateral shifter 자체가 한국 macro 환경과 동시 결정되면 share exogeneity 가정만으로 식별이 보장되지 않는다. Reviewer가 이 점을 지적할 가능성이 높다.

"First-stage F가 강한 IV가 좋은 IV"라는 일반화는 틀렸다. F가 100인데 endogenous한 IV보다 F가 8인데 valid한 IV가 낫다. 약한 IV 문제는 inference 방법으로 처리할 수 있지만 endogenous IV는 처리 방법이 없다.

### 2.3 권고

ADH 8국 IV를 main으로 유지한다. 약한 first-stage F 문제는 robust inference 방법으로 처리한다. 구체적으로 Anderson-Rubin test와 Lee et al. 2022 의 tF inference를 main inference로 쓴다.

본 PAP § 6.5의 layer 5가 이미 AR + tF를 포함한다. 이를 "robustness layer"가 아니라 "main inference layer"로 격상한다. 5-layer 표 (§ 6.6)에서 column (5) AR + tF가 main result가 되고 column (1)-(4)는 robustness 비교가 된다.

KR-CN bilateral IV를 robustness로 처리하되, 명시적으로 외생성의 한계를 paper Section 4에 인정한다. "KR-CN bilateral은 한국 mechanism에 적합하지만 endogeneity 우려가 있고, ADH 8국 IV는 외생성이 강하지만 weak F다. 본 paper는 ADH 8국을 main으로 사용하고 KR-CN을 robustness로 보고한다."

이러한 framing이 reviewer에게 더 honest하고 학술적으로 안전하다.

---

## 3. 세 번째 이슈 — 시군구 sparse cell 문제

### 3.1 문제 정의

이 이슈는 이전 conversation에서 6개 외 7번째로 추가된 것인데, 사실상 paper의 정체성을 결정할 만큼 큰 문제다. Sparse cell 문제가 무엇인지부터 짚는다.

한국 256개 시군구 중에 인구 5만 명 이하인 군이 꽤 많다. 영양군, 봉화군, 청송군, 울릉군 같은 곳이다. 이런 곳에서 절망사 같은 특정 사인의 연간 사망자가 0명, 1명, 2명 수준이다. 

작은 군에서 어느 해 자살이 0명이었다가 다음 해 2명이 되면 사망률이 0에서 갑자기 30/10만으로 점프한다. 이건 진짜 변동이 아니라 small-number noise다. 본 PAP § 2.3.2의 +1 smoothing이 이를 부분적으로 처리하지만 완전하지 않다.

5-year stacked로 가도 이 문제가 사라지지 않는다. 5년 stacking은 시간 noise를 줄이지만 단면 noise는 그대로다. Bartik IV가 일부 작은 군 (특정 산업 비중 높은 곳)에 의존하면 Rotemberg weight가 작은 군에 몰릴 수 있다.

미국 county vs 한국 시군구의 인구 분포 차이가 결정적이다. 미국 county는 평균 인구 10만+이고 가장 작은 county도 1만+이다. 한국 시군구는 평균 인구는 비슷하지만 최소값이 1만 이하로 떨어진다. Pierce-Schott의 spec이 한국에서 그대로 작동한다고 가정할 수 없다.

### 3.2 위험성

이 sparse cell 문제는 reviewer가 가장 쉽게 잡는 약점이다. "Small cell noise"라는 한 줄짜리 reviewer comment 하나로 reject 당할 수 있다. 본 PAP의 robustness 한 줄("+0.5, +0 (drop), Poisson regression도 보고")로는 부족하다.

또한 sparse cell이 식별 진단 결과에 영향을 줄 수 있다. Rotemberg HHI가 낮게 나오더라도 0 cell이 많은 시군구가 산업별 just-identified β_j 계산에 noise를 만들면 § 5.1.5의 Test B (β_j 분포)가 흔들린다.

### 3.3 권고

세 가지 보완을 추천한다. 첫째, Sample restriction을 main spec의 옵션으로 추가한다. 1990년 인구 5만 이상 시군구로 한정하면 256개 중 약 70-80개가 빠져서 약 180개 시군구로 분석한다. 추정 안정성이 크게 올라간다. 본 PAP § 7.5에 이미 "인구 50k 미만 vs 이상" subsample 분석이 들어있는데, 이를 robustness가 아니라 main spec 후보로 격상한다.

둘째, Poisson regression을 robustness가 아니라 main으로 격상한다. Outcome을 count로 두고 Poisson 또는 negative binomial regression을 쓰는 것이 작은 cell 문제에 더 robust하다. ln(rate + 1)보다 이게 작은 cell에 대한 표준 처리다. 의료 통계 분야에서는 Poisson이 표준이다.

셋째, 시군구 대신 권역 단위로 aggregate하는 spec을 robustness로 추가한다. 광역시·도 단위 (16개)는 너무 적고, 기능적 노동시장권 (Functional Labor Market Area) 단위가 적당하다. 한국 통계청이 정한 노동시장권이 있다. 이러면 50-70개 정도라 cell 안정성이 올라간다.

PAP에 sparse cell 문제를 4번째 식별 위협으로 명시하고 § 5에 검정 6 (small county sensitivity)를 추가한다. 미국 county vs 한국 시군구 인구 분포 비교 표 하나만 넣어도 reviewer가 이 이슈를 신경 쓴다는 걸 알아준다.

---

## 4. 네 번째 이슈 — Pre-period 데이터 한계

### 4.1 문제 정의

본 PAP § 5.3 검정 3 (pre-trend event-study)에서 1990-1996 pre-period (k = -7 to -1)를 사용한다. 그런데 PAP § 2.2에서 KOSTAT 사망 microdata가 1997년부터라고 명시했다. Pre-period 데이터가 아예 없다.

§ 5.3.3의 pre-period 결과 표 (1990-1996 β_k 값)는 데이터가 없는 상태에서 가상으로 작성된 placeholder다. 실제로는 1990-1996년 시군구 단위 사망률 변화 (Δ mortality 1990-1996)를 산출할 수 없다.

마찬가지로 § 5.2.2의 share-covariate balance 표 Panel B (Δ ln(GRDP) 1990-1996, Δ population 1990-1996, Δ mortality 1990-1996, Δ despair mortality 90-96)도 사망률 관련 trend는 측정 불가능하다.

### 4.2 위험성

PAP에 가상 데이터로 만든 표가 있는 것은 reviewer 신뢰도에 큰 타격이다. PAP는 "회귀 실시 전에 사전 명시"이지 가상 결과를 보고하는 문서가 아니다. 만약 본 PAP가 실제 paper에 그대로 인용되면 reviewer가 "어떻게 1997년 이전 사망률 데이터를 얻었나"라고 의심한다.

또한 pre-trend 검정이 paper의 핵심 식별 진단인데, 데이터가 없으면 검정이 진정으로 수행되지 않는다. 본 PAP가 사망률 데이터 가용 시작점인 1997년 자체를 baseline으로 삼고 있어서, post-period만 있고 pre-period가 없다는 근본적 데이터 한계를 가진다.

Pierce-Schott 2020이 미국에서 1990-2000 pre-period를 사용했던 것은 미국 county 사망 데이터가 1990년 이전부터 가용했기 때문이다. 한국의 데이터 가용성과 다르다.

### 4.3 권고

세 가지 수정이 필요하다. 첫째, § 5.2.2의 share-covariate balance Panel B에서 사망률 관련 변수 (Δ mortality, Δ despair)를 빼거나, KOSIS의 시도 단위 사망률 데이터로 대체한다. 시도 단위는 1995년부터 가용하므로 시도 단위 pre-trend는 측정 가능하다. 다만 시군구 단위 검정의 powerful함이 떨어진다.

둘째, § 5.3 검정 3의 pre-period를 "재정의"한다. 1997-2001 (5년)을 truncated pre-period로 활용한다. 2001년 12월 중국 WTO 가입을 main treatment shock으로 두고, 1997-2001을 pre-period로 본다. 이러면 pre-period가 5년이라 짧지만 측정 가능하다. 다만 1997 IMF 외환위기 영향이 pre-period에 들어가서 추가 noise가 생긴다.

셋째, 데이터 한계를 paper의 limitation으로 명시한다. "한국 사망 microdata가 1997년부터 가용해 pre-period가 4년으로 제한된다. Pierce-Schott의 미국 분석은 더 긴 pre-period를 활용했지만 본 paper는 데이터 한계로 인해 pre-trend 검정의 power가 약하다."

§ 5.3.3의 가상 데이터 표는 PAP에서 빼거나 명시적으로 "실제 분석 후 채워진다 (placeholder)"라고 표시한다.

---

## 5. 다섯 번째 이슈 — Multiple testing 보정의 약함

### 5.1 문제 정의

본 PAP § 10.3에서 multiple testing 보정을 정리했다. Main 5개 outcome에 Bonferroni p<0.01, Robustness 8개에 보정 X (보고만), Hetero 6개에 FDR (Benjamini-Hochberg)을 적용한다. 합계 약 240개 회귀.

이 보정이 약한 이유 두 가지가 있다.

첫째, Main outcome 5개와 Hetero의 demographic 6 cell이 사실상 같은 검정 공간이다. § 8.1의 Hetero 표를 보면 ln(despair mortality) outcome을 demographic 6 cell로 나눈 것이다. 즉 main outcome (despair total)이 cell별로 다시 검정된다. 이를 분리해서 main 5개에 Bonferroni, hetero 6개에 FDR을 따로 적용하는 것은 통계적으로 일관되지 않다.

둘째, FDR만으로는 검정 사이의 상관 구조를 적절히 처리하지 못한다. 심혈관계 사망률과 호흡기 사망률은 같은 사람들이 죽는 경우가 많아서 강하게 상관된다. 한 outcome이 유의하면 다른 outcome도 유의할 가능성이 높다. FDR이 over-reject할 수 있다.

### 5.2 위험성

검정 240개에서 5%가 우연히 유의하다고 나오면 12개 정도가 false positive다. 보고된 결과 중 어느 것이 진짜이고 어느 것이 우연인지 reviewer가 의심한다. 특히 hetero 분석의 demographic cell별 결과가 cherry pick된 것 아닌지 의심받기 쉽다.

또한 PAP의 multiple testing 보정 약함은 PAP commit 자체의 가치를 약화시킨다. PAP의 핵심 가치가 사전 약속과 false positive 통제인데, 보정이 약하면 사전 약속만 했지 통계적 보호는 부족한 셈이다.

### 5.3 권고

본 PAP § 10.3을 다음과 같이 다시 쓴다.

"본 연구는 confirmatory와 exploratory를 엄격히 분리한다. Confirmatory는 § 1.3의 사전 가설 H1-H5에 해당하는 5개 검정으로, 각각 p<0.05를 main으로 하고 5개 가족 Bonferroni 보정 p<0.01을 보충 보고한다. Exploratory는 § 8의 모든 heterogeneity 분석으로, Romano-Wolf step-down (1000 bootstrap iterations) 보정을 적용한다. Hetero 분석은 별도 table로 분리 보고하고 main contribution과 명시적으로 구분한다."

Romano-Wolf step-down은 검정 사이의 상관 구조를 직접 사용해서 보정한다. Bootstrap을 1000번 정도 돌려서 만약 모든 효과가 0이라면 가장 큰 t-stat이 어느 정도 나올지의 분포를 만들고, 그 분포 기준으로 검정한다. 상관 강한 검정들은 같이 움직이니까 효과적으로 독립 검정 수가 줄어들어서 보정이 덜 강해진다. 동시에 상관 구조를 데이터에서 직접 측정하니까 가정이 덜 들어간다. 노동경제학·교육경제학 paper에서 표준이 되고 있다.

특히 H4 (남성 > 여성) 같은 사전 가설은 confirmatory로 처리한다. 이건 사전 명시라 fishing이 아니다. 그 외 § 8의 demographic cell별 분석은 exploratory로 처리해서 Romano-Wolf로 보정한다.

---

## 6. 여섯 번째 이슈 — Spillover spec 정의 부족

### 6.1 문제 정의

본 PAP § 7.3에서 β_m vs β_n decomposition (Finkelstein-Notowidigdo-Shi 2026)을 robustness로 명시했다. β_m은 own-county effect (자기 시군구 무역 충격이 자기 사망률에), β_n은 spillover (인접 시군구 무역 충격이 자기 사망률에)다. Spatial weight matrix W로 인접 시군구를 가중평균한다.

PAP에 "rook contiguity + 50km 이내"라고 적혀있지만 이게 부족하다. 세 가지 디테일이 빠졌다.

첫째, Row-normalize 여부가 안 적혀있다. Spatial weight matrix W는 row 합이 1이 되도록 normalize하는 것이 표준이다. 안 그러면 시군구마다 인접 수가 다르니까 (서울 강남구는 옆이 6개, 영양군은 옆이 2개) 추정이 왜곡된다. 6개에 둘러싸인 시군구는 spillover 영향을 6배 받게 잡힌다. Row-normalize를 하면 가중치 합이 1이라 비교 가능해진다.

둘째, 자기 자신 포함 여부가 안 적혀있다. β_n을 추정할 때 가중평균에 자기 시군구를 포함하는 것이 아니라 빼는 것이 맞다. 자기 시군구는 이미 β_m으로 잡고 있으니까. 명시 안 되어 있다.

셋째, Distance decay 함수가 빠졌다. "50km 이내"를 어떻게 처리할지다. 0/1 dummy인지, 거리 역수인지, exp(-distance)인지에 따라 추정 결과가 크게 달라진다. 특히 한국처럼 시군구 면적 차이가 큰 나라에서는 어떤 함수를 쓰냐가 중요하다. 강원도 인제군에서 50km 안에 시군구 3개, 서울 강남구에서 50km 안에 시군구 30개다.

### 6.2 위험성

Spillover spec이 정확히 정의되지 않으면 사후에 결과 보고 조정한다고 의심받을 수 있다. PAP의 핵심 가치가 사전 약속인데 spec이 모호하면 약속이 약해진다.

또한 β_m과 β_n collinearity 문제가 진단되지 않았다. 충격이 시군구마다 충분히 다양해야 두 계수를 분리해서 추정할 수 있다. 모든 인접 시군구가 같은 충격을 받으면 자기 충격과 spillover 충격이 collinear해서 분리가 안 된다. 이게 가능한지 미리 진단해야 한다.

### 6.3 권고

본 PAP § 7.3을 다음과 같이 다시 쓴다.

"Spatial weight matrix W는 다음과 같이 정의한다. (1) Base specification: rook contiguity (인접 시군구만 1, 나머지 0), 자기 자신 제외, row-normalize. (2) Robustness 1: 50km cutoff with inverse distance decay $w_{ij} = 1/d_{ij}$ if $d_{ij} < 50km$ else 0, row-normalize. (3) Robustness 2: exponential decay $w_{ij} = \exp(-d_{ij}/30km)$, row-normalize. 모든 W에서 자기 자신 제외. 식별을 위해 β_m과 β_n collinearity 진단으로 condition number를 보고하고 10 이하 확인."

추가로 β_n의 부호 가설을 미리 명시한다. 직관적으로는 β_m과 β_n이 같은 부호일 것이다. 옆 시군구가 충격받으면 우리 시군구도 비슷하게 영향받으니까. 다만 반대 부호도 가능하다. 옆 시군구에서 일자리 잃은 사람이 우리 시군구로 이주하면 우리 시군구 노동공급이 늘어서 임금이 떨어지고 절망사가 더 늘 수 있다. 이런 가능성을 PAP에 사전 명시한다.

---

## 7. 일곱 번째 이슈 — 시나리오 B 발생 시 contribution 약함

### 7.1 문제 정의

본 PAP § 9.2에서 3 시나리오를 사전 작성했다. 시나리오 A (β < 0 유의), B (β ≈ 0), C (β > 0)다.

Section 1에서 짚은 net export 변수의 한계 때문에 가장 가능성 높은 결과가 시나리오 B다. 이때 paper 해석은 "Korea's export-led structure may offset the negative effects observed elsewhere - but does not produce the protective effect hypothesized."

이 해석이 너무 추상적이다. "may offset"이라는 가정형은 검증되지 않은 추측이다. PAP의 핵심 가치는 사전 약속인데, 시나리오 B에서 paper가 실제로 무엇을 기여하는지 명시되지 않았다.

### 7.2 위험성

시나리오 B가 가장 가능성 높은데 그 시나리오에서 paper의 contribution이 약하다는 것은 paper 자체의 risk가 크다는 의미다. SSCI submission 시 reviewer가 "이 paper가 무엇을 보여주나"라고 물으면 답이 "효과가 없거나 상쇄된다"인데, 이건 강한 contribution이 아니다.

또한 시나리오 B에서 추가 분석을 시도하면 사후 추가 분석 (post hoc)이 되어 PAP commit을 위반한다.

### 7.3 권고

§ 9.2 시나리오 B 해석을 다음과 같이 다시 쓴다.

"시나리오 B (β ≈ 0)가 나오면, net effect가 0인 것 자체가 발견이다. 이는 한국이 수출과 수입 양방향 효과를 모두 받고 있고, 한쪽이 다른 쪽을 상쇄하고 있다는 가설을 지지한다. 이를 검증하기 위해 export shock과 import shock을 분리한 추가 분석을 수행한다. (1) Export Bartik과 Import Bartik을 분리한 다중 IV 회귀. (2) 두 효과의 부호와 magnitude 비교. (3) 시군구별 export-import dichotomy의 heterogeneity. 만약 분리 분석에서 두 효과가 부호 반대로 유의하게 나오면 한국 무역의 양방향성이 paper의 main contribution이 된다."

이렇게 하면 시나리오 B를 맞이하면 자동으로 분리 분석으로 넘어간다는 약속을 미리 적어두는 것이다. 사후 추가 분석이 아니라 사전 명시된 분석이 된다. 이는 사실상 Issue 1의 권고 (H1을 양방향으로 쪼갤 것)와 일관된다. 양방향 분리를 main에 두면 시나리오 B 자체가 사라지고, 양방향 분리를 시나리오 B의 backup으로 두면 PAP의 falsifiability 보강이 된다.

---

## 8. v4.1 확장 부분에서 발견된 추가 이슈

v4.0에서 v4.1로 확장된 부분 (§ 5 6검정 상세화, Appendix D, E)을 검토하면서 추가로 발견된 작은 이슈 두 가지가 있다.

### 8.1 § 5.1의 Rotemberg 권고 미적용

§ 5.1.4에서 v4.0 KR-CN bilateral의 expected Rotemberg weight 분포를 제시했다. HHI 0.13으로 v3.x의 0.91 대비 크게 개선됐다. 그런데 이는 expected (predicted) 분포이지 실제 데이터에서 측정한 것이 아니다. 가상 weight 분포를 PAP에 넣는 것은 placeholder로 명시해야 한다. § 5.1.4에 "expected"라고 적혀있긴 하지만 표 자체가 실제 결과처럼 보이는 형태다.

권고는 § 5.1.4의 표를 "Phase 3 분석 후 채워질 예시 표 (placeholder)"라고 명시적으로 표시한다. 또는 표를 빼고 expected HHI 범위만 텍스트로 적는다.

### 8.2 Appendix D의 코드 sketch와 실제 panel 구조의 mismatch

Appendix D의 Rotemberg implementation 코드가 실제 panel 구조와 일관되지 않은 부분이 있다.

`shares_matrix`가 (N regions × J industries)이고 `shifts_matrix`가 (J industries × T years)인데, `x_endog`와 `x_fitted`가 (N×T,) flattened array다. 코드 안에서 `np.outer(shares_matrix[:, j], shifts_matrix[j, :]).flatten()`로 z_j를 만드는 방식이 5-year stacked panel에서는 맞지 않는다. 5-year stacked는 N × P (P=5 periods)이지 N × T (T=27 years)가 아니다.

권고는 Appendix D 코드를 5-year stacked panel 구조에 맞게 수정한다. 또는 annual panel 분석에서만 코드가 작동한다고 명시한다.

또 한 가지, `compute_rotemberg` 함수에서 `x_endog`와 `x_fitted`를 둘 다 받지만 실제 Rotemberg weight 계산에는 `x_fitted`만 사용한다. `x_endog`는 함수 안에서 쓰이지 않고 있다. 코드 정리가 필요하다.

### 8.3 Appendix E의 Pre-trend Figure와 데이터 한계의 불일치

Appendix E의 Figure 사양에서 "X-axis: event time k (-7 to +25, relative to 1997)"이라고 명시했다. 그런데 Issue 4에서 짚었듯 1990-1996 (k = -7 to -1) 데이터가 없다.

권고는 Appendix E의 figure 사양을 1997-2001을 truncated pre-period로 사용하는 spec에 맞춰 수정한다. 또는 시도 단위 pre-period를 사용하는 별도의 figure 사양을 만든다.

---

## 9. 종합 정리

본 PAP는 학부생 수준을 한참 넘는 진지한 학술 문서이며 박사 1-2년차 working paper에 준하는 식별 전략과 식별 진단을 갖추었다. 다만 위에서 짚은 7개 이슈를 보완하지 않으면 SSCI 중상위 단독 저자 publishable 수준에 도달하기 어렵다.

7개 이슈를 우선순위별로 다시 요약한다.

가장 큰 이슈 두 개는 paper의 정체성을 결정하는 문제다. Issue 1 (H1 양방향 분리)과 Issue 3 (sparse cell)이 이에 해당한다. 이 두 이슈가 해결되어야 paper의 main thesis와 분석 단위가 안정된다.

중간 위험 이슈 두 개는 식별 신뢰성을 결정한다. Issue 2 (KR-CN bilateral의 외생성 위협)와 Issue 4 (pre-period 데이터 한계)가 이에 해당한다. 이 두 이슈가 해결되어야 reviewer가 식별 전략을 신뢰한다.

작은 위험 이슈 세 개는 통계 처리와 spec 디테일이다. Issue 5 (multiple testing 보정), Issue 6 (spillover spec), Issue 7 (시나리오 B contribution)이 이에 해당한다. 이 이슈들은 paper가 통과하기 위해 보완되어야 하지만 main thesis 자체에는 영향이 작다.

추가 발견 이슈 (§ 8) 세 가지는 PAP 작성의 detail 수준 문제다. § 5.1.4의 가상 weight 표 placeholder 명시, Appendix D 코드의 panel 구조 mismatch, Appendix E figure 사양의 데이터 한계 반영이 필요하다.

---

## 10. 본 PAP를 어떻게 활용할 것인가

본인이 mechanism focus paper로 전환했으므로 broad PAP는 별도 paper로 추진하지 않는다. 다만 본 PAP의 식별 전략과 식별 진단 framework은 mechanism focus paper에 그대로 활용할 수 있다.

Mechanism focus paper의 구조를 본 PAP의 기여로 정리하면 이렇다. § 4 (식별 전략)와 § 5 (식별 진단)은 mechanism focus paper에서도 그대로 사용할 수 있다. Bartik IV의 share exogeneity, Rotemberg HHI, share-covariate balance, pre-trend, AKM placebo, share permutation 이 6개 진단은 어느 paper든 적용 가능하다. § 6 (5-layer SE)도 동일하게 적용 가능하다.

다만 § 1 (가설), § 3 (main spec), § 7-8 (robustness, hetero), § 9 (시나리오 해석)은 mechanism focus에 맞춰 다시 써야 한다. 가족 구조 매개 분석이 main이 되고, 무역 충격의 사망률 직접 효과는 reduced form section에서 다룬다.

본 PAP에서 짚은 Issue 1 (H1 양방향 분리)은 mechanism focus paper에서도 부분적으로 의미가 있다. 무역 충격이 가족 구조에 미치는 효과 자체가 export shock과 import shock에 따라 다를 수 있다. 다만 mechanism focus paper의 main thesis가 "가족 구조 매개"이므로 양방향 분리는 robustness 정도로 처리한다.

Issue 3 (sparse cell)과 Issue 4 (pre-period 데이터 한계)는 mechanism focus paper에서도 그대로 적용된다. Sample restriction과 Poisson regression을 main에 포함하고, pre-period를 1997-2001 truncated로 처리하는 것은 어느 paper든 필요하다.

Issue 5 (multiple testing 보정)와 Issue 6 (spillover spec)도 동일하게 mechanism focus paper의 기여 framework에 들어간다.

Issue 2 (KR-CN bilateral vs ADH 8국)는 mechanism focus paper에서도 결정해야 한다. 어느 IV가 main이 될지 본 PAP의 권고 (ADH 8국 main)를 따른다.

Issue 7 (시나리오 B contribution)은 mechanism focus paper에서는 다른 형태로 등장한다. Mechanism focus의 "가족 구조 채널 portion이 작게 나오는 시나리오"가 시나리오 B에 해당한다. 이때도 사전에 contribution을 명시해야 한다.

이처럼 본 PAP의 framework은 broad paper로서는 보완이 많이 필요하지만 mechanism focus paper의 base로 재활용할 가치가 충분하다. 본 피드백 문서를 mechanism focus paper의 PAP 작성 시 reference로 사용하면 효율적이다.

---

**END OF PAP v4.1 EXPANDED FEEDBACK DOCUMENT**

본 피드백 문서는 학습 차원에서 작성되었으며 본인의 학술 글쓰기와 식별 전략 설계 능력 향상을 목적으로 한다. Mechanism focus paper 작업 중 식별 진단 단계에서 본 문서의 framework을 참조한다.
