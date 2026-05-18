# Phase 2-B Step 5a — KIET60 매핑 inspect
_2026-05-05_

## KIET60 ↔ KSIC mapping: `0_raw\hs_ksic_concordance\KIET60_to_KSIC_v2.xlsx`
- size: 17.6 KB
- sheets: ['연계표', 'Sheet1']
- shape: (101, 5)
- columns: ['1레벨', '2레벨', '3레벨', '표준산업분류 10차', '표준산업분류 9차']
- 첫 10 rows:
```
 1레벨 2레벨 3레벨 표준산업분류 10차 표준산업분류 9차
 I0 제조업 NaN NaN NaN NaN
I1 농림어업 NaN NaN A 농업, 임업 및 어업 A 농업, 임업 및 어업
 I2 광업 NaN NaN B 광업 B 광업
 I3 제조업 I31 고위기술산업군 I3101 의약 C21 의료용 물질 및 의약품 제조업 C21 의료용 물질 및 의약품 제조업
 NaN NaN I3102 반도체 C261 반도체 제조업 C261 반도체 제조업
 NaN NaN I3103 디스플레이 C2621 표시장치 제조업 C2621 평판 디스플레이 제조업
 NaN NaN I3104 컴퓨터 C263 컴퓨터 및 주변 장치 제조업 C263 컴퓨터 및 주변장치 제조업
 NaN NaN I3105 통신기기 C264 통신 및 방송장비 제조업 C264 통신 및 방송 장비 제조업
 NaN NaN I3106 가전 C265 영상 및 음향 기기 제조업 C265 영상 및 음향기기 제조업
 NaN NaN NaN C266 마그네틱 및 광학 매체 제조업 C266 마그네틱 및 광학 매체 제조업
```

## KIET60 ↔ HS6 mapping: `0_raw\hs_ksic_concordance\KIET60_to_HS6.xlsx`
- size: 375.8 KB
- sheets: ['Sheet1']
- shape: (6909, 8)
- columns: ['hsc', 'productcode', '레벨3코드', '레벨3산업명', '레벨2코드', '레벨2산업명', '레벨1코드', '레벨1산업명']
- 첫 10 rows:
```
 hsc productcode 레벨3코드 레벨3산업명 레벨2코드 레벨2산업명 레벨1코드 레벨1산업명
10110 Live horses/asses/mules/hinnies: pure-bred breeding animals NaN NaN NaN NaN I1 농림어업
10111 Horses:-- Pure-bred breeding animals NaN NaN NaN NaN I1 농림어업
10119 Horses:-- Other NaN NaN NaN NaN I1 농림어업
10120 Asses, mules and hinnies NaN NaN NaN NaN I1 농림어업
10121 Horses; live, pure-bred breeding animals NaN NaN NaN NaN I1 농림어업
10129 Horses; live, other than pure-bred breeding animals NaN NaN NaN NaN I1 농림어업
10130 Asses; live NaN NaN NaN NaN I1 농림어업
10190 Mules and hinnies; live NaN NaN NaN NaN I1 농림어업
10210 Live bovine animals: pure-bred breeding animals NaN NaN NaN NaN I1 농림어업
10221 Cattle; live, pure-bred breeding animals NaN NaN NaN NaN I1 농림어업
```

## baseline_shares_1994_manufacturing 의 KSIC4 분포
- baseline shares rows: 9,739
- distinct KSIC4: 70
- KSIC4 sample (top 20 by employment): {'D181': 266198.0, 'D289': 128060.0, 'D343': 110992.0, 'D291': 109549.0, 'D293': 105813.0, 'D281': 96342.0, 'D369': 88933.0, 'D252': 87986.0, 'D323': 85426.0, 'D154': 85190.0, 'D151': 76383.0, 'D172': 74940.0, 'D222': 68915.0, 'D179': 68592.0, 'D193': 64425.0, 'D174': 62341.0, 'D321': 59858.0, 'D271': 58950.0, 'D221': 49126.0, 'D361': 49001.0}

## KSIC4 → KIET60 매핑 시도
- detected KSIC col: `None`
- detected KIET col: `None`
- ⚠️ KSIC 또는 KIET 컬럼 자동 인식 실패. 수동 컬럼 매핑 필요.

## HS6 → KIET60 매핑 sample (Comtrade input 준비용)
- HS col: `hsc`, KIET col: `None`

## 결정 사항

- KSIC4 → KIET60 매핑률 ≥ 90% 인지 확인
- HS code length (HS2/4/6/10) 확인 → Comtrade 와 정합성
- KSIC 6차 vs 9차 mismatch 심각 시 별도 차수 crosswalk turn
- OK 시 Step 2-B.5b (Comtrade ΔM 2000-2010 → KIET60 → Bartik IV)