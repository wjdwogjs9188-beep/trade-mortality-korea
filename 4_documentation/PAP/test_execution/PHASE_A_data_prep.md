# Phase A — 데이터 prep + bilateral 노출 집계

**작성일**: 2026-05-04
**대상 실행자**: Claude Code (substantive 코딩)
**소요 추정**: 2시간 (ECOS API 호출 + WEO 처리 + 무역 집계)
**선행 의존**: 없음 (모든 raw 데이터 이미 보유)
**후속 단계**: Phase B (Test 1 / 1b / 3 / first-stage F 실행)

---

## 0. 본 phase 의 목적

PAP v3.5 의 Test 1 (Romer-Romer style macro predictability) + Test 1b (WEO surprise robustness) + § 4.1 (first-stage F) 을 실행하기 위해 필요한 *aggregated dataset* 3개를 만든다:

1. **`3_derived/macro/macro_quarterly_panel.parquet`** — 한국 거시 분기 시계열 (실현치 only, ECOS 기존 11개 + 신규 3개)
2. **`3_derived/macro/weo_korea_vintages.parquet`** — IMF WEO Korea 연간 forecast vintage matrix (1990 S/F ~ 2022 F)
3. **`3_derived/trade/bilateral_exposure_5yr.parquet`** — KR-CN bilateral net exposure, 5-year stacked, HS-2자리 chapter level + total
4. **`3_derived/trade/adh8_exposure_5yr.parquet`** — ADH-8 imports from CN, 5-year stacked, 동일 grain

Phase B 에서 이 4개를 join 해서 회귀 실행한다.

---

## 1. 산출물 1 — `macro_quarterly_panel.parquet`

### 1.1 신규 ECOS 호출 (3개 시리즈)

기존 `2_scripts/lib/ecos_api.py` 활용. `2_scripts/data_collection/12_ecos_test1_macro_vars.py` 신규 작성:

```python
# 12_ecos_test1_macro_vars.py
"""
Test 1 (macro predictability) 용 추가 ECOS 시리즈 호출.
기존 ecos_macro/ 11개 외에 다음 3개 신규:
  - 200Y007  분기 GDP 성장률 (실질, 원계열)
  - 401Y014  수출물가지수 (월별, 원화기준 원지수)
  - 401Y015  수입물가지수 (월별, 원화기준 원지수)
"""
from pathlib import Path
import pandas as pd
from lib.ecos_api import ECOSClient
from lib.config import RAW_DIR

OUT = RAW_DIR / "ecos_macro"
client = ECOSClient()  # API key from .env

specs = [
    ("200Y007", "Q", "20001Q1", "20244Q4", "분기GDP성장률"),
    ("401Y014", "M", "200001",  "202412",  "수출물가지수"),
    ("401Y015", "M", "200001",  "202412",  "수입물가지수"),
]

for code, freq, start, end, label in specs:
    df = client.fetch_table(code, freq=freq, start=start, end=end, items="ALL")
    fname = f"{code}_{freq}_{start}_{end}_{label}.csv"
    df.to_csv(OUT / fname, index=False, encoding="utf-8-sig")
    print(f"[{code}] {len(df):,} rows -> {fname}")
```

**검증**: 호출 후 `0_raw/ecos_macro/_manifest.csv` 에 3개 line 추가 (기존 11개 → 14개).

### 1.2 분기 panel 집계

`2_scripts/build_panel/5A_macro_quarterly_panel.py`:

```python
# 5A_macro_quarterly_panel.py
"""
ECOS 14개 시리즈 → 분기 단위 한국 거시 panel.
월별 시리즈는 quarter 평균/말 (시리즈 성격에 따라 결정).
산출: 3_derived/macro/macro_quarterly_panel.parquet

컬럼:
  year, quarter,
  gdp_growth_yoy,         # 200Y007 그대로
  fx_kr_usd,              # 731Y004 분기말 환율
  fx_kr_usd_logreturn,    # log(fx_t / fx_{t-1})
  px_export,              # 401Y014 분기 평균
  px_import,              # 401Y015 분기 평균
  cpi,                    # 901Y009 분기 평균
  cpi_yoy,                # YoY % 변화
  bok_rate,               # 722Y001 분기말
  bok_rate_d,             # bok_rate 차분
  m1, m2, mb,             # 161Y001, 161Y006, 102Y002 분기 평균

검증:
  - 1차: 시계열 길이 (2000Q1 ~ 2024Q4 = 100 분기)
  - 2차: NaN check (gdp_growth_yoy 는 일부 누락 가능 — 명시 flag)
  - 3차: 환율 logreturn 의 mean ≈ 0, std ~ 0.04 (분기 단위, 한국 실측)
"""
```

### 1.3 5-year stack 단위 집계 보조

회귀에 쓸 form 은 5-year stacked. 분기 panel 을 5-year 평균 / log change 로 집계:

```python
# 5B_macro_5yr_stack.py
"""
macro_quarterly_panel.parquet → 5-year stack
stack: 2000-2004, 2005-2009, 2010-2014, 2015-2019, 2020-2024 (= 5 stack)

각 stack 내 평균 / 5-year log change 계산:
  d5_gdp_growth   = mean(gdp_growth_yoy) over the stack
  d5_fx_logret    = sum(log return) over the stack
  d5_cpi_yoy      = mean(cpi_yoy)
  d5_bok_rate_d   = sum(d) over the stack
  d5_px_export_logret, d5_px_import_logret
"""
```

---

## 2. 산출물 2 — `weo_korea_vintages.parquet`

`2_scripts/data_collection/13_weo_korea_extract.py`:

```python
# 13_weo_korea_extract.py
"""
IMF WEO Historical Forecasts xlsx → Korea 연간 forecast vintage matrix.

입력: 0_raw/weo/WEOhistorical.xlsx  (수동 배치 필요 — 사용자 업로드)
출력: 3_derived/macro/weo_korea_vintages.parquet

shape: (year, vintage) → real GDP growth forecast %
  year: 1988 ~ 2024 (raw 파일은 2022까지)
  vintage: ['S1990', 'F1990', 'S1991', 'F1991', ..., 'F2022'] (66 vintage)

추가 derived columns:
  realized_gdp = year-row의 가장 최신 vintage value (= 사후 실측)
  surprise_F_minus_1 = realized - F{year-1} forecast = year-1 가을 발행 forecast 대비 surprise
  surprise_S_year     = realized - S{year} forecast    = year 봄 발행 nowcast 대비
"""
import openpyxl, pandas as pd
from pathlib import Path
from lib.config import RAW_DIR, DERIVED_DIR

WEO = RAW_DIR / "weo" / "WEOhistorical.xlsx"
OUT = DERIVED_DIR / "macro" / "weo_korea_vintages.parquet"

wb = openpyxl.load_workbook(WEO, read_only=True, data_only=True)
ws = wb["ngdp_rpch"]

rows = list(ws.iter_rows(values_only=True))
header = rows[0]
data = [r for r in rows[1:] if r[2] == "KOR"]   # ISO Alpha-3
df = pd.DataFrame(data, columns=header)

# 'year' 와 vintage cols 만 유지
vintage_cols = [c for c in header if isinstance(c, str) and c.endswith("ngdp_rpch")]
df = df[["year"] + vintage_cols].copy()
df = df.replace(".", pd.NA).apply(lambda c: pd.to_numeric(c, errors="coerce"))

# realized = 가장 최신 vintage value (각 year 별)
def latest_realized(row):
    s = row.drop("year").dropna()
    return s.iloc[-1] if len(s) else pd.NA
df["realized"] = df.apply(latest_realized, axis=1)

# surprise: F{Y-1} = year-1 fall forecast for year Y
def surprise(row, kind):
    y = int(row["year"])
    if kind == "F-1":
        col = f"F{y-1}ngdp_rpch"
    elif kind == "S0":
        col = f"S{y}ngdp_rpch"
    return row["realized"] - row[col] if col in row.index and pd.notna(row[col]) else pd.NA
df["surprise_F_minus_1"] = df.apply(lambda r: surprise(r, "F-1"), axis=1)
df["surprise_S_year"] = df.apply(lambda r: surprise(r, "S0"), axis=1)

OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(OUT, index=False)
print(f"[WEO Korea] year range {df.year.min()}-{df.year.max()}, vintages {len(vintage_cols)}, "
      f"surprise_F_minus_1 nonnull {df.surprise_F_minus_1.notna().sum()}")
```

**선행 작업**: WEO xlsx 파일을 `0_raw/weo/WEOhistorical.xlsx` 로 복사. 사용자가 업로드한 위치는 별도 (uploads/) — Claude Code 가 직접 가져올 수 없으므로 사용자가 수동 복사.

```bash
mkdir -p 0_raw/weo
cp <사용자_업로드_경로>/WEOhistorical.xlsx 0_raw/weo/
```

**검증**: surprise_F_minus_1 의 mean ≈ 0 (forecast unbiasedness 의 약한 형태), std ~ 1-2 percentage point (한국 한정).

---

## 3. 산출물 3 — `bilateral_exposure_5yr.parquet`

`2_scripts/build_panel/4B_bilateral_exposure_aggregate.py`:

```python
# 4B_bilateral_exposure_aggregate.py
"""
KR <-> CN bilateral 무역 raw → 5-year stacked exposure index.

raw 입력:
  0_raw/comtrade_korea_china/KR_imp_from_CN_{year}.csv  (25 files, 2000-2024)
  0_raw/comtrade_korea_china/KR_exp_to_CN_{year}.csv    (25 files)

출력: 3_derived/trade/bilateral_exposure_5yr.parquet

aggregation grain (Phase A scope):
  (1) total: 전체 합계 (HS 무관) → year-level scalar
  (2) hs2:   HS 2자리 chapter (cmdCode 처음 2 digit) → (year × hs2) 매트릭스

5-year stack:
  stack 정의: ['2000-2004', '2005-2009', '2010-2014', '2015-2019', '2020-2024']
  per-stack value = sum of primaryValue (USD nominal)
  net_exposure     = imp_value - exp_value
  d5_net_logchange = log(net_t) - log(net_{t-5})  for t = 2005, 2010, 2015, 2020 (4 stack 차이)
  d5_imp_logchange, d5_exp_logchange 도 별도 산출

컬럼 (total grain):
  stack, year_start, year_end, imp_value, exp_value, net_value, d5_net_logchange,
  d5_imp_logchange, d5_exp_logchange

컬럼 (hs2 grain):
  stack, hs2, year_start, year_end, imp_value, exp_value, net_value,
  d5_net_logchange, d5_imp_logchange, d5_exp_logchange

검증:
  - cross-check: total grain의 stack-level imp_value vs trade_collection_validation.md
    spot 값과 ±0.5% 이내 일치
  - HS2 sum = total (per stack, per direction)
"""
```

---

## 4. 산출물 4 — `adh8_exposure_5yr.parquet`

`2_scripts/build_panel/4C_adh8_exposure_aggregate.py`:

```python
# 4C_adh8_exposure_aggregate.py
"""
ADH 8국 imports from CN → 5-year stacked exposure shock (instrument).

raw 입력:
  0_raw/comtrade_adh_china/{ISO}_{year}.csv  (8 countries × 25 years = 200 files)

출력: 3_derived/trade/adh8_exposure_5yr.parquet

8 countries: AU, DK, FI, DE, JP, NZ, ES, CH

aggregation:
  per (country, year, hs2): sum of primaryValue (USD nominal)
  per (year, hs2): sum across 8 countries  → ADH-8 aggregate
  per (year): total sum (HS 무관)

5-year stack: 위 b1과 동일

컬럼 (total grain):
  stack, year_start, year_end, adh8_imp_value, d5_adh8_logchange

컬럼 (hs2 grain):
  stack, hs2, year_start, year_end, adh8_imp_value, d5_adh8_logchange
  + per-country 8개 (AU, DK, ..., CH) 의 imp_value 별도 보존 (debugging 용)

검증:
  - 8개국 sum = country-level sum (per stack, per hs2)
  - cross-check: total grain 의 stack 별 imp_value 가 KOSIS / WTO 통계와 ±2% 일치 (가능 시)
"""
```

---

## 5. 통합 실행 스크립트

`2_scripts/run_phase_A.sh` (또는 `.bat` for Windows):

```bash
#!/bin/bash
# Phase A 일괄 실행
set -e

cd "$(dirname "$0")/.."

echo "[1/4] ECOS 신규 시리즈 호출"
python 2_scripts/data_collection/12_ecos_test1_macro_vars.py

echo "[2/4] WEO Korea vintage 추출"
mkdir -p 0_raw/weo
# WEOhistorical.xlsx 가 0_raw/weo/ 에 있어야 함 — 사용자가 수동 배치
[ ! -f 0_raw/weo/WEOhistorical.xlsx ] && {
  echo "ERROR: 0_raw/weo/WEOhistorical.xlsx 없음. 사용자 업로드 파일을 수동 복사하세요."
  exit 1
}
python 2_scripts/data_collection/13_weo_korea_extract.py

echo "[3/4] macro 분기 panel + 5-year stack 빌드"
python 2_scripts/build_panel/5A_macro_quarterly_panel.py
python 2_scripts/build_panel/5B_macro_5yr_stack.py

echo "[4/4] bilateral & ADH-8 노출 5-year stack 빌드"
python 2_scripts/build_panel/4B_bilateral_exposure_aggregate.py
python 2_scripts/build_panel/4C_adh8_exposure_aggregate.py

echo "[done] Phase A 완료. 산출물:"
ls -la 3_derived/macro/macro_quarterly_panel.parquet
ls -la 3_derived/macro/macro_5yr_stack.parquet
ls -la 3_derived/macro/weo_korea_vintages.parquet
ls -la 3_derived/trade/bilateral_exposure_5yr.parquet
ls -la 3_derived/trade/adh8_exposure_5yr.parquet
```

---

## 6. 검증 게이트 (Phase B 진입 전 필수)

Phase A 완료 후 다음 5개 모두 PASS 해야 Phase B 진입:

| # | 체크 | PASS 기준 |
|---|------|-----------|
| 1 | macro_quarterly_panel | shape ≥ (100, 12), gdp_growth NaN < 5% |
| 2 | macro_5yr_stack | shape = (5, ≥6 cols) |
| 3 | weo_korea_vintages | year ∈ [1988, 2022], surprise_F_minus_1 nonnull ≥ 30 |
| 4 | bilateral_exposure_5yr (total) | 5 stack × {imp, exp, net} 모두 양수, d5 4 stack |
| 5 | adh8_exposure_5yr (total) | 5 stack × adh8_imp_value > 0, d5 4 stack |

각 PASS 결과를 `5_logs/integrity_checks/2026-05-04_phase_A_validation.md` 에 기록.

---

## 7. Phase B 미리보기 (참고만, 실행 X)

Phase A 완료 후 다음을 실행:
- Test 1 (Romer-Romer): `bilateral_exposure_5yr` 의 d5_net_logchange ~ lagged macro_5yr_stack
- Test 1b (WEO surprise): d5_net_logchange ~ lagged weo_surprise
- Test 3 (Pierce-Schott pre-trend): 1995-1999 sigungu mortality ~ 1997 baseline shares × bilateral exposure
- First-stage F: d5_bilateral_net ~ d5_adh8 + controls (KP rk-Wald F)

이 4개는 모두 Phase A 산출물 4개 + 기존 mortality / shares panel 만으로 실행 가능.

