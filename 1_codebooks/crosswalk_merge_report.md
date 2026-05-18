# Crosswalk Merge Report — 일반시 자치구 → Parent 시 collapse

- Generated: 2026-05-02
- Source: `1_codebooks/sigungu_crosswalk.csv`
- Output: `1_codebooks/sigungu_crosswalk_v2.csv`
- Mapping table: `1_codebooks/child_to_parent_mapping.csv`

## Summary

| metric | before | after | delta |
|---|---:|---:|---:|
| total rows | 6,723 | 6,723 | +0 |
| distinct h_code | 256 | 229 | -27 |
| distinct raw_code | 362 | 362 | +0 |
| child rows reassigned | — | 695 | — |

## Collapse policy

- **Collapsed**: 일반시 자치구 (광역시 외) — children sharing a parent 시 prefix.
- **Untouched**: 광역시 자치구 (sido 11/21/22/23/24/25/26), 세종, 강원/충남/전남/제주 일반시.
- 새 parent h_code 5건 (수원 31010, 성남 31020, 안양 31040, 전주 35010, 포항 37010) — pre-collapse 에는 raw_code 로도, h_code 로도 등장하지 않음 → child raw_code 이 parent h_code 로 합쳐지면서 신규 도입.
- 기존 parent h_code 6건 (안산 31090, 고양 31100, 용인 31190, 청주 33040, 천안 34010, 창원 38110) — 이미 v1 에 존재하나 일부 연도만 커버 → collapse 후 27 년 전체 커버.

## Child → parent mapping (32 children, 11 parents)

| child h_code | child name | parent h_code | parent name | parent was new |
|---:|---|---:|---|:---:|
| 31011 | 장안구 | 31010 | 수원시 | ✓ |
| 31012 | 권선구 | 31010 | 수원시 | ✓ |
| 31013 | 팔달구 | 31010 | 수원시 | ✓ |
| 31014 | 영통구 | 31010 | 수원시 | ✓ |
| 31021 | 수정구 | 31020 | 성남시 | ✓ |
| 31022 | 중원구 | 31020 | 성남시 | ✓ |
| 31023 | 분당구 | 31020 | 성남시 | ✓ |
| 31041 | 만안구 | 31040 | 안양시 | ✓ |
| 31042 | 동안구 | 31040 | 안양시 | ✓ |
| 31091 | 상록구 | 31090 | 안산시 | |
| 31092 | 단원구 | 31090 | 안산시 | |
| 31101 | 덕양구 | 31100 | 고양시 | |
| 31103 | 일산동구 | 31100 | 고양시 | |
| 31104 | 일산서구 | 31100 | 고양시 | |
| 31191 | 처인구 | 31190 | 용인시 | |
| 31192 | 기흥구 | 31190 | 용인시 | |
| 31193 | 수지구 | 31190 | 용인시 | |
| 33041 | 상당구 | 33040 | 통합청주시 | |
| 33042 | 서원구 | 33040 | 통합청주시 | |
| 33043 | 흥덕구 | 33040 | 통합청주시 | |
| 33044 | 청원구 | 33040 | 통합청주시 | |
| 34011 | 동남구 | 34010 | 천안시 | |
| 34012 | 서북구 | 34010 | 천안시 | |
| 35011 | 완산구 | 35010 | 전주시 | ✓ |
| 35012 | 덕진구 | 35010 | 전주시 | ✓ |
| 37011 | 남구 | 37010 | 포항시 | ✓ |
| 37012 | 북구 | 37010 | 포항시 | ✓ |
| 38111 | 의창구 | 38110 | 통합창원시 | |
| 38112 | 성산구 | 38110 | 통합창원시 | |
| 38113 | 마산합포구 | 38110 | 통합창원시 | |
| 38114 | 마산회원구 | 38110 | 통합창원시 | |
| 38115 | 진해구 | 38110 | 통합창원시 | |

## Validation

| check | result | detail |
|---|:---:|---|
| V1 row count preserved | PASS | in=6723 out=6723 |
| V2 raw_code preserved (no drops) | PASS | in=362 out=362 |
| V3 h_code count delta matches expected | PASS | in=256 out=229 delta=-27 expected=-27 (children=32 new_parents=5) |
| V4 collapsed parents balanced over all years | PASS | all 11 parents 1997-2023 |
| V5 광역시 자치구 untouched (강남구 spot) | PASS | identical=True |
| V5b 광역시 rows fully unchanged | PASS | all 7 metro sidos rows identical=True |
| V6 세종 untouched | PASS | identical=True |

**Overall**: ALL PASS

## Spot checks

| label | source h_code | expected | actual | result |
|---|---:|---:|---:|:---:|
| 고양 덕양구 → 고양시 | 31101 | 31100 | 31100 | PASS |
| 창원 의창구 → 통합창원시 | 38111 | 38110 | 38110 | PASS |
| 창원 마산합포구 → 통합창원시 | 38113 | 38110 | 38110 | PASS |
| 청주 상당구 → 통합청주시 | 33041 | 33040 | 33040 | PASS |
| 포항 남구 → 포항시 | 37011 | 37010 | 37010 | PASS |
| 서울 강남구 → 변경 없음 (광역시 자치구) | 11230 | 11230 | 11230 | PASS |
| 부산 해운대구 → 변경 없음 (광역시 자치구) | 21090 | 21090 | 21090 | PASS |

## Notes

1. raw_code 는 **건드리지 않음**. h_code 와 h_name 만 child → parent 로 재할당. event_note 에 `subdistrict_collapsed_to_parent_2026-05-02` 추가.
2. mapping_weight 컬럼은 v1 에 없음 (모든 매핑 1:1). 추후 필요시 별도 추가.
3. 통합창원시 38110 의 마산합포/마산회원구 (38113/38114) 는 1997-2009 에도 raw 38021/38022 로 등장 → collapse 후 raw 38010 (창원 舊), 38020 (마산), 38040 (진해), 38021/38022 (마산 자치구) 모두 h_code 38110 로 합산됨. 통합창원시 = 창원+마산+진해 전 영역으로 해석 일관.
4. 통합청주시 33040 의 raw 33310 (청원군, 1997-2013) 도 기존부터 33040 으로 매핑되어 있어 그대로 유지. collapse 후 청주시 = 상당+서원+흥덕+청원 전 영역.
5. **다음 panel build (사망/인구/산업) 에서는 이 v2 crosswalk + child_to_parent_mapping.csv 를 함께 적용**해야 KOSTAT raw 의 자치구 단위 record 가 parent 시 단위로 올바르게 합산됨.
