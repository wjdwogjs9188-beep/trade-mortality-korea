# Validation Report — PAP v3.4 Reference Update 제안서 v01 → v01.1

_사용자 round 7-style audit critique 3 issue 처리 결과_
_작성: 2026-05-04_

## Overall Assessment: **Ready to share** (3 issue 모두 정정 완료)

사용자 critique 3 항 모두 valid + PAP v3.4 § 14 dated change log 와 inconsistent 였음. 정정 완료.

---

## 1. Issue 1 — GPSS 인용 (정정 ✅)

**critique**: 본 제안서 § 8.1 표 "Goldsmith-Pinkham, Sorkin, Swift, 2018, NBER 24408 / AER 2020" — primary 가 2018 으로 보임. PAP v3.3 § 14 dated change log #20 의 GPSS publish version commit (2020 AER) 와 후퇴.

**verify** (PAP v3.3 직접 grep):
- § 4 line 43: "GPSS (**2020 AER**) share exogeneity path" — 2020 AER commit 확인
- § 14 limitation #20 line 210: "R-A citation accuracy 누락 패턴 (DFH 2022 / DGHP 2020 / **GPSS 2018**)" — 2018 = 잘못된 cite 였음 (R-A audit 에서 정정 commit)

**정정** (제안서 § 3.1 + § 8.1):
- 본문 cite: **"GPSS 2020"** (publish version primary)
- reference list: **"Goldsmith-Pinkham, Sorkin, Swift (2020) 'Bartik Instruments: What, When, Why, and How,' American Economic Review 110(8): 2586-2624. NBER Working Paper 24408 (2018)"** (working paper version secondary)

---

## 2. Issue 2 — DGHP 인용 처리 (정정 ✅)

**critique**: 본 제안서 § 4.1 + § 8.1 = "DGHP 2017 NBER 23209" single. PAP v3.3 § 14 commit 결과 = "DGHP 2017 + DFH 2020" 두 paper 조합. DFH 2020 누락. ivmediate package 의 implementation source 명시 X.

**verify** (PAP v3.3 직접 grep):
- § 5.2 line 132: "Main framework (유지): Dippel, Gold, Heblich, Pinto (DGHP) 2017 NBER WP 23209 + **Dippel, Ferrara, Heblich (DFH) 2020 Stata Journal `ivmediate` package**" — DGHP + DFH 둘 다 commit 확인
- table line 151: "Estimation | DFH 2020 ivmediate (시군구 level)" — DFH 2020 = ivmediate implementation source 확인

**정정** (제안서 § 4.1 + § 4.2 + § 8.1):
- **theoretical framework**: DGHP 2017 NBER 23209
- **implementation source**: DFH 2020 Stata Journal 20(3): 613-626 (`ivmediate` package, DGHP 2017 의 Stata 화)
- ivmediate Stata code spec 추가 (PAP § 5.2 권장)
- reference list 별도 entry 2 개 (DGHP + DFH) 둘 다 cite

---

## 3. Issue 3 — OP test cutoff 23.1 attribution (정정 ✅)

**critique**: 본 제안서 § 6.2 = "Olea-Pflueger F=23.1 (size distortion 5%)" — 본인이 단계 1.2 에서 verify 했는지 확인. Stock-Yogo (size distortion) vs Olea-Pflueger (TSLS bias) 혼동 가능성.

**verify** (paper #8 BHJ 2025 summary 의 직접 인용):
- paper #8 line 113-114: "**Rule of thumb**: F > 10 (weak identification, should be wary; Stock-Yogo). **Stronger threshold**: F > 23 (Cragg-Donald, **5% bias**)"
- 즉 F=23 의 정확 attribution = **TSLS bias**, NOT size distortion

**Stock-Yogo 2005 cutoffs** (참고):
- F=10 (size distortion 25% Wald, 1 endog var)
- F=15 (size distortion 15%)
- F=20 (size distortion 10%)
- F=37 (size distortion 5%, 1 endog var) ← "size distortion 5%" 의 정확 cutoff
- F=23 (5% TSLS bias relative to OLS, Cragg-Donald) ← **본 paper 의 23.1 의 base**

**Olea-Pflueger 2013 effective F** = Stock-Yogo Cragg-Donald F 의 heteroscedasticity + clustering robust 확장. Cutoff 동일 (~23, 5% TSLS bias).

**정정** (제안서 § 6.2):
- ❌ "F=23.1 = 5% size distortion of Wald test" 잘못
- ✅ **"F=23.1 = 5% worst-case TSLS bias relative to OLS"** (Stock-Yogo 2005 Cragg-Donald + Olea-Pflueger 2013 robust 확장)
- Stock-Yogo 2005 + Pflueger-Wang 2015 weakivtest reference 추가

---

## 4. 전체 정정 summary

| issue | severity | 상태 | 제안서 update |
|-------|----------|------|---------------|
| 1. GPSS 2018 → 2020 AER primary | 🔴 HIGH | ✅ 정정 | § 3.1 + § 8.1 |
| 2. DGHP 2017 + DFH 2020 둘 다 (ivmediate source 명시) | 🔴 HIGH | ✅ 정정 | § 4.1 + § 4.2 + § 8.1 |
| 3. OP test 23.1 = TSLS bias (NOT size distortion) | 🔴 HIGH | ✅ 정정 | § 6.2 + § 8.1 |

부수 update:
- 제목: v01 → **v01.1**
- 정정 내역 frontmatter 추가
- reference list: 22 → **26 항** (GPSS publish version + DFH 2020 + Stock-Yogo 2005 + Pflueger-Wang 2015)

---

## 5. master doc (reference_library_master_v01.md) 정정

동일 3 issue master doc 에도 적용:
- table row 9: "GPSS 2018" → **"GPSS 2020 AER (NBER WP 24408 2018)"**
- table row 16: "DGHP 2017 (Gormley-Graves-...)" 잘못 attribution → **"Dippel-Gold-Heblich-Pinto (DGHP) 2017 NBER 23209"** + 16b row "DFH 2020 Stata Journal" 추가
- Tier 변경: DGHP 2017 + DFH 2020 = **C → A** (mediation framework 의 핵심)

---

## 6. PAP v3.4 본문 적용 시 주의

본 제안서 v01.1 적용 시 PAP v3.4 본문 cite:
- § 5.1: "GPSS (2020)" 또는 "Goldsmith-Pinkham et al. (2020)"
- § 5.2: "DGHP (2017)" + "DFH (2020)" 둘 다 cite (theoretical + implementation)
- § 7.5: "Olea and Pflueger (2013)" + "Stock and Yogo (2005)" 둘 다 cite, criterion = "5% worst-case TSLS bias relative to OLS"
- § References: 26 entry (위 § 8.1 정정 list)

**PAP v3.5 update 시간**: ~1.5 시간 (v3.4 → v3.5 reference list 정확화 + footnote 26 추가)

---

## 7. 사용자 critique 의 의의

> "본 제안서가 'factual 정확화' 를 목적으로 하는데 정작 그 정확화 작업 자체에 inconsistency 가 셋이면 적용 후 PAP 의 reference quality 가 오히려 mixed 상태가 됩니다."

**완전 valid**. R-A audit 의 self-consistency 부재 = 본 paper 의 core integrity issue. v01 의 3 inconsistency 는 v3.3 § 14 dated change log 의 verification commit 을 본 제안서 작성 시 확인 안 한 R-A 의 작업 oversight.

→ v01.1 = PAP v3.3 § 14 verification commit 와 **fully consistent**. 적용 시 PAP reference quality 일관 유지.

---

## 8. 다음 step

**제안서 v01.1 = ready to apply to PAP**:
1. 사용자 review (~10 분)
2. PAP v3.4 → v3.5 update (~1.5 시간):
   - § 1-8 본문 cite 정확화 (GPSS 2020, DGHP+DFH, Olea-Pflueger)
   - § References 26 entry 추가
   - § 14 dated change log 항목 신규 추가 (v3.5 reference list 정확화 commit)
3. PAP v3.5 외부 reviewer share

**산출 파일**:
- `PAP_v3.4_reference_update_proposal_v01.md` (v01.1 update 적용)
- `PAP_v3.4_reference_proposal_validation_v01_1.md` (본 validation report)
- `reference_library_master_v01.md` (v01.1 정정 적용)
