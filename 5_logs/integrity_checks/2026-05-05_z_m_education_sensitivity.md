# z_m_education baseline sensitivity
_2026-05-05_

- 시군구 centroid: **251**
- universities_pre1990: **175** 학교

## Baseline 1985
- 학교 수: 171

## Baseline 1990
- 학교 수: 175

## Baseline 1995
- 학교 수: 175

## Baseline 별 z_m_edu correlation
```
 z_m_edu_y1985 z_m_edu_y1990 z_m_edu_y1995
z_m_edu_y1985 1.000000 0.989395 0.989395
z_m_edu_y1990 0.989395 1.000000 1.000000
z_m_edu_y1995 0.989395 1.000000 1.000000
```

## Baseline 별 nearest distance 통계
```
 nearest_dist_km_y1985 nearest_dist_km_y1990 nearest_dist_km_y1995
count 251.000000 251.000000 251.000000
mean 18.101075 17.807773 17.807773
std 22.224901 22.070875 22.070875
min 0.000000 0.000000 0.000000
25% 0.000000 0.000000 0.000000
50% 12.626262 12.460186 12.460186
75% 28.769717 28.373575 28.373575
max 180.180512 180.180512 180.180512
```

## 시군구별 baseline 차이 (z_m_edu max - min > 0.5)
- 2 시군구 (0.8%)
- 만약 차이 큼 (>10%) → § 9.4 spec 정합성 issue, 1985 vs 2008 baseline substantive 차이
- 만약 차이 작음 (<5%) → 본 paper § 9.4 의 1985 baseline 사용 정합

## 저장: 3_derived\exposure\z_m_education_baseline_sensitivity.parquet