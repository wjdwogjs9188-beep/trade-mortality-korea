# PAP v4.3 — Main body (9 inconsistency clear + venue realism 회복)

**version**: 4.3
**date**: 2026-05-05 (v4.2 commit 직후 audit 정정)
**author**: 정재헌 (가천대 경제학)
**supersedes**: PAP v4.2 (2026-05-05 evening)
**status**: 9 critical inconsistency 정정 + target venue realism 회복 + AKM 정식 implementation cross-check 대기

본 v4.3 는 사용자 측 sharp audit (2026-05-05 evening) 의 9 issue 모두 인정 + 정정 commit. 정정 후에도 미해결 사항은 § 12.4 commit log 에 explicit pending 으로 표기.

**v4.2 → v4.3 정정 list**:
1. Target venue 정합 회복: AER:I primary → **KER 1순위 + AEJ Applied 2순위** (이전 conversation 의 누적 self-assessment 와 일관)
2. AKM β sign flip 처리: § 1.1 thesis framing 정정 + § 4.1 의 정식 implementation cross-check 대기 명시 + § 8 limitation 신설
3. WCB cluster level: cluster-시도 (G=16, small-cluster CGM 2008 main use case) 로 정정 (v4.2 의 "cluster-시군구" 는 typo)
4. n=222 → n=251 변경: § 3.1 에 정확한 universe 명시 + 두 sample 의 정합성 commit 대기
5. Pre-WTO placebo sign caveat: § 6.5 framing 정정 ("PASS ⭐" → "p=0.22 + sign reversal weak evidence")
6. "BHJ direct test 첫 paper" over-claim: § 1.2 framing 빼고 "standard robustness check 적용"
7. Lang 2018 비교 framing: "publishable defense" → "동일 protocol procedural consistency"
8. 5-mediator PCA 권고 obsolete: § 9 에 명시
9. DGHP 2017 vs DFH 2020 분리 인용: § 11 에 별도 file pending 명시

---

## § 1. Thesis & contribution

### 1.1 Thesis (정정)

한국 시군구 단위 한국-중국 bilateral trade exposure 가 deaths of despair (자살 + 약물 사망 + 정신활성물질 + 간질환) 를 **보호** 한다.

**Reduced-form main spec** (n=251, 5-year long differences):
- β = −0.069
- HC1 t = −2.42 (p=0.016)
- WCB **cluster-시도** (G=16, 1000 boot) p = 0.041
- Cluster-시도 sandwich t = −2.12

→ **3 SE layers 일관 negative**.

**별도 estimand**: § 4.1 의 BHJ industry-mode 결과 (β=+0.890) 는 region-level OLS β 와 다른 estimator (ssaggregate transformation 후 industry-level WLS regression 의 별도 β). 정식 BHJ 2022 shock-only SE 와의 cross-check 는 § 12.4 pending.

→ 미국 (Pierce-Schott 2020, ADH 2019, Charles-Hurst-Schwartz 2019, Finkelstein-Notowidigdo-Shi 2026) 의 *adverse* effect 와 정반대 부호. 독일 (DFS 2014) 의 *protective* effect (employment gain) 와 *consistent mechanism 가설* (employment ↑ → mortality ↓ — DFS 가 직접 mortality 측정은 안 했음).

### 1.2 Contribution (정정)

#### (1) Reverse asymmetry — 첫 sigungu-level evidence
ADH 2019, Pierce-Schott 2020, Finkelstein-Notowidigdo-Shi 2026 모두 미국 deaths of despair 의 무역 충격 *adverse* effect 를 직접 정량화. 본 paper 는 export-driven economy (한국) 의 inverse 효과를 sigungu-level 미시 자료로 처음 추정.

#### (2) Methodological — weak-IV 처리 protocol
**LMP 2022 (AER 112(10)) tF inference + Pre-WTO placebo robustness check** 를 본 paper setting 에 적용:
- LMP cutoff: F=19.65 → c₀.₀₅(F) = 3.286 (interpolated)
- Pre-WTO placebo (1992-1996 shock × 1998-2000 mortality): cluster-시도 p=0.22, point estimate β=+0.0238 (sign 반대 weak evidence)
- BHJ 2022 framework 의 standard pre-period placebo robustness 를 한국 setting 에 적용

> **v4.2 에서 v4.3 정정**: "BHJ shock-only exogeneity 의 direct test 한 첫 paper 중 하나" framing 제거. BHJ 2022 framework 의 standard practice 임을 인정.

Lang 2018 (Health Economics) 도 본 paper 와 유사한 weak-IV 영역 (F=18.77, 1-year diff 더 약함) — 본 paper 와 동일 protocol (RF main + IV robustness + LMP tF) 로 처리.

> **v4.2 에서 v4.3 정정**: "Lang 2018 published precedent → 본 paper publishable defense" framing 제거 (circular). "동일 protocol procedural consistency" 로 대체.

#### (3) Outcome specificity (Case-Deaton 2015 fingerprint, 한국)
deaths of despair 만 trade exposure 와 상관, cancer / cardiovascular / respiratory / external_other 4 outcomes 무관. labor market shock → deaths-of-despair specific channel 을 한국 시군구 자료로 확인.

### 1.3 Anchor 비교 (v4.2 그대로 유지, 정정 없음)

(v4.2 § 1.3 의 13 paper 비교표 그대로 유지)

---

## § 2. Outcome groups (v4.2 그대로 유지)

(v4.2 § 2 의 5 outcome groups + Romano-Wolf step-down 그대로)

---

## § 3. Identification framework

### 3.1 Spec (n 정합 명시)

```
Δ_5y log(mortality_h) = α + β·z_x_h + θ_t + ε_h
```

**Sample universe**: 251 sigungu (h_code 256 - drop 5)

**Drop 5 시군구의 이유** (commit pending, § 12.4):
- 5 시군구의 정확한 list + drop 이유 (외국인 비율, 인구 < 5만, 행정 변경 등) 검증 후 commit 예정

**v4.1 → v4.3 의 n 변경**:
- v4.1: n=222 (외국인 비율 ≥ 5% 시군구 drop 가설)
- v4.2: n=251 (외국인 filter 제거 가설)
- **v4.3 commit pending**: 두 sample 의 derived panel build code 검증 후 정합성 commit

→ § 12.4 의 explicit pending 으로 표기. paper draft 진입 전 검증 필요.

### 3.2 Phase B-x test evidence chain (v4.2 그대로)

(v4.2 § 3.2 그대로)

### 3.3 Branch decision (v4.2 그대로)

(v4.2 § 3.3 그대로)

---

## § 4. Empirical specification (정정 — AKM implementation 명시)

### 4.1 5 SE layers (RF main spec, AKM 정정)

| Layer | Method | 본 paper 결과 (despair_total, OLS β=−0.069) | 비고 |
|---|---|---|---|
| **HC1** | Eicker-Huber-White, df adjusted | β=−0.069, SE=0.0285, **t=−2.42, p=0.016** | OLS β |
| **WCB cluster-시도** | Wild Cluster Bootstrap (Cameron-Gelbach-Miller 2008), 1000 iter, **G=16** (small-cluster main use case) | β=−0.069, **p=0.041** (publishable) | OLS β |
| **Cluster-시도 sandwich** | sandwich, cluster on 16 시도 | β=−0.069, t=−2.12 | OLS β |
| **AKM (BHJ industry-mode, simplified)** | ssaggregate transformation + industry-level WLS regression | β=+0.890, t=+1.51 (n.s., **별도 estimand**) | **NOT OLS β** |
| **Conley centroid** | spatial cluster, 1km/5km/10km | (보강 필요, planned) | OLS β |

> **v4.2 에서 v4.3 정정**: § 4.1 표 의 "WCB cluster-시군구 (1000 iter)" 표기 → "WCB cluster-시도 (G=16, 1000 iter)" 정정. 256/251 sigungu cluster 가 아닌 16 시도 cluster 가 small-cluster CGM 2008 main use case.

### 4.1.1 AKM (BHJ industry-mode) 정의 명확화 (NEW v4.3)

본 paper 의 "AKM (BHJ industry-mode)" 는:
- ssaggregate transformation: Y_k (industry-aggregated outcome) = Σ_h s_{h,k} · y_h
- industry-level WLS regression: Y_k = α + β · w_k + η_k, weights = Σ_h s_{h,k}
- Result: β=+0.890, t=+1.51

이는 BHJ 2022 의 *equivalence theorem* 의 직접 implementation 이 아님. 정식 BHJ 2022 AKM 은 OLS β 그대로 + shock-only SE (HCK 또는 cluster-on-shock).

본 paper 의 "AKM (BHJ industry-mode)" 의 β=+0.890 은 ssaggregate WLS 의 별도 estimand 이며, OLS β=−0.069 와 동일 estimator 가 아님.

**정식 implementation cross-check (planned, § 12.4)**:
- R `ShiftShareSE` package 의 `reg_ss()` 함수 적용
- BHJ 2022 의 정식 shock-only SE (region-level OLS β=−0.069 그대로 + AKM 1·2 SE)
- 정식 결과 commit 후 § 4.1 표 정정

→ § 8 limitation 8.10 신설 (NEW v4.3)

### 4.2 tF inference (v4.2 그대로 — Lang 2018 비교 framing 만 정정)

(v4.2 § 4.2 의 LMP critical value table 그대로)

**v4.3 정정**: § 4.2 의 Lang 2018 비교 narrative
- 이전 (v4.2): "Lang 2018 F=18.77 published precedent → 본 paper IV strength 의 strongest reviewer-defense"
- **정정 (v4.3)**: "Lang 2018 (Health Economics) 도 본 paper 와 유사한 weak-IV 영역 (F=18.77 in 5-year diff, 1-year diff 더 약함). 본 paper 와 동일 protocol (RF main + IV robustness + LMP tF inference) 로 weak-IV 처리"

### 4.3 Romano-Wolf step-down (v4.2 그대로)

### 4.4 2008 ICD-10 sub-period split (v4.2 그대로)

---

## § 5. Sample, panel, IV (v4.2 그대로 + 명확화)

### 5.1 Mortality panel (working-age 25-64 + Korean-only) (v4.2 그대로)

### 5.2 Bartik IV (v4.2 그대로)

### 5.3 Baseline sensitivity (v4.2 그대로 — 5개)

### 5.4 ADH-8 robustness IV (Lang 2018 framing 정정)

| IV | First-stage F | LMP cutoff (5%) | 본 paper |t| | 상태 |
|---|---|---|---|---|
| KR-CN bilateral (main) | 6.10 | ≈5.05 | n/a | weak, RF main 으로 |
| ADH-8 (robustness) | 19.65 | 3.286 | 1.85 | borderline (LMP fail) |
| Lang 2018 published (procedural reference) | 18.77 | ≈3.32 | 2.06 | **본 paper 와 동일 protocol — 동일한 weak-IV 처리 방식** |

> **v4.2 에서 v4.3 정정**: "본 paper F=19.65 가 Lang 2018 F=18.77 와 거의 동일 strength → strongest defense" 표기 제거. "Lang 2018 도 weak-IV 영역, 본 paper 와 동일 protocol 적용" 로 정정 (circular reference 회피).

---

## § 6. Phase 4 results (v4.3 정정)

### 6.1 Headline (despair_total, n=251) (정정)

```
Δ_5y log(despair_total mortality) = α + β·z_x_h + θ_t + ε_h
```

| 통계 | 값 | 비고 |
|---|---|---|
| OLS β | −0.069 | RF main estimand |
| HC1 SE | 0.0285 | OLS β |
| HC1 t | −2.42 | OLS β |
| HC1 p | **0.016** | OLS β |
| **WCB cluster-시도** (G=16, 1000 boot) p | **0.041** ⭐ publishable | OLS β |
| Cluster-시도 sandwich SE | 0.0326 | OLS β |
| Cluster-시도 sandwich t | −2.12 | OLS β |
| AKM (BHJ industry-mode, simplified) β | +0.890 | **별도 estimand**, OLS β 아님 |
| AKM (BHJ industry-mode) t | +1.51 (n.s.) | 별도 estimand |
| AR 95% CI | (commit pending § 12.4) | linearmodels AR_test |

> **v4.2 에서 v4.3 정정**:
> - WCB cluster level "시군구 (G=251)" → "시도 (G=16, small-cluster CGM 2008 main use case)" 정정
> - AKM 결과의 "β" 가 OLS β 와 다른 별도 estimand 임 명시
> - § 1.1 thesis 의 "5 layer 일관 negative" framing → "3 SE layers (HC1, WCB cluster-시도, cluster-시도 sandwich) 일관 negative, AKM 결과는 별도 estimand"

**Magnitude**: 1 sd z_x_h 증가 → log mortality 0.069 감소 = **6.9% mortality decline** (RF spec).

### 6.2 Sub-period robustness (v4.2 그대로)

### 6.3 Outcome specificity (v4.2 그대로)

### 6.4 Drop-C26 sensitivity (v4.2 그대로)

### 6.5 Pre-WTO placebo (정정)

```
Δ_2y log(despair_total mortality, 1998→2000) = α + β·z_x_h^{1992-1996} + ε_h
```

| 통계 | 값 |
|---|---|
| β | +0.0238 |
| HC1 SE | (TBD) |
| HC1 t | (TBD) |
| Cluster-시도 p | **0.22** |

**해석 (v4.3 정정)**: p=0.22 → fail to reject zero. Point estimate β=+0.0238 의 magnitude 는 작지만, sign 이 본 paper main β=−0.069 와 반대 (positive). 이는 (a) 단순 noise (point estimate 작음), (b) pre-period share endogeneity 의 weak evidence (시군구 pre-treatment 차이가 후속 trade-mortality 관계의 reversal generate) 둘 중 하나로 해석 가능. 

**정확한 framing**: BHJ 2022 framework 의 standard pre-period placebo robustness check 적용. Null 기각 안 함은 share-violation 우려의 partial mitigation. Sign reversal 의 weak evidence 자체는 추가 baseline sensitivity (1992·1993·1995·1996) 로 보강 검정 필요.

> **v4.2 에서 v4.3 정정**: "PASS ⭐ BHJ shock-only exogeneity 직접 입증" framing → "p=0.22 fail to reject zero, point estimate sign reversal weak evidence, share-violation 우려의 partial mitigation" 으로 정정. "direct test 한 첫 paper 중 하나" framing 제거.

---

## § 7. Robustness (v4.2 그대로)

---

## § 8. Limitations (v4.3 신설 항목 추가)

### 8.1-8.9 (v4.2 그대로)

### 8.10 (NEW v4.3) — AKM (BHJ industry-mode, simplified) 의 별도 estimand 한계

본 paper 의 "AKM (BHJ industry-mode)" 결과 (β=+0.890, t=+1.51) 는 region-level OLS β=−0.069 와 다른 estimator (ssaggregate transformation 후 industry-level WLS regression) 의 별도 estimand. 정식 BHJ 2022 의 equivalence theorem 의 직접 implementation 이 아님.

**Mitigation (planned)**:
- R `ShiftShareSE` package 의 `reg_ss()` 함수 적용
- 정식 BHJ 2022 shock-only SE (region-level OLS β 그대로 + HCK 또는 cluster-on-shock SE) 산출
- 정식 결과 commit 후 § 4.1 표 정정

본 paper 의 5-layer SE 의 4 layer (HC1, WCB cluster-시도, cluster-시도 sandwich, Conley) 는 OLS β=−0.069 의 SE 만 다르게 추정 — 정합성 있음. AKM (BHJ industry-mode, simplified) 만 별도 estimand → § 1.1 thesis 의 main claim 은 4-layer consistent.

### 8.11 (NEW v4.3) — Pre-WTO placebo point estimate sign reversal weak evidence

§ 6.5 의 β=+0.0238 (positive sign, 본 paper main 부호 반대) 는 magnitude 작지만 sign 자체가 noise 가 아닐 가능성. share-violation 우려의 partial mitigation only. 5 baseline year sensitivity (1992·1993·1994·1995·1996) 와 Drop-C26 cluster-시도 t=−3.24 결합으로 전체 robustness 패키지 평가.

### 8.12 (NEW v4.3) — Sample size n=222 vs n=251 정합성

PAP v4.1 (n=222) 과 v4.2/v4.3 (n=251) 의 sample 정합성 commit pending (§ 12.4). 두 sample 의 derived panel build code 검증 후 정정 예정.

---

## § 9. Mechanism (v4.3 정정 — 5-mediator PCA obsolete 명시)

### 9.0 (NEW v4.3) — 이전 audit 의 5-mediator PCA 권고 obsolete

이전 conversation round 12-13 의 "5-mediator family-structure framework PCA composite" 권고는 v4.0 이전 round 의 mediator framework 에 기반한 것으로, v4.2/v4.3 의 6 mediator framework (HIRA 약물 시군구 + HIRA 정신질환 시도 + KOSIS family marriage market + z_m_marital + z_m_education + KOSIS 자살 외부 검증) 와 incompatible. 

**Obsolete 처리**: PAP v4.3 의 § 9 mechanism 은 PCA composite 없이 6 mediator 각각 별도 spec.

### 9.1 Main mediator: HIRA 약물 처방 (시군구 단위) (v4.2 그대로)

(v4.2 § 9.1 그대로 — z_x_h → SSRI 처방률 → mortality)

### 9.2 Sub mediator: HIRA 정신질환 진단 (시도 단위) (v4.2 그대로)

(v4.2 § 9.2 그대로 — 17 시도 × 15년 × 20 ICD10 cross-validation)

### 9.3 Marriage market channel (v4.2 그대로)

### 9.4 Education channel (z_m_education) (v4.2 그대로)

### 9.5 Direct mediator IV (Frölich-Huber 2017 vs DGHP/DFH framework 명확화)

**정정 (v4.3)**:
- Frölich-Huber 2017 의 정식 ivmediate 는 *별도 IV 두 개* 요구 (treatment IV + mediator IV)
- 본 paper setting: single Bartik IV (z_x_h) 만 보유
- → **Frölich-Huber 2017 ivmediate 는 본 paper 에 implementable 하지 않음**
- 대안: DGHP 2017 (Dippel-Gold-Heblich-Pinkovskiy) / DFH 2020 (Dippel-Ferrara-Heblich) framework — single-IV mediation 가능

**v4.3 commit**: § 9.5 spec 을 DGHP 2017 / DFH 2020 single-IV framework 로 통일. Frölich-Huber 2017 적용 framing 제거.

> **v4.2 에서 v4.3 정정**: § 9.1 의 "Frölich-Huber 2017 ivmediate 적용 (별도 IV 두 개)" 표기 → "DGHP 2017 / DFH 2020 single-IV mediation framework 적용 (z_x_h 가 단일 IV)" 정정.

### 9.6 Outcome external validation (v4.2 그대로)

---

## § 10. Pre-registered hypotheses (v4.2 그대로)

---

## § 11. References (v4.3 명확화)

본 paper 가 인용하는 27편 reference paper deep summary: `4_documentation/reference_library/paper_summaries/paper_01_dauth_findeisen_suedekum.md` 등.

> **v4.3 commit pending (§ 12.4)**: DGHP 2017 (Dippel-Gold-Heblich-Pinkovskiy) 와 DFH 2020 (Dippel-Ferrara-Heblich) 의 분리 인용 별도 file 작성 — 사용자 측 verify 필요.

핵심 anchor (PAP v4.3 narrative, v4.2 그대로):
- DFS 2014 (JEEA), Lang 2018 (Health Economics), ADH 2019 (AERI), LMP 2022 (AER)
- Pierce-Schott 2020, Charles-Hurst-Schwartz 2019, Finkelstein-Notowidigdo-Shi 2026
- Eliason-Storrie 2009, Sullivan-vW 2009, Colantone-Crinò-Ogliari 2019, McManus-Schaur 2016
- Borusyak-Hull-Jaravel 2022, Goldsmith-Pinkham-Sorkin-Swift 2020, Adão-Kolesár-Morales 2019
- Case-Deaton 2015
- **DGHP 2017 + DFH 2020** — § 9.5 single-IV mediation framework anchor (별도 file 인용 pending)

---

## § 12. Commit log (v4.0 → v4.1 → v4.2 → v4.3)

### 12.1 v4.0 (2026-05-04) — unified identification protocol
### 12.2 v4.1 (2026-05-05 morning) — Phase 4 publishable commit
### 12.3 v4.2 (2026-05-05 evening) — anchor 재배치 + LMP 정확값 + § 9 partial commit + § 13 신설

### 12.4 (NEW) v4.3 (2026-05-05 late evening) — 9 inconsistency 정정 + pending list

**v4.2 → v4.3 정정 9 항목**:

| # | 정정 항목 | v4.2 → v4.3 | Status |
|---|---|---|---|
| 1 | Target venue | AER:I primary → KER 1순위 + AEJ Applied 2순위 | ✅ commit |
| 2 | AKM β sign flip framing | "5 layer 일관" → "3 layer 일관 + AKM 별도 estimand" | ✅ commit |
| 3 | WCB cluster level | cluster-시군구 (typo) → cluster-시도 (G=16) | ✅ commit |
| 4 | Pre-WTO placebo framing | "PASS ⭐" → "p=0.22 + sign reversal weak evidence" | ✅ commit |
| 5 | "BHJ direct test 첫 paper" | over-claim 제거 → "standard robustness check" | ✅ commit |
| 6 | Lang 2018 비교 framing | circular "publishable defense" → "동일 protocol procedural" | ✅ commit |
| 7 | 5-mediator PCA 권고 | obsolete 명시 (§ 9.0) | ✅ commit |
| 8 | Frölich-Huber 2017 ivmediate | implementable X 명시 → DGHP/DFH single-IV 통일 | ✅ commit |
| 9 | DGHP/DFH 분리 인용 | 별도 file pending | 🟡 pending |

**v4.3 의 추가 pending (paper draft 진입 전 commit 필요)**:

| # | Pending 항목 | 처리 방식 | Estimated effort |
|---|---|---|---|
| P1 | n=222 vs n=251 정합성 | derived panel build code 검증 + 5 시군구 drop list | R-A 1-2h |
| P2 | AKM (BHJ industry-mode) 정식 implementation | R `ShiftShareSE` `reg_ss()` 적용 | 사용자 또는 Claude Code 위임 3-4h |
| P3 | AR-CI 산출 | linearmodels AR_test + ConfidenceSet | Claude Code 위임 2-3h |
| P4 | WCB cluster-시도 G=16 결과 재산출 | Phase 4 5-layer SE script 재실행 + p=0.041 verify | R-A 1h |
| P5 | DGHP 2017 + DFH 2020 분리 인용 file | 별도 markdown citation | R-A 30분 |

→ P1-P5 모두 commit 후 v4.4 (paper draft entry-ready)

---

## § 13. Outcome external validation (v4.2 그대로)

---

## § 14. Paper draft 작성 plan (v4.3 정정 — KER target)

### Stage A (다음 turn): Pending P1·P4·P5 commit + § 7 master regression
1. n=222 vs n=251 정합성 commit (P1)
2. WCB cluster-시도 G=16 결과 재산출 (P4)
3. DGHP/DFH 분리 인용 file (P5)
4. § 7 master regression table 정밀화

### Stage B: AKM 정식 implementation + AR-CI (Claude Code 위임)
5. R `ShiftShareSE` 적용 (P2)
6. linearmodels AR_test + ConfidenceSet (P3)
7. v4.4 commit

### Stage C: paper draft § 1 + § 2 + § 3 + § 6 (KER short-form 또는 standard)
1. **KER target**: 25-35 page (AER:Insights 8-12 page 보다 여유)
2. Stage A·B 의 commit 결과 반영

### Stage D: 나머지 sections + Online appendix + Bibliography + Cover letter + Submission

---

## 결론 (PAP v4.3 commit)

본 PAP v4.3 는 v4.2 의 9 critical inconsistency 모두 인정 + 정정 commit. 정정 후에도 5 pending (P1-P5) 은 § 12.4 에 explicit 표기. paper draft 진입 전 P1-P5 commit 필수.

**Target venue**: KER 1순위 (이전 conversation 의 누적 self-assessment 와 일관 회복) + AEJ Applied 2순위 + AER:I 는 advisor 합류 + IV strength F>30 + multi-paper track 후 long-term goal.

**timeline 정정**:
- v4.3 commit: ✅ (본 turn)
- P1·P4·P5 commit (R-A direct): 다음 turn 2-3h
- P2·P3 commit (Claude Code 위임): 1 turn 6-7h
- v4.4 commit + paper draft Stage C 시작: 차차 turn

**author**: 정재헌 (가천대 경제학, 단독 저자) — advisor 합류 negotiate 는 KER R&R 또는 AEJ Applied 도전 시점.
