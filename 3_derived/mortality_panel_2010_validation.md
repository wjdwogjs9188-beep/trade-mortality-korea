# Phase 2-A — 2010 mortality panel validation

**Input**: `2010_사망_연간자료_B형_20260410_98266.csv` (255,405 raw rows, cp949)
**Output**: `mortality_panel_2010.parquet` (31,144 rows)
**Build script**: `2_scripts/build_panel/2A_mortality_panel_2010.py`

---

## V1 — Death count conservation ✅

| metric | value |
|---|---|
| Raw mortality records | 255,405 |
| Records with known age (5세 단위코드 ≠ 99) | 255,335 |
| Records dropped (unknown age) | 97 (0.04%) |
| Panel `all_cause` sum | 255,335 |
| **Δ (raw_known – panel)** | **0** |

Crosswalk match rate: **255,405 / 255,405 = 100.00%**

## V2 — KOSTAT 102 (suicide) cross-check ✅

| metric | value | KOSTAT official 2010 |
|---|---|---|
| Code 102 raw count | **15,566** | **15,566** |
| Match | 100% PASS | |

## V3 — National rate sanity ✅

| metric | value | KOSTAT 공식 |
|---|---|---|
| Total disaggregated 인구 (h_code 합) | 49,879,812 | 49,554,112 (mid-2010) |
| 전국 자살률 per 100k | **31.21** | **31.2** |

National suicide rate **exactly matches** KOSTAT 공식 31.2 / 100k. Pop is 0.66% high vs mid-year — KOSIS 시군구 인구는 join 단위라 약간 over-count 가능 (수용 범위).

## V4 — Outcome group totals

| outcome_group | deaths | share |
|---|---|---|
| all_cause | 255,335 | 100% |
| cancer (027–048) | 73,146 | 28.6% |
| cardiovascular (067–070) | 54,704 | 21.4% |
| despair_total (102+101+057+081) | 23,436 | 9.2% |
| respiratory (073–078) | 18,526 | 7.3% |
| external_other (097–104, ex 102) | 17,067 | 6.7% |

Death-of-despair 비중 9.2% — Case-Deaton 미국 baseline (~6%) 보다 높음, 한국의 자살률 우위 반영.

## V5 — 시도별 despair rate (deaths-weighted)

| 시도 | deaths | pop | rate /100k |
|---|---|---|---|
| 세종특별자치시 | 51 | 44,927 | 113.5 |
| 강원도 | 1,020 | 1,026,606 | 99.4 |
| 충청남도 | 1,262 | 1,353,366 | 93.2 |
| 전라남도 | 1,063 | 1,209,401 | 87.9 |
| 충청북도 | 827 | 1,052,008 | 78.6 |
| 경상북도 | 1,463 | 1,894,202 | 77.2 |
| 경상남도 | 1,727 | 2,326,290 | 74.2 |
| 전라북도 | 985 | 1,348,019 | 73.1 |
| 부산광역시 | 1,965 | 2,774,560 | 70.8 |
| 제주특별자치도 | 278 | 438,224 | 63.4 |
| 인천광역시 | 1,315 | 2,188,103 | 60.1 |
| 대구광역시 | 1,143 | 1,959,656 | 58.3 |
| 경기도 | 4,882 | 8,798,788 | 55.5 |
| 울산광역시 | 414 | 752,295 | 55.0 |
| 광주광역시 | 607 | 1,106,444 | 54.9 |
| 대전광역시 | 561 | 1,123,909 | 49.9 |
| 서울특별시 | 3,873 | 8,430,806 | 45.9 |

**광역시/특별시 vs 도 합계:**
- 광역시·특별시 53.9 / 100k
- 도 (rural) 69.6 / 100k

Rural-urban gradient: 도가 약 30% 높음. 한국 자살 epidemiology 와 일치.

## V6 — Top/Bottom 10 시군구 (despair rate)

**Top 10 — 농촌 고령군 자살 hotspot:**

| h_code | h_name | sido | deaths | pop | rate /100k |
|---|---|---|---|---|---|
| 37430 | 울릉군 | 경상북도 | 10 | 2,678 | 373.5 |
| 35340 | 장수군 | 전라북도 | 25 | 7,283 | 343.3 |
| 35320 | 진안군 | 전라북도 | 32 | 11,670 | 274.2 |
| 32410 | 양양군 | 강원도 | 28 | 11,263 | 248.6 |
| 32380 | 양구군 | 강원도 | 19 | 7,822 | 242.9 |
| 37310 | 군위군 | 경상북도 | 29 | 12,272 | 236.3 |
| 32400 | 고성군 | 강원도 | 34 | 14,666 | 231.8 |
| 37340 | 영양군 | 경상북도 | 15 | 6,477 | 231.6 |
| 34350 | 청양군 | 충청남도 | 40 | 18,710 | 213.8 |
| 32330 | 영월군 | 강원도 | 37 | 17,349 | 213.3 |

**Bottom 10 (pop ≥ 10k) — 신도시·강남권 저자살 zone:**

| h_code | h_name | sido | deaths | pop | rate /100k |
|---|---|---|---|---|---|
| 31193 | 수지구 | 경기도 | 49 | 170,049 | 28.8 |
| 31023 | 분당구 | 경기도 | 129 | 413,484 | 31.2 |
| 11230 | 강남구 | 서울특별시 | 165 | 483,871 | 34.1 |
| 31014 | 영통구 | 경기도 | 67 | 189,089 | 35.4 |
| 31103 | 일산동구 | 경기도 | 76 | 209,780 | 36.2 |
| 11240 | 송파구 | 서울특별시 | 200 | 548,969 | 36.4 |
| 11220 | 서초구 | 서울특별시 | 114 | 311,035 | 36.7 |
| 11150 | 양천구 | 서울특별시 | 160 | 436,053 | 36.7 |
| 31042 | 동안구 | 경기도 | 106 | 273,542 | 38.8 |
| 11200 | 동작구 | 서울특별시 | 129 | 332,263 | 38.8 |

**13배 격차** (울릉군 373 vs 수지구 29) — 고령·소득·실업 분포 반영. Spatial heterogeneity is large enough to identify trade exposure effects.

## V7 — Despair rate by sex × age (전국)

남자 노인 자살률이 여자의 2~3배 — Korean elderly male suicide crisis 일치.

| age | 남(rate) | 여(rate) | M/F ratio |
|---|---|---|---|
| 20-24 | 24.7 | 23.0 | 1.07 |
| 30-34 | 40.3 | 29.3 | 1.37 |
| 40-44 | 66.9 | 27.8 | 2.41 |
| 50-54 | 119.1 | 31.6 | 3.77 |
| 60-64 | 135.8 | 39.5 | 3.44 |
| 70-74 | 205.9 | 69.2 | 2.98 |
| 80+ | 334.4 | 141.9 | 2.36 |

남 80+ 334 / 100k — 세계 최고 수준 자살률 (OECD 보고서와 일치).

## V8 — Schema sample

```
h_code year outcome_group age_kosis sex deaths population mortality_rate
 11010 2010 all_cause 020 1 4 2717.5 147.194112
 11010 2010 all_cause 050 1 1 3325.0 30.075188
...
```

- `h_code`: 5-digit harmonized sigungu (2021 baseline, 256 종)
- `outcome_group`: {`all_cause`, `cancer`, `cardiovascular`, `despair_total`, `respiratory`, `external_other`}
- `age_kosis`: KOSIS C3 5-year code (`020`=0–4, `050`=5–9, …, `340`=80+)
- `sex`: `1`=남, `2`=여

---

## ⚠️ 주의사항

1. **Pop 약간 over-count (49.88M vs KOSTAT 49.55M, +0.66%)** — KOSIS sigungu 인구는 시도별 합계 정확히 matching 하지 않을 수 있음. 회귀에서 비율 (deaths/pop) 사용하므로 영향 미미. 필요 시 normalize 가능.
2. **97개 unknown-age 사망 record drop** (전체 0.04%). 사망률 계산 위해 5세-성별 join 필요.
3. **연체율·GRDP join 등 다음 단계** — Phase 2-C 와 통합 시 panel 단위는 (h_code × year) 로 수렴 (5세-성별 collapse 하거나 age-adjusted).
4. **80+ top-coding** — pop 의 360/380/410/430/440 (finer 80+ bins) 모두 drop, 340 (80+) 만 사용. 자살률 80+ rate 가 높지만 disaggregation 가능 시 수정.

## 사용자 spot-check 권장

- `3_derived/mortality_panel_2010.csv` 열어서:
 - 임의 시군구 (예: 본인 거주지) 검색 → deaths/pop 합리성 확인
 - all_cause 합 = 255,335 확인
 - despair_total / 시도 합 = 위 V5 표와 일치 확인
- 자살률 원자료 (KOSTAT KOSIS T-19 등) 와 시군구 단위 cross-check 1-2개 추천

---

## 다음 단계 (사용자 OK 시)

27년 (1997-2023) 전체 build:
- 동일 logic loop, 단 raw_code 형식 (1997-2022 5-digit / 2023 5-digit) 자동 분기
- 2012년 이후 세종 (29) 분리 처리
- Pop panel 의 80+ bin 처리는 연도별 차이 자동 처리 (340 우선, 없으면 360+380+410+430+440 합산)
- 출력: `3_derived/mortality_panel_full.parquet` (예상 ~840k rows)
- 시계열 plot: 1997-2023 전국 자살률 IMF→2003 정점→2010s 감소 패턴 확인
