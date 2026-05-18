# PAP v3.6 — z_m (Mediator-Specific Instrument) Protocol Draft v01

_Reviewer P1.A critique 반영. v3.5 z_x protocol 의 sister protocol. 둘 다 PAP commit 후 둘 다 통과 시 Stage 5 entry._
_작성: 2026-05-04 (Stage 5 entry 선결조건)_
_상위 PAP: PAP_2026_05_03_v3.3.md (status v3.4)_

---

## 0. 본 protocol 의 위치

**v3.5 IV protocol** (이전 작성, z_x 용):
- trade → mortality 단순 IV
- z_x = ADH-8 ← CN imports + KR-CN bilateral (1 instrument set)
- exclusion restriction on z_x
- weak-IV decision tree (F<10 / 10-23 / ≥23)

**v3.6 z_m protocol** (본 문서, mediator 용):
- trade → mediator → mortality (DGHP 2017 + DFH 2020 ivmediate)
- z_m = mediator-specific instrument (z_x 와 독립적 변동원)
- exclusion restriction on z_m + sequential ignorability
- weak-IV decision tree on z_m

**둘 다 통과 시**: ivmediate (z_x = trade IV, z_m = mediator IV) → total/direct/indirect 분해 식별

**z_m 부재 시**: mediation analysis 자체 미식별 → § 5.2 결과 의미 없음 → reviewer P1.A 의 black hole

---

## 1. DGHP 2017 + DFH 2020 의 z_m 요구사항

### 1.1 Theoretical (DGHP 2017 NBER 23209)

ivmediate 의 식별 가정:
1. **z_x exogeneity**: trade IV (Bartik shift-share) 가 mortality 와 mediator 모두에 first-stage 강력
2. **z_m exogeneity**: mediator IV 가 mediator 의 별도 변동 (z_x 와 독립) 에서 만들어짐
3. **Sequential ignorability**: z_x 와 z_m 이 independent 하게 mediator + outcome 의 unobserved confounder 와 orthogonal
4. **No reverse causality**: mortality → mediator path 부재

### 1.2 Identification 의 핵심 요구

z_m 이 z_x 와 같은 변동원 (lagged trade shares) 에서 만들어지면:
- collinear → indirect effect decomposition 자체 미식별
- direct effect = total - indirect 가 unstable
- ivmediate output 의 standard error 미정 또는 무한대

→ z_m 은 **trade shock 과 별개의 변동원** 에서 발굴 필수

---

## 2. z_m 후보 5 (한국 setting brainstorm)

각 후보의 source + variation 측면 + exclusion violation risk + first-stage strength expectation:

### 2.1 후보 A — Lagged mediator share (10년 lag)
- **Source**: 시군구 h 의 t-10 시점 marital_share / education_share
- **Variation**: 시군구 historical mediator level 의 cross-sectional 변동
- **Risk** (high): t-10 의 mediator share 자체가 trade shock 의 결과 (구조적 endogeneity)
- **First stage**: 강함 (mediator 의 persistence ~ 0.7-0.8)
- **Verdict**: ❌ exclusion violation. 사용 불가

### 2.2 후보 B — Birth cohort 변동 (10년 cohort)
- **Source**: 시군구 h 의 t 시점 working-age 25-64 의 출생 cohort 분포 (예: 1960s vs 1970s baby boom)
- **Variation**: cohort effect (인구학적, demographic), trade shock 과 독립
- **Risk** (low-medium): cohort birth 시점 (1960s) 의 시군구 출산률이 그 시점 산업 구조 와 correlated 가능성
- **First stage**: 중간 (cohort 가 mediator 결정의 강한 predictor — 미혼/이혼율 cohort 별 dramatically 다름)
- **Verdict**: ⚠️ promising. exclusion violation test 필요

### 2.3 후보 C — Religious affiliation share (시군구 변동)
- **Source**: 종교 기관 (성당/교회/사찰) 분포 + 종교 인구 비율 (KOSIS 종교조사)
- **Variation**: cross-sectional + 시간 역사적 변화 (개신교 ↑ 1990s, 천주교 ↑ 2000s)
- **Risk** (low): 종교가 trade exposure 와 독립 (종교 분포 = 역사적 + 지리적, 산업 구조와 무관)
- **First stage**: 강함 (개신교 = 이혼 stigma 높음, 미혼 ↓; 천주교 = 결혼 안정성 ↑; 무종교 = 미혼 ↑)
- **Risk** secondary: 종교 분포 자체가 mortality 에 직접 영향 (예: 자살 stigma) → exclusion violation
- **Verdict**: ⚠️ promising but exclusion 의 secondary risk

### 2.4 후보 D — Higher education institution density (대학교 + 전문대 분포)
- **Source**: 시군구 h 의 t 시점 4년제 + 전문대 + 대학원 캠퍼스 수 (대학정보공시)
- **Variation**: 1990s-2000s 대학 신설/지방분교 정책 (외생적 정책 충격)
- **Risk** (low): 대학 분포 = 정부 정책 + 역사적 (산업 구조 독립)
- **First stage**: 강함 (대학 access 가 education attainment 의 강한 predictor)
- **Risk** secondary: 대학 분포 자체가 사망률 에 직접 영향 (의료 access? 자살 rate?) → 경미
- **Verdict**: ✅ strong candidate for **education mediator** z_m

### 2.5 후보 E — Conscription (군 복무) variation
- **Source**: 시군구 h 의 t 시점 남성 working-age 25-64 의 군 복무 history (병역청 자료)
- **Variation**: 2000s 군 복무 기간 단축 (28개월 → 21개월), 대체복무 정책
- **Risk** (low): 군 복무 정책 = 외생적 (전국적 동일)
- **First stage**: 약함 (시군구 변동 < 정책 변동)
- **Verdict**: ❌ first-stage too weak for sigungu-level Bartik

---

## 3. 권장 z_m Protocol (Final Spec)

### 3.1 Marital mediator: z_m_marital = Religious institution density (후보 C)

**Construction**:
```
z_m_marital_{h, t} = Σ_r [ s_{h, r, t-10} × ΔReligious_density_{r, t-10→t} ]
```
- r = 종교 (개신교 / 천주교 / 불교 / 무종교 4 카테고리)
- s_{h, r, t-10} = 시군구 h 의 t-10 시점 종교 r 인구 비율
- ΔReligious_density = 전국 종교 r 의 t-10→t 시점 시설 수 변동

**Exclusion test** (Stage 5 진입 전 필수):
- z_m_marital 와 trade exposure z_x 의 correlation
- z_m_marital 와 mortality direct effect (mediator 통제 후 residual) correlation
- Pre-trend test (1985-1995 시점 z_m_marital 변동 vs 1997+ mortality)

### 3.2 Education mediator: z_m_education = Higher education institution density (후보 D)

**Construction**:
```
z_m_education_{h, t} = Σ_e [ s_{h, e, t-10} × ΔUni_density_{e, t-10→t} ]
```
- e = 교육 (4년제 / 전문대 / 대학원 3 카테고리)
- s_{h, e, t-10} = 시군구 h 의 t-10 시점 교육 e 인구 비율
- ΔUni_density = 전국 교육 e 의 t-10→t 시점 캠퍼스 수 변동

**Exclusion test**:
- 동일 (z_x correlation, mortality residual correlation, pre-trend)

### 3.3 Backup: 후보 B (Birth cohort) — z_m_cohort

z_m_marital + z_m_education 둘 다 fail 시 backup:
- 각 시군구 h 의 1955-1965 (Korea baby boom) cohort 비율
- exclusion: cohort effect = demographic, trade 와 독립 가정
- weakness: cohort 출생 시점 산업 구조 correlation 우려

---

## 4. z_m Decision Tree (v3.5 protocol 와 parallel)

| z_m strength (OP F) | branch decision |
|---------------------|-----------------|
| F ≥ 23 (5% TSLS bias) | ✅ z_m strong → ivmediate proceed with point estimate |
| 10 ≤ F < 23 | ⚠️ z_m weak — AR + tF confidence interval 사용 (Andrews-Stock-Sun 2019) |
| F < 10 | ❌ z_m too weak — alternative mediator 시도 또는 mediation 결과 not reportable |

z_x 와 z_m 모두 F ≥ 23 시 → ivmediate decomposition reportable.

---

## 5. Orthogonality Tests (v3.5 와 parallel)

### 5.1 Test 1 — z_x 와 z_m collinearity
```
corr(z_x, z_m) < 0.3 (rule of thumb)
또는 partialling out 후 z_m 의 marginal F-stat > 10
```

### 5.2 Test 2 — z_m exclusion (mortality 직접 효과 부재)
```
mortality_residual = mortality - β_x · trade_exposure - γ · mediator
corr(z_m, mortality_residual) ≈ 0 (test)
```

### 5.3 Test 3 — Pre-trend (z_m 의 leading vs lagging)
```
mortality_{t-5→t} on z_m_{t→t+5} (placebo)
z_m 이 mortality leading 이면 reverse causality
```

---

## 6. Stage 5 Entry 선결조건 (v3.6 protocol)

| 조건 | check |
|------|-------|
| 1. z_x 후보 (v3.5 protocol) F ≥ 10 | weakivtest |
| 2. z_m_marital (v3.6 protocol) F ≥ 10 | weakivtest |
| 3. z_m_education (v3.6 protocol) F ≥ 10 | weakivtest |
| 4. z_x ⊥ z_m correlation < 0.3 | partialling test |
| 5. z_m ⊥ mortality residual ≈ 0 | exclusion test |
| 6. z_m pre-trend test PASS | placebo |
| 7. denom missing 67 h_code 진단 (P1.D fix) | sub-script |
| 8. KR-CN bilateral IV exclusion (v3.5 K) | branch decision |

8 항 모두 PASS 시 → Stage 5 ivmediate entry.

---

## 7. Data 추가 신청 (z_m construction 에 필요)

### 7.1 KOSIS 종교조사 (z_m_marital)
- 시군구 × 시점 (1985, 1995, 2005, 2015 시점 census + 종교 시설 통계)
- 변수: 종교 r (개신교/천주교/불교/무종교) × 인구 비율 + 시설 수
- 신청: KOSIS 자동 또는 통계청 직접

### 7.2 대학정보공시 (z_m_education)
- 시군구 × 시점 (1990-2024 연간) 의 4년제 + 전문대 + 대학원 캠퍼스 + 정원
- 출처: 한국대학교육협의회 + 대학정보공시 (학교알리미)
- 신청: 공개 자료

### 7.3 추가 시간 비용
- KOSIS 종교조사: ~2 시간 다운로드 + cleaning
- 대학정보공시: ~3 시간 다운로드 + cleaning
- z_m construction script: ~2 시간 (Claude Code 위임)
- exclusion + weak-IV test: ~2 시간 (Stage 5 진입 직전)

**총 ~9-10 시간** = 1-2 작업일.

---

## 8. v3.5 protocol 와의 합치점 (PAP commit)

PAP v3.5 (z_x) + PAP v3.6 (z_m) 둘 다 PAP § 5 새 sub-section 으로:

- § 5.1 Bartik IV (z_x): v3.5 protocol
- § 5.2 Mediation (z_m): v3.6 protocol
- § 5.3 Joint identification: z_x + z_m 둘 다 통과 시 ivmediate

PAP v3.4 → v3.7 (major update — z_m protocol 추가):
- § 5.1, § 5.2 본문 update
- § 7.5 weak-IV diagnostics 에 z_m 도 적용 (총 2 instrument set 진단)
- § 8 limitation 추가: z_m 후보 (종교 + 대학) 의 exclusion violation risk

---

## 9. Reviewer P1.A 에 대한 R-A 응답

> "P1.A z_m 미정의 — 가장 큰 black hole. v3.6 z_m protocol 작성 필수."

**R-A 응답**:
- 본 v3.6 draft 가 reviewer 의 P1.A critique 직접 처리.
- z_m 후보 5 brainstorm + 2 권장 (종교 + 대학) + decision tree + orthogonality test 3 + Stage 5 entry 8 선결조건 명시.
- 다음 step: 사용자 검토 → KOSIS 종교 + 대학정보공시 데이터 신청 → Claude Code 위임 (z_m construction script) → exclusion test 후 PAP v3.7 commit → Stage 5 entry.

**예상 시간**: ~9-10 시간 (1-2 작업일) + reviewer 추가 검토 (z_m 권장 후보 적절성)

---

_본 v01 draft = z_m protocol 의 첫 commit. v3.5 (z_x) + v3.6 (z_m) sister protocol 시스템. 둘 다 통과 시만 Stage 5 진입._
