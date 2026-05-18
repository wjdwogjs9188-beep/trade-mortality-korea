# R-A 측 cumulative paragraph 권고 form — paper § 6.3 + § 8.3.3 의 substantive refinement (audit findings B + D + E + F)

**작성**: 2026-05-08 R-A (공동저자 mode) → 정재헌
**대상**: paper § 6.3 (Browning-Heinesen wording) + § 8.3.3 (Case-Deaton ICD-10 mapping) 의 cumulative refinement
**선행**: 2026-05-08 R-A audit findings (Finding B + D + E + F)
**Strict workflow anchor**: 본 wording 권고 form 위 사용자 측 별도 환경 commit prerequisite (memory: feedback_no_sandbox_analysis.md cumulative direction)

---

## § 6.3 — Finding B: Browning-Heinesen 2012 wording 정정

### 현재 paper § 6.3 line 64 wording

> "Browning and Heinesen (2012) review this evidence and similarly characterize the displacement-mortality response as **acute rather than amplifying**."

### Source 의 actual cumulative substantive form (browning2012.md 의 evidence-based 정합 form)

- **line 82**: Effects largest just after plant closure but **statistically significant after 20 years**; short-term effects do *not* simply represent a speeding-up of deaths
- **line 371 (Table 5)**: 79% (year 1) → 35% (1-4 yrs) → 17% (1-10 yrs) → **11% (1-20 yrs)**, all statistically significant
- **line 591 (Discussion)**: "Time pattern similar to Sullivan and von Wachter (2009) for the US ... long-term estimates [are] larger [than Eliason-Storrie]"
- **line 473-489 (Table 6)**: Alcohol-related mortality 11-15 years after — 45% higher hazard, statistically significant

### R-A 권고 wording (Path A — 자세한)

> "Browning and Heinesen (2012) similarly report a declining hazard pattern in Danish data — overall mortality 79 percent higher in the year of displacement, falling to 11 percent higher 1-20 years after the base year (their Table 5) — confirming that the displacement-mortality response declines over time rather than amplifying. They explicitly note that long-term effects remain statistically significant beyond Eliason and Storrie's four-year window, but the time pattern parallels Sullivan and Von Wachter (2009) and rules out long-run amplification."

### R-A 권고 wording (Path B — 간략)

> "Browning and Heinesen (2012), using Danish data, report a similar declining hazard pattern (overall mortality 79 percent in the year of displacement, falling to 11 percent at the 20-year horizon), inconsistent with long-run amplification."

### Substantive direction 의 cumulative anchor

paper § 6.3 의 narrative goal — long-run amplification 제거 — 자체는 source 와 정합. Browning-Heinesen 의 declining pattern 도 amplification 가설을 기각하는 evidence. 다만 "acute rather than amplifying" 의 cumulative wording 이 source 의 substantive message ("long-term significant + Sullivan-Von Wachter parallel") 와 cumulative inconsistency. R-A 권고 wording 위 declining pattern 의 substantive direction 의 cumulative form + long-term significance 의 cumulative honest disclosure.

---

## § 6.3 — references.md verification status #11 정정 권고

### 현재 wording

> "Browning, Heinesen (2012) — verified review characterization of the displacement-mortality response as acute-only rather than amplifying. Newly added to references."

### R-A 권고 wording

> "Browning, Heinesen (2012) — verified declining hazard pattern (Danish data, 79% year-1 → 11% 1-20 yrs, all statistically significant) parallels Sullivan-von Wachter (2009) US findings; long-term effects statistically significant beyond Eliason-Storrie's four-year acute window. Inconsistent with long-run amplification but not 'acute-only.' Newly added to references."

---

## § 8.3.3 — Finding D: 한국 code 102 의 Y87.0 추가

### 현재 paper § 8.3.3 line 37 wording

> "The Korean construction uses KOSTAT 104-cause classification codes 102 (suicide, **X60-X84**), 101 (accidental drug poisoning, X40-X49), 057 (mental and behavioral disorders due to psychoactive substance use, F10-F19), and 081 (chronic liver disease, K70-K77)."

### Codebook source (`kosis_104_to_icd10.yaml`)

```yaml
'102':
    label_kr: 고의적 자해(자살)
    icd10_likely: ['X60-X84', 'Y87.0']
    verification:
      method: KOSTAT 공식 자살 통계 vs raw 코드별 카운트 매칭
      year_2010: {raw_count: 15566, kostat_official: 15566, match: 100%}
      year_2011: {raw_count: 15906, kostat_official: 15906, match: 100%}
      year_2015: {raw_count: 13513, kostat_official: 13513, match: 100%}
      year_2019: {raw_count: 13799, kostat_official: 13799, match: 100%}
    confidence: HIGH
```

KOSTAT 공식 자살 통계와 4개년 (2010, 2011, 2015, 2019) 모두 raw count 100% 매칭 — mapping 신뢰도 HIGH.

### R-A 권고 wording

> "The Korean construction uses KOSTAT 104-cause classification codes 102 (suicide, **X60-X84 + Y87.0**), 101 (accidental drug poisoning, X40-X49), 057 (mental and behavioral disorders due to psychoactive substance use, F10-F19), and 081 (chronic liver disease, K70-K77)."

### Substantive direction 의 cumulative anchor

Case-Deaton (2015) PNAS 의 suicide spec (X60-X84 + Y87.0) 과 한국 code 102 spec (X60-X84 + Y87.0) 이 정확히 일치 영역. paper 본문이 Y87.0 을 누락하면 비교가 표면상 다르게 보임. 정정 후 substantive cross-comparison 의 cumulative consistency 확보.

---

## § 8.3.3 — Finding D 보강: sensitivity analysis description 정정

### 현재 wording

> "matching the exact Case-Deaton (2015) PNAS code list (K70 + K73-K74 from the chronic liver disease range; X40-X45 plus Y-code sub-codes from the poisoning range; F10-F19 excluded)"

### R-A 권고 wording

> "matching the exact Case-Deaton (2015) PNAS code list (K70 + K73-K74 from the chronic liver disease range; **X60-X84 + Y87.0 from the suicide range**; X40-X45 plus Y10-Y15 + Y45/Y47/Y49 sub-codes from the poisoning range; F10-F19 excluded)"

---

## § 8.3.3 — Finding E: 한국 code 101 vs Case-Deaton poisoning 비교 wording 정정

### 현재 paper § 8.3.3 line 37 wording

> "the Case-Deaton poisoning range is X40-X45 plus Y10-Y15 plus Y45/Y47/Y49 (drug-specific poisonings of undetermined intent and adverse-event sub-codes), **narrower than the Korean code 101 X40-X49 range**."

### Spec 비교

| Range | 한국 code 101 | Case-Deaton 2015 |
|-------|---------------|------------------|
| X-codes | X40-**X49** (broader) | X40-X45 |
| Y-codes | (없음, narrower) | Y10-Y15 + Y45/Y47/Y49 |

→ **Partial overlap pattern** (X-range 한국 broader + Y-range 한국 narrower). 일률적 "narrower" 단언 substantive 부정확.

### R-A 권고 wording (Path A — 자세한)

> "the Case-Deaton poisoning range is X40-X45 plus Y10-Y15 plus Y45/Y47/Y49 (drug-specific poisonings of undetermined intent and adverse-event sub-codes), which differs from the Korean code 101 X40-X49 range in two directions: the Korean range is **broader in the X-codes** (including X46-X49 in addition to X40-X45) but **narrower in the Y-codes** (excluding Y10-Y15 and Y45/Y47/Y49)."

### R-A 권고 wording (Path B — 간략)

> "the Case-Deaton poisoning range is X40-X45 plus Y10-Y15 plus Y45/Y47/Y49, which differs from the Korean code 101 X40-X49 in both X-range (broader, includes X46-X49) and Y-range (narrower, no Y-codes)."

---

## § 8.3.3 — Finding F: JEC 2019 attribution 좁히기

### 현재 paper § 8.3.3 line 37 wording

> "F10-F19 (mental and behavioral disorders due to psychoactive substance use) is *not* part of the original Case-Deaton (2015) PNAS definition; the Korean composite's inclusion of code 057 (which maps to F10-F19) reflects an **extension following the U.S. Joint Economic Committee (2019)** and broadly-comparable later definitions of deaths-of-despair."

### Source confirm (jec-report-deaths-of-despair.md)

- **Alcohol-related (line 205, 253)**: F10 명시, F11-F19 없음
- **Drug-related (line 221, 267)**: F11-F16 명시, F17-F19 없음
- 한국 code 057 = F10-F19 통째 vs JEC 2019 spec = F10 + F11-F16 → **partial overlap (F17-F19 영역의 한국 broader)**

### R-A 권고 wording

> "F10-F19 (mental and behavioral disorders due to psychoactive substance use) is *not* part of the original Case-Deaton (2015) PNAS definition; the Korean composite's inclusion of code 057 (which maps to F10-F19) reflects an extension **partially aligned with the U.S. Joint Economic Committee (2019), which adds F10 (alcohol-related) and F11-F16 (drug-related) but does not separately specify F17-F19**, and broadly-comparable later definitions of deaths-of-despair."

---

## R-A 의 권고 영역의 cumulative anchor

본 wording 권고 form 의 cumulative substantive direction 위 사용자 측 별도 환경 commit + R-A 의 후속 audit cycle 의 cumulative path 의 정통 form. 사용자 측 결정 영역의 substantive direction 위:

1. **§ 6.3 Browning-Heinesen wording 정정**: Path A (자세한) 또는 Path B (간략) 의 사용자 측 결정 영역
2. **references.md verification status #11 정정**: R-A 측 직접 Edit 가능 영역의 cumulative direction (verification status 영역 = R-A 측 wording 영역의 cumulative form)
3. **§ 8.3.3 Y87.0 추가** (Finding D): substantive 영역에 영향, 정정 simple
4. **§ 8.3.3 sensitivity analysis description 보강** (Finding D 보강): suicide range 명시
5. **§ 8.3.3 poisoning 비교 wording 정정** (Finding E): Path A (자세한) 또는 Path B (간략)
6. **§ 8.3.3 JEC 2019 attribution 좁히기** (Finding F): F17-F19 영역의 cumulative honest anchor

---

**End of R-A 측 cumulative paragraph 권고 form (audit findings B + D + E + F refinement)**
