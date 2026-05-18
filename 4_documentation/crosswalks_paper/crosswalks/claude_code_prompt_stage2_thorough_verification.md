# Stage 2 v4 Mortality Panel — 면밀 신뢰성 검증 prompt

## 작업 목적

`mortality_panel_v01.parquet` (Stage 2 v4 산출물) 의 신뢰성을 8개 layer 로 면밀히 검증.
모든 숫자가 KOSIS 공식 통계 + 다른 source 와 cross-check 되어 paper 학술 standard 통과 여부 확인.

## 입력 파일

- `3_derived/mortality/mortality_panel_v01.parquet`
- `3_derived/mortality/mortality_microdata_combined.parquet`
- `1_codebooks/sigungu_crosswalk_v2.csv`
- `1_codebooks/mortality_104_classification.csv`
- `0_raw/research_supp/시군구 사망원인.csv` (KOSIS 가공 패널, cross-check 용)
- `0_raw/kosis_population/population_combined.csv` (cross-check 용 인구)

## 산출물

`3_derived/mortality/thorough_verification_report.md` — 8 layer 검증 결과 종합 보고서

---

## Layer 1 — Multiple cause cross-check (KOSIS 공식 통계와 6개 outcome 모두 비교)

KOSIS 사망원인통계의 다음 사인별 사망자수와 panel 비교 (`0_raw/research_supp/시군구 사망원인.csv` 사용 또는 KOSIS 공식 발표 직접 입력):

```python
# 검증 연도: 2000, 2005, 2010, 2015, 2020, 2023 (6년)
# 검증 사인: despair_total 의 4 component + cancer + cardiovascular + respiratory

# Despair component 별 (KOSIS 공식 통계 기준)
KOSIS_OFFICIAL = {
    "suicide_102": {"2010": 15566, "2015": 13513, "2020": 13195, "2023": 13978},
    "drug_101":     {"2010": 357,   "2015": 392,   "2020": 559,   "2023": 547},
    "psych_057":    {"2010": 1142,  "2015": 1521,  "2020": 1845,  "2023": 2015},
    "liver_081":    {"2010": 6862,  "2015": 6925,  "2020": 6886,  "2023": 6912},
    "cancer":       {"2010": 72048, "2015": 76855, "2020": 82204, "2023": 85271},
    "cvd_067_070":  {"2010": 50890, "2015": 56760, "2020": 60578, "2023": 65198},
    "respiratory":  {"2010": 26020, "2015": 32240, "2020": 32093, "2023": 30988},
    "total_all":    {"2010": 255405,"2015": 275895,"2020": 304948,"2023": 352511},
}
```

(주의: 위 숫자는 KOSIS 공식 발표 추정값. 정확한 숫자는 KOSIS 사이트에서 검증 필요. 본인이 Layer 1 실행 후 panel 숫자가 ±2% 이내 일치하면 KOSIS 숫자도 정확한 것으로 판단 가능.)

각 (사인 × 연도) 별 panel ours vs KOSIS official 비교 → ±0.5% 합격, ±2% marginal, > 2% 재검토.

## Layer 2 — Sex × Age 분포 검증 (한국 인구학 패턴 일치)

### 2-1. 자살 성비 (남:여)

한국 자살 성비는 2000년대 이후 일관되게 약 2.3-2.5 : 1 (남:여).

```python
# 자살 (cause_104=102) 의 sex_code 1 vs 2 비율, 연도별
suicide_male = panel[(panel["outcome_group"]=="despair_total") & (panel["sex_code"]=="1")] # 남성 despair (suicide 포함)
# 더 정확히는 microdata 에서 cause=102 만:
suicide_micro = combined[combined["cause_104"]=="102"]
ratio_2010 = suicide_micro[(suicide_micro["year"]=="2010") & (suicide_micro["sex_code"]=="1")].shape[0] / \
             suicide_micro[(suicide_micro["year"]=="2010") & (suicide_micro["sex_code"]=="2")].shape[0]
```

기대: 2010 약 2.3, 2015 약 2.5, 2020 약 2.5, 2023 약 2.5. ±0.2 이내 합격.

### 2-2. 80+ 자살률

한국 80+ 자살률은 OECD 1위, 2010년대 이후 100/100k 이상 (특히 80+ 남성 200/100k).

```python
# panel 에서 80+ (age_5yr_code 18, 19, 20 = KOSTAT 80-84, 85-89, 90+)
elderly_suicide = panel[
    (panel["outcome_group"]=="despair_total") & 
    (panel["age_5yr_code"].isin(["18","19","20"]))
].groupby(["year","sex_code"])["deaths"].sum()
# 분모: 80+ 인구 (Stage 3 결합 전이라 manually 추정)
# 한국 80+ 인구 약 50만 → 80+ 자살률 = (자살자/50만)*100k 추정
```

기대: 80+ 남성 자살률 200-350/100k, 여성 100-200/100k.

### 2-3. Cancer 성비 (남:여 약 1.5:1)

남성 cancer 사망이 여성보다 1.5배 많음 (위암, 폐암, 간암 등 남성 우세).

## Layer 3 — Sigungu 단위 cross-check (KOSIS 시군구 사망원인 panel 과 비교)

`0_raw/research_supp/시군구 사망원인.csv` 가 KOSIS 가공 시군구 사망 panel. 이를 base 로 본 paper 의 panel 과 비교.

```python
kosis_sigungu = pd.read_csv("0_raw/research_supp/시군구 사망원인.csv", encoding="utf-8")
# 시군구 × 연도 × 성 × 사인 분류 panel
# 예: 11680 강남구 2020 자살자수가 panel 의 11680 강남구 2020 despair (despair 가 자살 포함) 와 일치하는지
```

10개 random sigungu × 4 연도 (2010, 2015, 2020, 2023) × 5 outcome group spot check. 95% 이상 ±2% 일치 합격.

## Layer 4 — Time series 패턴 검증 (한국사 연동)

자살률 시계열이 한국 historical pattern 과 일치하는지:

```python
# 인구 10만명당 자살률 (panel suicide / 한국 총인구 * 100k)
korean_pop = {
    "1997": 46_491_000, "2000": 47_008_000, "2003": 47_859_000,
    "2010": 49_410_000, "2015": 51_015_000, "2020": 51_836_000, "2023": 51_753_000
}
suicide_rate = {}
for y in korean_pop:
    n_suicide = combined[(combined["year"]==y) & (combined["cause_104"]=="102")].shape[0]
    suicide_rate[y] = n_suicide / korean_pop[y] * 100_000
```

기대 패턴 (한국 자살률 시계열):
```
1997  ~13     IMF 직전
2000  ~13     IMF 회복
2003  ~24     1차 정점 (IMF 후속, 카드대란)
2010  ~31     2차 정점 (글로벌 금융위기 후)
2015  ~26     감소기
2017  ~24     저점
2020  ~25     COVID 초기
2023  ~27     재상승
```

Panel 의 자살률 시계열이 위 패턴 (±2/100k) 일치하면 합격.

## Layer 5 — 분구 시군구 통합 검증

`sigungu_crosswalk_v2.csv` 의 자치구 collapse 가 panel 에서 정확히 작동하는지.

```python
# 통합 창원시 (38110) 의 deaths = (마산합포 + 마산회원 + 의창 + 성산 + 진해) 의 합 ?
# 단, panel 은 이미 collapsed 라 38110 한 row 만 있음. 
# Cross-check: KOSIS 시군구 사망원인.csv 의 통합창원시 합과 비교
changwon_panel = panel[panel["h_code"]=="38110"].groupby("year")["deaths"].sum()
# KOSIS 데이터에서 통합 창원시 또는 5개 자치구 합과 비교
```

10개 분구 collapse 사례 (창원, 청주, 고양, 수원, 성남, 안양, 안산, 용인, 천안, 전주, 포항) 모두 검증.

## Layer 6 — Internal consistency

### 6-1. Microdata vs Panel 합 일치

```python
panel_total = panel["deaths"].sum()
combined_valid = combined[
    combined["h_code"].notna() & 
    combined["sex_code"].isin(["1","2"]) & 
    combined["age_5yr_code"].notna() & 
    (combined["age_5yr_code"] != "99") & 
    combined["cause_104"].notna()
].shape[0]
assert panel_total == combined_valid
```

### 6-2. Despair 4 component 합산 정확성

```python
# Microdata 에서 cause_104 in {102, 101, 057, 081} 의 count
n_despair_micro = combined[combined["cause_104"].isin(["102","101","057","081"])].shape[0]
# Panel 의 despair_total 합
n_despair_panel = panel[panel["outcome_group"]=="despair_total"]["deaths"].sum()
# (단, microdata 는 valid 필터 후 비교)
```

### 6-3. 6 outcome group 합 = total deaths

```python
total_panel = panel["deaths"].sum()  # 7,298,820 (예상)
group_sums = panel.groupby("outcome_group")["deaths"].sum()
assert group_sums.sum() == total_panel
```

## Layer 7 — 0 cell + sparse 분포 검증

```python
# 0 cell 비율 (작은 시군구일수록 높아야 정상)
sigungu_0cell_pct = panel.groupby("h_code").apply(
    lambda x: (x["deaths"] == 0).sum() / len(x) * 100
).sort_values()

# 시군구 인구 (Stage 3 결합 전이라 KOSIS 인구 직접 join)
pop = pd.read_csv("0_raw/kosis_population/population_combined.csv", dtype=str)
pop_2020 = pop[(pop["year"]=="2020") & (pop["C2"]=="0") & (pop["C3"]=="000")]  # 시군구별 총 인구
pop_2020 = pop_2020[pop_2020["C1"].str.len()==5]
pop_2020["population"] = pop_2020["population"].astype(float)

# 인구 vs 0-cell 비율 correlation
# 작은 시군구일수록 0-cell 많아야 함 (음의 correlation 강한 신호)
```

기대: 인구와 0-cell 비율의 negative correlation (Spearman ρ < -0.5).

## Layer 8 — KOSIS 시도 합계 cross-check

광역시도 (16개) 단위로 panel 합 vs KOSIS 광역시도 발표 비교.

```python
# Panel 의 시도 합 (h_code 첫 2자리 sido)
panel["sido"] = panel["h_code"].str[:2]
sido_yearly_total = panel.groupby(["sido","year"])["deaths"].sum()

# KOSIS 시군구 사망원인.csv 의 시도별 합과 비교
# 또는 KOSIS 사망원인 사도/광역 단위 발표와 비교
```

서울 (11), 부산 (21), 대구 (22), 인천 (23), 광주 (24), 대전 (25), 울산 (26), 세종 (29), 경기 (31), 강원 (32), 충북 (33), 충남 (34), 전북 (35), 전남 (36), 경북 (37), 경남 (38), 제주 (39) — 17개 sido (세종 포함).

각 시도 × 4 연도 (2010, 2015, 2020, 2023) ±0.5% 일치 합격.

## 종합 보고서 구조

`thorough_verification_report.md` 에 다음 8 layer 결과 정리:

```markdown
# Stage 2 v4 — Thorough Verification Report

## Summary
- Layer 1 (Multi-cause KOSIS cross-check): X/Y PASS
- Layer 2 (Sex × Age 분포): X/Y PASS
- Layer 3 (Sigungu spot check): X/Y PASS
- Layer 4 (Time series 패턴): PASS / FAIL
- Layer 5 (분구 collapse 검증): X/Y PASS
- Layer 6 (Internal consistency): X/Y PASS
- Layer 7 (0 cell 분포): PASS / FAIL
- Layer 8 (시도 cross-check): X/Y PASS

## Detailed results
[각 layer 의 표 + 분석]

## Overall conclusion
[채택 / 추가 조사 / 재실행 권고]
```

## 검증 합격 기준

- **Layer 1, 5, 6, 8** (절대 정확성): ±0.5% 이내 일치 필수
- **Layer 2, 4** (분포 패턴): 한국 인구학 패턴과 정성적 일치
- **Layer 3** (sigungu spot check): 95%+ pairs ±2% 이내
- **Layer 7** (0 cell): 인구 vs 0-cell 비율 음의 correlation

8 layer 모두 PASS → Stage 2 v4 학술 standard 통과 확정. 일부 FAIL → 원인 추적 + 재실행.

---

이 prompt 를 Claude Code 에 전달. 산출물은 `3_derived/mortality/thorough_verification_report.md`.
