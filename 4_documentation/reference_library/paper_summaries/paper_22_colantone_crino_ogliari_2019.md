# [#22] Globalization and Mental Distress

## 메타정보
- **저자**: Italo Colantone (Bocconi), Rosario Crinò (Cattolica/CEPR/CESifo), Laura Ogliari (Milano/Centro d'Agliano)
- **출판년도**: 2019
- **학술지**: **Journal of International Economics** vol 119: 181-207
- **DOI**: 10.1016/j.jinteco.2019.04.008
- **JEL 분류**: F1

## Research Question
중국 수입 경쟁이 영국 worker 의 **mental distress (GHQ-12)** 에 미치는 인과 영향. 산업 단위 panel + individual fixed effects 로 selection 통제.

## Data
- BHPS (British Household Panel Survey), 1995-2007, 119 industries
- Census 와 cross-validation: BHPS 가 representative 함을 검증
- Outcome: GHQ-12 (General Health Questionnaire 12-item) — Likert mental distress score
- Worker × year panel + individual FE

## Identification
**Individual-level fixed effect spec** (region-level 이 아닌 worker-level):
```
MD_it = β1·IS_ψ5(i,t-1),t + I_i,t-6·β2 + J_ψ(i,t-1),t-6·β3
 + α_i + α_σ(i,t-1),t + α_ω(i,t-1),t + α_λ(i,t-1),t + α_m + α_h + ε
```
- IS = log change in real imports in worker's industry over 5 years
- α_i: individual FE
- α_σ,ω,λ: sector × year, occupation × year, × year FE
- IV: Chinese imports to other OECD countries (ADH-style)

**핵심**: individual FE 로 시간 불변 selection 통제. 같은 worker 가 시간에 따라 trade exposure 가 변할 때의 within-individual 변화 추정.

## Main Result
- 25→75 percentile import shock → mental distress £270/year compensation 필요
- **Right tail (severe distress)** 효과 더 큼 → trade shock 가 mental health inequality 증가
- Heterogeneity: youngest, large family, financial difficulty, short tenure, temporary contract, blue-collar / tradable job 에서 효과 큼
- **Family spillover**: 남편의 trade shock → 아내 mental distress 증가
- **Children**: paternal trade shock → child rearing investment ↓, child self-esteem ↓
- Channels: job displacement ↑, wage growth ↓, job satisfaction ↓, gloomy expectations

## Connection to Trade × Mortality Korea
**역할: SECONDARY HEALTH ANCHOR + MECHANISM ANCHOR**

- 본 paper 의 sigungu × year aggregate 와 다른 individual-level approach. Mental distress 가 mortality 의 mediator 임을 직접 증명
- 본 paper 는 individual-level NHIS data (Phase 5 mechanism) 의 이론적 anchor
- Family spillover 발견 — 본 paper 의 "wife/child mortality" outcome 추가 가능 (descriptive)

## 본 paper 와의 차별화
- **본 paper unique contribution**:
 - Korea = export-driven (Colantone 의 import-Bartik 가정 violated)
 - DFS-style net exposure framework (Colantone 못 한)
 - Mortality 직접 (Colantone 은 GHQ proxy)

## 본 paper § 1 인용 안
> "Recent evidence shows trade exposure increases mental distress (Colantone et al. 2019), 
> with effects spilling over to family members. This study extends the literature by examining 
> mortality outcomes in Korea, where the export-driven trade structure produces a fundamentally 
> different exposure pattern from the import-shock economies of Western Europe and the US."

## 본 paper § 9 mechanism 에 활용
- Individual NHIS data (Korean MDIS 신청 시) 의 mental distress proxy
- F32/F33 우울증 진단률 변화 = Colantone 의 GHQ analog
