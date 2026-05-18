# Age Band Semantic Audit (Tier B.4)

- Generated: 2026-05-03

## KOSIS C3 codes (population_combined.csv)

| code | label | included in 17 bands? |
|---|---|:---:|
| 000 | 계 | (=계, 제외) |
| 020 | 0 - 4세 | YES |
| 050 | 5 - 9세 | YES |
| 070 | 10 - 14세 | YES |
| 100 | 15 - 19세 | YES |
| 120 | 20 - 24세 | YES |
| 130 | 25 - 29세 | YES |
| 150 | 30 - 34세 | YES |
| 160 | 35 - 39세 | YES |
| 180 | 40 - 44세 | YES |
| 190 | 45 - 49세 | YES |
| 210 | 50 - 54세 | YES |
| 230 | 55 - 59세 | YES |
| 260 | 60 - 64세 | YES |
| 280 | 65 - 69세 | YES |
| 310 | 70 - 74세 | YES |
| 330 | 75 - 79세 | YES |
| 340 | 80세 이상 | YES |
| 360 | 80 - 84세 | NO |
| 370 | 85세 이상 | NO |
| 380 | 85 - 89세 | NO |
| 410 | 90 - 94세 | NO |
| 430 | 95 - 99세 | NO |
| 440 | 100세 이상 | NO |

## 제외 코드 의미

- `000` = 전체 합계 → 제외 (sum of detailed bands 와 중복)
- `360`, `370`, `380` = 80-84 / 85-89 / 90+ 세부 → **340 (80+) aggregate 와 중복** → 제외
- `410`, `430`, `440` = 90+ 세부 cohort → 340 에 포함됨 → 제외

**Conclusion**: 360+ 코드는 80+ aggregate (340) 의 sub-buckets. 340 만 사용하면 double count 없음 ✅.

## KOSTAT vs KOSIS age band 정합성

| KOSTAT age_5yr_code | KOSIS C3 | 의미 | match? |
|---|---|---|:---:|
| 1 (0세) + 2 (1-4세) | 020 (0-4세) | 합산 일치 | ✅ |
| 3 (5-9세) | 050 | 일치 | ✅ |
|... |... |... | ✅ |
| 17 (75-79세) | 330 | 일치 | ✅ |
| 18 (80-84) + 19 (85-89) + 20 (90+) | 340 (80+) | 합산 일치 | ✅ |

**Conclusion**: Stage 3 panel 의 age_band 매핑 silent error 없음 ✅.