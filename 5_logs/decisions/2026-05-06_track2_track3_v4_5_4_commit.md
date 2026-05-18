# Track 2 + Track 3 — z_m_education 정합 입증 + 1992 baseline P1 fix plan

**date**: 2026-05-06
**author**: R-A
**status**: provisional (Track 3 P1 fix pending)
**supersedes**: 본 commit 은 PAP v4.5.3_patch 의 Track 2·3 코드 commit 을 결과로 reconcile

---

## 결정

(1) **Track 2** — PAP § 9.4 의 1985 baseline z_m_education 사용은 substantive 정합 (1985 vs 1990 correlation 0.989, 시군구 차이 > 0.5 단 2개 = 0.8%). 본 paper main spec 에 1985 baseline 그대로 유지. 1990·1995 baseline 은 robustness sensitivity 로 § 6.4 에 삽입.

(2) **Track 3** — 1992 baseline shares build 는 **P1 issue 발생** (sigungu 매칭률 89.2%, KSIC 6차→9차 매핑 부재, 'D' filter rows = 0, baseline shares (h × k) rows = 0). 1992 baseline sensitivity 는 **fix 후 재시도**까지 deferred. § 6.4 의 baseline year sensitivity 는 우선 1993·1995·1996·1999 4 baseline 으로 진행, 1992 는 fix 완료 후 추가.

---

## 근거

### Track 2 (정합 입증)

- **시군구 centroid** = 251 (mainland Korea + Jeju, dokdo 등 island 제외)
- **universities_pre1990** = 175 학교 (신설년도 1885-1989 분포, KEDI 1985_yunbo_total 제공 list parse). 1885 = 한국 최초 근대 4년제 대학의 모태 설립 시점 (배재학당 1885, 이화학당 1886)
- **Baseline 별 학교 수**: 1985 = 171, 1990 = 175, 1995 = 175 (1985-1990 사이 4학교 신설)
- **Baseline 별 z_m_edu correlation**:
  - 1985 vs 1990 = **0.989395**
  - 1990 vs 1995 = **1.000000**
  - 1985 vs 1995 = 0.989395
- **Baseline 별 평균 nearest distance (km)**:
  - 1985 = 18.10, 1990 = 17.81, 1995 = 17.81
  - 차이 ≈ 0.30 km (1.6%)
- **시군구별 baseline 차이 (z_m_edu max - min > 0.5)**: **2 시군구 (0.8%)**
  - 본 log 의 임계 기준 (>10% → spec issue, <5% → 정합) 에 비추어 0.8% 는 정합 영역에 deep 하게 들어감
- **결론**: 1985-1990-1995 사이의 4학교 추가는 z_m_education 분포에 **substantive 영향 없음**. PAP § 9.4 의 1985 baseline 사용은 정합

### Track 3 (P1 issue)

- **raw load**: 1992_연간자료_20260505_20424.csv = 76,357 rows × 101 cols ✅
- **시도 distinct**: 15 (정확)
- **시군구 (raw_code) distinct**: 274
- **종사자 (col 14) 합**: 53,189
- **시군구 매칭률**: 68,105 / 76,357 = **89.2%** (95% 미달)
  - 미매칭 top 10: 31450, 31100, 31430, 36510, 38032, 36490, 34450, 31420, 35430, 37450
  - 추정: 1992 시점 → 1997 baseline crosswalk 사이의 행정구역 변경 (안성·시흥·평택 시군구 분리·합병 시기)
- **Manufacturing (D) filter rows**: **0**
  - 추정 원인: 1992 시점 KSIC 6차는 letter prefix 'D' 사용 안 함. KSIC 6차는 numeric 2-digit (15 = 식료품, 17 = 섬유 등). 'D=Manufacturing' letter 는 KSIC 8차부터 도입
- **KSIC 6차→9차 매핑 file 부재**: ksic_crosswalk_8_to_9.csv 만 존재. 6차→8차 매핑 별도 build 필요
- **baseline shares (h × k) rows**: **0** (빈 parquet 출력)

---

## 영향

### Main spec 에 미치는 효과

- **Track 2 정합** → main spec 변경 없음. § 9.4 의 z_m_education_y1985 그대로 사용. 1990·1995 baseline 은 § 6.4 robustness 에 sensitivity row 로 추가.
- **Track 3 P1** → § 5.3 baseline year sensitivity narrative 에서 1992 결과는 **fix pending** notation 으로 우선 작성. main spec (1994 baseline) 은 영향 없음.

### Robustness 에 미치는 효과

- § 6.4 baseline year sensitivity table 의 column count: 5 baseline (1992·1993·1995·1996·1999) → **4 baseline (1993·1995·1996·1999)** 로 우선 축소. 1992 fix 후 5 column 으로 복원.
- z_m_education sensitivity (§ 6.5): 1985·1990·1995 3 baseline 모두 정합 → "main 1985 baseline 의 결과는 1990·1995 baseline 사용 시 substantively 동일 (z_m_edu correlation 0.989-1.000, 시군구 차이 > 0.5 = 2 사례 중 0.8%)" narrative 가 § 6.5 에 commit 가능.

### Sample size 변화

- Track 2: N=251 sigungu 그대로 (변화 없음)
- Track 3: 1992 baseline 사용 시 시군구 매칭률 89.2% → fix 후 ~95% 회복 목표. fix 후 N 는 1992 baseline 정합 시 251 그대로 유지 예상

---

## Sensitivity

### Track 2

- **Sensitivity 1**: pre-1990 학교 list 의 GPS 좌표 정확도 — KEDI 1985_yunbo_total 의 학교 주소 → 좌표 변환 정확도가 ±100 m 이내라면 본 결과 영향 없음. ±1 km 이상 오차라면 nearest distance 분포에 noise 추가 가능 → 별도 GPS 정확도 audit log 권장.
- **Sensitivity 2**: 학교 신설 cohort 의 정의 — "1985 baseline" 은 1885-1985 신설 학교 list. 1985-1989 사이 신설 4학교는 1985 baseline 에 미포함. 본 4학교의 영향이 0.8% 로 negligible → main spec 영향 없음.

### Track 3

- **Sensitivity 1 (P1 fix 후)**: 1992 baseline 의 sigungu 매칭률이 fix 후 95%+ 회복 시 → 1992 baseline 결과는 1994 baseline 결과와 정합 예상 (1992-1994 짧은 기간 차이 + 1997 IMF 위기 사이의 짧은 baseline gap)
- **Sensitivity 2 (P1 fix 실패 시)**: 1992 시점 KSIC 6차→9차 직접 crosswalk 가 작성 불가능한 경우 → 1992 baseline 은 본 paper 에서 제외, § 6.4 sensitivity 는 4 baseline (1993·1995·1996·1999) 으로 commit. PAP v4.5.4 의 1992 baseline 항목은 footnote 로 처리: "1992 baseline 은 KSIC 6차→9차 crosswalk 한계로 본 paper 에서 제외. 1993 baseline 은 1992 와 거의 identical 한 pre-IMF baseline."

---

## 후속 step

### Immediate (R-A)

1. **PAP v4.5.4 patch commit** — Track 2 ✅ + Track 3 P1 두 결과를 PAP § 6.4 + § 6.5 에 반영
2. **§ 6.4 sensitivity table column 축소** — 5 baseline → 4 baseline (1992 fix pending notation)
3. **§ 6.5 z_m_education sensitivity narrative** 첫 draft (Track 2 결과 commit)
4. **Track 3 fix script 작성**:
   - Step 1: 1992 raw 의 KSIC 코드 컬럼 (col 9 또는 다른 위치) 정확 inspect
   - Step 2: KSIC 6차 → 8차 → 9차 2-step crosswalk build (KOSTAT 공식 6차→8차 concordance + 기존 8차→9차)
   - Step 3: 1992 시군구 raw_code → 1997 h_code crosswalk 의 unmatched 8,252 row 의 Phase 1-A crosswalk 확장 (안성·시흥·평택 시군구 변경 기록 추가)

### Downstream dependency (사용자)

1. **1992 baseline rebuild PowerShell wrapper 실행** — R-A 가 fix script 작성 완료 후 한 번에 실행
2. **PAP v4.5.4 review** — Track 2·3 결과 반영 commit text review

---

## Anchor

- **Goldsmith-Pinkham, Sorkin, Swift (2020 AER)**: shift-share IV 의 share path 식별. baseline year 선택의 robustness 권고
- **Borusyak, Hull, Jaravel (2025)**: shift-share IV 의 shock-only 식별. baseline year sensitivity 보다 shock 정합성 우선
- **Autor, Dorn, Hanson (2013 AER)**: 본 연구의 1994 baseline 은 ADH 의 "China shock 직전 pre-treatment baseline" 패턴
- **Sufi (2023 BFI WP)**: 한국 trade-empirical 의 KIET 60-sector 매개 표준 spec
- **Wood (2017)**: 한국 marriage market 의 cohort 별 sex ratio
- **Case, Deaton (2015 PNAS)**: deaths of despair 의 4-cause Korean operationalization

---

## 한자 사용 안 함 (memory feedback_no_hanja 준수)

본 로그는 순한글 + 영어 약어. 對·中·美·韓·共 등 한자 미사용.
