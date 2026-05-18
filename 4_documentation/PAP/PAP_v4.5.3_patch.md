# PAP v4.5.3 — Patch (DGHP A-2 + Finkelstein deaths of despair + Track 2·3 코드)

**version**: 4.5.3 (patch on v4.5.2)
**date**: 2026-05-05
**author**: 정재헌 (가천대학교 경제학)
**supersedes**: v4.5.2 의 § 1.3 (Finkelstein) + § 9.5 (DGHP framework)

본 patch 는 R-A direct deep inspect 결과 commit:
1. DGHP 2017 Section 2-3 의 Assumption A-2 정확 spec
2. Finkelstein 2026 deaths of despair Figure 5 의 sub-category 분리
3. Track 2·3 코드 작성 완료 (사용자 PC 실행 대기)

---

## 1. § 9.5 — DGHP 2017 Assumption A-2 정확 spec

본문 직접 verify (NBER WP 23209 Section 2):

> **Assumption A-2**: The following independence relations hold in the mediation model (1)–(3):
> 
> ```
> T ⊥/⊥ M (T 와 M error terms 상관 — T endogenous)
> M ⊥/⊥ Y (M 과 Y error terms 상관 — M endogenous)
> T ⊥/⊥ Y | M (T 와 Y error terms 가 M 에 conditional 시 상관)
> T ⊥⊥ Y (T 와 Y error terms 는 unconditional 독립)
> ```
> 
> "Assumption A-2 states that error terms T, Y are unconditionally independent, but correlate conditional on M."

**Lemma L-2 의 새 exclusion restriction**:
> Z ⊥⊥ M | T (Z 가 T 에 conditional 시 M 에 외생)
> Z ⊥⊥ Y(m) | T (Z 가 T 에 conditional 시 counterfactual Y(m) 에 외생)

**Substantive 의미**:
- T 와 Y 의 unconditional 독립 = "M 이 T 와 Y 의 상관의 유일 source"
- 즉 T (treatment) 가 Y (outcome) 에 영향 미치는 channel 은 M (mediator) 만
- Direct effect (T → Y not through M) = 0 의 strong 가정. 이는 DGHP 의 *core assumption*

**Bounds option (Section 2.3)**:
> "We relax Assumption A-2 in Section 2.3 to derive bounds instead of point estimates."
> "Allowing ρ_TY ≠ 0 is equivalent to stating that the statistical dependence among error terms T, M, Y is unrestricted."

→ A-2 relax 시 ρ_TY (T 와 Y 의 unconditional correlation) ≠ 0 허용 → bounds (Conley-Hansen-Rossi 2012 spirit).

### v4.5.3 정정 — § 9.5

```
**Single-IV mediation framework (DGHP 2017 NBER WP 23209)**:

본 paper 의 § 9 mechanism 의 6 mediator 각각 별도 channel 의 single-IV mediation framework. Frölich-Huber 2017 의 dual-IV requirement 부적용 — DGHP 의 single-IV 가능.

**Identification (DGHP 2017 Section 2)**:

- **Assumption A-1** (Standard IV): Z ⊥⊥ ε_T, ε_M, ε_Y
- **Assumption A-2** (DGHP's core): T 와 Y 의 error terms unconditionally independent (T ⊥⊥ Y), but correlate conditional on M (T ⊥/⊥ Y | M)
  - 의미: M 이 T 와 Y 의 상관의 유일 source
  - Direct effect of T on Y (not through M) = 0 강한 가정

**Lemma L-2**: A-1 + A-2 하에서 Z 가 M 의 causal effect on Y 식별 가능 (Z ⊥⊥ Y(m) | T)

**Implementation**: Standard 2SLS

**Bounds (Section 2.3)**: A-2 relax 시 (T ⊥⊥ Y unconditional 가정 풀기) bounds derive 가능

**본 paper 적용** (6 mediator 각각):
- Assumption A-2 의 strong 가정 — direct effect = 0 = 본 paper 의 각 mediator 가 trade exposure 의 mortality 영향의 유일 channel 이라는 가설
- 한계: A-2 위반 시 (즉 trade exposure 가 mediator 외 channel 로 mortality 에 영향) bounds 보고로 robustness check

**6 channel decomposition**:
- Channel 1 (HIRA SSRI 처방률, 시군구), Channel 2-4 (KOSIS 이혼·출생·혼인), Channel 5 (z_m_marital), Channel 6 (z_m_education)
- 각 channel k: indirect = ζ_k · β_k, direct = β_direct, total = β_direct + ζ_k · β_k

**P2 Stage B Claude Code 위임 시**: DGHP 정식 implementation = Stata `ivmediate` (DFH 2020) 또는 R 직접 구현.
```

## 2. § 1.3 — Finkelstein 2026 deaths of despair sub-category

본문 직접 verify (BFI WP 2026-33, Figure 5):

> "Figure 5 shows the impacts on deaths classified as 'deaths of despair', as well as for the three sub-categories: drug-related deaths, suicides, and alcohol-related deaths."
> 
> "**For the full sample**, there is a statistically significant increase in deaths of despair, with increases in **all three sub-categories**, and **statistically significant increases in drug-related deaths and in suicides**."
> 
> "**For men who were 25-44 in 1994**, there is a statistically significant increase in **alcohol-related mortality**, and large but imprecise increases in drug-related mortality."

### v4.5.3 정정 — § 1.3 anchor 비교 표 Finkelstein 행

| 이전 (v4.5.2) | 정정 (v4.5.3) |
|---|---|
| Finkelstein 2026: all-cause +0.68% (15y post-NAFTA), particularly working-age men, all-cause not drug-specific | Finkelstein-Notowidigdo-Shi 2026 (BFI WP 2026-33): **all-cause age-adjusted mortality +0.68% (SE 0.19), 15y post-NAFTA. Deaths of despair (Figure 5): drug-related + suicide statistically significant for full sample. Working-age men (25-44 in 1994): alcohol-related significant, drug-related large but imprecise** |

→ Finkelstein 2026 이 본 paper 의 despair_total composite (자살 + 약물 + 정신활성 + 간) 와 직접 비교 가능. Drug-related, suicide, alcohol-related 모두 sub-category 보고됨 (Figure 5).

## 3. Track 2·3 코드 작성 완료 (사용자 PC 실행 대기)

### Track 2 — z_m_education baseline sensitivity

**Script**: `Documents/Claude/Projects/논문을쓰자/z_m_education_baseline_sensitivity.py`

**Input**:
- `0_raw/sigungu_centroid/sigungu_centroid_table.csv` (251 시군구 lat/lng)
- `0_raw/edu_university_list_1990/universities_4year_pre1990_clean.csv` (175 학교 with year + lng/lat)

**Output**:
- `3_derived/exposure/z_m_education_baseline_sensitivity.parquet`
- `5_logs/integrity_checks/<date>_z_m_education_sensitivity.md`

**처리**:
1. 1985/1990/1995 sub-cohort 추출 (year ≤ X filter)
2. Haversine distance 계산 (시군구 centroid × nearest 4년제 대학)
3. z_m_edu = -log(distance + 0.1)
4. 4 baseline 의 correlation + 시군구별 차이 magnitude

**해석 권고** (사용자 결과 보면):
- correlation > 0.95 → 1985 baseline 사용 정합 (§ 9.4 spec 그대로 유지)
- correlation < 0.90 → 1985 vs 2008 baseline 의 substantive 차이, § 9.4 spec 재검토

### Track 3 — 1992 광업제조업조사 baseline shares build

**Script**: `Documents/Claude/Projects/논문을쓰자/build_baseline_shares_1992.py`

**Input**:
- 1992 광업제조업조사 microdata (사용자 이번 conversation 업로드)
- `1_codebooks/sigungu_crosswalk.csv` (1997 baseline crosswalk, 1992-1996 동일 가정)

**Output**:
- `3_derived/bartik/baseline_shares_1992_ksic9_2digit.parquet`
- `3_derived/bartik/denominator_E_h_1992.parquet`
- `5_logs/integrity_checks/<date>_baseline_shares_1992.md`

**처리** (기존 `02_build_baseline_shares_1994.py` 패턴 확장):
1. positional column loading (cp949 mojibake 우회)
2. 시도 col 0, 시군구 col 1, KSIC 6차 col 3-5, 종사자 col 14
3. 시군구 crosswalk (1997 baseline) 매칭
4. Manufacturing (D) only filter
5. KSIC 6차 → KSIC 9차 2-digit 변환 (임시 manual — 정확 매핑 file 별도 필요)
6. h_code × ksic9_2digit aggregate → employment + share

**한계 명시**:
- KSIC 6차 → 9차 정확 매핑 file 부재 (`crosswalks/` 폴더 에 8차→9차 만)
- 임시 manual mapping (ksic_2 그대로 ksic9_2digit 로) — 사용자 결과 받은 후 R-A 다음 turn 에 정밀화

### PowerShell wrapper

**Script**: `Documents/Claude/Projects/논문을쓰자/run_track2_track3.ps1`

**사용법**:
```powershell
cd C:\Users\82103\Documents\Claude\Projects\논문을쓰자
.\run_track2_track3.ps1
```

**예상 시간**: Track 2 (5분) + Track 3 (10-30분) = **약 15-40분**

---

## 4. v4.5.3 commit 정합성

| 항목 | Status |
|---|---|
| § 1.3 Finkelstein deaths of despair sub-category | ✅ commit |
| § 9.5 DGHP A-2 정확 spec + Lemma L-2 | ✅ commit |
| § 9.5 의 6 channel decomposition explicit | ✅ commit |
| Track 2 코드 작성 (사용자 실행 대기) | ✅ |
| Track 3 코드 작성 (사용자 실행 대기) | ✅ |

**v4.5.3 = paper draft Stage C 진입 prerequisite 의 9/9 commit** (P1·P4·P5·P6·P8 R-A direct + P2·P3 Stage B + Track 2·3 코드 작성 + DGHP/Finkelstein verify).

---

## 5. 사용자 측 다음 작업 (1 일)

1. **PowerShell 실행** (15-40분):
   ```powershell
   cd C:\Users\82103\Documents\Claude\Projects\논문을쓰자
   .\run_track2_track3.ps1
   ```

2. **결과 R-A 에 보고**:
   - `5_logs/integrity_checks/<date>_z_m_education_sensitivity.md` 의 4 baseline correlation
   - `5_logs/integrity_checks/<date>_baseline_shares_1992.md` 의 시군구 매칭률 + 종사자 합

3. **HIRA 약물 fetch** (계속):
   ```powershell
   .\run_hira_drug_extended.ps1
   ```

---

## 6. R-A 다음 turn 작업 (Track 2·3 결과 받은 후)

1. **§ 9.4 + § 5.3 v4.5.4 patch** (Track 2·3 결과 반영)
2. **z_x_h^{1992} 산출 + 1992 vs 1994 sensitivity 회귀 script** (R-A 코드 + 사용자 실행)
3. **Stage B Claude Code 위임 prompt** (P2 AKM + P3 AR-CI)
4. **Paper draft § 1 + § 2** (Stage C 시작)

---

## 결론 (PAP v4.5.3 patch commit)

본 v4.5.3 = R-A direct deep inspect (DGHP A-2 + Finkelstein deaths of despair) + Track 2·3 코드 commit. **paper draft Stage C 진입 prerequisite 9/9**.

**Author**: 정재헌 (가천대학교 경제학)
**Date**: 2026-05-05
**Verified by**: R-A direct PDF inspect + Track 2·3 코드 작성
