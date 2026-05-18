# Research Status — 2026-05-03

## 1. 현재 stage 위치

- **Stage 1 (완료)**: Raw 수집·검증 (KOSTAT 사망 microdata, KOSIS 인구 1B040M5, 시군구 사망원인)
- **Stage 2 v4 (완료, 2026-05-03)**: 사망 panel 구축 — `mortality_panel_v01.parquet`, 7,297,865 records, 9 검증 PASS
- **Stage 3 v1 (완료, 2026-05-03)**: 인구 panel + 연령 표준화 사망률 panel — `population_panel_v01.parquet` (210,222 rows) + `mortality_rate_panel_v01.parquet` (74,196 rows), 9 검증 PASS
- **Stage 4A (진행 중, 2026-05-03 착수)**: 무역 데이터 수집 — UN Comtrade API
  - KR-CN bilateral: 25년 × 2방향 = 50 파일 모두 다운로드 완료
  - ADH 8 ← CN imports: 일부 진행 중 (AU, DK, FI, JP 거의 완료. DE 일부, NZ/ES/CH 미확인)
  - CN → World: 미진행
- **Stage 4B/4C (예정)**: HS vintage concordance + KSIC2-HS6 + Bartik IV
- **Stage 5 (예정)**: 회귀 분석 (5-year stacked first-difference 2SLS, 5-layer SE, 6 진단)

## 2. 산출물 inventory

### Stage 2 사망 panel
- `3_derived/mortality/mortality_panel_v01.parquet` — 1,483,920 cells (229 sigungu × 27 yr × 2 sex × 20 age × 6 outcome)
- `3_derived/mortality/mortality_microdata_combined.parquet` — 통합 microdata
- 모든 9 검증 PASS (KOSIS cancer C00-C97 ±0.05%, suicide ±0.06%, mutual exclusivity 등)

### Stage 3 인구 panel + 사망률 panel
- `3_derived/population/population_panel_v01.parquet` — 210,222 rows (229 × 27 × 2 × 17 age band)
- `3_derived/mortality/mortality_rate_panel_v01.parquet` — 74,196 rows (h × yr × sex × outcome → ASR + ln_asr)
- KOSIS 한국 총인구 cross-check 0.124% – 1.173% (모두 ±2% 이내)
- ASR 시계열: 1997=58.8 → 2010=47.0 → 2023=35.3 (한국 historical pattern 일치)
- Mortality join coverage 100.0000%

### Stage 4A 무역 데이터 (ongoing)
- `0_raw/comtrade_korea_china/` — 50 파일 (KR_imp_from_CN, KR_exp_to_CN × 2000-2024) ✅
- `0_raw/comtrade_adh_china/` — ADH 8국 진행 중. AU/DK/FI/JP 완료에 가까움, DE 2007 까지, FI 2017-2018 누락, NZ/ES/CH 미확인
- `0_raw/comtrade_china_world/` — 미생성 (Stage 4A `--cn-world` 또는 `--all` 후 생성)

### 코드북 + 가이드
- `1_codebooks/sigungu_crosswalk_v2.csv` — 256 raw → 229 h_code (자치구 collapse)
- `2_scripts/build_panel/2A_mortality_panel.py`, `3A_population_panel.py`, `4A_trade_collection.py`
- 모든 stage validation report 존재

## 3. 어제 대비 변경 사항

(첫 보고서이므로 baseline 으로만 기록)

- 메모리 7개 등록 (user_profile, project_dissertation, project_data_status, project_104_codebook, reference_who_icd10_f10_f19, reference_library_md, reference_research_archive)
- Daily status archive 시스템 구축 (이 파일 + `_index.md` + `_trajectory.md` + `latest.md`)
- Schedule task `dissertation-context-refresh` 등록 (매일 09:06)

## 4. 메모리 업데이트 제안

- **추가 권장**: `project_stage_progress.md` 신규 생성 — Stage 1-5 별 산출물 / 검증 결과 / 의사결정 누적. 현재는 `project_dissertation.md` 가 cover 하지만 stage 별 세부 사항이 늘어나면 분리 필요.
- **갱신 권장**: `project_data_status.md` 가 v4.0 reset 직후 작성된 것이라 이번 Stage 2/3 v1 채택 + Stage 4A 진행 사항 반영 안 되어있음. 다음 conversation 에서 갱신 검토.
- **현 상태 유지**: 나머지 메모리는 stable (코드북, 참고논문 라이브러리, ICD-10).

## 5. 참고논문 rotation 학습 결과

(첫 실행이라 rotation 미진행. 다음 실행부터 시작.)

권장 첫 rotation: **Pierce-Schott 2020** (본 연구 가장 가까운 reference, IV 설계의 직접 모델). 그 다음 ADH 2013 → Case-Deaton 2015 → BHJ practical guide → Goldsmith-Pinkham-Sorkin-Swift 2018 → Finkelstein-NAFTA 순.

## 6. 다음 작업 추천 (priority 순)

### A. Stage 4A 완료 (current, 진행 중)
- ADH 8 ← CN: NZ, ES, CH 확인 + DE/FI 누락분 채움
- CN → World: `--cn-world` flag 로 추가 다운로드
- KITA cross-check 실행: `--cross-check` flag, default mode (KR-CN HS 01-99) 에서 ±5% 검증

### B. Stage 4B HS vintage + KSIC2 concordance
- HS96 baseline 으로 vintage 통합 (WITS / UN concordance)
- KSIC2-HS6 매핑: Pierce-Schott / Dauth-Findeisen-Suedekum 표준 concordance 사용 (이전에 KIET 60대산업 reject 됨)
- KR-CN HS6 → KSIC2 시군구 산업 비중 결합용 기반 마련

### C. Stage 4C Bartik IV
- 시군구 × KSIC2 산업 비중 panel (사업체조사 raw)
- KR-CN bilateral net export 변화 (Δ5yr, Pierce-Schott style)
- Bartik shift-share IV 구축 (Goldsmith-Pinkham-Sorkin-Swift 2018 share exogeneity)
- ADH 8 OHIE → CN import 변화로 instrument

### D. Stage 5 회귀 분석
- 5-year stacked first-difference 2SLS
- 5-layer SE (HC1, Cluster-sido, AKM, Conley, AR+tF)
- 6 identification diagnostics (First-stage F, Rotemberg HHI, Share balance, Pre-trend, AKM placebo, Permutation)
- Romano-Wolf step-down (다중 검정)

### E. 외부 데이터 수집 (병행 가능)
- HIRA 의약품 ATC4: N06A 항우울제, N02A 오피오이드 (시군구 의약품 사용)
- ECOS 연체율 panel (현재 in_progress, Phase 1-C)

### F. PAP 갱신
- `research_proposal.md` Appendix A 변경 사항 누적 기록
  - Stage 1: 시군구 baseline 256 → 229
  - Stage 2 v4: cancer 027-048 → 027-047 (KOSIS C00-C97 정합)
  - Stage 3 v1: hybrid sigungu merge, 1997 = 1998 proxy, 17 통합 age band, 2010 baseline 직접 표준화
  - Stage 4A: KR-CN HS 01-99 + ADH/CN-World HS 28-97 (KITA validation 정확도)

## 7. 미해결 의사결정 / Risk

### A. 외부 피드백 대기 중 (`stage3_for_review_2026_05_03.md`)
6개 항목 reviewer 의견 대기:
- A. Hybrid merge 설계의 학술적 정당성
- B. 1997 = 1998 proxy vs 1997 drop (26년 단축)
- C. Despair_total 안의 liver dominance (통합 vs decomposition main outcome)
- D. 2010 baseline 외 추가 baseline (WHO 2000 / 2020 한국) 권장 여부
- E. ln(ASR+1) vs Poisson IV (offset=log pop)
- F. 80+ 단일 band 한계 (90+ 분리 불가)

### B. KSIC2-HS6 concordance 결정 보류
- 이전에 KIET 60대산업 mapping reject (KSIC2 너무 coarse)
- 대안: Pierce-Schott 2020 부록 concordance 또는 Dauth-Findeisen-Suedekum 2014 standard
- Stage 4B 착수 전 결정 필요

### C. Comtrade quota / API 키 분산
- 4 키 모두 active. KR-CN 50 calls 완료, ADH 14,000 calls 진행 중
- KR-CN HS 01-99 default 로 변경 후 KR-CN 재다운로드 필요? (이전엔 manufacturing-only 였을 가능성)
- Stage 4A 새 스크립트 (4-key rotation 내장) resume 시 truncated 자동 감지

### D. 80+ 자살률 분석 한계
- 한국 OECD 1위 80+ 자살률 = 본 연구 핵심 outcome 중 하나
- KOSIS C3 340 단일 코드라 90+ 분리 불가 → aggregate 보고만 가능
- Sensitivity test: 80+ 만 따로 분석 vs 65+ 등 cutoff 이동

---

## 메타

- 보고서 저장: `archive/2026/05/research_status_2026-05-03.md`
- Schedule task: `dissertation-context-refresh` (매일 09:06)
- 다음 자동 실행: 2026-05-04 09:06
