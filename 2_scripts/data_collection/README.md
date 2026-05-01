# Data Collection Scripts

API에서 raw 데이터를 다운로드하는 스크립트. 모두 Python.

## 실행 환경

**Cowork sandbox는 ECOS·Comtrade 도메인 차단됨** → 사용자 PC에서 직접 실행 필요.

### Windows PowerShell

```powershell
# 프로젝트 폴더로 이동
cd C:\Users\82103\Downloads\trade_mortality_korea

# 패키지 설치 (한 번만)
pip install -r requirements.txt

# 다운로드 시작
python 2_scripts\data_collection\01_ecos_explore.py            # 1. ECOS 후보 통계표 탐색
python 2_scripts\data_collection\02_ecos_household_delinquency.py  # 2. 가계대출 연체율
python 2_scripts\data_collection\03_comtrade_adh_china.py      # 3. ADH 8국 × China imports
python 2_scripts\data_collection\04_comtrade_korea_china.py    # 4. Korea-China bilateral
python 2_scripts\data_collection\05_comtrade_china_world.py    # 5. China-World (alt IV)
```

## API Key 위치

`.env` 파일 (이미 입력됨):
- ECOS: `3CQCQ9VQG9HHCIDB3JN5`
- Comtrade primary: `46d4526cc65d48c9874f4ee13885fecf`
- Comtrade secondary: `9c836df777a3498b97187b9dbcc6aa8a`

## 예상 시간

| 스크립트 | API calls | 시간 (free tier 기준) |
|---|---|---|
| 01_ecos_explore | ~10 | 1 분 |
| 02_ecos_delinquency | 후보 표 × 분기 | 5-15 분 |
| 03_comtrade_adh_china | 8 × 25 = 200 | 30-60 분 |
| 04_comtrade_korea_china | 2 × 25 = 50 | 10-20 분 |
| 05_comtrade_china_world | 25 | 5-10 분 |

## Resume 기능

03/04/05 스크립트는 이미 다운로드된 파일은 자동 skip → 중간 끊겨도 안전하게 재실행 가능.

## 출력 위치

```
0_raw/
├── ecos_delinquency/
│   ├── candidate_tables.csv
│   ├── items_141Y005.csv
│   └── (가계대출 연체율 STAT)_M_*.csv
├── comtrade_adh_china/
│   ├── _download_log.csv
│   ├── AU_2000.csv  AU_2001.csv ...
│   ├── DK_2000.csv  ...
│   └── (8 국가 × 25 년 = 200 파일)
├── comtrade_korea_china/
│   ├── KR_imp_from_CN_2000.csv ~ 2024.csv
│   └── KR_exp_to_CN_2000.csv ~ 2024.csv
└── comtrade_china_world/
    └── CN_exp_world_2000.csv ~ 2024.csv
```

## 다운로드 후 검증

각 스크립트 끝에 `_download_log.csv` 자동 생성. 거기서 `status=ok` 행 개수 확인.

문제 있으면:
- `rows=0`: 해당 (국가, 연도) 데이터 없음
- `status=ERR`: rate limit 또는 API 오류 → 재실행 시 skip 후 retry
