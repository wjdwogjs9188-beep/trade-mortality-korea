# Reviewer critique — RESEARCH_OVERVIEW 2026-05-04

**작성**: 2026-05-04, R-A 박사급 critique
**대상 문서**: `RESEARCH_OVERVIEW_for_feedback_2026_05_04.md` (3,622 words, 11 sections)
**Conditional**: Stage 5 진입 전 P1.A-E 처리 시 SSCI Q1 (AEJ Applied / JHE) submission ready

---

## P1 — 식별·측정 자체가 흔들리는 이슈 (5 항)

### P1.A 🔴 z_m_marital exclusion restriction 의 비-mediator 채널 3개

**위치**: § 3.4, § 10 P1 #2
**Issue**: sex ratio → marital share → mortality 만 가정. 다른 채널 미검토:
1. Gendercide / 가정폭력: 남초 시군구 → 폭력 ↑ → 외상사·자살 *직접*
2. 매매혼·결혼이주: 남초 → 베트남·필리핀 결혼이주 ↑ → 외국인 비율 변동 → 1997-2007 외국인 식별 불가 measurement 영향
3. 청년 인구 유출: 남초 → 결혼 못한 남성 유출 → mortality denominator bias

**근거**: Edlund-Lee (2009) NBER WP 14495 자체가 sex ratio → crime + violence 다룸. 본 paper 가 Park-Cho 만 인용 = partial citation.

**해결**: § 7 limitation 명시 + Imai-Yamamoto ρ ±0.5 sensitivity (현재 ±0.3).

### P1.B 🔴 z_m_education 1990 baseline 의 89 신설학교 endogenous

**위치**: § 3.4, § 10 P1 #3
**Issue**: KESS 196 vs yunbo 1990 107 = 차이 **89 학교 = post-1990 신설**. Bound-Jaeger (1996) 가정 = "거리 long-run 외생적" 인데 신설 대학은 trade-shock 후 endogenous (예: 제조업 쇠퇴 시군구 정부 보상 정책).
**해결**: 1990 baseline 학교 107만 사용 (KESS 196 → yunbo 107 cross-verify), post-1990 신설 89 제외 + 1985/1990 baseline 둘 다 sensitivity.

### P1.C 🟡 12+ branch decision tree 학술 수용 가능성

**위치**: § 3.7, § 10 P1 #1
**Issue**: Pierce-Schott 2020 / Finkelstein 2026 = single decision (post-hoc 보고). 12+ branch pre-commit = AER/QJE precedent 부재. "over-engineered protocol" reject 위험.
**근거**: AEA registry typical pre-commit = 3-4 branch. 12+ unprecedented.
**해결**: 9 branch 통합 (3 main + 3 fallback × 3 SI) 또는 § 8 contribution 으로 "transparent 12-branch" framing.

### P1.D 🔴 5-year stack × cohort timing 부정합 (가장 critical)

**위치**: § 3.4 z_m_marital + § 5.1 main 2SLS
**Issue**: z_m_marital cohort = 1986-1995 출생, 25년 후 결혼시장 진입 = 2011-2020 만. main panel period 1 (1997-2001) = cohort 진입 *전*. Period 1 의 z_m_marital first-stage F < 1 가능 (정의상 0).

| period | 연도 | 25-29세 cohort | 1995 census 0-9세 (z_m main) 매칭 |
|--------|------|---------------|----------------------------------|
| 1 | 1997-2001 | 1968-1972 출생 | ❌ 매칭 안 됨 |
| 2 | 2002-2006 | 1973-1977 | ❌ |
| 3 | 2007-2011 | 1978-1982 | ❌ (1986+ 만 보유) |
| 4 | 2012-2016 | 1983-1987 | 🟡 부분 (1986-1987) |
| 5 | 2017-2021 | 1988-1992 | ✅ 완전 |

**해결 옵션 3개**:
- (a) period 3-5 만 z_m_marital 적용 → power loss (3 periods)
- (b) cohort lag 동적 — period 별 *다른 census* 사용 (period 1 → 1975 census 0-9세 = 1966-1975 cohort, period 2 → 1980 census 0-9세, ...) ← **가장 학술적**
- (c) period 1 drop → 4 periods, period 2 여전히 문제

**근거**: 본 paper § 4.2 "1995 census 0-9세 = 1986-1995 cohort" → 2011-2020 결혼시장. period 1 무관.

### P1.E 🔴 PAP v3.4 main body ↔ v4.0 commit 미완

**위치**: § 9.2, § 10 P1 #5
**Issue**: v4.0 protocol pre-commit 직전 인데 v3.4 main body 가 v4.0 정합 commit 안 됨. § 5 의 12-branch tree + § 4 SI sensitivity 가 v3.4 § 5.2 mediation 과 conflict 가능. 회귀 결과 본 후 cherry-pick risk.
**해결**: Phase B-x/B-m 시작 *전* v4.0 main body commit 필수 (~3h R-A 작업).

---

## P2 — 제출 전 보강 (5 항)

### P2.A 🟡 H1 → H1a/H1b 분리 (export-gain vs import-loss)
사용자 self-critique #1 동의. DFS 2014 (Germany) precedent.

### P2.B 🟡 Sparse cell — Poisson with offset main spec
log(rate+1) 는 sparse cell bias 감추기. main → Poisson 권장.

### P2.C 🟡 F17 (담배) 057 sensitivity
F17 = 담배. Case-Deaton 2015 정의 제외. 057 (F10-F19) 포함 → sensitivity test 필수.

### P2.D 🟡 Multiple testing family — 240 vs 10 inconsistency
**위치**: § 5.6 (10) vs § 7.2 #5 (~240) — 본 문서 내부 inconsistency.
**해결**: confirmatory family (10) vs exploratory (230) 명확 분리. Romano-Wolf 만 confirmatory 적용.

### P2.E 🟡 Pre-period 1995-1999 power 부족
KOSTAT mortality 1997+ 시작 = pre-period 실제 1997-1999 (3 년). Pierce-Schott 2020 = 8 년. 1997 IMF 위기 confound.
**해결**: pre-period = 1997-2001 (pre-WTO) + 1997 IMF 효과 통제 변수.

---

## P3 — Polish (4 항)

### P3.A 1995 census only z_m_marital → 1985/1990 census 추가
**(P1.D 와 직접 연결)** 1985/1990/1995 triple-source 가 학술 표준.

### P3.B KESS 196 vs yunbo 107 차이 source 명시
89 학교 차이 = (a) 캠퍼스 vs 본교 (b) 폐교 통합 (c) 분교 별도 카운트 — 어느 것? § 4.6 detail 추가.

### P3.C v3.4 main body 외국인 빼기 narrative inconsistency
§ 7.1 #1 "외국인 0.5% over-counting" vs PAP v3.3 § 14 #22 "외국인 빼기 over-correction" — direction 반대. v3.4 정정 시 일관성 commit.

### P3.D Bilingual strategy
SSCI 제출 = English only. Submission 전 single language commit.

---

## Strength 3 + Weakness 3

**Strength**:
1. Pre-commit transparency — 12+ branch tree 가 over-engineered 라도 cherry-pick 회피 = 학술 정직성 ↑
2. Korea-specific structural framing — § 0 #3 (export-driven economy) = Pierce-Schott 단순 적용 회피
3. Self-critique 7 항 (§ 7.2) — 학부생 paper 에서 보기 드문 epistemic humility

**Weakness**:
1. **z_m cohort timing bug (P1.D)** — 본 paper 의 가장 critical 한 잠재 식별 실패
2. Sequential Ignorability ρ ±0.3 부족 — 한국 cultural confounding 의 ρ 가 ±0.5 까지 갈 수 있음
3. PAP v3.4 → v4.0 commit 미완 — protocol 등록 전 main body 정합성 보장 안 되면 reviewer rejection risk

---

## Overall Assessment

**Conditional accept** — Stage 5 진입 전 P1.A-E 모두 처리 시 SSCI Q1 (AEJ Applied / JHE) submission ready.

**P1.D + P1.E 가 가장 critical**. P1.A-C 는 limitation 명시 + sensitivity 로 충분.

---

## NEXT_STEP_PROMPT (paste 용)

```
RESEARCH_OVERVIEW_for_feedback_2026_05_04.md 의 R-A reviewer critique 받음. P1 5항 + P2 5 + P3 4 = 14 issue.

가장 critical (P1) 5 처리 task:

1. P1.A z_m_marital exclusion: § 7 limitation 에 sex ratio → 폭력/매매혼/유출 3 채널 명시 + Imai-Yamamoto ρ ±0.5 sensitivity 추가 (현재 ±0.3)
2. P1.B z_m_education 외생성: KESS 196 vs yunbo 107 cross-verify 후 1990 baseline 107 만 사용 (post-1990 신설 89 제외)
3. P1.C 12-branch tree 학술 합리성: 9 branch 로 통합 (3 main + 3 fallback × 3 SI) 또는 § 8 contribution 으로 transparent framing
4. P1.D cohort timing bug: z_m_marital cohort 1980-1995 vs main panel period 1997-2001 의 timing mismatch. 옵션 (a) period 3-5 만 z_m_marital, (b) cohort lag 동적, (c) period 1 drop. 결정 필요.
5. P1.E PAP v3.4 → v4.0 main body commit: § 5.2 mediation + § 7 5-layer SE + § 8 limitation 모두 v4.0 정합성 update (~3 시간)

P2 5 + P3 4 는 P1 처리 후 단계적.

본 paper 의 PAP v4.0 + Stage 5 진입 전 P1.D + P1.E 가 가장 critical. P1.D 는 본 paper 의 잠재 식별 실패 (z_m_marital first-stage period 1 무용 가능성).
```

---

_작성: 2026-05-04, R-A 박사급 critique mode_
