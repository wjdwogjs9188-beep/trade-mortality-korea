# Claude Code Prompt — Stage 4A 무역 데이터 수집 (v1)

## 작업 목적

Pierce-Schott 2020 / Autor-Dorn-Hanson 2013 표준 IV 설계용 양국 무역 panel 구축.

**Endogenous variable**: KR ← CN HS6 import flow (한국의 대중국 수입 충격)
**Instrument**: 8 OHIE ← CN HS6 import flow (8개 Other High-Income Economies 의 대중국 수입 — 한국 demand shock 와 무관한 China supply-side variation 추출)

8 OHIE = Australia, Denmark, Finland, Germany, Japan, New Zealand, Spain, Switzerland (Pierce-Schott 표준 set, ADH 와 동일).

## 입력 파일

외부 데이터 — 직접 다운로드:
- BACI database (CEPII): https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
- UN Comtrade API: https://comtradeapi.un.org/data/v1/get/C/A/HS (cross-check 용)
- KITA 한국무역통계 (선택): https://www.kita.net (한국 측 자료, mirror cleaning 비교용)

## 산출물

```
4_trade/raw/baci/                                 # BACI raw 다운로드 (HS92, HS96, HS02, HS07, HS12, HS17, HS22 vintages)
4_trade/raw/comtrade/                             # Comtrade cross-check (선택)
4_trade/processed/baci_kr_cn_hs6_panel.parquet    # KR ← CN HS6 import (1995-2023)
4_trade/processed/baci_ohie_cn_hs6_panel.parquet  # 8 OHIE ← CN HS6 import (1995-2023)
4_trade/processed/trade_panel_v01.parquet         # 통합 panel (year × HS6 × indicator)
4_trade/trade_collection_validation.md            # 검증 보고서
```

---

## 처리 단계

### Step 1 — Source 선택 + 다운로드 전략 결정

**Primary source**: **BACI** (CEPII).

**이유**:
1. 1995-2023 HS6 양국 reconciled 무역 데이터 (mirror cleaning 완료)
2. Pierce-Schott, Dauth-Findeisen-Suedekum, Autor-Dorn-Hanson 등 학술 표준 source
3. 한 번에 zip 다운로드 가능 (Comtrade API rate limit 회피)
4. HS vintage별 (HS92/HS96/HS02/HS07/HS12/HS17/HS22) 분리 제공 → time-consistent classification 가능

**Cross-check**: UN Comtrade (HS6 × year × KR × CN 일부 sample) — BACI 의 mirror cleaning 정합성 확인.

### Step 2 — BACI 다운로드

```python
# BACI download structure (CEPII):
# Files: BACI_HS{vintage}_Y{year}_V{release}.csv
# Columns: t (year), i (exporter ISO3 numeric), j (importer ISO3 numeric), k (HS6), v (value USD), q (quantity)

import requests, zipfile, io, pathlib

BACI_DOWNLOAD_URLS = {
    "HS92": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS92_V202501.zip",  # 1995-1996
    "HS96": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS96_V202501.zip",  # 1996-2001
    "HS02": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS02_V202501.zip",  # 2002-2006
    "HS07": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS07_V202501.zip",  # 2007-2011
    "HS12": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS12_V202501.zip",  # 2012-2016
    "HS17": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS17_V202501.zip",  # 2017-2021
    "HS22": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS22_V202501.zip",  # 2022-2023
}
# 주의: V 버전 (202501, 202401 등) 은 release 시점에 따라 변경. CEPII 사이트에서 latest 확인.

OUTPUT_DIR = pathlib.Path("4_trade/raw/baci")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for vintage, url in BACI_DOWNLOAD_URLS.items():
    target = OUTPUT_DIR / f"{vintage}.zip"
    if target.exists():
        print(f"  skip {vintage} (already downloaded)")
        continue
    print(f"  downloading {vintage} ...")
    r = requests.get(url, stream=True, timeout=600)
    r.raise_for_status()
    target.write_bytes(r.content)
    print(f"    -> {target} ({target.stat().st_size/1e6:.1f} MB)")
```

**주의**:
1. BACI release 버전 (V202501) 은 매년 변경. CEPII 사이트에서 latest URL 직접 확인 후 업데이트.
2. 각 zip 파일 크기 1-3 GB. 전체 ~10 GB.
3. 다운로드 실패 시 manual download 후 `4_trade/raw/baci/` 에 unzip.
4. Country code 매핑 파일 (`country_codes_V202501.csv`) 도 함께 다운로드 — i, j 컬럼은 ISO3 numeric (KOR=410, CHN=156 등).

### Step 3 — KR-CN 양국 panel 추출

```python
import pandas as pd, glob

# Country codes
KR_NUM = 410   # Korea, Republic of
CN_NUM = 156   # China

OHIE_NUM = {
    "AUS": 36,   # Australia
    "DNK": 208,  # Denmark
    "FIN": 246,  # Finland
    "DEU": 276,  # Germany
    "JPN": 392,  # Japan
    "NZL": 554,  # New Zealand
    "ESP": 724,  # Spain
    "CHE": 756,  # Switzerland
}

# Process all BACI vintages
all_kr_cn = []
all_ohie_cn = []

for vintage_dir in sorted(OUTPUT_DIR.glob("HS*")):
    for csv_file in sorted(vintage_dir.glob("BACI_*_Y*_V*.csv")):
        df = pd.read_csv(csv_file, dtype={"t": str, "i": int, "j": int, "k": str, "v": float})
        # KR ← CN: importer=KR, exporter=CN
        kr_cn = df[(df["i"] == CN_NUM) & (df["j"] == KR_NUM)].copy()
        kr_cn["importer"] = "KOR"
        kr_cn["vintage"] = vintage_dir.name
        all_kr_cn.append(kr_cn)
        # 8 OHIE ← CN: importer=OHIE, exporter=CN
        ohie_cn = df[(df["i"] == CN_NUM) & (df["j"].isin(OHIE_NUM.values()))].copy()
        # importer ISO3 매핑
        num_to_iso = {v: k for k, v in OHIE_NUM.items()}
        ohie_cn["importer"] = ohie_cn["j"].map(num_to_iso)
        ohie_cn["vintage"] = vintage_dir.name
        all_ohie_cn.append(ohie_cn)

kr_cn_panel = pd.concat(all_kr_cn, ignore_index=True)
ohie_cn_panel = pd.concat(all_ohie_cn, ignore_index=True)

# Standardize columns: year, hs6, importer, value_usd
for d in [kr_cn_panel, ohie_cn_panel]:
    d.rename(columns={"t": "year", "k": "hs6", "v": "value_usd"}, inplace=True)
    d["hs6"] = d["hs6"].astype(str).str.zfill(6)

kr_cn_panel.to_parquet("4_trade/processed/baci_kr_cn_hs6_panel.parquet", index=False)
ohie_cn_panel.to_parquet("4_trade/processed/baci_ohie_cn_hs6_panel.parquet", index=False)
```

**주의**: BACI 의 i = exporter, j = importer (CEPII 표준). 다른 source 와 헷갈리지 말 것.

### Step 4 — HS vintage 통합 (time-consistent HS6 classification)

문제: HS6 코드는 5년마다 개정 (HS92, HS96, HS02, HS07, HS12, HS17, HS22). 같은 상품이 vintage 마다 다른 코드를 가질 수 있음 → time-series 분석 시 시계열 일관성 깨짐.

해결: WTO/UN concordance 사용하여 모든 vintage 를 **HS92 또는 HS96** baseline 으로 통합.

```python
# WTO concordance tables 다운로드 (또는 CEPII 부속 파일 사용)
# https://wits.worldbank.org/product_concordance.html
# 표준 방식: HS22 → HS17 → HS12 → HS07 → HS02 → HS96 → HS92 chain mapping

# 학술 standard: ADH (HS96), Pierce-Schott (HS92 or HS96)
# 본 paper 권장: HS96 baseline (Korean trade data 1995 부터 cover, HS96 가 가장 안정)

# concordance 적용 후 hs6_consistent 컬럼 추가
kr_cn_panel["hs6_consistent"] = kr_cn_panel.apply(map_to_hs96, axis=1)
ohie_cn_panel["hs6_consistent"] = ohie_cn_panel.apply(map_to_hs96, axis=1)
```

**주의**: Concordance 적용 시 1:N 매핑 (한 신 코드가 여러 구 코드로 분리) → value 분배 방식 표준화 필요. CEPII 또는 WITS 의 weighted concordance 권장.

이 step 은 복잡하고 시간 소요 → **1차 prototype 단계에서는 vintage 별 raw 그대로 유지** + Stage 4B 에서 concordance 정밀 처리. 이번 Step 4 는 logging 만 (각 vintage 별 row 수, value 합계 보고).

### Step 5 — 통합 trade panel 생성

```python
# Long format: year × hs6 × importer × indicator
panel_long = pd.concat([
    kr_cn_panel.assign(indicator="kr_cn_import"),
    ohie_cn_panel.assign(indicator="ohie_cn_import"),
], ignore_index=True)

# 각 (year, hs6, importer) 조합별 value 합 (vintage 안 쪽 중복 방지)
panel_agg = panel_long.groupby(
    ["year", "hs6", "importer", "indicator"], as_index=False
)["value_usd"].sum()

panel_agg.to_parquet("4_trade/processed/trade_panel_v01.parquet", index=False)
```

### Step 6 — UN Comtrade cross-check (선택)

BACI 의 mirror cleaning 결과가 Comtrade raw 와 일관되는지 spot check:

```python
# UN Comtrade API: free tier 100 calls/hour
# Sample: KR ← CN HS6 = 854231 (반도체 IC) for 2010, 2015, 2020, 2023
import requests, time

API_KEY = ""  # 비어있으면 free tier
def comtrade_call(year, reporter, partner, cmd):
    url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
    params = {
        "reporterCode": reporter,
        "partnerCode": partner,
        "period": year,
        "cmdCode": cmd,
        "flowCode": "M",  # M = Import
        "freqCode": "A",  # A = Annual
    }
    r = requests.get(url, params=params, headers={"Ocp-Apim-Subscription-Key": API_KEY} if API_KEY else {})
    time.sleep(2)  # rate limit
    return r.json()

# Sample 4 cells comparison
sample_codes = ["854231", "854011", "640299", "271019"]
for year in ["2010", "2015", "2020", "2023"]:
    for cmd in sample_codes:
        ct = comtrade_call(year, 410, 156, cmd)
        baci_val = panel_agg[(panel_agg["year"]==year) & (panel_agg["hs6"]==cmd) & 
                              (panel_agg["importer"]=="KOR")]["value_usd"].sum()
        print(f"  {year} HS{cmd}: BACI={baci_val:,.0f} | Comtrade={ct...}")
```

**합격 기준**: ±5% 이내 일치 (mirror cleaning 차이 정상 범위).

### Step 7 — 검증

#### V1 — Year coverage
```python
years = sorted(panel_agg["year"].unique())
expected = [str(y) for y in range(1995, 2024)]
assert set(years) == set(expected), f"missing years: {set(expected) - set(years)}"
```

#### V2 — Importer coverage
```python
expected_imp = {"KOR", "AUS", "DNK", "FIN", "DEU", "JPN", "NZL", "ESP", "CHE"}
actual_imp = set(panel_agg["importer"].unique())
assert actual_imp == expected_imp
```

#### V3 — HS6 coverage
```python
n_hs6 = panel_agg["hs6"].nunique()
assert 4500 <= n_hs6 <= 5500, f"HS6 count {n_hs6} out of expected range"
# HS6 code 약 5,000개 (vintage 마다 다름). 모든 vintage 통합 시 unique HS6 약 7,000.
```

#### V4 — KR-CN annual flow sanity check
```python
KR_CN_OFFICIAL = {  # KITA 한국무역협회 공식 통계 (단위: million USD)
    "2000": 12798,  # KR import from CN
    "2010": 71574,
    "2015": 90250,
    "2020": 108885,
    "2023": 142800,
}
for y, official in KR_CN_OFFICIAL.items():
    panel_total = panel_agg[(panel_agg["year"]==y) & (panel_agg["importer"]=="KOR") & 
                             (panel_agg["indicator"]=="kr_cn_import")]["value_usd"].sum() / 1e6
    diff_pct = abs(panel_total - official) / official * 100
    print(f"  {y}: BACI={panel_total:,.0f} | KITA={official:,} | diff={diff_pct:.2f}%")
    assert diff_pct < 5.0, f"BACI vs KITA diff > 5% in {y}"
```

#### V5 — 8 OHIE ← CN flow sanity check
```python
OHIE_CN_OFFICIAL = {  # WTO Trade Profiles, OHIE 8국 합계 import from CN (million USD)
    "2010": 250000,  # approx
    "2020": 600000,  # approx
}
for y, official in OHIE_CN_OFFICIAL.items():
    panel_total = panel_agg[(panel_agg["year"]==y) & (panel_agg["importer"].isin(OHIE_NUM.keys())) & 
                             (panel_agg["indicator"]=="ohie_cn_import")]["value_usd"].sum() / 1e6
    print(f"  {y} OHIE total: BACI={panel_total:,.0f} | WTO~={official:,}")
    # 합격 기준 ±10% (WTO official 추정값 기반이라 보수적)
```

#### V6 — Comtrade cross-check sample (Step 6 결과)
```python
# Sample 4 cells 모두 ±5% 이내
```

#### V7 — Vintage 별 정합성 (overlap years)
```python
# HS96 vintage 와 HS02 vintage 가 모두 cover 하는 연도 (2002 등) 에서 같은 (importer, hs6) 의 value 가 ±2% 이내
```

---

## Expected 결과

- BACI 다운로드: 7개 vintage zip 파일 (~10 GB)
- `baci_kr_cn_hs6_panel.parquet`: 약 200,000-500,000 rows (29 year × 5,000 HS6)
- `baci_ohie_cn_hs6_panel.parquet`: 약 1,500,000-3,500,000 rows (29 year × 5,000 HS6 × 8 importer)
- `trade_panel_v01.parquet`: 통합 long format
- V1-V5 PASS 필수, V6-V7 권장

---

## 결과 검토 (사용자 직접 확인)

다음 6가지 본인이 직접 검증:

1. BACI 7개 vintage 다운로드 완료 (각 zip 파일 크기 1-3GB 범위)
2. KR-CN HS6 panel 행 수 약 200k-500k 범위
3. OHIE-CN HS6 panel 행 수 약 1.5M-3.5M 범위
4. KITA cross-check 5년 모두 ±5% 이내 (V4)
5. Year cover 1995-2023 (29년) (V1)
6. Importer 9개 (KOR + 8 OHIE) (V2)

위 6개 OK 면 Stage 4A 채택.

---

## 주의 사항

1. **CEPII BACI URL 버전 확인**: V202501 등 release 버전이 매년 갱신. https://www.cepii.fr 에서 latest 확인 후 URL 업데이트.
2. **Country code 표준**: BACI 는 ISO3 numeric 사용 (KOR=410, CHN=156 등). UN Comtrade 와 동일.
3. **Mirror cleaning 차이**: BACI 는 reporter 와 partner 양측 보고를 reconcile. 단방향 raw flow (KR import from CN) 와 약간 다를 수 있음. ±5% 이내 정상.
4. **HS vintage 통합**: Step 4 는 prototype 단계 skip. Stage 4B (concordance 정밀 처리) 에서 처리.
5. **KSIC2-HS6 concordance**: 본 step 에 포함 안 함. Stage 4B 에서 별도 처리 (Pierce-Schott / Dauth-Findeisen-Suedekum 표준 concordance 사용).
6. **HS6 0 cell 처리**: 양국 무역 0인 HS6-year 조합은 panel 에 row 없음. 회귀 분석 시 0 채워서 balanced panel 생성 (Stage 4C 에서 처리).
7. **Free Comtrade API rate limit**: 100 calls/hour, 1000/day. Step 6 cross-check 만 하면 충분 (16 calls).

---

## 다음 Stage 4B (예정)

- HS vintage time-consistent concordance 적용 (HS96 baseline)
- KSIC2-HS6 concordance (Pierce-Schott 또는 Dauth-Findeisen-Suedekum 표준)
- 시군구 × KSIC2 산업 비중 결합 → Bartik shift 구축
- KR-CN import 변화 (Δ5yr) 계산
- IV: 8 OHIE → CN import 변화 (Δ5yr)

---

이 prompt 를 Claude Code 에 file path 로 전달:
`C:\Users\82103\Desktop\뉴 논문\crosswalks\claude_code_prompt_stage4a_trade_collection.md`
