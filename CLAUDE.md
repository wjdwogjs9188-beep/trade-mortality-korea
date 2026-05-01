# Trade × Mortality Korea — Project Context

## 연구 개요

**제목:** Trade Exposure and Mortality in Export-Oriented Korea: A Hidden Protective Effect Beneath ADH-Style Bartik Designs

**핵심 가설:** 한국은 미국·독일과 달리 export-driven 무역구조 (특히 對중국 중간재). ADH-style Bartik IV로 보면 import-induced 유효 노출이 산업 단위 비교에서 약하게 나옴. 본 연구는 Korea-China bilateral net exposure (수입 - 수출) 을 IV로 사용해 사망률 인과효과 추정.

**비교 framework:**
- 미국 (Pierce-Schott 2020 AERI; Finkelstein-Notowidigdo-Shi 2026 NAFTA): β_m=+1.4%, β_n=-1.1%
- 독일 (Dauth-Findeisen-Suedekum 2014): export gain +442k jobs
- 한국 (본 연구): TBD — preliminary v3.x β=-0.041 reduced form

**사용자:** 정재헌 (가천대 경제학 학부생). 한국어 선호, 엄밀한 방법론 중시. 박사논문급 퀄리티 목표.

---

## 현재 상태 (2026-05-01 기준)

### Phase 0 ✅ 완료
- 폴더 구조 + 메타 문서 (`README.md`, `METHODOLOGY.md`, `CHANGELOG.md`, `DATA_SOURCES.md`)
- 5개 zip raw 추출
- `3_derived/raw_inventory.csv` (초기 501개 → 현재 481개 파일, Phase 1 완료 후 재생성 권장)
- ⚠️ Phase 0-E (git init) 진행 중 (Claude Code 에서)

### Phase 1 — 1-A/C/D/E 완료, 1-B 재수집 대기, 1-F 진행 중
- **1-A 시군구 crosswalk** ✅ 완료 (2026-05-01)
  - `1_codebooks/sigungu_crosswalk.csv` (6,723 rows, 1997-2023, 256 distinct h_code)
  - `1_codebooks/sigungu_changes_history.md` (행정 변경 111건)
  - 5/5 검증 통과 (매칭률 100%, 사망자 합 보존, 군위 cross-sido transfer 검증)
  - decision log: `5_logs/decisions/2026-05-01_sigungu_h_code_definition.md`
- **1-B 무역 IV 재수집** — Comtrade 7/42 받힘. **35개 남음** (DE 2013-2024, ES 2004-2024, FI 일부, CN_world 2015-17). API 일일 한도 소진 → **내일 09:00 KST (UTC 자정) 자동 재개**
- **1-C ECOS 거시 통계** ✅ **16개 통계표** 완료 (~420k rows)
  - `0_raw/ecos_macro/` 11개: 132Y001/003 산업별대출 (지역×용도), 161Y001 M1, 161Y006 M2, 102Y002 본원통화, 301Y015 지역경상수지, 403Y001/002 국가별 수출입, 722Y001 기준금리, 731Y004 환율, 901Y009 CPI
  - `0_raw/ecos_delinquency/` 5개: 141Y005 예금은행 연체율, 151Y002/003/005/006 가계대출 (업권/지역/용도별)
  - GRDP 는 ECOS에 없음 → KOSIS 별도 다운 필요 (Phase 2-C)
- **1-D 사망 104 코드북** ✅ 완료 — `1_codebooks/mortality_104_classification.csv` + `kosis_104_to_icd10.yaml`
- **1-E KOSIS 인구 panel** ✅ 완료 — `0_raw/kosis_population/population_combined.csv` (516,750 rows, **286 sigungu** (5자리), 1993-2023, 31년)
  - KOSIS API 한도 → UI 다운 4분할 → cp949→utf-8 변환
  - ✅ **사망 raw ↔ crosswalk 매칭률 27년 모두 100%** (6,723/6,723) — 본 연구 main 분석 데이터 손실 0%
  - 인구 panel 286 시군구 중 9개는 시 합계 코드 (수원시·성남시·청주시 등 자치구 분리 시의 시 전체) — Phase 2-A 에서 자치구 단위만 join (정상 처리)
- **1-F HIRA 약물 panel** 🟡 다운 진행 중 (Phase 5 mechanism 용)
  - HIRA 주소 master 추가 (HIRA→KOSIS sigungu 매핑 lookup, 273 lines)

### Phase 2 — 다음 (Master panel build)
- **2-A 사망률 panel** — sigungu × year × cause (raw KOSTAT microdata + crosswalk + 인구 → mortality rate)
- **2-B Bartik IV** — shock × baseline employment shares (산업 노출 변수)
- **2-C 거시 컨트롤 panel** — sido level + 전국 시계열 (ECOS 16 + KOSIS GRDP)
- **2-D Master panel merge** = A + B + C → `3_derived/master_panel.parquet`

### Phase 3-7 미시작

---

## ⭐ 핵심 검증 사항

### 1. 사망원인 104 코드북 (사용자 메모리 정정)

| 코드 | 라벨 | ICD-10 | 비고 |
|------|------|--------|------|
| 102 | 고의적 자해(자살) | X60-X84 | ✅ KOSTAT 4년치 100% 매칭 |
| **029** | **식도의 악성신생물** | C15 | ❌ 약물남용 아님 (이전 메모리 오류) |
| **069** | **기타 심장 질환** | I26-I51 | ❌ 알코올성간질환 아님 (이전 메모리 오류) |

**v3.x "기타 심장질환 -3.8% 보호효과" 발견 재해석:** ICD 매핑은 맞았고 라벨이 'alcohol'로 오기되어 있었음. 발견 자체는 살아있되 Other heart diseases (I26-I51) 보호효과로 해석.

### 2. Deaths of Despair 한국 매핑 (Case-Deaton 2015 정의)

| 구성 | 코드 | ICD-10 |
|------|------|--------|
| 자살 | 102 | X60-X84 |
| 약물 사망 (불의 중독) | 101 | X40-X49 |
| 정신활성물질 (drug/alcohol) | 057 | F10-F19 |
| 알코올성 간질환 | 081 | K70-K77 (간 질환 통합) |

**한계:** 코드 057은 F10-F19 통합 코드. **F17 담배는 Case-Deaton 명시적 제외**인데 한국 microdata에선 분리 불가 → sensitivity test 필요 (코드 101+081만으로 robustness).

### 3. 본 연구 outcome groups

| 그룹 | 코드 |
|------|------|
| `despair_total` | 102 + 101 + 057 + 081 |
| `cardiovascular` | 067-070 |
| `cancer` | 027-048 |
| `respiratory` | 073-078 |
| `external_other` | 097-104 minus 102 |

---

## 🔴 Raw 데이터 7대 issue (사용자 직접 검증)

1. ~~무역 IV 데이터 부족 (G8 9년치만)~~ — **부분 해결**: Comtrade ADH 8국 + KR-CN bilateral + CN→World 다운. KR-CN bilateral 50/50 ✅, AU/CH/DK/JP/NZ 125/125 ✅, DE/ES/FI/CN-world 7/42 받힘 (35개 남음, 내일 09:00 KST 자동)
2. ~~연체율 1년치만~~ — **해결: ECOS 141Y005 다운 완료. 시도 레벨이라 sigungu 단위는 불가**
3. **ICD-10 컬럼 없음** — 104 코드만 가용 (해결: 코드북 매핑 완성)
4. **산업 microdata 헤더 비대칭** — 1994-1999 vs 2000-2009 vs 2010-2024 구조 다름 (별도 처리 필요)
5. ~~**시군구 코드 비일관**~~ — **해결: Phase 1-A 시군구 crosswalk 완성**. 사망 raw 27년 (1997-2022 = 3-digit 시도+시군구, 2023 = 5-digit 시군구) 모두 100% 매핑됨
6. HIRA 파일은 약물 panel 아님
7. `시군구 사망원인.csv`의 C1_NM은 시군구가 아니라 ICD 대분류

---

## 📁 프로젝트 구조

```
trade_mortality_korea/
├── 0_raw/                     # 원본 (수정 금지)
│   ├── mortality_kostat/      # 사망 microdata 27년 (1997-2023, 27 csv)
│   ├── industry_census/       # 산업 microdata 31년 (1994-2024, 31 csv)
│   ├── kosis_population/      # 인구 panel 31년 (1993-2023, 516k rows) ⭐ 1-E
│   ├── ecos_delinquency/      # ECOS 연체율·가계대출 (5개 통계표)
│   ├── ecos_macro/            # ECOS 거시 (11개: M1/M2, 환율, 금리 등) ⭐ 1-C
│   ├── comtrade_adh_china/    # ADH 8국 × CN imports (168/200, 35개 누락 내일)
│   ├── comtrade_korea_china/  # KR-CN bilateral (50/50 ✅)
│   ├── comtrade_china_world/  # CN→World (22/25, 3개 누락 내일)
│   ├── ssaggregate-main/      # BHJ ssaggregate R 패키지
│   ├── research_supp/         # 보조 자료 (시군구 출생/혼인/이혼 등)
│   ├── research_materials/    # 참고 자료
│   └── (HIRA 폴더 — 다운 완료 후 추가)
├── 1_codebooks/
│   ├── kosis_104_to_icd10.yaml         # ⭐ 본 연구 outcome 매핑
│   ├── mortality_104_classification.csv  # 104 항목 전체
│   ├── sigungu_crosswalk.csv           # ⭐ Phase 1-A (6,723 rows, 256 h_code)
│   └── sigungu_changes_history.md      # 행정 변경 111건
├── 2_scripts/
│   ├── lib/
│   │   ├── config.py          # paths + .env loader
│   │   ├── ecos_api.py        # ECOS REST 클라이언트
│   │   └── comtrade_api.py    # Comtrade REST 클라이언트
│   ├── 00_build_inventory.py  ✅
│   ├── code_verification/
│   │   └── verify_104_codes.py  ✅
│   ├── data_collection/       # 데이터 수집 (15+ scripts)
│   │   ├── 01-05 ECOS·Comtrade 초기 수집
│   │   ├── 06_comtrade_refetch_chunked.py  # HS2 분할 재수집
│   │   ├── 07_ecos_macro_panel.py + 07b/c debug
│   │   ├── 08_kosis_population.py + 08b debug
│   │   ├── 09_kosis_force_cleanup.py
│   │   ├── 10_kosis_combine_ui_csvs.py + 10b finalize
│   │   └── cleanup_truncated.py
│   ├── sigungu_crosswalk/     # Phase 1-A 작업 (12 scripts)
│   │   └── step1-5 + anomaly check + finalize
│   └── utils/
│       ├── pdf_to_docx.py     # CLI (PDF/DOCX/XLSX/MD 변환)
│       └── pdf_to_docx_gui.py # GUI (mammoth + pdf2docx + pandas)
├── 3_derived/                 # 정제·intermediate
├── 4_results/                 # 회귀 출력 (table, fig)
├── 5_logs/
│   └── decisions/             # 결정 로그 (날짜별)
│       ├── 2026-05-01_mortality_104_codes.md
│       └── 2026-05-01_sigungu_h_code_definition.md
├── 6_papers/                  # 참고 논문
├── 7_paper/                   # 본 연구 원고
├── .env                       # API keys (git ignore)
├── requirements.txt
└── CLAUDE.md                  # 이 파일
```

---

## 🔑 환경 변수 (.env)

```
ECOS_API_KEY=<see .env>
COMTRADE_API_KEY=<see .env>            # 계정 1 primary (오늘 한도 소진)
COMTRADE_API_KEY_SECONDARY=<see .env>  # 계정 1 secondary
COMTRADE_API_KEY_TERTIARY=<see .env>   # 계정 2 primary (2026-05-01 추가)
COMTRADE_API_KEY_QUATERNARY=<see .env> # 계정 2 secondary
DATA_GO_KR_API_KEY=<see .env>
KOSIS_API_KEY=<see .env>
```

내일 09:00 KST 이후: 계정 1 키 한도 자동 리셋. .env 의 4 keys 모두 활성 (현재는 계정 1 두 줄 임시 주석처리됨 → 복구).

(절대 git commit 하지 말 것. `.gitignore`에 `.env` 등록.)

---

## 📚 Reference library (20편 마크다운)

위치: `C:\Users\82103\Desktop\연구 자료\참고논문\md\` (외부)

**핵심:**
- `Autor-Dorn-Hanson-ChinaSyndrome.md` — ADH 2013 baseline IV
- `pierce_schott_aeri_2020.md` + `2016094pap.md` (FEDS longer) — Pierce-Schott
- `BFI_WP_2026-33.md` — **Finkelstein-Notowidigdo-Shi 2026 NAFTA** (β_m, β_n benchmark)
- `case-deaton-2015-...md` — deaths of despair 정의
- `127_Dauth_Findeisen_Suedekum.md` + `dp10469.md` + `dp11299.md` — DFS German
- `1806.md` (Adão-Kolesár-Morales 2019) — AKM cluster SE
- `w24408.md` (Goldsmith-Pinkham 2018) — Rotemberg
- `w24997.md` + `borusyak-...practical-guide-2025.md` — BHJ
- `BFI_WP_2023-109.md` — **Sufi 2023 BFI Korea**
- `mian-s5.md` — Mian-Sufi-Verner household debt
- `annurev-economics-080218-025643.md` — Andrews-Stock-Sun weak IV (tF)

**OCR 필요 (이미지만):** `t0151 (1).md`, `w5570 (1).md`

---

## ⚙️ Pipeline 결정 (확정)

1. **Harmonized sigungu 단위** ✅ **2021 KOSTAT baseline (256 h_code)**
   - 결정 근거: `5_logs/decisions/2026-05-01_sigungu_h_code_definition.md`
2. **Baseline year** — 미확정 (권장: **2000 baseline + 1997 robustness**)
3. **연체율 변수 처리** — 미확정 (권장: **시도 레벨 그대로 + 가계대출/소득 비율 robustness**)

---

## 🛠 작업 스타일 (사용자 선호)

- 한국어 응답
- 솔직한 진단 (t-stat, F-stat, 저널 가능성)
- 퀄리티 > 속도
- 모든 단계에 KOSTAT cross-check + decision log
- 5-layer SE: HC1, cluster-sido, AKM, Conley, AR + tF
- v3.x mislabel 사고 후 traceability 최우선
- raw 데이터 절대 직접 수정 금지 (`0_raw/` 읽기만)

---

## 🚀 즉시 다음 작업 (내일 첫 세션, 2026-05-02 09:00 KST 이후)

1. **`.env` 4 keys 복구** (cfbae160, 9c836df7, 1e492bf1, b801d8d4)
2. **`python 2_scripts/data_collection/06_comtrade_refetch_chunked.py`** → yes
   - Comtrade 35개 남은 chunk 자동 재개 (DE 2013-2024, ES 2004-2024, FI 일부, CN_world 2015-17)
   - API 일일 한도 09:00 KST 리셋 후 진행
3. **`python 2_scripts/00_build_inventory.py`** 갱신 (Phase 1 완료 후 raw 인벤토리 재생성)
4. **Phase 2-A 사망률 panel 시작** — `2_scripts/build_panel/2A_mortality_panel.py`
   - raw KOSTAT microdata 27년치 + crosswalk + 인구 → sigungu × year × outcome group mortality rate
   - outcome groups: despair_total, cardiovascular, cancer, respiratory, external_other (CLAUDE.md 위 표 기준)

---

## 메모리 / 결정 로그 위치

- 본 파일 (`CLAUDE.md`) — 항상 최신
- `5_logs/decisions/YYYY-MM-DD_*.md` — 중요 결정마다 별도 마크다운
- 매 Phase 완료 시 `CHANGELOG.md` 업데이트
