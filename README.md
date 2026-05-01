# Trade × Mortality Korea

**Author:** 정재헌 (Jae-Heon Jeong)
**Affiliation:** Department of Economics, Gachon University
**ORCID:** 0009-0009-9403-0940
**Status:** v4.0 reset — raw 데이터 검증 완료, 27개 reference paper 학습 완료, 새 파이프라인 구축 시작
**Last update:** 2026-05-01

---

## 연구 질문

한국 같은 export-oriented 경제에서 중국과의 무역 노출이 시군구 단위 사망률에 미친 인과적 효과는 무엇인가?

방법론과 가설은 [METHODOLOGY.md](METHODOLOGY.md) 참고.

---

## 폴더 구조

```
trade_mortality_korea/
├── 0_raw/         읽기 전용 raw 데이터 (5 zip 추출)
├── 1_codebooks/   변수 정의 yaml (ICD-10, KSIC, 시군구)
├── 2_scripts/     Python 파이프라인 (00_*.py ~ 11_*.py)
│   └── lib/       공유 모듈 (validate, icd10, io, log)
├── 3_derived/     파이프라인 결과 (.parquet, git 제외)
├── 4_results/     표·그림 (git 포함)
├── 5_logs/        실행 로그 + 방법론 결정 기록
├── 6_papers/      27개 reference paper 리뷰
└── 7_paper/       논문 v4.0 작성
```

자세한 설명은 [DATA_SOURCES.md](DATA_SOURCES.md), [METHODOLOGY.md](METHODOLOGY.md) 참고.

---

## 빠른 시작

```bash
# 환경 설정
pip install -r requirements.txt

# 전체 파이프라인 실행 (raw → 최종 결과)
make all

# 또는 단계별
python 2_scripts/00_extract_zips.py
python 2_scripts/01_build_mortality_panel.py
# ... 11_make_figures.py 까지
```

실행 시 `5_logs/pipeline_runs/YYYY-MM-DD_HH-MM_<script>.log` 자동 생성.

---

## 핵심 원칙

1. **0_raw는 절대 수정 X** — 모든 변환은 Python script가 3_derived/ 로 출력
2. **모든 사인 분류는 ICD-10 raw 직접 매핑** — KOSIS 104항목 코드 신뢰 X (이전 v3.x mislabel 문제)
3. **모든 panel은 KOSTAT 공식 cross-check 자동 통과** 후에만 생성
4. **변수 정의는 1_codebooks/ yaml에만** — Python 코드 하드코딩 금지
5. **모든 회귀는 5-layer SE 동시 보고** — HC1, cluster-sido, AKM, Conley, AR + tF
6. **모든 결정은 5_logs/decisions/YYYY-MM-DD_*.md** 로 기록

---

## 현재 상태 (2026-05-01)

- ✅ Phase 0: 폴더 구조 + raw 추출 + INVENTORY 진행 중
- ⏳ Phase 1: Codebook 작성 (ICD-10, KSIC, 시군구)
- ⏳ Phase 2: 모든 panel 구축
- ⏳ Phase 3: Bartik IV (4 gate 검증)
- ⏳ Phase 4: 회귀 + 5-layer 추론
- ⏳ Phase 5: 이질성 + mechanism
- ⏳ Phase 6: Robustness battery
- ⏳ Phase 7: 논문 v4.0 작성
