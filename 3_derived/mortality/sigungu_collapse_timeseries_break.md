# Sigungu Collapse Timeseries Break Audit (Tier B.6)

- Generated: 2026-05-03
- Method: 분구·통합 직전 5년 vs 직후 5년 평균 ASR (despair_total, KR2010 baseline) 비교.
- Threshold: |Δ%| > 20% → BREAK 의심 (raw_code aggregation 또는 외부 shock).

## 11 collapse cases

| h_code | city | split_year | pre5_asr | post5_asr | diff% | flag |
|---|---|---:|---:|---:|---:|:---:|
| 31050 | 부천시 | 2016 | 41.39 | 36.92 | -10.80% | OK |
| 33040 | 청주시 | 2014 | 46.32 | 37.59 | -18.85% | OK |
| 38110 | 창원시 | 2010 | 47.21 | 37.73 | -20.07% | BREAK |
| 31100 | 고양시 | 2005 | 40.54 | 32.65 | -19.45% | OK |
| 31110 | 수원시 | 2003 | 31.83 | 26.65 | -16.27% | OK |
| 31130 | 성남시 | 1989 | — | — | — | NO DATA |
| 31170 | 안양시 | 1992 | — | 46.72 | — | NO DATA |
| 31190 | 안산시 | 2002 | 61.63 | 40.30 | -34.61% | BREAK |
| 31460 | 용인시 | 2005 | — | — | — | NO DATA |
| 34010 | 천안시 | 2008 | 52.27 | 51.68 | -1.14% | OK |
| 35010 | 전주시 | 1989 | — | — | — | NO DATA |
| 37010 | 포항시 | 1995 | — | 57.21 | — | NO DATA |

**Summary**: BREAK=2 | OK=5 | NO DATA=5

## 해석

- `OK` (|Δ%| ≤ 20%): h_code aggregation 이 raw_code 변경을 완전 흡수 → panel 시계열 연속성 ✅.
- `BREAK` (|Δ%| > 20%): 분구·통합 직후 ASR 가 ±20% 초과 변동. raw_code → h_code aggregation 누락 가능 OR 외부 shock (예: 2010 정책 변화).
- `NO DATA`: 분구가 panel 시작 (1997) 이전 → pre/post 5년 비교 불가능 (성남 1989, 안양 1992, 전주 1989, 포항 1995).

**참조**: 수원·성남·안양·안산·고양·용인·천안·전주·포항 일반구 분구는 행정구역 (geographic) 변경. h_code = 시 단위 (parent) 이라 자치구 분리 후 panel cell 합 = 시 전체 → 시계열 연속.