# Stage 2 검증 가이드 — 본인이 직접 실행

본인 PC 에서 단계별로 실행. 각 단계의 expected output 과 비교.

## 0. 사전 준비

### 0.1 Python 환경 + 작업 폴더

cmd 또는 PowerShell 열고 프로젝트 폴더로 이동:

```cmd
cd C:\Users\82103\Downloads\trade_mortality_korea
```

Python 인터프리터 실행:

```cmd
python
```

또는 Jupyter notebook / VS Code 의 Python 환경에서 진행해도 OK.

### 0.2 Library import

```python
import pandas as pd
import numpy as np
pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 200)
```

---

## 검증 1: Panel 파일 로드 + 기본 shape

```python
panel = pd.read_parquet("3_derived/mortality/mortality_panel_v01.parquet")

print(f"Shape: {panel.shape}")
print(f"Columns: {panel.columns.tolist}")
print(panel.head)
print(panel.dtypes)
```

### Expected:
```
Shape: (1483920, 7)
Columns: ['h_code', 'h_name', 'year', 'sex_code', 'age_5yr_code', 'outcome_group', 'deaths']
```

### PASS 기준
- shape 가 정확히 `(1483920, 7)`
- 7개 컬럼 모두 존재
- deaths 가 int64 (정수)

### FL 시
- shape 가 다르면 panel 산출 코드의 dimension 정의 잘못. 즉시 보고.

---

## 검증 2: Outcome group 별 deaths 합

```python
group_sums = panel.groupby("outcome_group")["deaths"].sum.sort_values(ascending=False)
total = panel["deaths"].sum
for g, s in group_sums.items:
 print(f"{g:20s} {int(s):>10,} ({100*s/total:.2f}%)")
print(f"{'TOTAL':20s} {int(total):>10,}")
```

### Expected:
```
other 2,099,237 (29.12%)
cancer 1,912,048 (26.53%)
cardiovascular 1,544,441 (21.43%)
respiratory 611,890 (8.49%)
despair_total 574,662 (7.97%)
external_other 465,791 (6.46%)
TOTAL 7,208,069
```

### PASS 기준
- TOTAL = 7,208,069 정확히
- 6개 group 비율이 위와 ±0.01% 이내 일치

### FL 시
- TOTAL 다르면 outcome 매핑 또는 panel aggregation 오류. 즉시 보고.

---

## 검증 3: KOSTAT 자살 cross-check (가장 중요)

```python
# Despair_total 의 cause_104=102 만 분리하려면 combined microdata 필요
# 메모리 절약: cause_104 컬럼만 로드
combined_min = pd.read_parquet(
 "3_derived/mortality/mortality_microdata_combined.parquet",
 columns=["year", "h_code", "sex_code", "age_5yr_code", "cause_104"]
)

# Valid records 만 (panel 과 일치하는 정의)
valid = combined_min[
 combined_min["h_code"].notna
 & combined_min["sex_code"].isin(["1", "2"])
 & combined_min["age_5yr_code"].notna
 & (combined_min["age_5yr_code"]!= "99")
 & combined_min["cause_104"].notna
]

# 자살 (cause 102) 연도별
suicide = valid[valid["cause_104"] == "102"].groupby("year").size

KOSTAT_OFFICIAL = {
 "2010": 15566,
 "2011": 15906,
 "2015": 13513,
 "2019": 13799,
}

print(f"{'Year':6s} {'Ours':>10s} {'Official':>10s} {'Diff':>10s} {'%':>10s}")
for y, off in KOSTAT_OFFICIAL.items:
 ours = int(suicide.get(y, 0))
 diff = ours - off
 pct = 100 * diff / off
 print(f"{y:6s} {ours:>10,} {off:>10,} {diff:>+10,} {pct:>+9.4f}%")
```

### Expected:
```
Year Ours Official Diff %
2010 15,566 15,566 0 +0.0000% (또는 ±0.06% 이내)
2011 15,906 15,906 0 +0.0000%
2015 13,513 13,513 0 +0.0000%
2019 13,799 13,799 0 +0.0000%
```

### PASS 기준
- 4개 연도 모두 |%| ≤ 0.5%

### FL 시
- 1% 초과면 cause 매핑 또는 sigungu 매핑 오류 가능. 즉시 보고.

---

## 검증 4: 한국 공식 통계 cross-check (cancer + 전체 사망)

KOSIS 공식 사망원인통계와 비교. KOSIS 사이트 (kosis.kr) 에서 "사망원인별 사망자수, 사망률" 검색하면 공식 숫자 확인 가능.

```python
# 연도별 cancer + total
cancer_yearly = panel[panel["outcome_group"] == "cancer"].groupby("year")["deaths"].sum
total_yearly = panel.groupby("year")["deaths"].sum

print(f"{'Year':6s} {'Cancer':>10s} {'Total':>10s}")
for y in ["1997", "2000", "2005", "2010", "2015", "2020", "2023"]:
 c = int(cancer_yearly.get(y, 0))
 t = int(total_yearly.get(y, 0))
 print(f"{y:6s} {c:>10,} {t:>10,}")
```

### Expected vs 공식:
```
Year Panel Cancer 공식 Cancer Panel Total 공식 Total
1997 53,758 ~50,000 244,579 ~243,000
2000 59,175 ~57,000 248,720 ~247,000
2005 66,273 ~65,000 245,865 ~244,000
2010 73,146 ~72,000 255,335 ~255,000
2015 78,280 ~77,000 275,854 ~275,000
2020 83,771 ~82,000 304,921 ~305,000
2023 65,497 ~88,000(?) 262,683 ~352,000(?)
```

### PASS 기준
- 1997-2020 까지 ±2% 이내
- **2023 은 deviation 클 수 있음** — KOSTAT B형 microdata 가 partial release 가능. 별도 점검.

### 2023 partial release 확인
```python
# 2023 의 raw record 수가 다른 연도와 비슷한지 확인
yearly_n = combined_min.groupby("year").size
print(yearly_n.tail(5))
```

만약 2023 의 record 수가 2022 보다 50% 이상 적으면 partial release 확정. paper Section 3 limitation 명시.

---

## 검증 5: 0 cell 분포

```python
# 전체 0 cell 비율
n_zero = (panel["deaths"] == 0).sum
print(f"전체 0-cell: {n_zero:,} / {len(panel):,} = {100*n_zero/len(panel):.2f}%")

# Outcome group 별 0 cell 비율
print(f"\nOutcome group 별 0-cell:")
for g in sorted(panel["outcome_group"].unique):
 sub = panel[panel["outcome_group"] == g]
 zg = (sub["deaths"] == 0).sum
 print(f" {g:20s} {int(zg):>8,} / {len(sub):>8,} = {100*zg/len(sub):.2f}%")

# 시군구 크기별 0 cell 비율 (작은 군에서 더 많아야 정상)
sigungu_total = panel.groupby("h_code")["deaths"].sum.sort_values
print(f"\n시군구별 deaths 합 (작은 5개):")
print(sigungu_total.head)
print(f"\n시군구별 deaths 합 (큰 5개):")
print(sigungu_total.tail)
```

### Expected:
```
전체 0-cell: 약 638,863 / 1,483,920 = 약 43.05%

Outcome group 별:
 cancer 약 36-37%
 cardiovascular 약 43%
 despair_total 약 43-44%
 external_other 약 41%
 other 약 33%
 respiratory 약 60% ← 가장 높음 (작은 군 + 청년 layer)

작은 시군구 (예: 울릉군, 영양군, 봉화군) 이 작은 합 → 0 cell 더 많음
큰 시군구 (서울 강남, 수원, 고양) 가 큰 합 → 0 cell 적음
```

### PASS 기준
- 전체 0-cell 비율 35-50%
- respiratory > cardiovascular > cancer 순서 (점진적 증가)
- 작은 시군구 → 큰 시군구 monotonic

### Sparse 우려 신호
- 60% 초과면 sample restriction (인구 5만+) robustness 필요

---

## 검증 6: 시군구 spot check (구체적 5개 시군구)

```python
# 6개 시군구 sample (광역시 자치구 + 일반시 + 농촌 군)
SAMPLE_CHECK = {
 "11680": "서울 강남구 (대도시 부유)",
 "31100": "고양시 (분구 통합 결과)",
 "38110": "통합창원시 (자치구 5개 통합)",
 "33010": "통합청주시 (자치구 4개 통합)",
 "37430": "울릉군 (작은 군)",
 "32070": "영양군 (작은 군 추정)",
}

for h_code, name in SAMPLE_CHECK.items:
 sub = panel[panel["h_code"] == h_code]
 if len(sub) == 0:
 print(f"{h_code} ({name}): NOT FOUND ⚠️")
 continue
 despair = sub[sub["outcome_group"] == "despair_total"]["deaths"].sum
 total = sub["deaths"].sum
 n_years = sub["year"].nunique
 h_name = sub["h_name"].iloc[0]
 print(f"{h_code} ({h_name}, {name})")
 print(f" 연도수: {n_years}, 27년 합 deaths: {int(total):,}, despair: {int(despair):,}")
```

### Expected (대략):
```
11680 (강남구): 27년 deaths 약 50,000, despair 약 4,000
31100 (고양시): 27년 deaths 약 50,000-60,000, despair 약 4,500
38110 (창원시): 27년 deaths 약 80,000-100,000, despair 약 7,000
33010 (청주시): 27년 deaths 약 70,000-90,000, despair 약 6,000
울릉군: 27년 deaths 약 1,500-2,500, despair 약 100-200 (작은 군)
영양군: 27년 deaths 약 2,500-4,000 (작은 군)
```

### PASS 기준
- 6개 시군구 모두 FOUND (NaN 없음)
- 27년 = 27 (모든 시군구가 모든 연도 cover)
- 시군구 size 와 deaths 합 monotonic (큰 도시 > 작은 군)

### FL 시
- 어느 시군구가 NOT FOUND 면 sigungu_crosswalk_v2 에 매핑 누락. crosswalk 다시 검토.
- 27년 미만이면 panel skeleton 의 unbalanced. 즉시 보고.

---

## 검증 7: Crosswalk_v2 자치구 collapse 확인

```python
xw = pd.read_csv("1_codebooks/sigungu_crosswalk_v2.csv", dtype=str)
print(f"Crosswalk shape: {xw.shape}")
print(f"Distinct h_codes: {xw['h_code'].nunique}") # 229 기대

# 고양시 자치구 collapse 확인
goyang_codes = ["31100", "31101", "31103", "31104"]
sample = xw[xw["raw_code"].isin(goyang_codes)][["year", "raw_code", "h_code", "h_name"]]
print(f"\n고양시 자치구 collapse:")
print(sample.sort_values(["raw_code", "year"]).head(20))
# 기대: 31100, 31101, 31103, 31104 모두 같은 h_code (예: 31100, 고양시)

# 통합창원시 자치구 collapse 확인
changwon_codes = ["38110", "38111", "38112", "38113", "38114", "38115"]
sample2 = xw[xw["raw_code"].isin(changwon_codes)][["year", "raw_code", "h_code", "h_name"]]
print(f"\n통합창원시 자치구 collapse:")
print(sample2.sort_values(["raw_code", "year"]).head(20))

# 광역시 자치구 (서울 강남) 변화 없음 확인
gangnam = xw[xw["raw_code"] == "11680"][["year", "raw_code", "h_code", "h_name"]]
print(f"\n서울 강남구 (광역시 자치구, 변화 없어야 함):")
print(gangnam.head(5))
# 기대: h_code = 11680, h_name = "강남구"
```

### PASS 기준
- 고양시 4개 codes 모두 같은 h_code
- 창원 자치구 codes 모두 같은 h_code (38110)
- 강남구는 11680 그대로 유지

### FL 시
- 일반시 자치구가 다른 h_code 면 collapse 실패. 즉시 보고.
- 광역시 자치구가 collapse 됐으면 logic 오류. 즉시 보고.

---

## 검증 8: Mortality_104_classification 코드북

```python
cb = pd.read_csv("1_codebooks/mortality_104_classification.csv")
print(f"Shape: {cb.shape}") # 104 rows
print(cb.head)
print(cb.columns.tolist)

# 본 paper 핵심 코드 확인
KEY_CODES = {
 102: "자살",
 101: "유독성 물질에 의한 불의의 중독 및 노출",
 57: "정신활성물질 사용에 의한 정신 및 행동장애",
 81: "간 질환",
 67: "고혈압성 질환",
 68: "허혈성 심장질환",
 69: "기타 심장질환",
 70: "뇌혈관질환",
}

# cb 의 cause_104 column 형식 확인 (정수인지 string 인지)
print(f"\ncause_104 dtype: {cb['cause_104'].dtype}")
print(f"Sample values: {cb['cause_104'].head.tolist}")

# 핵심 코드 8개 확인
for code, expected_kr_label in KEY_CODES.items:
 row = cb[cb["cause_104"] == code]
 if len(row) == 0:
 print(f" {code:3d} NOT FOUND ⚠️")
 else:
 kr = row["label_kr"].iloc[0] if "label_kr" in row.columns else row.iloc[0]
 print(f" {code:3d}: {kr}")
```

### PASS 기준
- 104 rows
- 8개 핵심 코드 모두 found
- label_kr 이 expected 와 의미 일치 (정확 일치 아니라 약간 다른 표현 OK, 예: "자살" vs "고의적 자해")

### FL 시
- 핵심 코드 한 개라도 missing 또는 label 다르면 코드북 출처 확인. 즉시 보고.

---

## 검증 9: Validation.md 보고서 직접 읽기

```python
with open("3_derived/mortality/mortality_panel_validation.md", encoding="utf-8") as f:
 content = f.read

print(content[:3000]) # 첫 3000자
print
print("---" * 20)
print(content[-3000:]) # 마지막 3000자
```

### 확인할 부분
- "Overall: ALL PASS" 또는 "FL — DO NOT ADOPT"
- per-year 표의 27년 합산:
 - n_in 합 = 7,209,019
 - foreign 합 = 0
 - unmapped(dom) 합 = 0
 - sex_drop 합 = 작은 숫자 (수십~수백)
 - age_drop (=age=99) 합 = 949
 - cause_drop 합 = 작은 숫자 (수십)
 - n_valid 합 = 7,208,069
 - suicide(102) 합 = 약 350,000-400,000

### 직접 합산 검증 (텍스트에서 표 추출 + 합)
```python
# 보고서 안에서 per-year 표 찾아서 직접 합산
# Markdown 표 형식이라 visual 검토가 가장 빠름
```

---

## 검증 10: Combined microdata 의 raw_code 와 h_code 매칭

```python
sample = pd.read_parquet(
 "3_derived/mortality/mortality_microdata_combined.parquet",
 columns=["year", "raw_code", "h_code", "h_name"]
).head(1000000) # 첫 100만 row 만 sample

# raw_code → h_code 매핑이 일관적인지 (같은 raw_code+year 에 다른 h_code 가 매핑되면 안 됨)
mapping_check = sample.dropna(subset=["h_code"]).groupby(["year", "raw_code"])["h_code"].nunique
multi = mapping_check[mapping_check > 1]
print(f"Inconsistent mappings: {len(multi)}")
if len(multi) > 0:
 print(multi.head(20))

# 자치구 collapse 작동 확인 — raw_code 31101 (덕양구) 의 h_code 가 31100 인지
sub = sample[sample["raw_code"] == "31101"].head(5)
print(sub)
# 기대: h_code = 31100, h_name = "고양시"
```

### PASS 기준
- Inconsistent mappings = 0
- 자치구 raw_code → parent h_code (예: 31101 → 31100) 정확히

---

## 종합 체크리스트 — 본인이 직접 확인 후 표시

| # | 검증 | 결과 (○/×) |
|---|------|---|
| 1 | Panel shape (1,483,920 × 7) | |
| 2 | Outcome group 합 (TOTAL = 7,208,069) | |
| 3 | KOSTAT 자살 cross-check (4/4 ±0.5%) | |
| 4 | Cancer + total 시계열 (1997-2020 ±2%) | |
| 4b | 2023 partial release 여부 | |
| 5 | 0 cell 비율 (35-50% 범위) | |
| 6 | 6개 시군구 spot check (FOUND + 27년) | |
| 7 | Crosswalk 자치구 collapse (고양/창원) | |
| 8 | Classification 8개 핵심 코드 found | |
| 9 | Validation.md "ALL PASS" + 합산 일치 | |
| 10 | Combined microdata 매핑 일관성 | |

10개 모두 ○ 면 Stage 2 채택 OK. 한 개라도 × 면 보고 부탁.

각 단계 결과를 알려주시면 그에 따라 다음 step (Stage 3 prompt 작성 또는 Stage 2 재시도) 결정합니다.
