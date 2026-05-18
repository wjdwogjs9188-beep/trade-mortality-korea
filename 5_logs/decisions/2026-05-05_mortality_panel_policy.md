# Mortality panel policy commitments (Phase 2-A 입력)

**date**: 2026-05-05
**author**: R-A
**status**: final (PAP v4.0 § 4 main body rewrite 시 통합)

QA report (v02_1) 발견 3가지 결정 잠금. 본 로그가 PAP § 4 의 mortality panel 정의 부분의 single source of truth.

## 결정 1 — Working-age 25-64

### 결정
**Main spec: 25-64세 working-age population 만**.

### 근거
- **Case-Deaton (2015 PNAS)**: white middle-age (45-54) 중심 deaths of despair 증가 → working-age 가 trade shock susceptible cohort
- **ADH (2013 AER)**: prime-age (15-64) labor force, mortality regression 도 25-64
- **Pierce-Schott (2020 AERI)**: 25-64
- **Finkelstein-Notowidigdo-Shi (2026 BFI)**: 25-64
- **DGHP (2017)**: 25-64

→ **선행 anchor papers 모두 25-64**. PAP v4.0 § 4 도 25-64 명시.

### 영향
- panel 다시 build (~30min Python ETL)
- 현 v01 panel 의 all-age 버전은 → robustness 로 격하 (`_robustness_all_age.parquet`)
- 외부 검증: KOSIS suicide 25-64 stat (1990-2023, n=34) 와 비교

### 한계
- F17 (담배) 사망 → 65세+ peak. working-age 제한이 F17 channel underestimate 가능 (이미 Case-Deaton 도 동일 한계 인정)
- working-age 정의가 다른 vintage paper (예: WHO 15-64) 와 비교시 caveat 필요

## 결정 2 — 분자/분모 universe matching

### 문제
- **분자** (KOSIS 사망 microdata): 한국 내 모든 사망 — 한국인 + 외국인 (불법체류자 포함, ~0.5%)
- **분모** (현재 v01 인구 panel = 행안부 주민등록): 한국 국적자만

→ 분자 inflate (외국인 사망 포함) + 분모 narrow → mortality rate 과대 추정 (~0.3%).

### 결정
**Main spec: Korean-only universe (분자 + 분모 모두)**.

### 구현
1. **분자**: KOSIS 사망 microdata 의 `사망자국적` (또는 동등) 컬럼으로 외국인 filter
   - 컬럼 부재 시 → 외국인 사망 추정치 (연도별 ~0.5%) 로 mark + sensitivity drop
2. **분모**: 행안부 주민등록 Korean 그대로 사용
3. **Robustness**: KOSIS 인구 (행안부 + 외국인등록) 분모 + microdata 그대로 분자 = "all-resident" 변형

### 영향
- mortality rate 약 ~0.3% 더 낮게 (deflation in main spec)
- 결과 sign·magnitude 에 거의 영향 없음 (외국인 사망이 시군구 across 거의 uniform)

## 결정 3 — 2008 ICD-10 revision break

### 문제
QA 발견: drug_101 (-20%), psych_057 (-22%) 가 2008 전후 급변. classification artifact 의심.

### 배경
한국 ICD-10:
- 2007 (4차 개정): F17 분류 명확화, 외인사 (V01-Y89) 세부 변경
- 2016 (5차 개정): COVID 코드 추가 (이건 후순위)

### 결정
**Main spec**: 모든 연도 포함 + `post_2008_icd_revision` dummy + 사인별 cross-walk dict.

### Sensitivity (PAP § 11)
1. **2007-2009 drop**: ICD 전환기 3년 제외
2. **사인별 break test**: 사망원인 057, 101 별도 ICD-10 매핑 v3 (2008 이전) vs v4 (2008 이후) 비교
3. **결과**: 만약 main spec 결과가 sensitivity 에서 50%+ 감소 → ICD artifact 의심, paper limitation 으로 명시

### 영향
- panel 에 `period_pre2008` / `period_post2008` 변수 추가
- Romano-Wolf family 의 H4 (drug deaths) 와 H5 (psychiatric) 는 dummy interaction 추가

## 결정 4 — small cell smoothing (deaths < 5)

### 문제
QA: 22.3% cells 가 deaths < 5. log(asr + 1) 변환 중인데 여전히 noise 多.

### 결정
**Main spec**: log(asr + 1) 유지 (Pierce-Schott 와 동일).

### Sensitivity (Phase 4 SE layer)
1. **Poisson regression**: count outcome + offset(log(pop))
2. **Bayesian smoothing**: empirical Bayes 수축 (시군구 작은 cell → 시도 평균 쪽)
3. **Inverse propensity weight**: deaths > 5 cells 만 사용

→ 3개 sensitivity 결과 중 main spec 과 같은 sign + 50% 이상 magnitude → robust.

## 정책 commit 후 다음 step (Phase 2-A 본 build)

1. **build script** (R-A 직접): `2_scripts/mortality/01_working_age_panel_build.py`
   - 입력: `0_raw/mortality_kostat/*.csv` + `0_raw/kosis_population/population_combined.csv` + `1_codebooks/kosis_104_to_icd10.yaml`
   - filter: age 25-64 + 한국 국적
   - aggregate: h_code × year × outcome_group
   - join: pop panel (working-age + Korean only)
   - rate: deaths / pop × 100000 = age-specific mortality rate (ASR 동등)
   - output: `3_derived/mortality/sigungu_mortality_panel_v02_wa.parquet`
2. **외부 validation**: KOSIS suicide 25-64 vs panel suicide 25-64 (1990-2023, n=34)
3. **Test 3 final 실행** (script 24): pre-trend exogeneity 검정 — Phase B-x final dependency
4. **첫 reduced form**: Δlog despair_total ~ z_x_h^{KR-CN} + year FE

## Anchor 문서

- Case & Deaton (2015 PNAS): "Rising morbidity and mortality in midlife among white non-Hispanic Americans"
- ADH (2013 AER): "The China Syndrome: Local Labor Market Effects of Import Competition in the United States"
- Pierce & Schott (2020 AERI): "Trade Liberalization and Mortality"
- Finkelstein, Notowidigdo, Shi (2026 BFI): "The Effect of NAFTA on Drug-Related Mortality"
- DGHP (2017): "Trade and Manufacturing Jobs in Germany"

## Memory 업데이트 권장

- `feedback_panel_codebook_reference.md` 에 working-age policy 추가
- `project_data_status.md` 에 외국인 universe issue + 2008 ICD break 추가
