# P1 issues clear — Phase 4 진입 준비 완료 **date**: 2026-05-05
**author**: **status**: final 본 reviewer (`my paper review mode`) 의 P1 2건 처리 완료. Phase 4 진입 가능. ## P1.A — Dashboard headline 격하 ✅ **Reviewer 지적**: cluster-sido F=19.65 < OP 23.1 cutoff → tF inference 의무. 현재 cluster t=−3.11 < tF cutoff 3.43 → "p=0.002" 는 weak-IV 하 inference-valid 아님. **처리**:
- `research_dashboard.html` headline pill: `✅ 유의 (보호효과)` → `preliminary · tF borderline`
- 본 결과를 advisor / external review 시 "Phase 4 의 WCB + AKM + Conley 후 final" 로 framing
- Final inference 는 **둘 중 하나** 의 cutoff 통과 시에만: - WCB-sigungu F ≥ 23.1 → standard inference - 또는 t (after WCB / Conley) > tF cutoff (F-dependent) ## P1.B — Working-age panel verification ✅ **Reviewer 지적**: `mortality_rate_panel_v02_2_wa.parquet` 부재. 본 build 한 v02_wa 가 실제 working-age 인지 검증 필요. **처리** (`03_verify_working_age_panel.py` 실행): | 검증 항목 | 기대값 | 실제값 | 판정 |
|-----------|--------|--------|------|
| 종로구 2020 pop_wa (both sex WA) | 70-100k | **89,510** | ✅ |
| 전국 despair_total 2010 rate | 45-50 / 100k | **48.2** | ✅ KOSIS 매칭 |
| 종로구 1998-2022 WA 추세 | -20~-30% (고령화) | **-23%** | ✅ 패턴 부합 |
| panel coverage | 256 h_code, 27y, 5 outcome | **31,494 rows** | ✅ | **Naming 정정 (P3 cosmetic)**:
- 본 paper 의 panel 이름: `sigungu_mortality_panel_v02_wa.parquet`
- Reviewer 명시 이름: `mortality_rate_panel_v02_2_wa.parquet`
- → 같은 의미. 다음 PAP rewrite 시 naming 통일 ## 첫 reduced form 결과 (preliminary status) 기존 결과는 **이미 working-age panel 기반** — re-estimation 불필요. | outcome | β (1 sd 노출) | cluster-sido t | p (raw) | tF status |
|---------|---------------|----------------|---------|-----------|
| despair_total | **−0.069** | −3.11 | 0.002 | borderline (vs cutoff 3.43) |
| cancer | −0.005 | −0.15 | 0.881 | n.s. |
| cardiovascular | −0.013 | −0.50 | 0.618 | n.s. |
| respiratory | −0.012 | −0.20 | 0.845 | n.s. |
| external_other | +0.014 | +0.18 | 0.858 | n.s. | **Final framing** (Phase 4 후 최종 update):
- 현재: "preliminary protective effect, awaiting Phase 4 5-layer SE resolution"
- Phase 4 통과 시: "first paper-grade evidence of trade-induced mortality decrease in export-driven economy" ## Phase 4 진입 prompt (Reviewer 의 NEXT_STEP_PROMPT 채택) 다음 turn 또는 위임. 7 step:
1. Working-age panel verify (✅ 본 turn 완료)
2. 5-layer SE 동시 출력 (HC1 + WCB-sigungu + cluster-sido + AKM + Conley)
3. tF inference 적용 (cutoff F-dependent)
4. Romano-Wolf step-down (1000 boot, 10 family)
5. Pre-trend placebo 1992-1996 (Comtrade pre-WTO 사용자 side 다운 의존)
6. 2008 ICD-10 sub-period split (1997-2007 / 2008-2023)
7. Output: `4_results/phase_4_main_spec_results.csv` + decision log 추정 시간: 2-3h (Comtrade 1992-1996 다운 제외). ## 정확한 진가 인정 (Reviewer Strength) 본 reviewer 가 인정한 4 강점 — 본 paper § 4·7·8 에 직접 인용 가능: 1. **F=48 (bilateral, HC1) strong** — A.ii main spec 의 statistical 정당성. ADH-8 weak 격하 = conservative 자세
2. **KOSIS suicide 15/15 within ±0.2%** — replication-grade external validity
3. **Channel-specificity (only despair sig)** — deaths-of-despair mechanism consistent
4. **Sign-match with DFS Germany (−3.8%)** — export-driven economy 의 기대부호. 미국 (Pierce-Schott +1.4%) 과 정반대 = paper 핵심 contribution ## Anchor 비교 unit caveat (P2.C — dashboard 추가 필요) `research_dashboard.html` 의 anchor chart 에 caption 추가:
> "각 paper 의 1-sd 노출 정의가 다름 (Pierce-Schott NTR gap × 中 import share, DFS German manufacturing trade exposure, 본 paper z_x_h KR-CN bilateral). Ordinal comparison 만 valid, magnitude 직접 비교는 unit-dependent." ## 다음 turn 후보 (B-1) Phase 4 main spec runner (위 reviewer prompt) — 2-3h
(B-2) 1992-1996 Comtrade 다운 (사용자 side, 15min API 호출) → pre-WTO placebo enable
(B-3) PAP § 7 main body rewrite (3h, dedicated turn) 권장: (B-1) 우선 — paper 의 final inference 결정. Pre-WTO placebo (B-2) 는 Phase 4 결과 후 진행.
