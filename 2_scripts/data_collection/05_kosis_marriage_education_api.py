"""KOSIS API 로 혼인상태별 + 교육정도별 시군구 인구 다운로드.

mediator rate 분모용 (paper § 5.2 mediation analysis).
12 URL = 6 시점 (1995, 2000, 2005, 2010, 2015, 2020) × (혼인 + 교육) 2 dimension.

사용자 KOSIS_API_KEY: URL 의 인증키 그대로 사용 (.env 불필요).

산출:
    0_raw/kosis_marriage_education/
    ├── kosis_marriage_1995.csv  (DT_1IN9503)
    ├── kosis_marriage_2000.csv  (DT_1PM0001)
    ├── kosis_marriage_2005.csv  (DT_1IN0508)
    ├── kosis_marriage_2010.csv  (DT_1IN1006)
    ├── kosis_marriage_2015.csv  (DT_1PM1504)
    ├── kosis_marriage_2020.csv  (DT_1PM2002)
    ├── kosis_education_1995.csv (DT_1IN9502)
    ├── kosis_education_2000.csv (DT_1INOO02)
    ├── kosis_education_2005.csv (DT_1IN0504)
    ├── kosis_education_2010.csv (DT_1IN1004)
    ├── kosis_education_2015.csv (DT_1PM1501)
    └── kosis_education_2020.csv (DT_1PM2001)

실행:
    cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
    python 2_scripts\\data_collection\\05_kosis_marriage_education_api.py
"""

from __future__ import annotations
import json
import re
import time
import sys
from pathlib import Path
import pandas as pd
import requests

# === Configuration ===
ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "0_raw" / "kosis_marriage_education"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 기존 다운로드 파일 무시하고 재실행 여부 (outputFields fix 후 재실행 = True)
FORCE_REDOWNLOAD = True

# 표준 outputFields (시군구 dimension 코드/이름 포함)
# - OBJ_ID + NM: dimension value ID + name
# - C1 ~ C5 + C*_NM: 분류 코드 + 이름 (시군구 detail 핵심)
STANDARD_OUTPUT_FIELDS = (
    "outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_ID+NM"
    "+ITM_ID+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE"
    "+C1+C1_NM+C2+C2_NM+C3+C3_NM+C4+C4_NM+C5+C5_NM"
)


def patch_output_fields(url: str) -> str:
    """URL 의 `outputFields=...&` 부분을 표준 outputFields 로 교체.

    KOSIS API 가 dimension code (C1, C2, ..., C5) 와 이름 (C1_NM, ...) 을
    response 에 포함하도록 강제 — 시군구 detail 회복 핵심.
    """
    return re.sub(r"outputFields=[^&]+", STANDARD_OUTPUT_FIELDS, url)

# 사용자 제공 KOSIS API URL 9 개
URLS = {
    "marriage_1995": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T1+T2+T3+&objL1=ALL&objL2=000+100+120+130+150+160+180+190+210+230+260+280+310+330+360+370+990+&objL3=ALL&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=1995&endPrdDe=1995&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN9503",
    "education_1995": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T1+T2+T3+&objL1=ALL&objL2=00+11+15+20+25+30+35+40+45+50+55+60+62+95+&objL3=ALL&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=1995&endPrdDe=1995&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN9502",
    "marriage_2000": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T1+&objL1=ALL&objL2=ALL&objL3=000+100+120+130+150+160+180+190+210+230+260+280+310+330+360+370+990+&objL4=ALL&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2000&endPrdDe=2000&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM0001",
    "education_2000": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T1+T2+T3+&objL1=ALL&objL2=00+11+15+20+25+30+35+40+45+50+55+60+65+70+72+95+&objL3=ALL&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2000&endPrdDe=2000&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1INOO02",
    "marriage_2005": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T11+T12+T13+T14+T20+T21+T22+T23+T24+T30+T31+T32+T33+T34+&objL1=ALL&objL2=000+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2005&endPrdDe=2005&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN0508",
    "education_2005": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T60+T61+T62+T63+T64+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=000+010+015+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2005&endPrdDe=2005&outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_ID+NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN0504",
    "marriage_2010": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=ALL&objL4=ALL&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2010&endPrdDe=2010&outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_NM+ITM_ID+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN1006",
    "marriage_2015": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=ALL&objL4=ALL&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2015&endPrdDe=2015&outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_NM+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM1504",
    "marriage_2020": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T11+T12+T13+T14+T20+T21+T22+T23+T24+T30+T31+T32+T33+T34+&objL1=ALL&objL2=000+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2020&endPrdDe=2020&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM2002",
    "education_2010": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=000+010+015+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2010&endPrdDe=2010&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN1004",
    "education_2015": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=000+010+015+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2015&endPrdDe=2015&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM1501",
    "education_2020": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=000+010+015+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2020&endPrdDe=2020&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM2001",
}

# === KOSIS API call function ===

# 17 시도 코드 (KOSIS 행정구역 표준)
# 코드: 11서울 21부산 22대구 23인천 24광주 25대전 26울산 29세종
#      31경기 32강원 33충북 34충남 35전북 36전남 37경북 38경남 39제주
SIDO_CODES = ["11", "21", "22", "23", "24", "25", "26", "29",
              "31", "32", "33", "34", "35", "36", "37", "38", "39"]
SEJONG_CODE = "29"
SEJONG_BIRTH_YEAR = 2012  # 세종특별자치시 출범


def parse_year_from_label(label: str) -> int | None:
    """'marriage_2010' → 2010 추출."""
    m = re.search(r"_(\d{4})$", label)
    return int(m.group(1)) if m else None


def fetch_kosis_split(label: str, base_url: str) -> pd.DataFrame:
    """시도 별 분할 호출 후 합치기 (40,000 cell limit 회피).

    URL 의 `objL1=ALL` 또는 `objL1=&` 를 `objL1={sido_code}` 로 substitute.
    세종 (29) 은 2012 이전 표에서 부재 → skip (err 21 회피).
    """
    year = parse_year_from_label(label)
    all_dfs = []
    for sido in SIDO_CODES:
        # 세종 2012 이전 skip (err 21 정상)
        if sido == SEJONG_CODE and year is not None and year < SEJONG_BIRTH_YEAR:
            print(f"  [skip] {label} sido={sido} (세종 {SEJONG_BIRTH_YEAR} 이전)")
            continue
        # URL 변형 (objL1 = sido 코드 specific)
        if "objL1=ALL" in base_url:
            url = base_url.replace("objL1=ALL", f"objL1={sido}")
        elif "objL1=&" in base_url:
            url = base_url.replace("objL1=&", f"objL1={sido}&")
        else:
            # objL1 parameter 부재 — sido level 분할 못 함
            print(f"  [WARN] {label}: objL1 parameter 부재, 시도 split 불가")
            return fetch_kosis(label, base_url)

        sub_df = fetch_kosis(f"{label} sido={sido}", url)
        if not sub_df.empty:
            all_dfs.append(sub_df)
        time.sleep(1.5)  # KOSIS rate limit 회피

    if not all_dfs:
        print(f"  [FAIL] {label}: all sido empty")
        return pd.DataFrame()

    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"  [combined] {label}: total {len(combined):,} rows from {len(all_dfs)} sido")
    return combined


def fetch_kosis(label: str, url: str, max_retries: int = 3) -> pd.DataFrame:
    """KOSIS API 호출 + JSON parse → DataFrame.

    KOSIS API response 형태:
      - 정상: list of dict [{"TBL_ID": "...", "DT": "...", ...}, ...]
      - 에러: dict {"err": "...", "errMsg": "..."} 또는 {"RESULT": {...}}
    """
    for attempt in range(max_retries):
        try:
            r = requests.get(url, timeout=120)
            r.raise_for_status()
            data = r.json()
            if not data:
                print(f"  [WARN] {label}: empty response")
                return pd.DataFrame()

            # type check
            if isinstance(data, dict):
                # KOSIS error response
                print(f"  [API ERROR] {label}: dict response (not list)")
                print(f"    response: {json.dumps(data, ensure_ascii=False)[:500]}")
                # 가능한 error keys: err, errMsg, RESULT
                if "err" in data:
                    print(f"    err code: {data.get('err')}, msg: {data.get('errMsg', '')}")
                if "RESULT" in data:
                    print(f"    RESULT: {data['RESULT']}")
                return pd.DataFrame()

            if not isinstance(data, list):
                print(f"  [FORMAT ERROR] {label}: unexpected type {type(data).__name__}")
                return pd.DataFrame()

            df = pd.DataFrame(data)
            print(f"  [OK] {label}: {len(df):,} rows, columns={df.columns.tolist()[:6]}...")
            return df

        except requests.exceptions.RequestException as e:
            print(f"  [retry {attempt+1}] {label}: {e}")
            time.sleep(5)
        except json.JSONDecodeError as e:
            print(f"  [JSON error] {label}: {e}")
            print(f"    response: {r.text[:300]}")
            return pd.DataFrame()
    print(f"  [FAIL] {label} after {max_retries} attempts")
    return pd.DataFrame()


# === Main ===

def main() -> int:
    print("=" * 70)
    print("KOSIS Marriage + Education API 다운로드")
    print(f"  6 시점 × (혼인 + 교육) = {len(URLS)} URL")
    print(f"  저장: {OUT_DIR}")
    print("=" * 70)

    success = 0
    fail = 0
    for label, url in URLS.items():
        out_path = OUT_DIR / f"kosis_{label}.csv"
        if (not FORCE_REDOWNLOAD) and out_path.exists() and out_path.stat().st_size > 100:
            print(f"\n[skip] {label} (already downloaded, {out_path.stat().st_size/1e6:.1f} MB)")
            success += 1
            continue

        # outputFields patch (시군구 dimension 코드/이름 강제 출력)
        url_patched = patch_output_fields(url)

        print(f"\n[fetch] {label} (시도 17개 분할, outputFields patched)")
        df = fetch_kosis_split(label, url_patched)
        if df.empty:
            fail += 1
            continue
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"  [save] {out_path.name} ({len(df):,} rows, {out_path.stat().st_size/1e6:.2f} MB)")
        success += 1
        time.sleep(2)  # API rate limit 회피

    # Summary
    print()
    print("=" * 70)
    print(f"완료: {success} / {len(URLS)} 성공, {fail} 실패")
    print("=" * 70)
    print()
    print("다운로드 파일 inventory:")
    for f in sorted(OUT_DIR.glob("*.csv")):
        size_mb = f.stat().st_size / 1e6
        try:
            df = pd.read_csv(f, nrows=1)
            cols = df.columns.tolist()
            row_count = sum(1 for _ in open(f, encoding="utf-8-sig")) - 1
            print(f"  {f.name}: {row_count:,} rows, {size_mb:.2f} MB, columns={cols[:5]}...")
        except Exception as e:
            print(f"  {f.name}: read error {e}")

    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
