# Phase B-x pre-flight profile (2026-05-04)

Phase B-x scripts 22·23·24·25 가 의존하는 5개 입력의 raw 상태 점검.
Codebook-first 원칙대로 0_raw·1_codebooks 만 inspect.

## 1) ECOS macro panel (script 22 input)

- file count: **12**
- 파일명 코드 매칭: **3/6**
 - ❌ `200Y110` — 국내총생산에 대한 지출 (실질, 분기 및 연간)
 - ❌ `402Y014` — 수출물가지수 (기본분류)
 - ❌ `401Y015` — 수입물가지수 (기본분류)
 - ✅ `901Y009` — 소비자물가지수
 - ✅ `731Y004` — 환율
 - ✅ `722Y001` — 한국은행 기준금리

- 상위 5개 파일 (size):
 - 901Y009_M_200001_202412_CPI_소비자물가지수.csv (14545 KB)
 - 403Y001_M_200001_202412_국가별_수출.csv (5991 KB)
 - 403Y002_M_200001_202412_국가별_수입.csv (5986 KB)
 - 731Y004_M_200001_202412_환율_주요국통화별_월.csv (2311 KB)
 - 132Y003_A_2008_2024_산업별대출금_예금은행_지역별_용도별.csv (1883 KB)

⚠️ **[P1]** missing codes: ['200Y110', '401Y015', '402Y014']
 - script 22 (Test 1) 부분적으로만 작동. 누락된 매크로는 회귀에서 제외됨

## 2) WEO Historical xlsx (script 23 input)

- size: 8.56 MB
- sheets: ['Info', 'ngdp_rpch', 'pcpi_pch', 'bca_gdp_bp6']
- main sheet: `ngdp_rpch` shape head=(5, 70)
- sample columns: ['country', 'WEO_Country_Code', 'ISOAlpha_3Code', 'year', 'S1990ngdp_rpch', 'F1990ngdp_rpch', 'S1991ngdp_rpch', 'F1991ngdp_rpch', 'S1992ngdp_rpch', 'F1992ngdp_rpch', 'S1993ngdp_rpch', 'F1993ngdp_rpch']
- Korea (KOR) rows: **40**
✅ **[OK]** WEO 로드 가능. script 23 의 long-format 변환에서 vintage_year/horizon 추출

## 3) KR-CN bilateral csv (script 22, 23 input)

- file count: **50** (CLAUDE.md 기대: 50/50 ✅)
- 샘플 컬럼 (KR_exp_to_CN_2000.csv): ['typeCode', 'freqCode', 'refPeriodId', 'refYear', 'refMonth', 'period', 'reporterCode', 'reporterISO', 'reporterDesc', 'flowCode']
- year range (filename): 2000-2024, n_year=25
- flow tags: ['exp', 'imp']
✅ **[OK]** 50 파일 (M+X × 2000-2024)

## 4) 시군구 centroid (script 25 + Conley SE input)

- rows: **251** (기대 251)
- columns: ['h_code', 'name', 'lng', 'lat', 'geom_type']
- distinct h_code: 251
- lng 유효: 251/251
- lat 유효: 251/251
✅ **[OK]** 251/251 정확 매칭

## 5) sigungu crosswalk (script 25 sido cluster input)

- rows: **6,723** (기대 6,723)
- columns: ['year', 'raw_code', 'h_code', 'h_name', 'sido_code', 'sido_name', 'event_note']
- distinct h_code: 256 (기대 256)
- year range: 1997-2023
✅ **[OK]** crosswalk 정상

## 종합
- OK: **4/5**

| input | status | flag |
|-------|--------|------|
| ecos_macro | PARTIAL | P1 |
| weo | OK | OK |
| krcn | OK | OK |
| centroid | OK | OK |
| crosswalk | OK | OK |

## 다음 단계 (Suggested next steps)
1. ❌ Test 1 / 1b 입력 결손 — 위 missing 항목 우선 보강 후 재 preflight
3. **Phase 2-B 의존 (Test 3·25)**: dry-run 으로 끝남. Phase 2-B 1990 baseline 별도 turn 필요
4. preflight 통과 시 `run_phase_bx_all.ps1` 한 번 실행 → 4개 log 일괄 생성