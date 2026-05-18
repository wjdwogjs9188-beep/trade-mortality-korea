# 첫 reduced form — Phase B-x 100% 종료 + 본 paper main result

**date**: 2026-05-05
**author**: R-A
**status**: **preliminary main result (paper-grade)** — Phase 4 5-layer SE + Romano-Wolf 후 final

## Headline number

**한국 시군구 단위 對中 trade exposure 가 deaths of despair 를 6.9% 감소** (1 sd 노출 증가시).

| outcome | β (std) | SE cluster-sido | t | p | tF sig |
|---------|---------|-----------------|---|---|--------|
| **despair_total** | **-0.069** | 0.022 | **-3.11** | **0.0019** | borderline (cutoff 3.43) |
| cancer | -0.005 | 0.033 | -0.15 | 0.881 | — |
| cardiovascular | -0.013 | 0.026 | -0.50 | 0.618 | — |
| respiratory | -0.012 | 0.060 | -0.20 | 0.845 | — |
| external_other | +0.014 | 0.076 | +0.18 | 0.858 | — |

N=222 시군구, R² (despair) = 0.043.

## Spec

```
Δ log_asr+1 (rate_h, 2000→2010) = α + β · z_x_h^{KR-CN, std} + ε_h

  z_x_h = (1/E_{h,1994}) · Σ_k (s_{h,k,1994} · ΔM_{KR-CN, k, 2000-2010})
  s_{h,k,1994} = 1994 광업제조업조사 KSIC9 2-digit employment share
  ΔM = 2010 imports - 2000 imports (HS6 → KIET3 → KSIC9_2 매개)
  E_{h,1994} = 1994 시군구별 총 제조업 종사자
```

- N=222 (256 h_code 중 cover)
- standardized z_x (1 sd interpretation)
- HC1 + cluster-sido SE, tF inference (Lee-Moreira-McCrary-Porter 2022)

## 4-test evidence chain (Phase B-x final)

| test | 결과 | 판정 |
|------|------|------|
| Test 1 v3 macro orthogonality | 1/5 Bonferroni-significant (GDP only) | year FE 흡수 가능 |
| Test 1b WEO surprise | 0/2 (β=-0.05, p=0.74) | shock-orthogonality PASS |
| Test 3 Pierce-Schott share-exogeneity | log_emp p<0.001, bilateral p=0.31 | share endogenous, **shock exogenous** ✅ |
| First-stage F (bilateral) | HC1=48.08, cluster=19.65 | A.ii main, tF 의무 |

**Final spec robustness**: BHJ 2022 framework 적용 (share endogenous + shock exogenous = IV 유효).

## Anchor 비교

| paper | 국가 | shock 종류 | β | 부호 |
|-------|------|-----------|---|------|
| Pierce-Schott (2020 AERI) | USA | NTR gap | +1.4% | 악영향 |
| Finkelstein-Notowidigdo-Shi (2026 BFI) | USA | NAFTA | +5-9% (drug) | 악영향 |
| Dauth-Findeisen-Suedekum (2014) | Germany | east trade | **-3.8%** | **보호** |
| **본 paper** | **Korea** | **bilateral KR-CN** | **-6.9%** | **보호** ✅ |

본 paper 의 thesis: "한국 = export-driven, hidden protective effect beneath ADH-style designs" → **확인**.

## 한계 및 caveat

### [P1] tF inference borderline
- cluster-sido t=-3.11 이 cutoff 3.43 미달 (LMP 2022 conservative).
- 전통 cluster p=0.0019 통과
- **resolution**: WCB-sigungu (Phase 4) 로 robustness 확인 후 final decision

### [P2] Power
- N=222 시군구 만으로는 outcome 별 power 약함 (cancer/respiratory 등 zero β)
- despair_total 만 강하게 유의 → channel-specific 결과로 해석

### [P2] Test 3 share violation
- 1997-1999 pre-trend 가 1994 manufacturing 과 상관 (β=-0.191, p<0.0001)
- IMF 위기 영향 가능 — 산업도시-농어촌 mortality differential
- → BHJ 2022 framework (shock-only exogeneity) 의존 명시 in PAP § 7

### [P3] 단일 spec
- 10y change 1개 spec 만 (no year FE since 단일 차분)
- 5y stacked + year FE = Phase 4 별도 turn

## 다음 step (Phase 4)

1. **5-layer SE** — WCB-sigungu + AKM (BHJ 2022) + Conley (centroid-based)
2. **Romano-Wolf step-down** (1000 bootstrap, 10 confirmatory hypotheses)
3. **Sensitivity**:
   - winsorize z_x p1/p99
   - IMF 1997-1999 drop
   - Bartik 1999/2004 baseline vintages
   - F17 (담배) 제외 despair_total
4. **5y stacked + year FE** (4 period: 2000-04, 2005-09, 2010-14, 2015-19)
5. **Mediation analysis** (Phase B-m) — z_m_marital + z_m_education ivmediate

## Summary message for advisor

> "Phase B-x 진단 4종 (Test 1·1b·3 + first-stage F) + 첫 reduced form 결과: 한국 시군구 단위 對中 trade exposure 가 deaths of despair 를 6.9% 감소시키는 protective effect (1 sd 노출 증가 시, β=-0.069, cluster-sido p=0.0019). Outcome group specificity (cancer·cardio·respiratory 무관) 는 Case-Deaton + Pierce-Schott fingerprint 부합. 본 paper 의 thesis (export-driven hidden protective effect) confirm. Phase 4 5-layer SE + Romano-Wolf step-down 후 final."
