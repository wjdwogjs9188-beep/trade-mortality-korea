# R-A 측 wording 권고 form — paper § 6 또는 § 7.1.1 narrative 의 sigungu 정의 명시적 anchor (Finding O cumulative refinement)

**작성**: 2026-05-08 R-A → 정재헌
**대상**: paper § 6 또는 § 7.1.1 narrative 위 sigungu_crosswalk version + 자치구 inclusion 패턴 의 명시적 anchor
**선행**: 2026-05-08 Option B variant audit cycle + 사용자 측 14/32 children inclusion 보강
**Strict workflow anchor**: 사용자 측 paper 본문 commit prerequisite (분업 경계 외)

---

## R-A 직전 turn 의 권고 wording 의 부정확 영역

직전 turn 의 R-A 권고 wording:
> "통합청주시 four autonomous districts (상당구, 서원구, 흥덕구, 청원구) treated as separate h_codes 33041, 33042, 33043, 33044"

actual evidence-based form:
- 청주 4 자치구 중 33041 (상당구) + 33043 (흥덕구) 만 sample inclusion
- 33042 (서원구) + 33044 (청원구) 미포함

직전 권고 wording 이 "all 4 separately" framing 위 actual sample 영역과 정합 안 됨.

## 14/32 children inclusion 패턴 evidence-based form

| 일반시 (parent) | total v1 children | intersection 147 inclusion | 패턴 |
|----------------|------------------:|--------------------------:|------|
| 수원 (31010) | 4 | 3 (영통 31014만 out) | partial |
| 성남 (31020) | 3 | 1 (분당 31023만 in) | partial |
| 안양 (31040) | 2 | 2 | full |
| 안산 (31090) | 2 | 0 | empty |
| 고양 (31100) | 3 | 0 | empty |
| 용인 (31190) | 3 | 0 | empty |
| 청주 (33040) | 4 | 2 (상당 33041, 흥덕 33043) | partial |
| 천안 (34010) | 2 | 0 | empty |
| 전주 (35010) | 2 | 2 | full |
| 포항 (37010) | 2 | 2 | full |
| 창원 (38110) | 5 | 2 (마산합포 38113, 마산회원 38114) | partial |

inclusion source = main 221 ∩ HIRA 168 dropping pattern (자치구 단위 inclusion, parent 시 collapse 영역 미적용).

## R-A 권고 wording (Path A — 자세한, R-A 권고)

> "Throughout this paper, the sigungu unit is defined per sigungu_crosswalk v1, which retains the urban autonomous-district structure of 일반시 (e.g., 청주 상당구 33041 + 흥덕구 33043 are treated as separate h_codes; the 통합청주시 parent collapse to h_code 33040 is **not** applied). The intersection 147 sample includes 14 of 32 v1 autonomous-district children, with the dropping pattern determined by the main 221 and HIRA 168 sample availability. An alternative parent-시 collapse specification (sigungu_crosswalk v2, 229 h_codes, full child-to-parent collapse) is documented in `1_codebooks/crosswalk_merge_report.md` and reserved as a robustness sensitivity for the R&R cycle, where reviewer cross-check on city-level sample consistency may be requested."

## R-A 권고 wording (Path B — 간략)

> "Throughout this paper, the sigungu unit follows sigungu_crosswalk v1 (autonomous-district level, no parent-시 collapse). The intersection 147 sample includes 14 of 32 일반시 autonomous districts, with city-level inclusion being partial in some cases (e.g., 청주 4 districts → 2 in sample). The alternative parent-시 collapse (v2, 229 h_codes) is reserved as a robustness sensitivity for the R&R cycle."

## Severity

**Medium** — substantive sample 정의 consistency. 직전 turn 의 wording 부정확 정정 + KER reviewer cross-check 시 partial-inclusion 패턴의 honest disclosure 영역.

## R-A 권고

Path A (자세한) — 시 단위 일관성 결여의 honest disclosure + R&R cycle 위임 영역의 cumulative carry. 사용자 측 결정 영역.

---

**End of R-A 측 wording 권고 form (Finding O 보강 cumulative refinement)**
