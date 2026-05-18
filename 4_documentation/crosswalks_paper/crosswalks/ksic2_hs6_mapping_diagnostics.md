# KSIC2 ↔ HS6 mapping diagnostics (KIET 60대산업 bridge)

**Inputs**

- 60대산업-HSCODE.xlsx — 6,909 HS rows (6,909 unique HS6 after normalization)
- 60대산업-표준산업분류_V2.xlsx (sheet 연계표) — KIET 60-ind → KSIC10차

**Outputs**

- `ksic2_to_hs6.csv` — 9,868 (KSIC2, HS6, weight) rows
- `unmatched_hs6.csv` — 14 HS6

## Coverage summary

- Mapped HS6: **6,895 / 6,909 = 99.80%**
- 1-to-1 (HS6 → 1 KSIC2): 4,687
- 1-to-many (HS6 → ≥2 KSIC2): 2,208
- Max KSIC2 per HS6: 4
- Weight sum per HS6 ≈ 1: 6,895/6,895

## Weight distribution

```
count 9868.000000
mean 0.698723
std 0.295437
min 0.250000
25% 0.500000
50% 0.500000
75% 1.000000
max 1.000000
```

## KSIC2-level coverage

| ksic2 | name | n_hs6_mapped | sum_weight |
|---|---|---|---|
| 1 | 농업 | 395 | 131.67 |
| 2 | 임업 | 395 | 131.67 |
| 3 | 어업 | 395 | 131.67 |
| 5 | 석탄, 원유 및 천연가스 광업 | 122 | 30.50 |
| 6 | 금속 광업 | 122 | 30.50 |
| 7 | 비금속광물 광업 | 122 | 30.50 |
| 8 | 광업 지원 서비스업 | 122 | 30.50 |
| 10 | 식료품 | 816 | 408.00 |
| 11 | 음료 | 816 | 408.00 |
| 12 | 담배 | 17 | 17.00 |
| 13 | 섬유제품(의복 제외) | 639 | 319.50 |
| 14 | 의복·의복액세서리·모피 | 275 | 275.00 |
| 15 | 가죽·가방·신발 | 119 | 119.00 |
| 16 | 목재 및 나무제품 | 202 | 202.00 |
| 17 | 펄프·종이·종이제품 | 164 | 164.00 |
| 18 | 인쇄 및 기록매체 복제업 | 19 | 19.00 |
| 19 | 코크스·연탄·석유정제품 | 49 | 49.00 |
| 20 | 화학물질 및 화학제품(의약 제외) | 1683 | 1363.50 |
| 21 | 의료용 물질 및 의약품 | 154 | 154.00 |
| 22 | 고무 및 플라스틱 | 156 | 156.00 |
| 23 | 비금속 광물제품 | 203 | 203.00 |
| 24 | 1차 금속 | 472 | 472.00 |
| 25 | 금속가공제품(기계 및 가구 제외) | 288 | 288.00 |
| 26 | 전자부품·컴퓨터·영상·음향·통신 | 324 | 237.50 |
| 27 | 의료·정밀·광학·시계 | 227 | 227.00 |
| 28 | 전기장비 | 304 | 217.50 |
| 29 | 기타 기계 및 장비 | 575 | 575.00 |
| 30 | 자동차 및 트레일러 | 74 | 74.00 |
| 31 | 기타 운송장비 | 121 | 121.00 |
| 32 | 가구 | 40 | 40.00 |
| 33 | 기타 제품 제조업 | 205 | 205.00 |
| 35 | 전기·가스·증기 및 공기조절 | 1 | 1.00 |
| 36 | 수도 | 63 | 15.75 |
| 37 | 하수·폐수·분뇨처리 | 63 | 15.75 |
| 38 | 폐기물 수집·운반·처리·원료재생 | 63 | 15.75 |
| 39 | 환경 정화 및 복원업 | 63 | 15.75 |

### Manufacturing (KSIC2 10–33) check

- Mapped KSIC2 in 10–33: 24 / 24
- KSIC2 (10–33) with **0 HS6 mapped**: 

## Top 20 unmatched HS6 (productcode shows what missed)

| hs6 | productcode | lvl1 | lvl2 | lvl3 |
|---|---|---|---|---|
| 242400 | | | | |
| 300402 | | | | |
| 383775 | | | | |
| 392421 | | | | |
| 490100 | | | | |
| 490520 | Maps and hydrographic or similar charts of all kinds, includ | | | |
| 490590 | Maps and hydrographic or similar charts of all kinds, includ | | | |
| 610530 | | | | |
| 747989 | | | | |
| 771719 | | | | |
| 840422 | Auxiliary plant for use with boilers of heading 84.02 or 84. | | | |
| 843140 | Parts suitable for use solely or principally with the machin | | | |
| 845099 | Household or laundry-type washing machines, including machin | | | |
| 848171 | Taps, cocks, valves and similar appliances for pipes, boiler | | | |

### Unmatched HS6 by 레벨1 code

| 레벨1코드 | n |
|---|---|
| (no level) | 14 |

## Decisions / limitations

1. **HS6 zero-padding**: 5-digit hsc treated as HS6 with leading 0 (Excel auto-stripped).
2. **NaN inheritance**: 1레벨/2레벨/3레벨 ffill in KSIC linkage (parent inheritance).
3. **Single-letter sections** (A/B/D/E/F/...) expanded to all KSIC2 within the section using KSIC10차 standard.
4. **Multi-mapping weight**: row-equal-split. A linkage row with N KSIC2 contributes 1/N to each. Aggregated per (60-ind, KSIC2) and normalized so sum across KSIC2 per HS6 = 1.
5. **Fallback**: when 레벨3코드 is NaN (581 HS rows in I1/I2/I4/I5), use 레벨1코드 (e.g., I1→A→{01,02,03}).
6. **Population weighting**: not applied (균등 분할 baseline). Robustness: 사업체통계 종사자 수 가중 — Stage 5 secondary.

## Step 5 — Comtrade KR-CN 2010 cross-check

| dataset | unique HS6 | unique cover | value cover |
|---|---|---|---|
| KR_exp_to_CN_2010 | 3,761 | **100.00%** | **100.00%** ($116.8B / $116.8B) |
| KR_imp_from_CN_2010 | 4,318 | **100.00%** | **100.00%** ($71.6B / $71.6B) |

**결론**: KIET 60-industry bridge 가 actual KR-CN 무역의 HS6 universe 를 100% cover.
14개 unmatched (KIET 원파일 내) 는 obsolete 또는 미사용 코드로, 실 Comtrade 에는 출현하지 않음. 
Bartik IV (Stage 5) 에서 추가 fallback 불필요.

## Quality verdict

학술 사용 가능 quality 모든 기준 통과:

- ✅ HS6 cover 율 ≥ 90% (실제: 99.80% on KIET file, 100.00% on Comtrade KR-CN)
- ✅ KSIC2 제조업 24개 (10–33) 모두 매핑 (0 인 KSIC2 없음)
- ✅ 누락 HS6 14개 모두 KIET file 의 미분류 row (실 거래 영향 0)
- ✅ Weight 합 == 1 per HS6 (numerical precision OK)

매핑표 채택 후 panel_construction_execution_guide.md Stage 5 진행 가능.
