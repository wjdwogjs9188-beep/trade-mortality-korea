"""KOSIS API outputFields patch test.

marriage_2020 (DT_1PM2002), 서울 (sido=11) 만 호출해서 시군구 detail 회복 verify.
실행 시간 ~10초. 정상 response 면 main script (05_*) 12 URL 재실행 진행.

verify 항목:
  1. response = list (dict 면 error)
  2. 각 row 에 C1, C1_NM, C2, C2_NM 등 dimension code/name field 존재
  3. C1_NM (또는 NM) 값이 "강남구", "종로구" 식 시군구 이름
  4. DT 값이 전국합 (8M) 이 아닌 시군구 단위 수십만~백만

실행:
    cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
    python 2_scripts\\data_collection\\test_kosis_outputfields_patch.py
"""
import re
import json
import requests

# 원본 URL (사용자 제공 marriage_2020)
ORIG_URL = (
    "https://kosis.kr/openapi/Param/statisticsParameterData.do?"
    "method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk="
    "&itmId=T10+T11+T12+T13+T14+T20+T21+T22+T23+T24+T30+T31+T32+T33+T34+"
    "&objL1=ALL"
    "&objL2=000+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+"
    "&objL3=&objL4=&objL5=&objL6=&objL7=&objL8="
    "&format=json&jsonVD=Y&prdSe=F&startPrdDe=2020&endPrdDe=2020"
    "&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+"
    "&orgId=101&tblId=DT_1PM2002"
)

# Patch outputFields → C1~C5 dimension code/name 강제 출력
NEW_OUTPUT_FIELDS = (
    "outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_ID+NM"
    "+ITM_ID+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE"
    "+C1+C1_NM+C2+C2_NM+C3+C3_NM+C4+C4_NM+C5+C5_NM"
)

url_patched = re.sub(r"outputFields=[^&]+", NEW_OUTPUT_FIELDS, ORIG_URL)
url_patched = url_patched.replace("objL1=ALL", "objL1=11")  # 서울만

print("=" * 70)
print("KOSIS outputFields PATCH TEST")
print("Target: marriage_2020 (DT_1PM2002), sido=11 (서울)")
print("=" * 70)
print(f"\nPatched URL:\n{url_patched}\n")

r = requests.get(url_patched, timeout=60)
print(f"HTTP status: {r.status_code}")

try:
    data = r.json()
except json.JSONDecodeError as e:
    print(f"[FAIL] JSON parse error: {e}")
    print(f"Response text: {r.text[:500]}")
    raise SystemExit(1)

print(f"Response type: {type(data).__name__}")

if isinstance(data, dict):
    print(f"[ERROR] dict response (not list)")
    print(f"  full response: {json.dumps(data, ensure_ascii=False)[:500]}")
    if "err" in data:
        print(f"  err code: {data.get('err')}, msg: {data.get('errMsg', '')}")
    raise SystemExit(2)

if not isinstance(data, list):
    print(f"[ERROR] unexpected type")
    raise SystemExit(3)

print(f"\n[OK] list response, {len(data):,} rows")
print(f"\nKeys (1st row): {list(data[0].keys())}\n")

print("First 5 rows:")
for i, row in enumerate(data[:5]):
    print(f"  [{i}] {json.dumps(row, ensure_ascii=False)}")

# Sigungu detail check
print("\n" + "=" * 70)
print("시군구 detail 회복 verify")
print("=" * 70)

c_keys = [k for k in data[0].keys() if k.startswith("C") and (k.endswith("_NM") or k[1:].isdigit())]
print(f"Dimension code/name keys: {c_keys}")

for k in c_keys:
    if k.endswith("_NM"):
        unique_vals = list({row.get(k) for row in data if row.get(k)})
        print(f"  {k}: {len(unique_vals)} unique, sample={unique_vals[:5]}")

# DT 첫 값 확인
print(f"\nDT 첫 값: {data[0].get('DT')}")
print("(전국합 = ~8M, 서울 시군구 단위 = ~수십만~백만 expected)")
