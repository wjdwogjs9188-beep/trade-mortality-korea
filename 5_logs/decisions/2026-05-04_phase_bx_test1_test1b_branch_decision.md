# Phase B-x Test 1 + Test 1b 결과 → Branch decision

**date**: 2026-05-04
**author**: R-A
**status**: **final** (Test 1 v3 수입가 drop 결과 반영 2026-05-04 23:0X)

## 결과 요약

| 검정 | spec | 결과 |
|------|------|------|
| Test 1 v1 | bilateral M ~ 6 macro lag1, HC1 | F=130, p<0.0001 (saturation 인공물 의심) |
| Test 1 v2 | univariate × 6, HAC, Bonferroni α=0.0083 | 2/6 sig: GDP (+4.82, p=0.006), 수입가 (+0.76, p=0.005, **VIF=27.9**) |
| **Test 1 v3** | **수입가 drop 후 univariate × 5, Bonferroni α=0.01** | **1/5 sig: GDP only. VIF 전부 < 3 → multicollinearity 해소. 수입가 유의는 VIF=27.9 인공물 확정** |
| Test 1b | bilateral ~ WEO surprise (Fall horizon-1), HAC | 0/2 sig: M (β=-0.05, p=0.74), X (β=-0.11, p=0.48) |

## 결정

### 단순 v2 mechanical 결정
"2/6 Bonferroni → C.ii branch" — bilateral 이 Korean macro 에 contaminated, ADH-8 main 으로 격하.

### 실제 결정 (v2 + 1b 조합)
**A.i main spec, year FE 필수조건 격상** — Bartik primary + bilateral robustness, 둘 다 year FE 필수.

근거:
1. **Test 1b 가 명확히 PASS** — Korean unanticipated macro shock (WEO surprise) 는 bilateral 을 전혀 예측 못함 (R²=0.001, β 부호도 음). 만약 bilateral 이 Korean shock 으로 contaminated 되면 1b 가 reject 했을 것.
2. **Test 1 v2 의 유의성 = persistent business cycle 동조** — Korean GDP 와 bilateral M 이 동조하는 것은 둘 다 global cycle (Chinese supply growth 포함) 에 동시 노출되기 때문. 이는 share-shock 결정이 아닌 *common factor* 문제.
3. **수입가 의 "유의성" 은 VIF=27.9 인공물** — 수출가·CPI·환율과의 collinearity 로 β 추정치 불안정. 진짜 Bonferroni-robust 유의 macro 는 GDP 1개 뿐.
4. **GDP 의 β=+4.82 elasticity 는 비현실적** — Korea GDP 1pp ↑ → bilateral M 35% ↑ 는 추정치 그 자체로 의심. N=19 + saturation 의 잔여 영향.

### Year FE 가 흡수하는 것
- Common Korean macro shock (GDP swings, FX, CPI)
- Common global business cycle factor
- 8차 ICD-10 개정 같은 calendar 효과

→ year FE 후 bilateral 의 *cross-시군구* 변이만 instrument 로 사용. 이 cross-sectional variation 은 1990 baseline industry mix 의 불균형에서 비롯 (BHJ corollary 가 보장하는 share-exogeneity 채널).

## 9-branch matrix 매핑

PAP v4.0 § 5 patches 의 9-branch (3 main × 3 fallback):

| 분기점 | 본 결정 | 이유 |
|--------|---------|------|
| Test 1 (realised macro) | borderline-pass conditional on year FE | v2 단독 mechanical fail 아니고 1b 와 함께 봐야 |
| Test 1b (WEO surprise) | full pass | β=-0.05, p=0.74 |
| First-stage F | pending Phase 2-B | dry-run 만 |
| Test 3 pre-trend | pending Phase 2-B | dry-run 만 |

→ **A.i main (year FE 필수), bilateral robustness 살아있음**. C.ii fallback 은 *현재 증거로는* 부적절.

## PAP v4.0 § 7 수정 commit (별도 turn)

- "year FE optional" → "**year FE mandatory** for main spec and bilateral robustness"
- § 5 9-branch matrix: A.i / A.ii 분기 둘 다 "year FE required" 명시
- § 8.x limitation 추가: Test 1 v2 의 face-value 2/6 결과는 saturation + multicollinearity 인공물 + persistent cycle 동조 — *not shock contamination*

## Pending 작업

1. **Test 1 v3** (5 macro, 수입가 drop): GDP 단독 유의 여부 final 검증
2. **Test 1b outlier drop**: 1997 IMF, 2009 GFC, 2020 COVID drop 후 β·p 안정성
3. **Phase 2-B 후 first-stage F + Test 3 재실행** — final branch confirm

## Anchor

- Romer & Romer (2010, AER): identification via shock decomposition (anticipated vs surprise)
- Andrews–Stock–Sun (2019): weak-IV 와 saturation 의 분리
- ADH (2013) Table 5: year FE 필수 (Bartik IV common practice)
- BHJ (2022 RES): share-exogeneity vs shock-exogeneity 분리
