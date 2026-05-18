"""KOSIS API dimension 구조 verify — 5 표 patched test (sido=11 만).

marriage_2020 (DT_1PM2002) = C1 시도, C2 연령 → 시군구 부재 확인됨.
나머지 5 표가 진짜로 시군구 dimension 가지는지 verify.

각 표 sido=11 (서울) patched 호출 → C1~C5 dimension 구조 + sample value 확인.

실행:
 cd C:\\Users\\82103\\Downloads\\trade_mortality_korea
 python 2_scripts\\data_collection\\test_kosis_dimension_verify.py
"""
import re
import json
import time
import requests

NEW_OUTPUT_FIELDS = (
 "outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_ID+NM"
 "+ITM_ID+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE"
 "+C1+C1_NM+C2+C2_NM+C3+C3_NM+C4+C4_NM+C5+C5_NM"
)

# 5 표: marriage 2010/2015 + education 2010/2015/2020
URLS = {
 "marriage_2010_DT_1IN1006": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=ALL&objL4=ALL&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2010&endPrdDe=2010&outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_NM+ITM_ID+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN1006",
 "marriage_2015_DT_1PM1504": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=ALL&objL4=ALL&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2015&endPrdDe=2015&outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_NM+ITM_NM+UNIT_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM1504",
 "education_2010_DT_1IN1004": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=000+010+015+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2010&endPrdDe=2010&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1IN1004",
 "education_2015_DT_1PM1501": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=000+010+015+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2015&endPrdDe=2015&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM1501",
 "education_2020_DT_1PM2001": "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MGQ0M2M4MDM5YTgwMDNjMzBlMjhmYzk3OTcxNjhjZDk=&itmId=T10+T20+T21+T22+T23+T30+T31+T32+T33+T40+T41+T42+T43+T50+T51+T52+T53+T54+T55+T60+T61+T62+T63+T64+T65+T70+T71+T72+T73+T74+T80+T81+T82+T83+T84+T90+&objL1=ALL&objL2=ALL&objL3=000+010+015+020+025+030+035+040+045+050+055+060+065+070+075+080+085+086+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=F&startPrdDe=2020&endPrdDe=2020&outputFields=ORG_ID+TBL_ID+TBL_NM+ITM_ID+ITM_NM+PRD_SE+PRD_DE+LST_CHN_DE+&orgId=101&tblId=DT_1PM2001",
}

def patch(url: str) -> str:
 """outputFields patch + objL1=ALL → objL1=11 (서울만)."""
 u = re.sub(r"outputFields=[^&]+", NEW_OUTPUT_FIELDS, url)
 return u.replace("objL1=ALL", "objL1=11")

def verify_table(label: str, url: str) -> None:
 print("=" * 70)
 print(f"TEST: {label}")
 print("=" * 70)

 url_p = patch(url)
 try:
 r = requests.get(url_p, timeout=60)
 except Exception as e:
 print(f" [HTTP ERROR] {e}\n")
 return

 print(f" HTTP {r.status_code}")
 try:
 data = r.json
 except json.JSONDecodeError:
 print(f" [JSON FL] {r.text[:300]}\n")
 return

 if isinstance(data, dict):
 print(f" [API ERROR] {json.dumps(data, ensure_ascii=False)[:400]}\n")
 return

 if not isinstance(data, list) or not data:
 print(f" [EMPTY] type={type(data).__name__}\n")
 return

 print(f" [OK] {len(data):,} rows")
 print(f" Keys: {list(data[0].keys)}")

 # C1~C5 + NM unique 분석
 c_keys = sorted([k for k in data[0].keys
 if (k.startswith("C") and k[1:].isdigit)
 or (k.startswith("C") and k.endswith("_NM"))])
 print(f" Dimension columns: {c_keys}")
 for k in c_keys:
 if k.endswith("_NM"):
 uniq = sorted({row.get(k) for row in data if row.get(k)})
 print(f" {k}: {len(uniq)} unique, sample={uniq[:6]}")

 # DT 첫 값 + sample row
 print(f" DT first 3: {[row.get('DT') for row in data[:3]]}")
 print(f" Sample row: {json.dumps(data[0], ensure_ascii=False)}\n")

def main -> None:
 for label, url in URLS.items:
 verify_table(label, url)
 time.sleep(2)

if __name__ == "__main__":
 main
