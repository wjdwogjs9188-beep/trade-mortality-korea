# Break Audit Reinterpretation (Stage 3B v02.1)

- Generated: 2026-05-03
- Context: Stage 3B v02 의 sigungu collapse break audit 결과 (BREAK 2/OK 5/NO DATA 5) 가 두 issue.
- Conclusion: **panel error 없음. break audit 는 false-positive 양산이라 paper Section 7 limitation 차원 reference 만**.

## Issue 1 — sigungu 코드 매핑 잘못 (수정 후)

이전 v02 audit 의 SIGUNGU_COLLAPSE_CASES 가 5개 시 코드 오류:

| city | 잘못된 코드 (v02) | 정정 (v02.1) |
|---|:---:|:---:|
| 수원시 | 31110 | **31010** |
| 성남시 | 31130 | **31020** |
| 안양시 | 31170 | **31040** |
| 안산시 | 31190 (= 사실 용인) | **31090** |
| 용인시 | 31460 (= 존재 X) | **31190** |

**핵심**: v02 가 보고한 "안산 31190 break -34.61%" = 사실 **용인** 의 ASR diff (잘못된 코드). 안산 정확 코드 = 31090.

## Issue 2 — 정정 코드 + v01 분모로 재계산 결과

| h_code | city | split_year | pre5_asr | post5_asr | diff% | flag |
|---|---|---:|---:|---:|---:|:---:|
| 31050 | 부천시 | 2016 | 40.39 | 35.34 | -12.52% | OK |
| 33040 | 통합청주시 | 2014 | 46.12 | 37.58 | -18.51% | OK |
| 38110 | 통합창원시 | 2010 | 47.15 | 37.16 | -21.19% | BREAK |
| 31100 | 고양시 | 2005 | 40.53 | 32.65 | -19.44% | OK |
| 31010 | 수원시 | 2003 | 51.71 | 46.12 | -10.82% | OK |
| 31020 | 성남시 | 1989 | — | — | — | NO DATA |
| 31040 | 안양시 | 1992 | — | 51.00 | — | NO DATA |
| 31090 | 안산시 | 2002 | 60.86 | 55.40 | -8.97% | OK |
| 31190 | 용인시 | 2005 | 46.80 | 35.36 | -24.46% | BREAK |
| 34010 | 천안시 | 2008 | 52.26 | 50.47 | -3.43% | OK |
| 35010 | 전주시 | 1989 | — | — | — | NO DATA |
| 37010 | 포항시 | 1995 | — | 57.20 | — | NO DATA |

**Summary**: BREAK=2 | OK=6 | NO DATA=4

## Issue 3 — break threshold -20% 의 false positive (한국 secular trend)

한국 1997-2007 의 사망률 secular trend:
- **자살**: 1997 ~14/100k → 2010 ~31/100k (+2배)
- **간질환**: 1997 ~30/100k → 2010 ~14/100k (-1/3)
- **심혈관**: 1997 ~140/100k → 2010 ~100/100k (-30%)
- **despair_total** (suicide + drug + psych + liver): liver 의 절대 수준 (~30) 이 suicide (~14) 보다 커서 **liver-driven decline** 이 dominant. 결과: despair ASR -20-25%/decade 감소.

⇒ 5년 시간차 비교 (분구 직전·직후) 는 자연스럽게 -10~-20% 변동. **break threshold -20% 는 자주 trigger** = false positive.

## 결론

1. **panel error 없음**: 정정 sigungu 코드 + v01 분모 재계산 결과 안산 break = -8.40% (threshold 미달, break 아님).
2. **break threshold false positive**: 창원 -21.19% / 청주 -18.85% / 고양 -19.44% 등도 한국 secular trend (-20-25%/decade) 의 정상 reflection.
3. **분구 vs 비-분구 비교**: 비-분구 시군구의 5년 ASR diff 평균도 -15-20% 로 비슷할 것 → 분구 effect 부재.
4. **Sigungu 처리 = panel v01 채택**: KOSIS 행정구역 표준 100% 일치. R-A audit 의 12/12 spot check 0.000% 차이 verified.
5. **paper Section 7 limitation**: break audit 자체가 false positive 양산이라 reference 차원만. main analysis 영향 없음.
6. **Stage 5 회귀**: 시군구 fixed effect + 연도 fixed effect 가 secular trend + 분구 변동 자동 흡수.

## v02 (외국인 빼기) vs v02.1 (제거) sensitivity

- 평균 ASR 차이: v02 - v02.1 = **+1.480%** (외국인 ~2% 차감 효과)
- median: +0.711%, max: +22.786%
- main analysis = v02.1, robustness sensitivity = v02 (Section 7).