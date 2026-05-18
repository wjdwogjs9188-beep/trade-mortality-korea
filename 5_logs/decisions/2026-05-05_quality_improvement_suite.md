# Quality improvement suite — A + B + C + D
_2026-05-05_

# Option A — AKM v4 canonical BHJ 2022 weights

Canonical formula: Y_k = Σ_r s_{r,k} y_r where s_{r,k} = within-region share
(NOT v3 의 industry-normalized weights)

## Region-level OLS (baseline)
- N = 222, β = -0.0685, t (HC1) = -2.12

- canonical S (within-region share): shape (222, 22)
- S column sum (across regions): [59.88911049  0.         19.27832483 24.06116957  5.3031223 ]...
- S row sum (across industries, should be ≤1): mean=1.000
- industries: 22 → 21 after drop zero-exposure

## Canonical BHJ ssaggregate (WLS, weights = Σ_r s_{r,k})
- β = +0.8901, SE = 0.5913, t = +1.51
- N (industries) = 21

## Industry-level OLS (unweighted, comparison)
- β = +0.3231, t = +2.22


# Option B — Drop-C26 (전자) sensitivity

Q: 본 paper 의 result β=−0.069 가 C26 (전자, Rotemberg weight 80.7%) 단독 driven?

## Drop-C26 result (Bartik 재구성, 21 industries)
- N = 222
- β = -0.0756 (vs main β=−0.0685, drop -0.71pp)
- HC1 t = -2.26, p = 0.0240
- cluster-sido t = -3.24, p = 0.0012
- ✅ **β robust to dropping C26** — single-industry story 부정
- broader trade exposure 의 protective effect 확인

## Drop top-3 (C26 + C24 + C20)
- N = 222, β = -0.0713, t = -2.08


# Option C — Anderson-Rubin CI (weak-IV-robust inference)

AR test: weak-IV 하 valid inference (Anderson-Rubin 1949 + Andrews-Stock-Sun 2019)
주의: AR 은 IV interpretation 시 사용. Reduced-form 시 HC1 t-stat 그대로.

## IV setup
- N (IV panel) = 220
- First stage F (HC1) = 48.08
- Reduced form β (mortality on z_x) = -0.0664
- First stage π (employment on z_x) = +0.2919
- IV β (mortality on employment) = β_RF / π = -0.2275

## AR test of H0: β_IV = 0
- AR statistic = 3.31
- AR p-value = 0.0689
- ⚠️ AR borderline (p=0.069)

## AR confidence set (grid search, ±5 around point estimate)
- AR-CI 95%: [-0.497, +0.013]
- ⚠️ AR-CI includes 0 → cannot reject β_IV = 0 (weak inference)


# Option D — Suicide-only alternative outcome (cause 102 만)

Q: 본 paper 의 despair_total 결과가 suicide-only 에서도 같은 부호?

- ⚠️ Suicide-only 분리는 mortality_kostat microdata 직접 처리 필요 (panel 부재)
- 본 turn 에서는 panel 의 4 outcome × decomposition 만 가능
- Phase 5 별도 turn 에서 microdata-level suicide-only build 권장
- cancer: N=222, β=-0.0050, t=-0.19
- cardiovascular: N=222, β=-0.0129, t=-0.46
- respiratory: N=198, β=-0.0118, t=-0.27
- external_other: N=222, β=+0.0135, t=+0.29


# 종합 verdict

- saved: `4_results\regression\quality_improvement_suite.csv`
- log: `5_logs\decisions\2026-05-05_quality_improvement_suite.md`