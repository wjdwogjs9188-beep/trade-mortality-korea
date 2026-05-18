# Phase 2-B Step 1 — 1994 광업제조업조사 schema probe
_2026-05-05_

## File
- path: `0_raw\kosis_business_survey\microdata_1994_2024\1994_연간자료_20260415_74722.csv`
- size: 96.4 MB
- encoding: `utf-8-sig`
- columns (15):
```
  [ 0] 11
  [ 1] 010
  [ 2] 51
  [ 3] C
  [ 4] 12
  [ 5] 1
  [ 6] *
  [ 7] *.1
  [ 8] ****
  [ 9] **
  [10] *.2
  [11] *.3
  [12] *.4
  [13] *.5
  [14] *.6
```

## 주요 컬럼 후보
- **sigungu** (`시군구,행정,지역,소재지,주소,구시군`): (none)
- **sido** (`시도,광역,특별시도`): (none)
- **ksic** (`산업,KSIC,업종,산업분류`): (none)
- **employee** (`종사자,종업원,근로자,고용,인원`): (none)
- **workplace** (`사업장,사업체,공장,본사`): (none)
- **weight** (`가중치,weight,wt,design`): (none)

## 샘플 (first 5 rows, first 12 cols)
```
11 010 51 C 12 1 * *.1 **** ** *.2 *.3
11 010 51 D 17 9 *   * **** **   *   *
11 010 51 D 17 9 *   * **** **   *  **
11 010 51 D 18 1 *   * **** **   *   *
11 010 51 D 18 1 *   * **** **   *  **
11 010 51 D 22 1 *   * **** **   *  **
```

## Row count + 시도 분포
- total rows: **2,518,453**

## Codebook (`0_raw/kosis_business_survey/codebook/`)
- files: 60
  - `2002년 광공업 조사표(공장,본사).hwp` (400 KB)
  - `2002년 광공업 조사표(공장,본사).pdf` (488 KB)
  - `2002년_광업제조업통계조사표1(공장용).pdf` (340 KB)
  - `2002년_광업제조업통계조사표2(본사용).pdf` (362 KB)
  - `2002년_광업제조업통계조사표3(정보통신부문).pdf` (79 KB)
  - `2005_조사개요.hwp` (32 KB)
  - `2005년기준광업제조업조사표1.hwp` (130 KB)
  - `2005년기준광업제조업조사표1.pdf` (348 KB)
  - `2006년 광업제조업조사표.hwp` (128 KB)
  - `2006년 광업제조업조사표.pdf` (350 KB)
- ⚠️ 1994 전용 codebook 없음. ms_2000_*.md 또는 ms_1990_*.md 사용 필요

## 다음 step (2-B.2) 입력으로 사용할 결정 사항
- [ ] sigungu 컬럼 확정 (위 후보 중 1개)
- [ ] sigungu 코드 형식 (3/4/5-digit, 시도+시군구 결합)
- [ ] h_code crosswalk 매핑 전략 (1997-2023 crosswalk 의 1997 baseline 적용?)
- [ ] KSIC 차수 (현 crosswalk 9차 vs 1994 KSIC ?차)
- [ ] 종사자 컬럼 확정 (계 vs 상용 vs 임시 vs 일용)
- [ ] firm 가중치 (있으면 sample 가중)