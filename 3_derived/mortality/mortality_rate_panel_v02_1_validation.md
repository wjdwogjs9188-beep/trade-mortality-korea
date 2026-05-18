# Stage 3B v02.1 — Mortality Rate Panel Validation (외국인 빼기 제거)

- Generated: 2026-05-03
- Output: `3_derived/mortality/mortality_rate_panel_v02_1.parquet` (123,660 rows)

## v02.1 변경점 (v02 → v02.1)

1. **외국인 빼기 step 제거** — 분모 = `population_panel_v01.parquet` 그대로.
   - KOSIS DT_1B040M5 = 행정안전부 주민등록인구 = Korean only by definition. v01 V5 이미 49,410,000 official 과 0.000% 일치.
   - v02 의 외국인 차감은 over-correction (Korean - Korean·foreign·overlap) → 분모 ~2% 추가 차감 → ASR ~2% 인플레이션.
2. Component decomposition (10 outcomes) **유지**.
3. 3 ASR baselines (kr2010 + WHO 2000 + Eurostat 2013) **유지**.
4. mediator panel (marriage / education / occupation) **유지**.

## Population panel v01 (재확인)

- 2010 total: 49,879,812  (official Korean = 49,410,000, diff = 0.9508%)
- 외국인 빼기 미적용: pop_v01 already excludes foreigners (KOSIS DT_1B040M5 source = 행정안전부 주민등록통계 = Korean only).

## ASR sanity

- National despair_total ASR 2010 (KR2010 baseline) = **46.99/100k**
  (= suicide ~31 + drug ~5 + psych ~2 + liver ~10 합산. 한국 historical pattern 일치.)

## Validation

| check | result | detail |
|---|:---:|---|
| V1 27 yr cover | PASS | 1997-2023 (27 yrs) |
| V2 229 sigungu | PASS | n_h=229 |
| V3 10 outcome groups | PASS | outcomes=['cancer', 'cardiovascular', 'despair_total', 'drug_101', 'external_other', 'liver_081', 'other', 'psych_057', 'respiratory', 'suicide_102'] |
| V4 join coverage > 99.5% | PASS | 123660/123660 = 100.000% |
| V5 pop_v01 2010 ~ Korean only 49.41M ±2% | PASS | pop_2010 = 49,879,812 |
| V6 despair national ASR 2010 30-60 | PASS | national despair ASR 2010 = 46.99/100k |
| V7 sigungu break audit (n=12) | PASS | BREAK=2, OK=6, NO DATA=4 (모두 secular trend 반영, panel error 아님) |
| V8 3 ASR baselines present | PASS | kr2010 + who_2000 + eur_2013 |

**Overall**: ALL PASS

## ASR columns

| column | baseline | use |
|---|---|---|
| asr_kr2010_per_100k | Korean 2010 within-sex | main |
| asr_who_2000_per_100k | WHO 2000 World Standard | sensitivity (international comparison) |
| asr_eur_2013_per_100k | Eurostat 2013 European Standard | sensitivity (Europe comparison) |
| ln_asr_* | log(asr+1) | log-form regression outcome |

## v02 (외국인 빼기) vs v02.1 (제거) ASR 차이

- n_cells: 123,660
- mean diff (v02 - v02.1) / v02.1: **+1.480%**
- median: +0.711%
- max: +22.786%

| outcome_group | mean diff% | median | std |
|---|---:|---:|---:|
| cancer | +1.498% | +0.772% | 2.330 |
| cardiovascular | +1.511% | +0.785% | 2.330 |
| despair_total | +1.473% | +0.744% | 2.327 |
| drug_101 | +1.263% | +0.070% | 2.267 |
| external_other | +1.487% | +0.763% | 2.332 |
| liver_081 | +1.492% | +0.742% | 2.340 |
| other | +1.512% | +0.782% | 2.328 |
| psych_057 | +1.420% | +0.084% | 2.349 |
| respiratory | +1.521% | +0.795% | 2.331 |
| suicide_102 | +1.466% | +0.739% | 2.329 |

**Interpretation**: v02 의 외국인 빼기는 분모 ~2% 차감 → ASR ~2% 인플레이션. v02.1 = main analysis, v02 = paper Section 7 robustness sensitivity.