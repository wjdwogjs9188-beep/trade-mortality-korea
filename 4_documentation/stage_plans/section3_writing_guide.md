# Section 3 (Data) 작성 가이드

## 무역 충격, 가족 해체, 그리고 절망사: 한국의 숨은 메커니즘

**작성 목적:** Paper의 Section 3 (Data)을 어떻게 쓸지에 대한 상세 가이드. Reviewer가 paper의 데이터 출처와 변수 정의를 이해하기 위해 필요한 정보를 어떻게 본문에 정리할지 다룬다.

**Section 3 분량 목표:** 1500-2500단어 (paper 전체의 약 10-15%). SSCI 중상위 기준.

**중요:** 이 가이드는 paper 본문에 들어갈 내용이고, 본인이 작업할 때 사용하는 panel 구축 작업 문서와는 다르다. Section 3은 reviewer가 paper의 데이터를 이해하기 위한 정보만 담고, 작업 단계 디테일(폴더 구조, cleaning 코드, 시군구 crosswalk 작업)은 panel 구축 작업 문서에 따로 정리한다.

---

## 1. Section 3의 역할

학술 논문의 Section 3은 paper에서 사용하는 데이터의 출처, 변수 정의, 처리 방법을 명확히 정리하는 부분이다. Reviewer가 본 paper의 분석을 신뢰할 수 있는지를 데이터 quality와 처리 절차로 판단한다. 데이터 설명이 모호하거나 핵심 정보가 빠지면 paper의 식별 전략 자체가 흔들려 보인다.

본 paper의 Section 3은 다음 세 가지를 명확히 전달해야 한다. 첫째, 분석에 사용한 데이터의 출처가 무엇이고 어떤 단위로 정리했는가. 둘째, 핵심 변수(종속변수, 처치변수, 매개변수, 통제변수)의 정의가 정확히 무엇인가. 셋째, 데이터 처리 과정에서 발생한 결정 사항(시군구 crosswalk, 결측치 처리, 변수 변환)의 학술적 정당화는 무엇인가.

이 세 가지를 약 4-5개 subsection으로 구성한다. 각 subsection의 분량은 변수의 중요도에 따라 차등 배분한다.

---

## 2. Subsection 3.1 — 분석 단위와 panel 구조

### 2.1.1 이 subsection의 목적

이 subsection의 목적은 paper의 분석 단위(시군구 c × 연도 t)와 panel의 전체 구조를 reviewer에게 한눈에 보여주는 것이다. Section 3의 첫 부분이라 이후 변수 설명의 context를 제공한다.

### 2.1.2 다뤄야 할 핵심 정보

먼저 분석 단위를 명시한다. 본 paper는 시군구 c와 연도 t의 조합을 분석 단위로 한다. 시군구는 행정구역상 시(city), 군(county), 구(district)의 통칭이며, 한국의 표준 지역 분석 단위다. 미국 county와 비슷한 size이지만 인구 분포가 더 균등하지 않다. 가장 큰 시군구는 서울 강남구로 인구 50만 이상이고, 가장 작은 군은 인구 1만 이하의 군 단위다.

다음으로 baseline 시군구를 정의한다. 본 paper는 2021년 KOSTAT 행정구역 기준 256개 시군구를 baseline으로 한다. 분석 기간(1997-2023) 동안 행정구역 변경이 여러 번 있었으므로(예: 2010년 마산-창원 통합) 일관된 crosswalk으로 통합 처리한다.

분석 기간을 명시한다. 본 paper의 분석 기간은 1997년부터 2023년까지 27년이다. 1997년이 시작 연도인 이유는 KOSTAT 사망 microdata가 1997년부터 시군구 단위로 가용하기 때문이다. 2023년이 종료 연도인 이유는 본 paper 작성 시점에서 가용한 가장 최근 사망 데이터이기 때문이다.

Panel 구조를 명시한다. Full panel은 시군구 c × 연도 t × 성별 g × 5세 연령 a × 사인 d 의 5차원 panel이다. Aggregate level에서 시군구 c × 연도 t panel은 256 × 27 = 6,912 cells다. 5-year stacked first-difference 분석을 위해 27년을 5년 period로 분할하면 5개 period × 256 시군구 = 1,280 cells가 된다.

### 2.1.3 작성 시 강조점

이 subsection에서 강조할 점은 본 paper의 panel이 충분히 큰 sample size를 가진다는 것이다. 시군구 256개와 27년의 조합은 cross-sectional variation과 time-series variation을 모두 활용할 수 있는 풍부한 panel임을 명시한다.

또한 행정구역 변경 처리의 중요성을 짚는다. 한국 시군구는 1997년부터 2023년까지 여러 번 통합되거나 분리되었다. 일관된 crosswalk이 없으면 같은 지역이 다른 시군구로 잡히는 inconsistency가 발생한다. 본 paper는 2021년 baseline에 맞춰 모든 연도를 일관되게 매핑한다는 것을 명시한다. Crosswalk의 detail은 online appendix로 빼낸다.

작성 시 주의점은 이 subsection을 짧고 구조적으로 쓰는 것이다. 200-350단어 이내로 끝낸다. Section 3 전체의 entry point 역할을 하므로 reviewer가 panel 구조를 빠르게 파악할 수 있어야 한다.

---

## 3. Subsection 3.2 — 종속변수: 사망률 데이터

### 3.1 이 subsection의 목적

이 subsection의 목적은 paper의 종속변수인 5개 outcome group의 사망률을 어떻게 정의하고 계산했는지 명확히 설명하는 것이다. 사망률 정의가 모호하면 reviewer가 결과를 신뢰하지 못한다.

### 3.2 다뤄야 할 핵심 정보

먼저 데이터 출처를 명시한다. 사망 데이터는 KOSTAT(통계청)의 사망 microdata를 사용한다. 이 데이터는 통계청이 1997년부터 매년 공개하는 사망신고 microdata로, 1건의 사망이 1행으로 기록된다. 27년치 microdata는 약 700만 건의 사망 records를 포함한다.

각 record의 핵심 변수를 짧게 설명한다. 사망자 주소 행정구역시도와 시군구 코드, 사망연월일, 성별, 연령 5세 단위, KOSTAT 104분류 사망원인 코드가 본 paper의 분석에 사용된다.

다음으로 5개 outcome group의 정의를 명시한다. 절망사(deaths of despair)는 Case-Deaton 2015의 정의를 따라 자살(KOSTAT 코드 102), 약물 과다복용(101), 정신활성물질 사용 정신질환(057), 만성 간질환과 간경변(081)의 합으로 정의한다. 이 정의는 미국 절망사 문헌의 표준이며 한국에 직접 적용 가능하다.

심혈관계 사망(cardiovascular)은 코드 067-070, 암(cancer)은 027-048, 호흡기계(respiratory)는 073-078, 외인사 기타(external other)는 097-104에서 자살(102)을 제외한 나머지로 정의한다. 심혈관계와 암은 만성질환이라 단기 무역 충격에 반응하지 않을 것으로 예상되므로 placebo로 작동한다.

사망률 계산 방법을 명시한다. 시군구 c, 연도 t의 outcome group d의 사망률은 인구 10만명당 사망자 수로 계산한다. 인구 분모는 KOSIS의 시군구 × 성 × 5세 연령 인구 panel을 사용한다. 연령 표준화 사망률(age-standardized mortality rate)을 계산하기 위해 2000년 한국 인구 분포를 표준 인구로 사용한다.

로그 변환을 명시한다. Main specification에서는 ln(deaths/pop × 100,000 + 1)을 사용한다. +1 smoothing은 작은 시군구의 0 사망 cell 처리를 위한 것이다. Robustness로 +0.5 smoothing, 0 cell drop, level 사망률, Poisson 회귀를 보고한다.

### 3.3 작성 시 강조점

이 subsection에서 강조할 점은 사인 분류의 정확성과 일관성이다. KOSTAT 104분류 코드는 ICD-10 기반으로 시기에 따라 코딩 방식이 변경되었을 수 있다. 1997-1999년과 2000년 이후의 코딩 일관성을 어떻게 확인했는지 짧게 짚는다. 가지고 있는 KOSTAT 코드북(2020년 사망원인통계 질병분류코드)을 reference로 사용한다.

작은 시군구의 0 cell 문제를 명시적으로 다룬다. 인구 5만 미만 시군구에서 특정 outcome group의 연간 사망자가 0인 경우가 종종 있다. 이는 시군구 단위 사망률 분석의 표준적 한계다. +1 smoothing이 이를 부분적으로 해결하지만 완전하지는 않다는 것을 인정하고, robustness section에서 다양한 처리 방법을 보고한다는 것을 명시한다.

작성 시 주의점은 사망 데이터의 raw 처리 단계(cp949 인코딩 처리, 27개 CSV 결합 등)는 paper에 안 쓰는 것이다. 이런 작업 디테일은 panel 구축 작업 문서와 online appendix로 빼낸다. 본문에는 reviewer가 변수의 의미를 이해하기 위한 정보만 담는다. 이 subsection은 400-600단어 이내로 끝낸다.

---

## 4. Subsection 3.3 — 처치변수: Bartik 도구변수

### 4.1 이 subsection의 목적

이 subsection의 목적은 paper의 핵심 처치변수인 Bartik 도구변수의 구축 방법을 정확히 설명하는 것이다. Bartik IV는 본 paper의 식별 전략의 중심이므로 reviewer가 IV 구축 절차를 정확히 이해해야 한다.

### 4.2 다뤄야 할 핵심 정보

먼저 Bartik IV의 구조를 식으로 명시한다. 시군구 c, 연도 t의 Bartik IV는 다음과 같이 정의된다.

$$\text{Bartik}_{c,t} = \sum_{j} s_{cj,1997} \cdot g_{j,t}$$

여기서 $s_{cj,1997}$는 시군구 c의 1997년 산업 j 고용 비중이고, $g_{j,t}$는 산업 j의 t시점 무역 충격이다.

다음으로 산업 분류 baseline을 명시한다. 본 paper는 KSIC(한국표준산업분류) 2자리 분류를 사용한다. 1997년 산업 census는 KSIC 8차 분류를 사용했으므로, 이를 일관된 분류로 변환하기 위해 KSIC crosswalk(8차→9차→10차→11차)을 사용한다. 산업 j는 약 24개의 제조업 KSIC2 산업을 의미한다. 비제조업 산업은 무역 충격이 적용되지 않으므로 비중에는 포함되지만 충격 값은 0으로 처리한다.

1997년 baseline shares 계산 방법을 명시한다. KOSIS 산업 census 1997년 자료에서 시군구 c의 산업 j 종사자 수 $L_{cj,1997}$을 얻고, 시군구 c의 전체 종사자 수 $L_{c,1997}$로 나눠서 비중을 계산한다.

$$s_{cj,1997} = \frac{L_{cj,1997}}{L_{c,1997}}$$

베이스라인 연도를 1997년으로 정한 이유를 명시한다. 1997년은 중국 WTO 가입(2001) 이전이라 China Shock의 영향을 받지 않은 산업 구조다. 또한 1997년은 IMF 외환위기 직전이라 한국 산업 구조의 baseline으로 적합하다. 본 paper는 robustness로 1990년과 2000년 baseline shares도 사용해서 결과의 일관성을 확인한다.

무역 충격 $g_{j,t}$의 정의를 명시한다. Main specification에서는 한국과 중국의 양자 무역(KR-CN bilateral)의 net export 변화를 사용한다. 산업 j의 t시점 KR-CN net export는 한국의 중국 수출에서 중국의 한국 수출(한국 입장에서 수입)을 뺀 값이다. 변화는 1997년 대비 t시점의 변화 또는 5년 전 대비 t시점의 변화로 측정한다.

$$g_{j,t} = \Delta \ln(\text{NetExport}^{KR-CN}_{j,t})$$

Robustness로 ADH 8개국(호주, 스위스, 독일, 덴마크, 스페인, 핀란드, 일본, 뉴질랜드)의 대중국 수입 변화를 사용한다. 이는 한국 노동시장과 외생적인 충격 source다.

데이터 출처를 명시한다. 무역 데이터는 UN Comtrade에서 받았고, HS6(Harmonized System 6자리) product 코드 단위다. KSIC 산업 분류와 HS6 product 코드의 매핑은 KSIC-ISIC4-CPC21-HS2012 단계적 변환을 통해 수행한다.

### 4.3 작성 시 강조점

이 subsection에서 강조할 점은 Bartik IV의 학술적 표준성이다. Bartik IV는 Goldsmith-Pinkham-Sorkin-Swift 2018가 정리한 표준 도구변수이며, Pierce-Schott 2020, Autor-Dorn-Hanson 2013 등 무역 문헌의 표준이다. 본 paper도 이 표준 절차를 따른다는 것을 명시한다.

또한 KR-CN bilateral과 ADH 8국 IV의 trade-off를 짧게 설명한다. KR-CN bilateral은 한국의 무역 메커니즘에 직접 적합하지만 한국 노동시장과 동시 결정될 가능성이 있다. ADH 8국 IV는 외생성이 더 강하지만 한국 노동시장과의 관련성이 약할 수 있다. Main specification으로 KR-CN을 사용하고 ADH를 robustness로 보고하는 결정을 짧게 정당화한다. 약한 IV 문제는 Anderson-Rubin과 tF inference로 처리한다는 것을 Section 4(Identification)에서 다룰 것임을 짧게 언급한다.

작성 시 주의점은 KSIC-HS 변환의 detail을 짧게 다루는 것이다. 변환 과정의 문제(직접 매핑 부재, 단계적 변환의 정보 손실)를 인정하되 변환 매트릭스의 robustness를 짧게 짚는다. 자세한 내용은 online appendix로 빼낸다. 이 subsection은 500-700단어 이내로 끝낸다.

---

## 5. Subsection 3.4 — 매개변수: 가족 구조 지표

### 5.1 이 subsection의 목적

이 subsection의 목적은 paper의 핵심 매개변수인 가족 구조 지표 5개를 어떻게 정의하고 계산했는지 명확히 설명하는 것이다. 가족 구조 채널이 paper의 main contribution이므로 매개변수의 정의가 정확해야 한다.

### 5.2 다뤄야 할 핵심 정보

먼저 5개 매개변수의 정의를 표로 정리한다. 결혼율(crude marriage rate)은 인구 1000명당 혼인 신고 건수로 정의한다. 이혼율(crude divorce rate)은 인구 1000명당 이혼 신고 건수로 정의한다. 출생률(crude birth rate)은 인구 1000명당 출생아 수로 정의한다. 합계출산율(total fertility rate)은 가임 여성(15-49세) 1인이 평생 낳을 것으로 기대되는 평균 자녀 수다. 1인가구 비율(single-person household rate)은 전체 가구 중 1인가구의 비율이다.

데이터 출처를 명시한다. 결혼율, 이혼율, 출생률, 합계출산율은 KOSIS의 시군구 단위 인구동향조사 결과를 사용한다. 각 지표는 1997-2023년 시군구 panel로 가용하다. 1인가구 비율은 KOSIS 인구주택총조사 시군구 결과에서 받는다. 인구주택총조사는 5년 간격(1995, 2000, 2005, 2010, 2015, 2020)으로 실시되므로 연간 panel을 만들기 위해 linear interpolation을 사용한다.

각 매개변수의 한국 baseline 값을 짧게 보여준다. 1997년 한국 평균 결혼율은 약 8.7건/1000명, 이혼율은 약 2.0건/1000명, 출생률은 약 13.5명/1000명, 합계출산율은 약 1.52, 1인가구 비율은 약 12%였다. 2020년에는 결혼율 4.2건, 이혼율 2.1건, 출생률 5.3명, 합계출산율 0.84, 1인가구 비율 32%로 변화했다. 이 수치들은 한국 가족 구조 변화의 폭이 매개 효과 검출에 충분히 크다는 것을 보여준다.

매개변수 변환을 명시한다. Main specification에서는 매개변수의 로그 변환 또는 비율 그대로 사용한다. 결혼율, 이혼율, 출생률은 log 변환(ln(rate + 1))을 사용한다. 합계출산율과 1인가구 비율은 비율 그대로 사용한다. Robustness로 level 변환과 standardized 변환을 보고한다.

### 5.3 작성 시 강조점

이 subsection에서 강조할 점은 가족 구조 지표가 paper의 매개 분석에 적합한 이유다. 다섯 개 지표가 가족 구조의 다른 측면(결혼 진입, 결혼 해체, 출산 결정, 누적 출산력, 가족 단위 해체)을 포괄한다는 것을 짚는다. 한 가지 지표만 사용하지 않고 다섯 개를 모두 보는 이유는 가족 구조 변화의 multidimensional 특성 때문이다.

또한 시군구 단위 가족 구조 지표가 한국에서 풍부하게 가용하다는 사실을 강조한다. 미국에서는 county 단위 결혼율, 이혼율 데이터의 quality와 coverage가 시기에 따라 다르다. 한국 KOSIS 데이터는 시군구 단위 panel로 일관되게 가용하므로 매개 분석에 적합하다.

1인가구 비율의 interpolation을 명시적으로 다룬다. 5년 간격 데이터를 연간 panel로 만들 때 linear interpolation을 사용하는 것은 표준적이지만 매개 분석의 timing 식별에 영향을 줄 수 있다. Robustness로 interpolation 없이 5년 간격 panel만 사용한 결과를 보고한다.

작성 시 주의점은 가족 구조 지표의 변환과 처리를 정확히 명시하는 것이다. 어떤 변환을 사용했는지, 결측치를 어떻게 처리했는지, interpolation 가정이 무엇인지가 reviewer의 reproducibility 평가에 영향을 준다. 이 subsection은 400-600단어 이내로 끝낸다.

---

## 6. Subsection 3.5 — 보조 매개변수와 통제변수

### 6.1 이 subsection의 목적

이 subsection의 목적은 paper의 보조 매개변수(노동시장, 가구 부채, 의료 인프라)와 통제변수의 정의를 짧게 설명하는 것이다. 가족 구조 채널이 main이지만 다른 채널과 비교하기 위해 보조 매개변수도 사용한다.

### 6.2 다뤄야 할 핵심 정보

먼저 보조 매개변수 세 가지를 짧게 다룬다.

노동시장 매개변수는 시군구별 실업률, 고용률, 경제활동참가율이다. KOSIS의 시군구 단위 노동시장 통계를 사용한다. 다만 시군구 단위 통계는 2008년 이후만 안정적이므로 2008-2023년 panel만 사용한다. 분석 기간 일부에 대한 보조 분석으로 활용한다.

가구 부채 매개변수는 ECOS 가계대출과 연체율이다. ECOS 데이터는 시도 단위(16개)이므로 시군구 분석에 직접 쓸 수 없다. 시도 단위 보조 분석 또는 robustness로 활용한다. 시군구 매개 분석에서는 가구 부채 채널을 직접 측정하지 못하는 한계가 있다는 것을 명시하고 limitation으로 다룬다.

의료 인프라 매개변수는 HIRA 시군구별 의료인력 panel이다. 인구 1000명당 의사 수와 정신건강 관련 의료인력 수를 매개변수로 사용한다. HIRA 데이터는 2009년 이후만 가용하므로 2009-2023년 보조 분석에만 사용한다.

다음으로 통제변수를 짧게 다룬다.

시군구 baseline 특성으로 1997년 인구 분포(성별, 연령), 도시화 정도(도시/농촌 dummy), 시도 fixed effects를 사용한다. 시간에 따라 변하는 통제변수로 시군구 GRDP(KOSIS), 인구 lag, ECOS macro 변수(CPI, 환율, 기준금리)를 사용한다.

연도 fixed effects와 시군구 fixed effects를 main specification에 포함한다. 5-year stacked first-difference에서는 시군구 fixed effects가 first-difference로 흡수되므로 period fixed effects만 명시적으로 포함한다.

### 6.3 작성 시 강조점

이 subsection에서 강조할 점은 보조 매개변수의 한계를 솔직히 인정하는 것이다. 노동시장 데이터는 2008년 이후만, 가구 부채는 시도 단위, 의료 인프라는 2009년 이후만이라는 시기적 제약을 명시한다. 이 한계가 paper의 main contribution(가족 구조 채널)에는 영향을 미치지 않지만 다른 채널과의 비교 분석은 partial하다는 것을 짚는다.

NHIS 진료 데이터 부재를 명시적으로 limitation으로 다룬다. 정신건강 채널을 직접 측정하지 못하는 것이 본 paper의 가장 큰 데이터 한계라는 것을 인정하고, 자살을 outcome으로 사용함으로써 부분적으로 보완한다는 것을 짚는다.

작성 시 주의점은 보조 매개변수가 main 분석을 흐리지 않게 하는 것이다. 가족 구조 채널이 paper의 핵심이고, 보조 매개변수는 비교를 위한 것이라는 점을 명확히 한다. 이 subsection은 300-500단어 이내로 끝낸다.

---

## 7. Section 3 전체의 톤과 스타일

Section 3의 톤은 정확하고 시스템적이다. 데이터 처리의 모든 결정을 학술적으로 정당화한다. 모호한 표현("적절히", "일반적으로")을 피하고 정확한 정의("5세 연령 bin", "log(rate + 1) 변환")를 사용한다.

문장 구조는 변수명 - 정의 - 출처 - 처리 방법 순으로 정리한다. 예를 들어 "결혼율(crude marriage rate)은 인구 1000명당 혼인 신고 건수로 정의되며, KOSIS 인구동향조사의 시군구 panel에서 받는다. Main specification에서는 ln(결혼율 + 1)로 변환해서 사용한다."

표(table)와 그림(figure)을 적극적으로 활용한다. 데이터 출처와 변수 정의를 표로 정리하면 reviewer의 가독성이 크게 올라간다. Section 3에 들어갈 표 후보는 다음과 같다. Table 1은 데이터 출처와 분석 기간을 정리한다. Table 2는 핵심 변수의 descriptive statistics(평균, 표준편차, 최소, 최대)를 시군구 단위로 정리한다. Table 3은 5개 outcome group의 사인 분류를 KOSTAT 코드와 함께 정리한다.

작성 시 주의점은 데이터 처리의 모든 결정을 정당화하는 것이다. 왜 1997년 baseline인지, 왜 5-year stacked인지, 왜 +1 smoothing인지, 왜 KSIC2 분류인지 등 모든 선택에 짧은 정당화를 추가한다. Reviewer가 "왜 이렇게 했나"라는 질문에 Section 3에서 답을 얻어야 한다.

---

## 8. Section 3 작성 순서 권장

Section 3은 panel 구축이 어느 정도 완료된 후에 작성한다. Panel 구축 과정에서 결정한 사항(시군구 crosswalk, 결측치 처리, 변수 변환)을 paper 본문에 정리하는 것이 효율적이다.

다음 순서를 권장한다.

먼저 panel 구축 작업 문서를 완성한다. 이 작업 문서에 본인의 모든 데이터 처리 결정을 기록한다.

그 다음 panel 구축 작업 문서에서 Section 3 본문에 필요한 정보만 추출한다. 폴더 구조, cleaning 코드 detail, 시군구 crosswalk의 step-by-step 작업 등은 빼고, 변수 정의와 처리 결정의 학술적 정당화만 가져온다.

그 다음 4개 subsection을 각각 작성한다. Subsection 3.1(panel 구조)부터 시작해서 3.2(종속변수), 3.3(처치변수), 3.4(매개변수), 3.5(보조 매개변수와 통제변수) 순으로 쓴다.

마지막으로 표 3개를 만들어 본문에 삽입한다. 데이터 출처 표, descriptive statistics 표, 사인 분류 표.

이 작업은 paper 작업의 중반(3-4개월차)에 시작한다. Reduced form 결과가 나오기 전에 Section 3은 완성도 있게 쓸 수 있다.

---

## 9. Section 3 본문에 들어갈 표(Table) 체크리스트

Section 3 작성 시 다음 표를 준비한다.

Table 1은 데이터 출처와 분석 기간을 정리한다. 종속변수, 처치변수, 매개변수, 통제변수 각각의 데이터 출처(KOSTAT, KOSIS, ECOS, HIRA, UN Comtrade), 분석 기간, 단위(시군구 또는 시도)를 표로 보여준다.

Table 2는 핵심 변수의 descriptive statistics를 정리한다. 시군구 단위 변수의 평균, 표준편차, 최소, 최대, 관측치 수를 1997년, 2010년, 2020년 세 시점으로 보여준다. 변화의 magnitude를 reviewer가 한눈에 파악할 수 있다.

Table 3은 5개 outcome group의 KOSTAT 104분류 코드 매핑을 보여준다. 절망사, 심혈관계, 암, 호흡기, 외인사 기타 각각이 어떤 코드를 포함하는지 명시한다. 사인 분류의 정확성을 reviewer가 검증할 수 있게 한다.

이 표들은 paper 본문에 삽입하고, 자세한 데이터 처리 절차는 online appendix로 빼낸다.

---

## 10. 다음 단계

이 가이드 다음으로 작성해야 할 문서는 panel 구축 작업 문서다. Section 3 작성 가이드와 분리되어야 하는 이유는 다음과 같다.

Section 3 작성 가이드는 reviewer를 위한 paper 본문을 어떻게 쓸지의 가이드다. 변수 정의와 처리 결정의 학술적 정당화에 초점을 맞춘다.

Panel 구축 작업 문서는 본인이 작업할 때 무엇을 어떻게 할지의 매뉴얼이다. Raw 데이터 폴더 구조, cp949 인코딩 처리, 27개 CSV 결합 코드, 시군구 crosswalk의 step-by-step 작업, 결측치 처리의 algorithm, 5-year stacked panel 구축의 코드 구조 등이 들어간다.

두 문서는 내용이 일부 겹치지만 목적과 톤이 다르다. Section 3 가이드는 학술 논문 본문 작성용이고, panel 구축 작업 문서는 본인 작업용이다. 후자는 paper의 online appendix 또는 replication package의 base가 된다.

다음에는 panel 구축 작업 문서를 만든다. 이는 Section 3보다 길고 상세하며, 모든 raw 데이터의 처리 단계를 본인이 따라할 수 있을 정도로 명시한다.

---

**END OF SECTION 3 WRITING GUIDE v1.0**
