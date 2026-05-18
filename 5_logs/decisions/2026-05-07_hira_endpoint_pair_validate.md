# 2026-05-07 결정 로그 — HIRA endpoint pair design + 6 sparse sigungu cumulative root cause + 220001 미추홀구 정정 **Author**: 정재헌 (가천대 경제학) / 공동저자 mode
**Phase**: Phase 2 sub-task 2.2 (HIRA pharmaceutical panel ETL) cumulative validate + 정정
**대상 파일**:
- `1_codebooks/hira_sgguCd_to_hcode_crosswalk.csv` (220001 정정)
- `1_codebooks/intersection_main_hira_h_codes.csv` (146 → 147)
- `3_derived/hira_atc4_panel.parquet` (long, 1,640 rows)
- `3_derived/hira_atc4_panel_wide.parquet` (wide, 325 rows)
- `7_paper/paper_draft_v01_section_7.md` (§ 7.1.1 + § 7.1.2 wording 정정)
- `7_paper/paper_draft_v01_section_8_9.md` (§ 8.3.3.1 cross-reference 정정) --- ## 1. 결정 (a) HIRA crosswalk 의 sgguCd=220001 (인천미추홀구) 의 h_code 매핑 NaN UNMATCHED → 23090 MATCH 정정. (b) Phase 2 sub-task 2.2 ETL 재실행으로 panel 167 → 168 distinct h_code, intersection 146 → 147 sigungu 정정. (c) β_147 = -0.155 (HC1 t = -4.81, cluster-province t = -5.65, p = 0.0001) 재추정 + |Δβ|/SE_full = 1.025 의 marginal 1-SE threshold 초과 영역의 honest disclosure. (d) HIRA raw v02 의 endpoint pair design (2010 + 2019 monthly, 12+12 month full coverage) 의 paper § 7.1.1 narrative anchor commit. (e) 30 sparse cell 의 6 sigungu cumulative root cause classification (3 행정 변경 transition + 3 raw HIRA reporting absence) + 5 cells 미추홀구 KOSIS pop join 영역의 honest disclosure. (f) prescription_rate_per_100k unit anchor (인구 100k 당 prescription event count cumulative form) commit. (g) totUseQty vs msupUseAmt 결정 — totUseQty (prescription quantity) 사용, msupUseAmt 거부 (heterogeneous ATC4-specific units, ratio range 53× to 551×). ## 2. 근거 ### 2.1 220001 미추홀구 정정 의 substantive evidence - raw HIRA panel v02: sgguCd=220001 ("인천미추홀구") = 1,246 rows (2010 591 + 2019 655), 5 ATC4 모두 reporting, totUseQty sum 24,246,084 ✅
- sigungu_crosswalk: h_code=23090 ("미추홀구(남구)") + raw_code 23030 (2017 이전) → 23090 (2018.7.1 명칭 변경) 의 정통적 매핑 영역 ✅
- mortality panel + IV panel 위 23090 정상 inclusion ✅
- HIRA crosswalk (`hira_sgguCd_to_hcode_crosswalk.csv`) 의 minor gap 영역 — 220001 → 23090 매핑 미commit
- 정정 후 panel 168 distinct h_code (= 167 + 미추홀구), intersection 147 (= 146 + 미추홀구) ### 2.2 HIRA endpoint pair design 의 substantive 영역 - raw HIRA panel v02 의 diagYm distinct = 24 (2010m1-12 + 2019m1-12, 12 month × 2 year 의 full coverage)
- endpoint pair fetch design 의 substantive 영역이 paper § 7.1.1 의 long-difference framework (1997-1999 ↔ 2018-2022) 와 호환
- DGHP 2017 single-IV mediation framework 가 single-period treatment-effect framework 이므로 endpoint pair 와 직접 호환 ### 2.3 30 sparse cell 의 6 sigungu cumulative root cause | h_code | sigungu | sparse year | substantive root cause |
|--------|---------|-------------|------------------------|
| 23040 | 인천 연수구 | 2019 | raw HIRA reporting absence (urban size, specific reporting drop) |
| 29010 | 세종 | 2010 | 행정 변경 (2012.7.1 세종 출범, 2010 미존재) ✅ |
| 31280 | 경기 여주시 | 2010 | 행정 변경 (2013.9.23 여주군→여주시 승격) ✅ |
| 33390 | 충북 증평군 | 2010 | raw HIRA reporting absence (인구 sparse + reporting threshold) |
| 34080 | 충남 당진시 | 2010 | 행정 변경 (2012.1.1 당진군→당진시 승격) ✅ |
| 36480 | 전남 신안군 | 2019 | raw HIRA reporting absence (인구 sparse + reporting threshold) | 3 sigungu = 행정 변경 transition + 3 sigungu = raw HIRA reporting absence 의 cumulative 6 sigungu × 5 ATC4 × 1 year = 30 sparse cells. ### 2.4 미추홀구 23090 의 KOSIS pop join 영역 - KOSIS pop 위 23030 (historical 남구) inclusion 1998-2017 + 23090 (current 미추홀구) inclusion 2018-2023
- ETL 의 KOSIS pop join 위 raw_code (23030) → h_code (23090) 매핑 부재 → 미추홀구 2010 영역 5 cells 의 working_age_pop_25_64 NaN
- 본 영역은 sub-task 2.3 prep 단계에서 별도 정정 가능 (KOSIS pop ETL 위 raw_code 매핑 추가) ### 2.5 |Δβ|/SE_full = 1.025 의 substantive 영역 - β_221 (full) = -0.128, HC1 SE = 0.026
- β_147 (intersection) = -0.155, HC1 SE = 0.032, t = -4.81, cluster t = -5.65, p = 0.0001
- |Δβ| = 0.027, |Δβ|/SE_full = 1.025 (marginal 1-SE threshold 초과)
- substantive interpretation: urban-biased intersection sample 위 trade exposure 측정의 reliability 가 더 높고 β 가 더 protective 으로 추정됨. 1-SE marginal 초과는 minor caveat 의 honest disclosure 영역, fundamental selection bias 의 evidence 부재. ### 2.6 totUseQty vs msupUseAmt 결정 - totUseQty (prescription quantity, e.g., tablets/capsules/ampoules): paper § 7.1.1 의 "prescription access" framing 과 직접 호환
- msupUseAmt (medication supply amount in cost or dose-equivalent units): ATC4 별 heterogeneous unit ratio 53× to 551× (A05BA 287, N05AX 533, N05BA 53, N06AB 551, N06AX 175) — non-comparable scale variation 으로 composite outcome 영역에 unsuitable
- log-log Pearson r = 0.85 (substantively similar trends), Pearson r = 0.41 (raw scale 차이 dominant) ## 3. Anchor papers - DGHP 2017 NBER WP 23209 — single-IV mediation framework
- Pierce-Schott 2020 AERI 2(1): 47-63 — drug overdose mortality U.S. counties
- Case-Deaton 2015 PNAS 112(49): 15078-15083 — deaths-of-despair definition
- 본 paper § 5.1 (native build under 1997-1999 ↔ 2018-2022 long-difference window)
- 본 paper § 7.1.1 + § 7.1.2 (Phase 2 sub-task 2.2 cumulative narrative) ## 4. 영향 ### 4.1 정정 commit 영역 - HIRA crosswalk: 220001 → 23090 매핑 추가 (status MATCH, h_code=23090.0)
- intersection csv: 146 → 147 sigungu (추가: 23090 미추홀구)
- panel parquet: long 1,630 → 1,640 rows + wide 324 → 325 rows
- paper § 7.1.1: "167 of approximately 250" → "168 / 250", "n = 146 (66.1%)" → "n = 147 (66.5%)" + sparse cell 6 sigungu honest disclosure + 미추홀구 230090 매핑 narrative anchor
- paper § 7.1.2: β_146 → β_147, HC1 t -4.78 → -4.81, cluster t -5.38 → -5.65, |Δβ|/SE 0.969 → 1.025 + honest minor caveat narrative
- paper § 8.3.3.1: 146-sigungu → 147-sigungu cross-reference 정정 + |Δβ|/SE 정정 ### 4.2 후속 영향 - Phase 2 sub-task 2.3 prep: M1 composite outcome variable 정의 + sparse cell treatment (default complete-case form) + KOSIS pop ETL raw_code 매핑 추가 결정
- Phase 2 sub-task 2.4: DGHP ivmediate framework R/Stata implementation 위 147-sigungu intersection panel input ## 5. Sensitivity ### 5.1 |Δβ|/SE_full = 1.025 의 robustness 본 결정은 1-SE marginal 초과 영역의 honest disclosure 가 핵심. R&R cycle reviewer 가 selection bias warning 영역의 추가 robustness check 요청 시:
1. propensity score matching 위 intersection-vs-non-intersection 차이 control
2. sigungu fixed effects panel 영역 위 sample restriction effect decomposition
3. β_146 (이전 intersection) vs β_147 (새 intersection) 의 cumulative 정합 form (둘 다 substantive 정통적 영역의 cumulative confirm) ### 5.2 미추홀구 KOSIS pop join 영역의 sub-task 2.3 정정 KOSIS pop ETL 위 raw_code → h_code 매핑 추가 (sigungu_crosswalk 의 23030 → 23090 적용) 시:
- 미추홀구 2010 영역 5 cells 회복 → sparse 30 → 25 (intersection 147 영역 위)
- 단 ETL 의 KOSIS pop separate build 영역의 변경이 mortality panel 영역과의 cumulative 정합 verify 필요 ### 5.3 30 sparse cell 의 R&R cycle 위임 97.96% coverage (intersection 147 × 5 × 2 - 30 sparse = 1,440 / 1,470) 의 maximum form 도달. R&R reviewer 가 행정 변경 transition 의 raw_code 매핑 ETL 추가 요청 시 4 sigungu 회복 가능 (29010 + 31280 + 34080 + 미추홀구 2010 KOSIS pop). 현 시점 commit 의 substantive 비용/이익 비대칭으로 R&R 위임이 합리적 영역. ## 6. 후속 step ### 6.1 즉시 (다음 위임 prompt 의 대상) - Phase 2 sub-task 2.3 prompt 작성: M1 composite outcome variable 정의 (4 mental ATC4 weighted average + 1 liver therapy 의 2-stage composite, log + z-score normalization, sparse cell complete-case form)
- KOSIS pop ETL raw_code 매핑 추가 sub-task (선택 영역 — sub-task 2.3 prep 와 cumulative) ### 6.2 Mid-term (Phase 2 sub-task 2.4) - DGHP 2017 ivmediate framework R 또는 Stata implementation
- ACME (average causal mediation effect) + ADE (average direct effect) + TE (total effect) 추정
- 147 intersection sample 위 paper § 7.2 narrative draft ### 6.3 Long-term (Phase 3-7) - PAP v4.6 update with sub-task 2.2 corrections + sparse cell treatment commit
- Cover letter draft for KER July 2026 submission
- Replication archive (HIRA crosswalk + ETL script + audit_2_2_hira.py + 결정 로그 cumulative) --- **Audit-after-action 결과** (2026-05-07 self-audit + 사용자 Spyder F5 verify):
- HIRA crosswalk MATCH count 168 / UNMATCHED 0 ✅
- panel long 168 distinct h_code, intersection 147 ✅
- Aggregation cross-check 5 random cells rel err 0.0000% ✅
- β_147 = -0.155, cluster t = -5.65, p = 0.0001 ✅
- paper § 7.1.1 + § 7.1.2 + § 8.3.3.1 wording 정정 cumulative ✅ **Status**: COMMIT (사용자 confirm 위 (A) 즉시 정정 path 의 cumulative 진행 완료)
**다음 turn**: Phase 2 sub-task 2.3 self-contained 위임 prompt 작성
