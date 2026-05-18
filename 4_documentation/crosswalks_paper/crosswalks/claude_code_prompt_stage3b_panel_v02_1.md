# Claude Code Prompt — Stage 3B Panel v02.1 (외국인 빼기 제거)

## 작업 목적

Panel v02 의 외국인 빼기 부분만 제거하여 panel v02.1 build. 다른 모든 v02 기능 유지.

**배경**: R-A audit 가 외국인 빼기 (Tier A.2) 처방했는데, R-A 측 verify 결과 KOSIS DT_1B040M5 가 **사실상 한국인 only** (행안부 한국인 only 와 -0.35% 차이). 외국인 빼기 = over-correction. v02 의 외국인 빼기 부분만 제거.

또한 break audit 결과 재해석:
- panel v02 의 안산 31090 break = -8.40% (사실 break 없음). Claude Code 가 audit 시 "안산 31190 break -34.61%" 보고 = 사실 용인 (코드 매핑 잘못).
- 한국 1997-2007 secular trend (자살 ↑, 간 ↓, 의료 발전) 자체가 -30~-50% 라 -20% break threshold 가 false positive 양산.

## 입력 파일

```
3_derived/mortality/mortality_panel_v02.parquet              (v02, 정확)
3_derived/mortality/mortality_rate_panel_v02.parquet         (v02, 분모만 over-correction)
3_derived/population/population_panel_v01.parquet            (v01, 한국인 only)
```

## 산출물

```
3_derived/mortality/mortality_rate_panel_v02_1.parquet       # 분자 v02 + 분모 v01 재계산
3_derived/mortality/mortality_rate_panel_v02_1_validation.md
3_derived/mortality/break_audit_reinterpretation.md          # break false positive narrative
```

**그대로 유지 (재build 불필요)**:
- `mortality_panel_v02.parquet` (component decomposition 10 outcome) ✅
- `mortality_panel_v02_marriage/education/occupation.parquet` (mediator panel) ✅
- `population_panel_v01.parquet` (한국인 only, main 사용) ✅
- `population_panel_v02.parquet` + `foreign_panel_v02.parquet` 도 robustness sensitivity 차원 보존

## 작업 단계

### Step 1: ASR 재계산 (분모만 변경)

mortality_rate_panel_v02 의 분자 (component decomposition deaths) 와 weight (2010 한국 + WHO 2000 + Eurostat 2013) 그대로. 분모만 population_panel_v02 → population_panel_v01 변경 후 ASR 재계산:

```python
import pandas as pd
import numpy as np

# 분자 (Stage 3B 의 v02 panel 그대로)
mort = pd.read_parquet("3_derived/mortality/mortality_panel_v02.parquet")

# 분모 v01 (한국인 only)
pop = pd.read_parquet("3_derived/population/population_panel_v01.parquet")

# Join
panel = mort.merge(pop, on=["h_code", "year", "sex_code", "age_band"], how="left")

# rate per 100k
panel["rate_per_100k"] = panel["deaths"] / panel["population"] * 100_000

# Direct standardization (3 baseline)
# 2010 한국 baseline within-sex weight (Stage 3A logic)
# WHO 2000 + Eurostat 2013 도 동일 logic
# ...

# 산출
panel.to_parquet("3_derived/mortality/mortality_rate_panel_v02_1.parquet")
```

Stage 3A + 3B 의 ASR 계산 logic 그대로 재사용. 단지 분모만 변경.

### Step 2: V1-V14 재검증

V5 KOSIS 한국 총인구 cross-check, V6 ASR 시계열 한국 historical pattern, V7 join coverage, V9 standardization weight 등 모두 v01 분모 사용 시점에서 재검증.

### Step 3: Break audit 재해석 보고서

`break_audit_reinterpretation.md` 작성:

> "본 conversation 의 R-A audit 결과 (Stage 3B 의 break flag 12 cases, BREAK 2/OK 5/NO DATA 5) 가 두 issue:
> 1. **R-A audit 의 sigungu 코드 매핑 잘못** — '안산 31190 break -34.61%' = 사실 용인 (31190 = 용인). 안산 정확 코드 = 31090, 정확 break = -8.40% (threshold -20% 미달, break 없음).
> 2. **break threshold -20% 의 false positive** — 한국 1997-2007 의 secular trend (자살 +2배, 간질환 -1/3, 심혈관 -30%) 가 -20% threshold 자주 trigger. 분구 시군구 vs 비-분구 시군구 비교 시 break flag rate 가 비슷하면 분구 효과 부재.
>
> 정확 결과: 안산 break 없음 (-8.40%), 창원 -20.07% 도 한국 secular trend 의 정상 reflection 가능. 분구 효과 = 정확히 panel v01 의 hybrid sigungu merge 로 처리됨 (R-A audit 가 verify 한 12/12 spot check 0.000% 차이).
>
> **paper limitation 불필요**. break audit 자체는 false positive 양산이라 reference 차원만."

### Step 4: 산출 정리 + Validation report

```
mortality_rate_panel_v02_1.parquet  # main analysis 사용
break_audit_reinterpretation.md     # paper Section 7 limitation 차원
mortality_rate_panel_v02_1_validation.md  # V1-V14 재검증
```

## Expected 결과

- mortality_rate_panel_v02.1.parquet ≈ 123,660 rows (229 × 27 × 2 × 10 outcome × 1 baseline = 123,660; 3 baseline column)
- V5 한국 총인구 cross-check: panel v01 = 한국인 only (행안부 -0.35%) 결과 그대로
- V6 ASR 시계열: 한국 historical pattern 일치
- V7 join coverage 100%
- V9 standardization weight Σ=1 per sex
- **모든 V1-V14 PASS**

## 결과 검토

다음 4 가지 본인 검증:
1. mortality_rate_panel_v02.1 의 분모 = v01 (한국인 only, 행안부 -0.35%)
2. mortality_rate_panel_v02 (외국인 빼기) vs v02.1 (외국인 빼기 제거) ASR 차이 — 차이가 ~5% 면 외국인 효과 (paper Section 7 robustness)
3. break audit 재해석 narrative paper limitation 차원만 (main analysis 영향 없음)
4. component decomposition + 3 baseline + mediator panel 모두 정확 사용 가능

위 4개 OK 면 panel v02.1 채택 + Stage 5 진입.

---

이 prompt 를 Claude Code 에 file path 로 전달:
`C:\Users\82103\Desktop\뉴 논문\crosswalks\claude_code_prompt_stage3b_panel_v02_1.md`
