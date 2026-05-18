# mediator_panel v02 validation

## Decisions applied
- 1990 drop (행정구역 mismatch)
- age filter: working-age 25-64 (DGHP 2017 mediation 표준)
- education 4 카테고리: NoHS/HS/SomeCollege/Bachelor+
- sigungu_crosswalk_v2 적용 (mortality panel v02_1 align)

## Marriage panel summary
- rows: 71,125
- years: [np.int64(1995), np.int64(2000), np.int64(2005), np.int64(2010), np.int64(2015), np.int64(2020)]
- unique h_code: 279
- marital_code values: ['1', '2', '3', '4']
- age_band values: ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64']

### Per-year cells + weighted pop sum:
- 1995: 11,352 cells, 247 h_code, pop sum 23,281,033
- 2000: 11,299 cells, 229 h_code, pop sum 25,170,829
- 2005: 11,865 cells, 229 h_code, pop sum 26,636,978
- 2010: 12,256 cells, 229 h_code, pop sum 27,878,248
- 2015: 12,170 cells, 229 h_code, pop sum 29,176,434
- 2020: 12,183 cells, 229 h_code, pop sum 29,661,965

## Education panel summary
- rows: 80,856
- years: [np.int64(1995), np.int64(2000), np.int64(2005), np.int64(2010), np.int64(2015), np.int64(2020)]
- unique h_code: 279
- education_band values: ['1.NoHS', '2.HS', '3.SomeCollege', '4.Bachelor+']
- age_band values: ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64']

### Per-year cells + weighted pop sum:
- 1995: 13,243 cells, 247 h_code, pop sum 23,281,133
- 2000: 13,154 cells, 229 h_code, pop sum 25,170,266
- 2005: 12,981 cells, 229 h_code, pop sum 26,636,978
- 2010: 14,052 cells, 229 h_code, pop sum 27,878,248
- 2015: 13,808 cells, 229 h_code, pop sum 29,176,434
- 2020: 13,618 cells, 229 h_code, pop sum 29,661,965

## Next step
- 11_mediator_mortality_rate.py: mortality numerator (혼인/교육 코드별 사망)
  + mediator denominator merge → mediator-specific mortality rate panel
