# Claude Code Prompt — KSIC2 ↔ HS6 매핑표 산출

## 작업 목적

KIET (한국산업연구원) 의 60대산업 분류를 bridge 로 사용해서 KSIC2 (한국표준산업분류 2자리) 와 HS6 (Harmonized System 6자리) 의 매핑표를 만든다. 이 매핑표는 본 paper 의 Bartik IV 계산 (Stage 5: Comtrade 무역 충격 산업별 집계) 에 사용된다.

매핑 chain: **HS6 → 60대산업 (3레벨) → KSIC10차 → KSIC2**

ISTANS (산업통상자원부 + KIET 공동 운영) 출처라 학술 인용 가능. 단계적 변환 (KSIC→ISIC4→CPC21→HS2012→HS6) 보다 정확도가 높음.

## 입력 파일

두 파일이 `뉴 논문/crosswalks/` 폴더에 있다:

1. **60대산업-HSCODE.xlsx** (6,909 rows)
   - 컬럼: hsc, productcode, 레벨3코드, 레벨3산업명, 레벨2코드, 레벨2산업명, 레벨1코드, 레벨1산업명
   - HSCODE 와 60대산업 분류 (3 레벨) 매핑
   - hsc 컬럼 길이 분포가 mixed 가능 (5-digit, 6-digit, leading zero issue)

2. **60대산업-표준산업분류_V2.xlsx** (101 rows, sheet '연계표')
   - 컬럼: 1레벨, 2레벨, 3레벨, 표준산업분류 10차, 표준산업분류 9차
   - 60대산업 분류 와 KSIC 9차/10차 매핑
   - 일부 cells NaN (parent 의 매핑을 inherit 하는 hierarchy 구조)

## 출력 파일

`뉴 논문/crosswalks/ksic2_to_hs6.csv` 를 산출. 컬럼:
- ksic2 (정수, 예: 21 = 의료용 물질 및 의약품 제조업)
- hs6 (문자열, 6-digit zero-padded, 예: "010110")
- weight (float, 일대다 매핑 시 가중치, 합 = 1)
- ksic2_name (한글 산업명)

추가로 다음 진단 파일:
- `뉴 논문/crosswalks/ksic2_hs6_mapping_diagnostics.md` — 매핑 quality report

## 처리 단계

### Step 1: 60대산업-HSCODE 파일 읽기 + 정제

- Sheet1 읽기 (openpyxl 또는 pandas read_excel)
- hsc 컬럼 길이 분포 확인 (.str.len().value_counts())
- HS6 표준 (6-digit) 으로 통일:
  - 5-digit 인 경우 leading zero 추가 (예: 10110 → "010110")
  - 6-digit 은 그대로 (zero-padding 유지)
  - 6-digit 초과 (예: 7-digit) 는 별도 표시 후 첫 6자리만 사용
- "999999" 같은 미분류 코드는 별도 처리 (Bartik IV 에서 무시)
- 출력: hs6_60ind 매핑 dataframe (hs6, 레벨3코드, 레벨3산업명, 레벨2코드, 레벨1코드)

### Step 2: 60대산업 표 읽기 + NaN inheritance 처리

- Sheet '연계표' 읽기
- forward fill (.ffill()) 로 1레벨, 2레벨 NaN 채우기 (parent inherit)
- 단 3레벨 NaN 인 row 는 그 row 가 2레벨 단위 매핑 (즉 3레벨 코드 없이 2레벨 까지만 KSIC 매핑) 인 경우와 구분
- 표준산업분류 10차 컬럼에서 KSIC 코드 추출 (예: "C21 의료용 물질 및 의약품 제조업" → "C21" → KSIC2 = 21)
- 정규식 또는 split 로 첫 token 추출 (대분류 알파벳 + 2-digit)
- 출력: ind_to_ksic 매핑 dataframe (3레벨 코드, KSIC2, KSIC2 산업명)

### Step 3: 두 파일 join

- hs6_60ind 와 ind_to_ksic 를 60대산업 코드 (3레벨 우선, 없으면 2레벨, 없으면 1레벨) 로 left join
- 일대다 매핑 처리: HS6 하나가 여러 KSIC2 에 매핑되면 균등 분할 (weight = 1/n)
  - **Robustness 옵션**: 인구 가중 (사업체통계의 KSIC2별 종사자 수) — 일단 균등 분할로 시작
- 매핑 실패 HS6 (60대산업 매핑 없음 또는 KSIC 매핑 없음) 은 별도 dataframe 으로 저장 (`unmatched_hs6.csv`)

### Step 4: 검증 + diagnostics

매핑 quality 체크:
1. 매핑된 HS6 의 unique 수 vs 입력 HSCODE 파일의 unique HS6 수 (cover 율)
2. 일대일 vs 일대다 매핑 비율 (weight = 1.0 vs weight < 1.0)
3. KSIC2별 매핑된 HS6 수 분포 (제조업 KSIC2 10-33 의 cover 균형)
4. 누락 HS6 의 productcode 텍스트 분석 (어떤 산업에 누락 많은지)

`ksic2_hs6_mapping_diagnostics.md` 에 다음 보고:
- 입력/출력 row 수
- HS6 cover 율 %
- 매핑 weight 분포
- KSIC2별 cover 표
- 누락 HS6 top 20 (산업명 텍스트와 함께)
- 처리 결정 사항 (HS6 zero-padding, NaN inheritance, 균등 분할 등)

### Step 5: Comtrade KR-CN 데이터와 cross-check

- 보유한 Comtrade KR-CN 50개 파일 중 1개 (예: KR_exp_to_CN_2010.csv) 의 cmdCode 컬럼 unique HS6 추출
- 이 HS6 set 이 ksic2_to_hs6 매핑표에 얼마나 cover 되는지 확인
- 누락률 5% 이상이면 보완 방법 제안 (단계적 변환 fallback, KIET 추가 자료 검색 등)

## 주의 사항

1. **인코딩**: xlsx 는 utf-8 기본, 한글 처리 시 시스템 locale 영향 확인.
2. **HS6 표준**: Comtrade 의 cmdCode 가 6-digit 정수 또는 string 인지 확인. 매핑 join 시 string 으로 통일.
3. **KSIC 버전**: 60대산업-표준산업분류 V2 는 KSIC 10차 와 9차 매핑이 둘 다 있음. main 은 10차 사용 (가장 최신).
4. **1997 산업 census 호환성**: 1997 census 는 KSIC 8차임. 8차→9차 변환은 별도 단계 (보유한 `research_supp/ksic_crosswalk_8_to_9.csv` 사용). 이 코드는 KSIC2 까지 정의하면 됨.
5. **Raw 파일 절대 수정 X**: 두 xlsx 는 read-only 로만 사용.

## 결과 검토 기준

매핑표가 학술 사용 가능한 quality 인지 판단 기준:
- HS6 cover 율 ≥ 90% (제조업 HS6 만 보면 ≥ 95%)
- KSIC2 제조업 24개 중 매핑 0인 KSIC2 가 1개 이하
- 누락 HS6 가 명확한 sector (예: 농림수산물, 미분류) 에 집중

위 기준 미달 시 단계적 변환 (UN CPC/ISIC 매핑) 을 보완으로 사용하는 hybrid 방법 고려.

## 출력 후 사용자 확인 필요한 것

1. HS6 cover 율 확인
2. 누락 HS6 top 20 의 산업 분포가 합리적인지 검토
3. 일대다 매핑이 너무 분산되어 있지 않은지 (weight 분포)
4. 매핑표 채택 결정 후 panel_construction_execution_guide.md Stage 5 진행

---

이 prompt 를 Claude Code 에 그대로 전달하면 됩니다. 산출물은 `뉴 논문/crosswalks/` 폴더에 저장됩니다.
