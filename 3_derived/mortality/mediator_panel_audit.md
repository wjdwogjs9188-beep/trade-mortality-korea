# Stage 3C — Individual-Level Mediator Panel Audit

- Generated: 2026-05-03
- Source: `3_derived/mortality/mortality_microdata_combined.parquet`
- Use case: Case-Deaton mediator framework (marriage / education / occupation 별 사망률)

## Marriage status (despair_total 분포 verification)

| marriage_status | label | deaths | share |
|---|---|---:|---:|
| 1 | 미혼 | 128,566 | 22.17% |
| 2 | 유배우자 | 288,225 | 49.71% |
| 3 | 사별 | 83,339 | 14.37% |
| 4 | 이혼 | 76,378 | 13.17% |
| 9 | 미상 | 3,311 | 0.57% |
| **TOTAL** | — | **579,819** | 100% |

## Education code (despair_total 분포)

| education_code | label | deaths | share |
|---|---|---:|---:|
| 1 | 무학 | 57,214 | 9.87% |
| 2 | 초등 | 141,462 | 24.40% |
| 3 | 중등 | 99,266 | 17.12% |
| 4 | 고등 | 180,236 | 31.08% |
| 5 | 대학재학 | 20,420 | 3.52% |
| 6 | 대학졸업 | 59,281 | 10.22% |
| 7 | 대학원 | 5,522 | 0.95% |
| 9 | 미상 | 16,418 | 2.83% |

## Occupation (top 10 KSCO codes, 모든 outcome)

| occupation_code | deaths | share |
|---|---:|---:|
| 13 | 5,368,192 | 68.14% |
| 06 | 859,705 | 10.91% |
| 99 | 457,259 | 5.80% |
| 09 | 311,514 | 3.95% |
| 05 | 293,570 | 3.73% |
| 03 | 164,925 | 2.09% |
| 02 | 133,330 | 1.69% |
| 07 | 112,123 | 1.42% |
| 08 | 80,582 | 1.02% |
| 01 | 59,184 | 0.75% |

**Note**: KSCO 13 = 무직 ~70% dominance → occupation 단독 mediator 효과 약함. 1-12 codes (취업자) restricted-sample analysis 권고.

## Use cases

1. **Marriage gradient**: 미혼/이혼 vs 유배우자 자살률 비교 (Case-Deaton 핵심 finding).
2. **Education gradient**: 학력 high → low 사망률 gradient (한국에서도 미국과 동일 패턴 verify).
3. **Trade × mediator interaction**: trade exposure 가 marriage breakdown / education low 경로로 사망률 증가시키는지 mechanism 분리.
4. **분모 정의**: 분모는 KOSIS 인구 panel + 미시 분포 (KOSIS 가족조사) 별도 join 필요. 본 mediator panel = 분자 only.

## 한계

- 분모 부재: marriage/education 별 사망률 (incident rate) 계산하려면 KOSIS 인구 panel 의 marriage·education 별 인구 분포 별도 다운 필요.
- 1997-1999 일부 microdata 의 occupation_code 결측률 높음 (~5%) — restricted-sample 권고.
- 한국 시군구 단위에서 marriage × education 4-way table 은 cell sparseness 증가 (despair는 자살 13k/year 정도).