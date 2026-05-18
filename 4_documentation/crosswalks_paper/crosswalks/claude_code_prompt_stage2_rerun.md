# Claude Code Prompt — Stage 2 사망 panel 재실행 (v4)

## 작업 목적

기존 Stage 2 산출물에 두 가지 문제 발견 → 삭제 후 재실행.

**문제 1**: 2023 file 이 partial (262,710 records, 1-9월 + 10월 일부) 이었음. 사용자가 full version (352,511 records, 1-12월) 으로 교체 완료.

**문제 2**: Cancer 정의 (027-048) 가 KOSIS 공식 "악성신생물(C00-C97)" 보다 +1.5% 큼. 코드 048 (양성신생물 + 행동양식 불명) 을 제외해서 027-047 로 narrow.

## 작업 단계

### Step 1: 기존 산출물 삭제

다음 파일 삭제 (Stage 2 v3 산출물):
```
3_derived/mortality/mortality_panel_v01.parquet
3_derived/mortality/mortality_microdata_combined.parquet
3_derived/mortality/unmatched_mortality.parquet
3_derived/mortality/mortality_panel_validation.md
```

### Step 2: Stage 2 코드 수정

`2_scripts/build_panel/2A_mortality_panel.py` 에서:

```python
# Before
OUTCOME_PRIORITY = [
    ("despair_total", {"102", "101", "057", "081"}),
    ("cardiovascular", {"067", "068", "069", "070"}),
    ("cancer", {f"{i:03d}" for i in range(27, 49)}),       # 027..048
    ("respiratory", {f"{i:03d}" for i in range(73, 79)}),   # 073..078
    ("external_other", {"097", "098", "099", "100", "103", "104"}),
]

# After (cancer 가 027-047 로 narrow)
OUTCOME_PRIORITY = [
    ("despair_total", {"102", "101", "057", "081"}),
    ("cardiovascular", {"067", "068", "069", "070"}),
    ("cancer", {f"{i:03d}" for i in range(27, 48)}),       # 027..047 (악성신생물만, C00-C97)
    ("respiratory", {f"{i:03d}" for i in range(73, 79)}),   # 073..078
    ("external_other", {"097", "098", "099", "100", "103", "104"}),
]
```

코드 048 (양성신생물) 은 자동으로 "other" 그룹으로 흡수.

### Step 3: Stage 2 전체 재실행

기존 코드의 모든 logic 그대로 (mutual exclusivity priority, 7 검증, KOSIS unit comparison 등). cancer set 만 변경.

### Step 4: 추가 검증 — KOSIS 공식 통계 cross-check (cancer)

KOSIS "악성신생물(C00-C97)" 전국 사망자 공식 통계와 panel cancer 합 비교:

```python
KOSIS_CANCER_OFFICIAL = {
    "1998": 51291,
    "2000": 58197,
    "2005": 65529,
    "2010": 72048,
    "2015": 76855,
    "2020": 82204,
    "2023": 85271,  # 2023 full version 으로 교체된 후 정확히 측정
}
```

각 연도 panel cancer 합 vs official 비교. **±0.5% 이내** 합격 (이전 +1.5% bias 가 사라져야 함).

### Step 5: 추가 검증 — 2023 record 수

2023 microdata 의 record 수가 약 **352,500 ± 1%** 인지 확인 (이전 partial 262,710 → full 352,511 변경).

Per-year processing summary 표에서 2023 의 n_in 이 약 352,511 인지 확인.

### Step 6: validation report 갱신

`mortality_panel_validation.md` 새로 작성. 기존 7 검증 + 추가 검증 (cancer cross-check, 2023 record 수) 모두 PASS 여부 보고.

## Expected 결과

- microdata combined: 약 7,300,000 records (이전 7,209,019 + 2023 추가 90k = 약 7.3M)
- Panel cells: 1,483,920 (변화 없음, dimensions 동일)
- Cancer 합 변화:
  - 2010: 73,146 → ~72,000 (KOSIS 72,048 와 ±0.5% 일치 예상)
  - 2020: 83,771 → ~82,200 (KOSIS 82,204 와 ±0.5% 일치 예상)
  - 2023: 65,497 → ~85,000 (KOSIS 85,271 와 ±0.5% 일치 예상)
- "other" 그룹: 048 추가 흡수로 약간 증가 (이전 29.12% → 약 30%)
- 자살 cross-check ±0.06% 유지

## 결과 검토

다음 5가지 본인이 직접 검증:

1. 2023 record 수 ~352,500 (full version 채택 확인)
2. Cancer KOSIS cross-check 7개 연도 모두 ±0.5% 이내
3. 자살 cross-check 4개 연도 ±0.5% 유지
4. Mutual exclusivity PASS (중복 0건)
5. 0 cell 비율 약간 변화 (cancer 가 줄어서 미세 변화)

위 5개 OK 면 Stage 2 v4 채택. 다음 step (Stage 3 인구 panel) 으로 진행.

---

이 prompt 를 Claude Code 에 그대로 전달.
