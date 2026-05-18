# Claude Code Prompt — 시군구 Crosswalk 분구 자치구 → Parent 통합

## 작업 목적

기존 sigungu_crosswalk.csv 의 250 baseline h_codes 에서 **자치구 분구 사례를 parent 시 단위로 collapse** 한다. 본 paper 의 panel 분석 (5-year stacked first-difference) 에서 시계열 일관성 (balanced panel) 을 보장하기 위함이다.

KOSTAT 2021 사망 microdata 가 250 sigungu code 로 분구 children 단위로 기록 (예: 31101 고양시 덕양구, 31103 일산동구, 31104 일산서구) 되는데, 분구 이전 (1997-2004) 에는 parent (31100 고양시) 만 있어서 unbalanced panel 이 됩니다. children → parent merge 로 모든 연도에 동일 단위 유지.

## 입력 파일

1. **`crosswalks/sigungu_crosswalk.csv`** — 현재 crosswalk
   - 컬럼 추정: year, raw_code, h_code, h_name, sido_code, sido_name, event_note (또는 유사)
   - 6,723 rows, 250 distinct h_codes
   - 본인이 만든 ground truth 매핑

2. **`crosswalks/sigungu_changes_history.md`** — 행정구역 변경 이력
   - 111 이벤트 (1997-2023)
   - 통합/분구/명칭변경/승격 분류

3. **`docs/h_code_policy.md`** (있으면) — h_code 정의 정책 6개 항목

## 출력 파일

1. **`crosswalks/sigungu_crosswalk_v2.csv`** — 분구 자치구 collapse 후 새 crosswalk
   - 같은 schema (year, raw_code, h_code, h_name, ...)
   - h_code 가 parent 시 단위로 통합됨
   - 예상 distinct h_code 수: 약 240 (250 - 분구 child 수 + 일부 회수)

2. **`crosswalks/crosswalk_merge_report.md`** — 진단 보고서
   - Before/after baseline h_code count
   - Child → parent 매핑 list (어느 자치구가 어느 시로 합쳐졌는지)
   - 검증 결과 (모든 raw_code 가 매핑됨, 새 h_code 가 모든 연도에 존재)

3. **`crosswalks/child_to_parent_mapping.csv`** — 자치구→parent 매핑 lookup table
   - child_h_code, child_h_name, parent_h_code, parent_h_name
   - 추후 다른 panel (사망, 인구, 산업 census) 처리 시 동일 logic 적용용

## 처리 단계

### Step 1: 자치구 분구 사례 식별

`sigungu_changes_history.md` 에서 다음 패턴의 이벤트 추출:
- "분구", "자치구 신설", "자치구 분리"
- "통합 [시] 출범" 후 자치구 5개 이상 가진 시 (마창진, 통합청주 등)

알려진 사례 (참고용, history.md 가 ground truth):
- **고양시 31100** → 덕양구 31101, 일산동구 31103, 일산서구 31104 (2005년 분구)
- **수원시 31010** → 장안/권선/팔달/영통구 (자치구 4개)
- **성남시 31020** → 수정/중원/분당구 (자치구 3개)
- **안양시 31040** → 만안/동안구 (자치구 2개)
- **부천시** → 원미/소사/오정구 (2016년 폐지) — 폐지 후 다시 부천시로 통합
- **통합 창원시 38110** (2010) → 의창/성산/마산합포/마산회원/진해구 (자치구 5개)
- **통합 청주시 33010** (2014) → 상당/서원/흥덕/청원구 (자치구 4개)
- **포항시 37010** → 남구/북구
- **전주시 35010** → 완산구/덕진구
- **광역시 자치구** (서울 25, 부산 16, 대구 8, 인천 10, 광주 5, 대전 5, 울산 5) — **이건 제외**. 광역시 자치구는 독립 panel 단위로 유지 (이미 KOSTAT 표준).

→ **collapse 대상**: 일반시 (특별시·광역시 외) 의 자치구만. 광역시 자치구는 그대로 유지.

### Step 2: Child → Parent 매핑 구축

각 collapse 대상 시에 대해:
- Parent h_code 결정: 통합 시점 또는 가장 이른 연도의 시 단위 h_code
- Children h_codes: 자치구 단위 h_codes
- 매핑: child h_code → parent h_code, child h_name → parent h_name

매핑 조건 명시:
- 광역시 자치구는 collapse X (독립 유지)
- 일반시 자치구는 collapse O
- 이미 시 단위인 곳은 변경 없음

### Step 3: Crosswalk 수정

기존 sigungu_crosswalk.csv 의 모든 row 에 대해:
- 자치구 child h_code 인 경우: parent h_code 로 변경 + h_name 도 parent 로 변경
- 일반시 / 군 / 광역시 자치구 / 세종시: 변경 없음

mapping_weight 컬럼이 있으면 모두 1.0 유지 (분구는 weight 없음).

### Step 4: 검증

다음 항목 확인 + 보고서 기록:
1. **Before/after distinct h_code count**: 250 → 약 240 (예상)
2. **Raw_code 매핑 완전성**: 모든 raw_code 가 새 h_code 에 매핑됨 (drop 없음)
3. **연도별 baseline 일관성**: 1997-2023 모든 연도에 collapsed h_code 가 등장하는지 (시계열 balanced)
4. **광역시 자치구 보존 확인**: 서울 강남구, 부산 해운대구 등이 그대로 독립 h_code 인지
5. **세종시 (29110) 처리**: 2012 이후 등장, 2012 이전 raw 데이터의 연기군/공주시 일부 매핑 확인

### Step 5: Sample spot check

다음 known mapping 검증 (5개):
- 31101 (고양 덕양구) → 31100 (고양시) ?
- 38110 자치구 5개 → 38110 (통합 창원시) ?
- 33010 자치구 4개 → 33010 (통합 청주시) ?
- 37010 (포항 남구), 37011 (포항 북구) → 37010 (포항시) ?
- 11680 (서울 강남구) → 변경 없음 (광역시 자치구) ?

## 진단 보고서 (`crosswalk_merge_report.md`) 구성

```markdown
# Crosswalk Merge Report — Children to Parent

## Summary
- Before: 250 distinct h_codes
- After: [N] distinct h_codes
- Reduction: [N] (자치구 분구 collapse)

## Child → Parent Mapping
| Parent h_code | Parent h_name | Children h_codes (collapsed) |
|---|---|---|
| 31100 | 고양시 | 31101 덕양, 31103 일산동, 31104 일산서 |
| 38110 | 통합창원시 | 38111 의창, 38112 성산, 38113 마산합포, ... |
| ... | ... | ... |

## Validation
- Raw_code 매핑 완전성: PASS / FAIL (어떤 raw_code 가 unmapped 인가)
- 연도별 balance: PASS / FAIL (어느 연도에 baseline 결손)
- 광역시 자치구 보존: PASS / FAIL
- 세종시 처리: PASS / FAIL

## Sample Spot Check
| raw_code | year | new h_code | new h_name | expected | result |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | OK |
```

## 주의 사항

1. **Raw 파일 절대 수정 X**: 기존 sigungu_crosswalk.csv 는 read-only. 새 v2 파일만 산출.
2. **광역시 자치구 처리 confusion 금지**: 서울 강남구 (11680), 부산 해운대구 (26350) 등은 collapse 대상 아님. 이미 표준 단위.
3. **세종시**: 2012 이후 신설. 2012 이전 raw 데이터가 어디 매핑되는지 (연기군 33910? 공주시 33020?) 는 sigungu_changes_history.md 의 결정 따름.
4. **encoding**: cp949 raw 데이터 처리 시 utf-8 변환 일관 적용.
5. **검증 우선**: validation 한 가지라도 FAIL 이면 commit 하지 말고 사용자에게 보고.

## 결과 검토 후 사용자 확인 필요

1. Before/after h_code count (예상 250 → 약 240)
2. Child → Parent 매핑 list 검토 (광역시 자치구가 collapse 안 됐는지 sanity check)
3. Validation 4개 모두 PASS 인지
4. Spot check 5개 모두 expected 와 일치하는지

위 4가지 OK 면 새 crosswalk_v2 채택. 다음 step 으로 panel_construction_execution_guide Stage 2 (사망 panel build) 진행.

---

이 prompt 를 Claude Code 에 그대로 전달. 산출물은 `crosswalks/` 폴더에 저장.
