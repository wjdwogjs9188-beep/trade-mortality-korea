# Claude 작업 실행 plan — Mechanism Focus Paper

## 무역 충격, 가족 해체, 그리고 절망사: 한국의 숨은 메커니즘

| Field | Value |
|-------|-------|
| 작성자 | Claude (사용자 정재헌과의 협업 plan) |
| 작성일 | 2026-05-02 |
| Version | v1.0 |
| 본 문서 목적 | 7개 가이드 문서 (research_proposal, raw_data_inventory, pap_v41_feedback, section1/2/3 writing guides, panel_construction_execution_guide) 학습 후 Claude 가 어떻게 사용자를 도울지의 작업 plan. 사용자 review 와 피드백 후 본격 작업 시작. |
| Review 기간 | 본 문서 commit 후 사용자가 검토하고 피드백을 줌 → 수정 후 v1.1 → 작업 시작 |

---

## 0. 본 문서의 위상

이 문서는 **PAP 가 아니다**. PAP 는 `research_proposal.md` 가 그 역할을 한다 (paper 의 사전등록 가설 + 식별 전략 + 회귀 spec).

본 문서는 **작업 협업 plan** 이다. 다음을 명시:

1. Claude 와 사용자의 역할 분담
2. Panel 구축 10 stage 를 Claude 가 어떻게 도울지
3. 회귀 분석 단계에서 Claude 의 역할
4. Paper 작성 단계에서 Claude 의 역할
5. 의사결정 protocol — 어느 시점에 무엇을 누가 결정
6. 막혔을 때 대처 + Comtrade quota 같은 외부 제약 처리
7. 6개월 timeline 의 Claude 기여
8. 학습 commitments

본 문서가 review 되고 commit 되면, 그 spec 따라 작업이 진행된다. 변경 시 v1.x 로 bump 하고 변경 사유 기록.

---

## 1. 연구 정체성 — Claude 의 이해

### 1.1 Paper 정체성

**Mechanism focus paper.** 무역 충격이 절망사로 이어지는 매개 경로 중 **가족 구조 채널** (결혼율↓, 이혼율↑, 출생률↓, 1인가구↑) 을 정량화. Pierce-Schott 2020 의 reduced form 을 mediation chain 으로 확장.

이는 PAP v4.1 (broad "Trade × Mortality") 에서 pivot 된 것. PAP v4.1 의 Issue 1 (net export 단방향성), Issue 7 (시나리오 B contribution 약함) 을 paper 정체성 전환으로 우회.

### 1.2 핵심 5 가설

- **H1**: 무역충격 → 결혼율↓, 이혼율↑, 출생률↓, 1인가구↑ (4 가족구조 변화)
- **H2**: 가족구조 변화 → 절망사 사망률 ↑
- **H3**: 매개 비중 ≥ 30%
- **H4**: working-age (25-54) 남성에서 효과 max
- **H5 (placebo)**: cancer, CVD 단기효과 X

### 1.3 식별 전략 핵심

- **Bartik IV**: 1997 시군구 산업비중 × KR-CN bilateral net export 충격
- **Share exogeneity** 가정 (GP 2018 path)
- **5-year stacked first-difference** (5 period × 256 시군구 = 1,280 obs)
- **6 식별 진단** (First-stage F, Rotemberg HHI, share-balance, pre-trend, AKM placebo, share permutation)
- **5-layer SE** (HC1, cluster-sido, AKM, Conley, AR+tF)
- **Multiple testing 보정**: Romano-Wolf step-down (1000 boot)

### 1.4 Submission target

- **First choice**: Demography (인구학 저널, 가족구조 channel focus 가 fit)
- 2nd: Social Science and Medicine
- 3rd: Journal of Population Economics
- 4th: Health Economics

### 1.5 Timeline

6개월 working paper 완성 + submission. 게재까지 추가 1-2년.

---

## 2. 역할 분담 — Claude vs 사용자

작업의 명확한 분담 — 누가 무엇을 책임지는지 사전 명시.

### 2.1 Claude 가 할 수 있는 것 (workspace 안)

- ✅ 파일 read / write / edit (Python, markdown, csv, parquet 등)
- ✅ 코드 작성 + bash 실행 (Linux sandbox 안)
- ✅ pandas, numpy, statsmodels, linearmodels 로 데이터 처리 + 회귀
- ✅ matplotlib 으로 figure 생성
- ✅ pandoc 으로 docx 변환
- ✅ git status / log 같은 read-only git 명령
- ✅ markdown 문서 작성 (PAP, 작업 가이드, paper 본문 draft)

### 2.2 Claude 가 할 수 없는 것 (사용자 PC 필요)

- ❌ 한국 정부 사이트 직접 접속 (KOSIS, KOSTAT, ECOS, 통계청)
- ❌ Comtrade API 호출 (quota 가 계정에 묶여있음, 사용자 .env 가 사용자 PC 에 있음)
- ❌ 사용자 PC 의 외부 application 실행 (Excel, Stata, R Studio)
- ❌ git commit / push (사용자 git 자격증명)
- ❌ KOSIS 인구주택총조사 같은 회원가입 후 다운로드
- ❌ NHIS 빅데이터 센터 같은 별도 신청 데이터

### 2.3 사용자가 결정해야 하는 것

- 🎯 paper 의 main thesis 변경 여부 (변경 시 v 번호 bump)
- 🎯 회귀 spec 의 main vs robustness 결정 (PAP 이미 명시, 변경 시 Appendix A 기록)
- 🎯 KOSIS 추가 다운로드 실행
- 🎯 행정구역 변천사 자료 수집 + 검증
- 🎯 학회 발표 / working paper 등재 / submission timing
- 🎯 지도교수 / 동료 연구자 review 요청 timing

### 2.4 협업 방식

| 작업 유형 | Claude 역할 | 사용자 역할 |
|---|---|---|
| 코드 작성 | 초안 작성, 디버깅 | review, 실행 (필요 시), 결과 공유 |
| 데이터 탐색 | 파일 read + 분석 | 다운로드, 권한 처리 |
| 회귀 분석 | spec 작성 + 실행 (workspace) | review, 해석 검토, 결과 사용 결정 |
| Paper 작성 | draft 작성, 인용 정리 | 본인 톤으로 rewrite, 학술적 판단 |
| 의사결정 | 옵션 제시 + trade-off 분석 | 최종 결정 |
| 문서 정리 | markdown / docx 생성 | 검토, 지도교수 공유 |

---

## 3. Panel 구축 단계 — Claude 의 도움 방식

`panel_construction_execution_guide.md` 의 10 Stage 각각에서 Claude 가 어떻게 기여하는지 명시.

### Stage 0: 환경 준비 (사용자 주도)

- **사용자**: 폴더 구조, git init, 가상환경, .gitignore 설정
- **Claude 도움**: `.gitignore` 내용 제안, 폴더 구조 검토, `code/00_setup.py` 의 path/상수 정의 코드 작성

### Stage 1: 시군구 Crosswalk (Claude 적극 기여 가능)

- **사용자**: 행정안전부 자료 수집 (KOSIS, 통계청 사이트)
- **Claude 도움**:
  - 행정구역 변경 사례 정리 표 작성 (Claude 가 알고 있는 사례 + 사용자가 가져온 자료 통합)
  - `crosswalks/sigungu_crosswalk.csv` 코드 작성 + 검증 스크립트
  - **이미 PAP v4.1 작업 시 만든 256 h_codes crosswalk** (`1_codebooks/sigungu_crosswalk.csv`, 6,723 rows) 가 있음 — 이를 새 paper 폴더로 이전 + mapping_weight 컬럼 추가
- **시간 단축**: PAP v4.1 의 crosswalk 재활용 → 1주 → 2-3일

### Stage 2: 사망 Panel (Claude 주도 가능)

- **사용자**: raw 데이터 위치 확인
- **Claude 도움**:
  - 27개 cp949 CSV 결합 코드 (이미 PAP v4.1 작업 시 작성됨, 재활용)
  - 사망원인 104분류 → 5 outcome group 매핑 코드 (이미 작성됨)
  - 시군구 매핑 + 검증
  - **PAP v4.1 의 2010 prototype 검증** 이미 통과 (KOSTAT 102 자살 100% 일치) → 27년 전체 build 만 진행하면 됨

### Stage 3: 인구 Panel + 사망률 (Claude 주도)

- **사용자**: 없음 (이미 데이터 보유)
- **Claude 도움**:
  - `population_combined.csv` (516k rows) 처리 — 이미 작성됨
  - 연령 표준화 (2000년 한국 인구 표준화) 코드
  - 사망률 계산 + 로그 변환

### Stage 4: 산업 Census 1997 (Claude 적극 기여)

- **사용자**: 1.6GB raw 데이터 위치 확인
- **Claude 도움**:
  - 195MB 1997 census 파일 chunked 처리 (cp949)
  - KSIC 8차 → 9차 → 10차 → 11차 단계적 변환
  - 시군구 × KSIC2 (24개 제조업) employment share matrix 산출
  - **검증**: 시군구별 share 합 = 1, 비제조업 합산
- **새 작업** (PAP v4.1 에서 미수행): Phase 1-F 가 여기에 해당

### Stage 5: KSIC-HS6 매핑 + Comtrade (가장 까다로움)

- **사용자**:
  - 통계청 자료실에서 KSIC-HS 직접 매핑 검색 (있으면 작업 단축)
  - Comtrade quota 회복 후 누락 데이터 추가 다운 (DE 5년 + ES 21년)
- **Claude 도움**:
  - 직접 매핑 없으면 단계적 변환 (KSIC2→ISIC4→CPC21→HS2012→HS6)
  - 일대다 매핑의 가중치 처리 (균등 분할 + sensitivity)
  - Comtrade 50 + 22 + 176 파일 (총 248개) 결합 + 산업별 무역충격 계산
  - signed log transformation (net export 음수 처리)

### Stage 6: Bartik IV (Claude 주도)

- **사용자**: 없음
- **Claude 도움**:
  - shares_1997 × shifts_jt = Bartik IV 계산
  - KR-CN main + ADH 8국 robust 별도 column
  - 5-year stacked + annual 둘 다 산출

### Stage 7: 가족구조 Mediator Panel (Claude 적극 기여)

- **사용자**: **KOSIS 인구주택총조사 시군구 결과 1995-2020 다운로드 (우선순위 1)** + 회원가입 + 5년 간격 6개 시점
- **Claude 도움**:
  - 출생/혼인/이혼 .xls 파일 처리 (xlrd)
  - 합계출산율 .xlsx 처리 (openpyxl)
  - 시군구 매핑 + 비율 계산 (per 1000명)
  - 1인가구 5년 간격 → 연간 panel linear interpolation + `imputed` 컬럼
- **새 작업** (PAP v4.1 에 없음): 새 paper 의 핵심 mediator

### Stage 8: 보조 Mediator + Control (Claude 주도)

- **사용자**: KOSIS 시군구 노동시장 panel 다운 (우선순위 3), GRDP (우선순위 4)
- **Claude 도움**:
  - HIRA 90MB 분기 → 연간 aggregate
  - ECOS 11+5 series broadcast (시도 → 시군구 5자리 prefix)
  - macro panel merge

### Stage 9: Master Panel Merge (Claude 주도)

- **사용자**: 없음 (review 만)
- **Claude 도움**:
  - 3개 panel 산출:
    1. `master_panel_sigungu_year.parquet` (시군구 × 연도, reduced form)
    2. `master_panel_5year_stacked.parquet` (5 period, main spec)
    3. `master_panel_demographic.parquet` (시군구 × 연도 × 성 × 연령, hetero)
  - 결측치 처리 + interpolation flag

### Stage 10: 검증 + Descriptive (Claude 주도)

- **사용자**: 결과 review
- **Claude 도움**:
  - 시계열 plot (한국 평균 자살률, 합계출산율, 1인가구 비율)
  - Cross-sectional variation 분포
  - paper Section 3 Table 1, 2, 3 산출 (markdown + docx)
  - `data_quality_report.md` 작성

### 시간 단축 합산

PAP v4.1 작업 재활용으로 다음 단축:
- Stage 1 (crosswalk): 1주 → 2-3일 (재활용)
- Stage 2 (사망 panel): 5-7일 → 3-4일 (코드 재활용 + 2010 검증 통과)
- Stage 3 (인구 + 사망률): 3-4일 → 2-3일 (이미 보유)

→ 6-8주 → **5-7주** 단축 가능

---

## 4. 회귀 분석 단계 — Claude 의 도움

Panel 구축 완료 후 (3개월차) 회귀 분석 시작.

### 4.1 Reduced Form (Phase 4)

- **Claude 도움**:
  - `linearmodels.IV2SLS` 코드 작성
  - 5개 outcome × 2개 IV (KR-CN main, ADH robust) = 10개 회귀
  - 결과 표 (Table 2) 자동 생성
  - First-stage F 보고

### 4.2 Mediation Analysis (핵심)

- **Claude 도움**:
  - 5개 mediator (혼인/이혼/출생/TFR/1인가구) × 2 stage = 10개 회귀
  - 매개 효과 $\delta_m \times \beta_m$ 계산
  - 가족구조 채널 비중 = $\sum_m \delta_m \beta_m / \beta_{total}$
  - 다른 채널 (노동시장, 부채, 의료) 과 비교 표

### 4.3 6 식별 진단 (Phase 3)

- **Claude 도움**:
  - 검정 0: Olea-Pflueger F (linearmodels)
  - 검정 1: Rotemberg decomposition (BHJ R 패키지 호출 또는 Python 구현)
  - 검정 2: Share-covariate balance 표 (Panel A levels, Panel B trends)
  - 검정 3: Pre-trend event-study + joint F-test (1997-2001 truncated period 사용 — Issue 4 반영)
  - 검정 4: AKM placebo 1000 iter
  - 검정 5: Share permutation 1000 iter

### 4.4 5-Layer SE

- **Claude 도움**:
  - HC1, cluster-sido, AKM (직접 구현), Conley (geopandas + custom), AR + tF (linearmodels + custom)
  - 5-column 표 자동 생성

### 4.5 Robustness + Heterogeneity

- **Claude 도움**:
  - 8개 robustness spec 자동 실행
  - Demographic 6 cell hetero
  - **Romano-Wolf step-down (1000 boot)** multiple testing 보정 (Issue 5 반영)

### 4.6 사용자 결정 시점

- 첫 reduced form 결과 후: spec 조정 필요 여부 (PAP 변경 시 Appendix A 기록)
- Identification 진단 결과 후: 합격 여부 (HHI < 0.25, joint F p > 0.10 등)
- Mediation 결과 후: 시나리오 A/B/C 판정 + 해석 방향
- Robustness 후: paper 본문 어느 spec 강조

---

## 5. Paper 작성 단계 — Claude 의 도움

### 5.1 Section 별 분담

| Section | Claude | 사용자 |
|---|---|---|
| Section 1 (Intro) | 6단락 draft (가이드 따라) | 본인 톤 rewrite, contribution 강조 |
| Section 2 (Background) | Korea timeline + 가족구조 + 4 channel 이론 | OECD 통계 정확성 검증, 한국적 맥락 |
| Section 3 (Data) | 5 subsection draft + Table 1, 2, 3 | 변수 정의 검증 |
| Section 4 (Identification) | Bartik 식 + 6 검정 보고 | 식별 가정 narrative |
| Section 5 (Reduced Form) | 결과 표 + 해석 draft | 수치 검증, contribution 연결 |
| Section 6 (Mediation) ⭐ | 매개 표 + 채널 비교 | 핵심 contribution 강화 |
| Section 7 (Robustness + Discussion) | 표 자동 생성 | Limitation, 정책 함의 |

### 5.2 Abstract + Conclusion

- **Claude**: 100-150단어 draft
- **사용자**: 본인 voice 로 다듬기

### 5.3 Native English check

- **Claude**: 1차 영문 draft 작성 가능
- **사용자**: native speaker 또는 번역 서비스로 최종 polish (학부생 단독 저자 신뢰도 위해 권장)

### 5.4 Reference + 인용 관리

- **Claude**: BibTeX 정리, in-text citation format 통일 (SSCI 표준)
- **사용자**: 추가 reference 검토

### 5.5 Working paper 등재 + Submission

- **Claude**: working paper 등재용 cover page, abstract, KIEP/KDI/한국경제연구원 형식 따른 docx 산출
- **사용자**: 실제 submission, 학회 발표, journal 선택

---

## 6. 6개월 Timeline — Claude 기여

| 월 | 작업 | Claude 주요 기여 |
|---|---|---|
| **1** | Panel 구축 stage 1-4 | crosswalk 재활용, 사망/인구 panel, 산업 census KSIC2 |
| **2** | Panel stage 5-9 + 첫 회귀 | KSIC-HS6 매핑, Comtrade 처리, Bartik IV, mediator panel, master merge |
| **3** | 식별 진단 + mediation analysis | 6 검정 코드 + 표, mediation chain 회귀 |
| **4** | Robustness + hetero + 보조 mediator | 8 robustness, 6 hetero, Romano-Wolf 보정 |
| **5** | Paper Section 1-7 작성 | 7 section draft (가이드 따라) |
| **6** | Refinement + submission | docx polish, working paper 형식, abstract |

**Critical milestones**:
- Week 6 (1.5개월): Reduced form panel 완성 (priority 1)
- Week 12 (3개월): Identification 진단 통과 + mediation 첫 결과
- Week 20 (5개월): Paper draft 1.0
- Week 24 (6개월): Submission

---

## 7. 의사결정 Protocol

### 7.1 사전 결정 (이미 PAP 에 명시 — 변경 불가)

- 분석 단위: 256 시군구 × 27년
- Baseline year: 1997
- Outcome: 5 group (despair, CVD, cancer, respiratory, external_other)
- Despair 정의: 102 + 101 + 057 + 081
- 5-year stacked first-difference
- KR-CN bilateral main IV
- 5-layer SE

→ **변경 시 Appendix A 에 기록**

### 7.2 데이터 단계 결정 (작업 중 발생)

| 결정 사항 | 결정 시점 | 결정자 | Claude 제안 방식 |
|---|---|---|---|
| KSIC-HS6 변환 가중치 | Stage 5 | 사용자 | 균등 분할 vs 인구 가중 trade-off 표 제시 |
| 1인가구 interpolation 방식 | Stage 7 | 사용자 | linear vs cubic spline 결과 비교 |
| Sample restriction (인구 5만+) | Stage 10 | 사용자 | 256 vs ~180 sigungu 결과 차이 보고 |
| 0 cell 처리 (+1 vs Poisson) | Stage 10 | 사용자 | 둘 다 robustness 보고 |

### 7.3 회귀 분석 단계 결정

| 결정 사항 | 결정 시점 | 결정자 |
|---|---|---|
| First-stage F 결과 후 IV 변경 여부 | Phase 4 | 사용자 (PAP 따름) |
| Mediation 시나리오 A/B/C 판정 | Phase 4-5 | 사용자 |
| Heterogeneity 어느 cut 강조 | Phase 5 | 사용자 |
| Limitation 어디까지 인정 | Phase 6 | 사용자 |

### 7.4 Paper 작성 결정

| 결정 사항 | 결정자 |
|---|---|
| Tone (자신감 vs 겸손) | 사용자 |
| Contribution 명시 강도 | 사용자 |
| Submission journal 선택 | 사용자 |
| Coauthor 추가 여부 | 사용자 |

---

## 8. 외부 제약 + 막혔을 때 대처

### 8.1 Comtrade quota

- **현 상태**: 4 keys × 250 calls/day = 1000 calls 한도
- **누락**: DE 5년 + ES 21년 + CN-World 3년 ≈ 25 country-years
- **대처**:
  - Quota 회복 (KST 09:00) 후 재시도
  - Account 1 만 사용 (Account 2 quota 문제 지속 시)
  - **누락 전체 안 채워도 main spec 가능** (KR-CN bilateral 만으로 충분, ADH 는 robustness)
  - → Comtrade 가 critical path 아님

### 8.2 KOSIS 추가 다운 지연

- **위험**: 우선순위 1 (1인가구) 가 핵심 mediator
- **대처**:
  - 다운 지연 시 1인가구 제외한 4 mediator (혼인/이혼/출생/TFR) 만으로 main spec 진행
  - 1인가구 늦게 다운되면 robustness 추가
  - Working paper 1.0 은 4 mediator, journal version 은 5 mediator

### 8.3 KSIC-HS6 매핑 막힐 때

- **대처 1**: 통계청 직접 매핑 검색 우선
- **대처 2**: BHJ ssaggregate R 패키지 안에 매핑 함수 있는지 확인
- **대처 3**: 단계적 변환 (KSIC→ISIC4→CPC21→HS2012→HS6) + sensitivity test
- **대처 4**: 막히면 사용자에게 보고, 1주일 더 시도, 그래도 안 되면 paper 에 limitation 명시

### 8.4 회귀 결과 unexpected

- **시나리오**: 가족구조 매개 효과 < 5% (시나리오 B)
- **대처**:
  - 시나리오 B 의 사전 작성된 narrative 사용 ("broader 사회변화 dominant")
  - 다른 채널 (노동시장, 부채) 의 매개 효과 비교
  - **Paper 정체성 변경 X** (PAP 따름)

### 8.5 학부생 신분 reviewer 우려

- **대처**:
  - Working paper 등재 (KIEP, KDI, 한국경제연구원) 로 publicity 확보
  - 학회 발표 (한국경제학회, AEA, EEA)
  - Submission affiliation 에 학교만, 직급 미표기
  - 지도교수 review 적극 활용

### 8.6 본 문서 commit 후 협업 mechanism

- 사용자가 막힐 때: 짧게 정리해서 Claude 에게 전달 → 같이 디버깅
- Claude 가 막힐 때: 즉시 사용자에게 보고 + 옵션 제시
- 결정 필요 시: Claude 가 trade-off 표 제시, 사용자 결정
- 매주 progress check: `docs/work_log.md` 에 사용자가 기록 (1줄도 OK)

---

## 9. 학습 Commitments

### 9.1 Claude 가 commit 하는 것

1. **PAP 따름**: research_proposal.md 의 가설/spec 변경 X (사용자 승인 없이)
2. **데이터 보존**: raw/ 폴더 절대 수정 X
3. **검증 우선**: 매 stage 끝나면 검증 → 사용자에게 보고
4. **정직성**: 작업 한계, 데이터 한계, 결과 한계 모두 명시
5. **재현성**: 모든 코드 + 결정 사항 git 또는 markdown 기록
6. **분리**: 파일 형식, 코드, 결정의 boundary 명확
7. **Multiple testing 정직**: Romano-Wolf 보정 결과 모두 보고
8. **Falsifiability**: 시나리오 B/C 결과도 paper 에 정직 보고
9. **Limitation 명시**: NHIS 부재, pre-period 4년 짧음, KSIC-HS6 변환 손실 등
10. **사용자 결정 우선**: trade-off 제시 후 사용자 final 결정 따름

### 9.2 Claude 가 NOT commit 하는 것

- ❌ 학술적 의사결정의 최종 권한 (Claude 는 옵션 제시까지)
- ❌ Submission timing (사용자 학사 일정 우선)
- ❌ Review 통과 보장 (학술 review 는 외부 reviewer 결정)
- ❌ 외부 데이터 접근 (사용자 PC + 자격증명 필요)
- ❌ Claude 가 모르는 한국 institutional detail (사용자 검증 우선)

### 9.3 사용자가 commit 해야 하는 것

1. **본 plan review + 피드백**: 본 문서 v1.0 검토 후 수정 또는 승인
2. **PAP commit**: research_proposal.md 가 final
3. **결정 책임**: 학술적 / 데이터 / 작성 결정의 final
4. **외부 데이터 다운**: KOSIS, Comtrade, 행정안전부 자료
5. **Review 협력**: 매 stage 결과 검토 + 피드백
6. **본인 voice**: paper 본문의 학술적 톤
7. **Submission**: working paper 등재 + journal 선택

---

## 10. 첫 시작 추천 단계

본 plan 이 review + commit 되면, 다음 순서로 시작:

### Step 1: 작업 폴더 정리 (사용자 + Claude, 1일)

- 새 paper 폴더 `family_disruption_paper/` 만들기
- raw/ 에 기존 데이터 복사 (또는 PAP v4.1 폴더와 같은 위치 재활용 결정)
- code/, processed/, panel/, crosswalks/, docs/, logs/ 하위 폴더
- `code/00_setup.py` 의 path/상수 정의 (Claude 작성)
- `.gitignore` 작성 (Claude 제안)
- git init (사용자)

### Step 2: PAP v4.1 작업물 재활용 평가 (Claude, 1-2일)

- PAP v4.1 의 `1_codebooks/sigungu_crosswalk.csv` (256 h_codes) 새 paper 에 이전 가능성 평가
- PAP v4.1 의 사망 panel build 코드 (2010 prototype 통과) 재활용 가능성
- 산업 census 처리 (Phase 1-F) 새 paper 에서 처음 진행

### Step 3: KOSIS 인구주택총조사 다운로드 (사용자, 2-3일)

- 우선순위 1: 1995, 2000, 2005, 2010, 2015, 2020 시군구 1인가구 비율
- 우선순위 2: 평균 결혼 연령, 비혼 비율
- 다운 후 raw/kosis_household/ 에 저장

### Step 4: Stage 1 (시군구 crosswalk) 시작 (Claude 주도, 2-3일)

- PAP v4.1 의 crosswalk 재활용 + mapping_weight 컬럼 추가
- 검증 스크립트 실행

### Step 5: Stage 2-3 (사망 + 인구 panel) 진행 (Claude 주도, 5-7일)

- 27년 사망 panel build (PAP v4.1 의 2010 prototype 통과 → 27년 진행)
- 인구 panel + 사망률 + 연령 표준화

### Step 6: 첫 progress review (사용자, 1일)

- Stage 1-3 결과 검토
- 다음 단계 (Stage 4 산업 census) 진행 승인

---

## 11. 본 문서의 review 항목 (사용자에게 요청)

본 문서가 v1.1 로 가기 전 사용자가 검토해야 할 부분:

1. **§ 1 연구 정체성 이해**: Claude 가 paper 정체성을 정확히 이해했나?
2. **§ 2 역할 분담**: Claude 가 할 수 있는/없는 것 구분이 정확한가?
3. **§ 3 Panel 단계별 plan**: 각 stage 의 분담이 적절한가?
4. **§ 4 회귀 분석 단계**: 6 검정 + 5-layer SE + Romano-Wolf 가 sufficient 한가?
5. **§ 5 Paper 작성 단계**: Claude 가 draft 작성, 사용자가 본인 voice 로 rewrite 의 분담 OK 한가?
6. **§ 6 Timeline**: 6개월 critical milestones 가 현실적인가?
7. **§ 7 의사결정 protocol**: 어느 시점에 누가 결정하는지가 명확한가?
8. **§ 8 막혔을 때 대처**: Comtrade quota / KOSIS 지연 / 시나리오 B 의 backup plan 이 충분한가?
9. **§ 9 commitments**: Claude 가 commit 하는 / NOT commit 하는 것이 명확한가?
10. **§ 10 첫 시작 단계**: Step 1-6 의 순서가 적절한가?

각 항목에 대해 OK / 수정 필요 / 추가 고려 사항 피드백 주시면 v1.1 로 업데이트.

---

## 12. 본 문서의 위치 + 형식

- **저장 위치**: `C:\Users\82103\Downloads\trade_mortality_korea\5_logs\my_execution_plan.md`
- **DOCX 변환**: 요청 시 즉시 산출 (지도교수 / 동료 공유용)
- **변경 시**: v 번호 bump + 변경 사유 본 문서 끝에 기록

---

**END OF MY EXECUTION PLAN v1.0**

본 문서는 Claude 가 사용자와 협업하여 mechanism focus paper 를 6개월 안에 작성하기 위한 작업 plan 이다. 사용자의 review + 피드백 후 v1.1 으로 commit 되면, 본 plan 따라 작업이 시작된다.
