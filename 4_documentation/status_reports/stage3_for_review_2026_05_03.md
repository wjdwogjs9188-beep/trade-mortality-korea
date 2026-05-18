# Stage 3 인구 Panel + 사망률 Panel 구축 — 외부 피드백용 상세 기록

작성일: 2026-05-03
프로젝트: Trade Shock × Family Disruption × Deaths of Despair (Korea)
문서 목적: Stage 3 작업 내용을 외부 reviewer 가 검토 가능한 형태로 정리

---

## 0. Stage 별 위치

```
Stage 1 (완료): Raw 수집·검증 (KOSTAT 사망 microdata, KOSIS 인구, KOSIS 시군구 사망원인)
Stage 2 (완료): 사망 panel 구축 (mortality_panel_v01.parquet, 7,297,865 records, 9 검증 PASS)
Stage 3 (이번): 인구 panel + 연령 표준화 사망률 panel 구축  ← 본 문서
Stage 4 (예정): Bartik IV panel 구축 (KSIC2 시군구 산업 비중 + KR-CN bilateral net export)
Stage 5 (예정): 회귀 분석 (5-year stacked first-difference 2SLS, 5-layer SE, 6 진단)
```

---

## 1. 작업 목적

KOSIS 주민등록인구 raw 를 처리하여 시군구 × 연도 × 성 × 연령 인구 panel 을 구축하고,
Stage 2 사망 panel 과 join 하여 연령 표준화 사망률 (per 100k) panel 을 생성.
회귀 분석에 직접 사용 가능한 형태로 산출.

**핵심 도전**:
1. KOSIS 인구 코드 체계 (5-digit C1) 와 KOSTAT 사망 코드 체계의 충돌 (특히 2023 부산 21310 vs 21510)
2. 분구 시군구 (수원, 부천 등) 의 parent code 와 children codes 가 같은 연도 raw 에 공존 → 합산 시 double-count 위험
3. KOSIS sigungu × sex × age 데이터 1998 부터 시작 → 1997 처리 필요
4. 연령 표준화 baseline 선정 + 0 cell handling

---

## 2. 입력 파일

| 파일 | 출처 | 행 수 | 비고 |
|------|------|-------|------|
| `0_raw/kosis_population/population_combined.csv` | KOSIS 주민등록인구 (1B040M5, 한국 국민만) | 516,750 | C1=시군구, C2=성, C3=연령 |
| `1_codebooks/sigungu_crosswalk_v2.csv` | 직접 구축 (Stage 1) | 6,723 | 256 raw_code → 229 h_code |
| `3_derived/mortality/mortality_panel_v01.parquet` | Stage 2 v4 산출물 | 1,483,920 cells | 사망 panel |

---

## 3. 산출물

| 파일 | 크기 | 행 수 | 내용 |
|------|------|-------|------|
| `3_derived/population/population_panel_v01.parquet` | 640 KB | 210,222 | 시군구 × 연도 × 성 × age_band 인구 |
| `3_derived/population/population_panel_validation.md` | 2.0 KB | — | V1-V5, V9 검증 보고 |
| `3_derived/mortality/mortality_rate_panel_v01.parquet` | 1.7 MB | 74,196 | h_code × year × sex × outcome → ASR (per 100k) + ln_asr |
| `3_derived/mortality/mortality_rate_validation.md` | 2.4 KB | — | V6-V8 검증 보고 |

`210,222 = 229 시군구 × 27 연도 × 2 성 × 17 age_band` (결측 0).
`74,196 = 229 × 27 × 2 × 6 outcome group` (결측 일부 — 0 인구 cell).

---

## 4. 처리 단계 (실제 실행된 9 단계)

### Step 1 — KOSIS population_combined.csv 처리

**필터 1**: C1 5-digit 만 유지 (시도/전국 합계 제외)
- raw 516,750 → 5-digit 479,808

**필터 2**: C2 ∈ {1, 2} 만 (계 행 제외)
- 5-digit 479,808 → sex 319,872

**필터 3**: C3 ∈ {17개 5세 band 코드} (000 제외, 410+ 제외)
- sex 319,872 → age 229,466

**필터 4**: year ≥ 1997
- age 229,466 → year≥1997 229,466

**KOSIS C3 코드 정의 (확인된 사실)**:
- 020=0-4세, 050=5-9세, 070=10-14세, 100=15-19세, 120=20-24세, 130=25-29세,
- 150=30-34세, 160=35-39세, 180=40-44세, 190=45-49세, 210=50-54세, 230=55-59세,
- 260=60-64세, 280=65-69세, 310=70-74세, 330=75-79세, **340=80세 이상** (단일 통합)
- 410, 430, 440 등은 90+ 세분 (340 안에 이미 포함) → 제외

### Step 2 — KOSTAT age 1-20 ↔ KOSIS C3 통합 매핑

```
unified age_band     KOSIS C3              KOSTAT age_5yr_code
01_02 (0-4세)        020                   1 + 2  (합산)
03    (5-9세)        050                   3
04    (10-14세)      070                   4
05    (15-19세)      100                   5
06    (20-24세)      120                   6
07    (25-29세)      130                   7
08    (30-34세)      150                   8
09    (35-39세)      160                   9
10    (40-44세)      180                   10
11    (45-49세)      190                   11
12    (50-54세)      210                   12
13    (55-59세)      230                   13
14    (60-64세)      260                   14
15    (65-69세)      280                   15
16    (70-74세)      310                   16
17    (75-79세)      330                   17
18_19_20 (80+)       340                   18 + 19 + 20  (합산)
```

→ **17개 통합 band** 사용. 양 panel 에서 일관 적용.

### Step 3 — Sigungu Crosswalk Hybrid Merge (핵심 설계 결정)

**문제 발견**: 단일 merge 전략으로 모두 해결 불가
- **Year-aware merge**: pop 의 2023 데이터가 KOSTAT 사망 코드 (21510 등) 가 아닌 KOSIS 인구 코드 (21310) 를 사용 → 2023 모두 unmatched
- **Year-agnostic merge**: 부천시 (31050) 는 1997-2015 동안 parent 코드 (31050) 와 children 코드 (31051, 31052, 31053) 가 raw 에 공존 → 같은 (year, h_code) 에 parent + children 동시 매칭 → double-count

**해결**: Hybrid merge with deduplication
- **Phase A (year-aware)**: `(year, raw_code) → h_code` 매칭. 217,396 rows 매칭.
- **Phase B (year-agnostic fallback)**: Phase A 미매칭 rows 에 대해 `raw_code → h_code` 일대일 매칭 시도하되, **(year, h_code) 가 Phase A 에서 이미 매칭됐으면 reject**. 2,754 rows 추가.
- 미매칭 9,316 rows: 모두 parent city totals (31010, 33010 등) → 자동 drop (children 으로 이미 매칭됨)

**결과**:
- 총 220,150 matched / 9,316 unmatched (정상 drop)
- Year-aware 에서 잡혀야 할 케이스 (Bucheon parent vs children) → Phase A 에서 children 만 매칭, parent 는 Phase B 에서 reject → double-count 방지
- Year-agnostic 으로 살릴 케이스 (2023 KOSTAT 코드) → Phase B 에서 fallback

이 hybrid 설계가 없었다면 KOSIS V5 cross-check 가 ±2% 를 넘었을 가능성 높음.

### Step 4 — Population Panel Collapse + 1997 Proxy

```python
pop_panel = matched.groupby(["h_code", "year", "C2", "age_band"], as_index=False)["population"].sum()
pop_panel = pop_panel.rename(columns={"C2": "sex_code"})
```

**1997 처리**: KOSIS sigungu × sex × age 데이터는 **1998 부터 시작** (1993-1997 은 sido 단위만). KOSTAT 사망 panel 은 1997 부터 27년 coverage 라 align 필요.

→ **1998 인구를 1997 proxy 로 사용**. 한국 시군구별 인구 변화 ~0.5%/yr 라 1년 차이 bias 미미. **Paper Limitation 에 명시 필수**.

산출: 210,222 rows = 229 × 27 × 2 × 17 (결측 0).

### Step 5 — Mortality Panel age_band 통합

Stage 2 mortality panel 은 KOSTAT 5세 코드 1-20 사용 → 17 통합 band 로 collapse.

```python
mort_band = mort.groupby(["h_code", "year", "sex_code", "age_band", "outcome_group"])["deaths"].sum()
# 1,483,920 → 1,261,332 cells
# (229 × 27 × 2 × 17 × 6 = 1,261,332)
```

검증: collapse 전후 deaths 합 동일 (V8).

### Step 6 — Mortality × Population Join

```python
panel = mort_band.merge(pop_panel, on=["h_code","year","sex_code","age_band"], how="left")
panel["rate_per_100k"] = panel["deaths"] / panel["population"] * 100_000
panel.loc[panel["population"] == 0, "rate_per_100k"] = pd.NA
```

Join coverage: **100.0000%** (mortality 의 모든 cell 이 인구와 매칭).

### Step 7 — 직접 연령 표준화 (2010 한국 baseline)

**Baseline 선정**: 2010 한국 전체 인구 (남녀 별도 표준 인구).
**방식**: Direct standardization (Pierce-Schott, Case-Deaton 표준 방식).
**Within-sex weighting**: 같은 성 안에서 age_band 비중. Σw_age = 1 per sex.
**결측 처리**: 인구 결측 (0 cell) 시 weight 재정규화 → downward bias 방지

```
ASR = Σ_age (rate_age × w_age)  /  Σ_age (w_age_available)
```

산출: h_code × year × sex × outcome → asr_per_100k.

### Step 8 — Log 변환

```python
asr["ln_asr"] = log(asr_per_100k + 1)
```

0 cell handling: log(0+1) = 0. 회귀 분석 dependent variable 로 사용 가능.

### Step 9 — 9가지 검증 (V1-V9, 모두 PASS)

| # | 검증 | 결과 |
|---|------|------|
| V1 | 인구 합 보존 (filter→merge→collapse) | PASS |
| V2 | 229 sigungu cover | 229 ✅ |
| V3 | 27 year cover (1997-2023) | ✅ (1997 = 1998 proxy) |
| V4 | 17 age_band cover | 17/17 ✅ |
| V5 | KOSIS 한국 총인구 cross-check (5년) | 0.124% – 1.173% (모두 ±2% 이내) |
| V6 | Despair ASR 시계열 한국 historical pattern | 1997=58.8 → 2010=47.0 → 2015<2010 → 2023=35.3 ✅ |
| V7 | Mortality join coverage | 100.0000% ✅ |
| V8 | Age band 매핑 무결성 (mortality deaths 합 보존) | PASS |
| V9 | 표준화 weight 합 = 1 (per sex) | PASS |

---

## 5. 핵심 설계 결정 4가지 요약

### (1) Hybrid sigungu merge

KOSIS 인구 코드 체계와 KOSTAT 사망 코드 체계의 부분적 충돌 + 분구 시군구 parent/children 공존 → 두 문제 동시 해결을 위해 Phase A (year-aware) + Phase B (year-agnostic fallback with (year, h_code) dedup) 도입.

### (2) 1997 인구 = 1998 proxy

KOSIS sigungu × sex × age 데이터 1998 시작 한계. 1년 proxy 로 27년 panel coverage 유지. Limitation 에 명시.

### (3) 17 통합 age band

KOSIS C3 020 + KOSTAT 1,2 → 0-4세 (band 01_02).
KOSIS C3 340 + KOSTAT 18,19,20 → 80+ (band 18_19_20).
나머지 1:1. 양 panel 일관 적용.

### (4) 2010 한국 baseline 직접 표준화 (within-sex)

Case-Deaton, Pierce-Schott 표준 방식. Sex 별 별도 가중. 인구 결측 시 weight 재정규화로 downward bias 차단.

---

## 6. ASR 시계열 패턴 (검증 V6 상세)

**전국 가중 평균 despair_total ASR (per 100k)**:

| 연도 | ASR | 비고 |
|------|-----|------|
| 1997 | 58.8 | IMF 직전, 간질환 사망률 정점 |
| 2010 | 47.0 | 자살률 정점 (~31), 간질환 급락 |
| 2015 | < 2010 | 자살률 감소기 |
| 2023 | 35.3 | 전체 감소 추세 |

**해석**: despair_total = suicide + drug + psych + **liver** 합산이라 1997 간질환 정점 (~30/100k) → 급락이 자살률의 1997-2010 상승 (~13 → ~31) 을 압도. 전체 panel 은 1997 → 2023 감소 추세. 한국 historical pattern 정합.

**Paper Table 권장 구조**:
- despair_total 통합 + 4 component decomposition (suicide, drug, psych, liver) 모두 제시
- Component 별 시계열 단독 제시 (자살은 1997→2010 상승, 그 외는 감소 또는 안정)
- 합산 통계만 보면 reviewer 가 "왜 자살은 늘었는데 despair 는 줄었나" 의문 제기 가능 → 사전 분해 제시로 차단

---

## 7. KOSIS V5 Cross-Check 상세

| 연도 | KOSIS 공식 (천명) | Panel 합 | 차이 % |
|------|------------------|----------|--------|
| 2000 | 47,008 | (panel 값) | (≤1.173%) |
| 2010 | 49,410 | (panel 값) | (≤1.173%) |
| 2015 | 51,015 | (panel 값) | (≤1.173%) |
| 2020 | 51,836 | (panel 값) | (≤1.173%) |
| 2023 | 51,753 | (panel 값) | (≤1.173%) |

**모두 ±2% 합격 기준 통과**. 0.124% 가 best, 1.173% 가 worst (어느 연도인지는 validation report 확인 필요).

**격차 원인 (정상)**:
1. KOSIS 공식 통계는 추계인구 또는 등록인구 기준 차이
2. Panel 은 주민등록인구 (1B040M5) 기반 — 외국인 미포함
3. 시점 cut-off 차이 (12.31 vs 연중 평균)
4. 분구 collapse 처리 시 미세 round-off

±2% 이내 → KOSIS 공식 통계와 학술 standard 부합.

---

## 8. 알려진 한계점 (Limitations)

| # | 한계 | 영향 | 대응 |
|---|------|------|------|
| 1 | 1997 인구 = 1998 proxy | 매우 미미 (~0.5%/yr) | Paper Appendix 명시 |
| 2 | 외국인 미포함 (주민등록인구만) | 미미 (한국 외국인 비율 < 4%, 시군구별 분포 균등) | KOSIS 공식 정의 일관 |
| 3 | 80+ 단일 band (90+ 세분 없음) | KOSIS C3 340 단일 코드 한계 | 80+ aggregate 로 보고 |
| 4 | 2010 baseline (다른 baseline 미실시) | 비교 가능성 제한 | Sensitivity: 2020 baseline 추가 검증 권장 |
| 5 | Despair_total 안에서 liver 가 1997 dominance | 통합 통계 해석 시 주의 | Component decomposition 으로 분해 제시 |

---

## 9. 코드 / 산출물 구조

```
2_scripts/build_panel/
├── 2A_mortality_panel.py         # Stage 2 v4
└── 3A_population_panel.py        # Stage 3 v1 (신규)

3_derived/
├── mortality/
│   ├── mortality_panel_v01.parquet
│   ├── mortality_panel_validation.md
│   ├── mortality_rate_panel_v01.parquet      # 신규 (Stage 3)
│   └── mortality_rate_validation.md          # 신규 (Stage 3)
└── population/                                # 신규 폴더 (Stage 3)
    ├── population_panel_v01.parquet
    └── population_panel_validation.md

1_codebooks/sigungu_crosswalk_v2.csv          # 256 raw → 229 h
```

---

## 10. Paper Appendix A 변경 사항 누적 (Stage 1-3)

| Stage | 변경 |
|-------|------|
| Stage 1 | Sigungu baseline 256 → 229 (자치구 collapse: 수원, 성남, 안양, 안산, 고양, 용인, 청주, 천안, 전주, 포항, 통합창원) |
| Stage 2 v4 | Cancer 정의 027-048 → 027-047 (KOSIS 악성신생물 C00-C97 정합) |
| Stage 3 (신규) | (a) Hybrid sigungu merge: year-aware + year-agnostic fallback with (year, h_code) dedup |
| Stage 3 | (b) 1997 인구 = 1998 proxy (KOSIS sigungu data 1998 시작) |
| Stage 3 | (c) Age band 통합: KOSIS C3 020 + KOSTAT 1,2 → 0-4세; KOSIS C3 340 + KOSTAT 18,19,20 → 80+ |
| Stage 3 | (d) 직접 연령 표준화: 2010 한국 인구 baseline, within-sex weight (Σw=1 per sex), 인구 결측 시 weight 재정규화 |

---

## 11. 외부 피드백 요청 항목

다음 항목에 대한 의견 요청:

### A. Hybrid merge 설계의 학술적 정당성
KOSIS 인구 vs KOSTAT 사망 코드 체계 충돌 + 분구 시군구 parent/children 공존을 동시 해결하는 hybrid merge 가 학술 reproducibility standard 에 부합하는지. 다른 표준 접근 방식이 있는지 (예: 항상 KOSIS-KOSTAT bridge file 별도 발행, 또는 모든 분구 시군구 통합 후 매칭).

### B. 1997 = 1998 proxy 처리의 적절성
1년 차이를 proxy 로 메우는 것이 학술 acceptable 인지, 또는 1997 자체를 panel 에서 drop 하고 1998-2023 (26년) 으로 단축하는 것이 더 깨끗한지.

### C. Despair_total 안의 liver dominance
1997 간질환 사망률 정점이 despair_total 시계열을 왜곡 (suicide 단독 추세와 반대 방향). Paper Main 에서 통합 통계 vs component decomposition 중 어느 쪽을 main outcome 으로 할지 권고. Case-Deaton 원논문은 합산 정의 사용 (suicide + drug overdose + alcohol-related liver) 이라 우리도 그 정의 따르되 decomposition 도 robustness 로 제시 가능.

### D. 2010 baseline 외 추가 baseline 권장 여부
연령 표준화 baseline 으로 2010 한국 인구 사용. WHO 2000 World Standard Population 또는 2020 한국 baseline 도 sensitivity 로 추가 보고할지 의견.

### E. ASR 의 log 변환 vs Poisson regression
회귀 분석에서 ln(ASR + 1) 사용 예정 (Pierce-Schott 표준). Poisson IV (deaths 직접 + offset = log(population)) 가 더 적절한지에 대한 의견.

### F. 80+ 단일 band 한계
KOSIS C3 340 단일 코드라 90+ 분리 불가. Paper 에서 80+ 자살률 (한국 OECD 1위 이슈) 분석 시 이 한계 언급 + 80+ aggregate 로 보고하는 것이 적절한지.

---

## 12. 다음 Stage 4 (예정)

- KSIC2 × 시군구 산업 비중 panel (사업체조사 raw 사용)
- KR-CN bilateral net export panel (Comtrade)
- KSIC2-HS6 concordance: KIET 60대산업 reject 후 BACI / Pierce-Schott / Dauth-Findeisen-Suedekum 표준 concordance 채택 검토
- Bartik shift-share IV 구축 (Goldsmith-Pinkham-Sorkin-Swift 2018 share exogeneity path)

---

작성: 정재헌 (가천대 경제학부 학부생, wjdwogjs9188@gmail.com)
프로젝트: SSCI mid-tier 단독 저자 paper 준비 중
연구주제: Trade Shock, Family Disruption, and Deaths of Despair: A Hidden Mechanism in Korea
