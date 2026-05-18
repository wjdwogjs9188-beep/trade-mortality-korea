# [#24] The Transformation of Manufacturing and the Decline in U.S. Employment

## 메타정보
- **저자**: Kerwin Kofi Charles (Chicago Harris), Erik Hurst (Booth), Mariel Schwartz (Chicago)
- **출판년도**: 2018 working paper / 2019 NBER Macro Annual published
- **학술지**: **NBER Macroeconomics Annual** vol 33: 307-372 (University of Chicago Press)
- **WP version**: BFI WP 2018-20 / NBER WP 24468

## Research Question
2000년 이후 manufacturing 부문 변화 (capital intensification + employment 감소) 가 prime-age employment 와 **opioid 사용·death** 에 미치는 영향.

## Data
- US 722 commuting zones, 2000-2017
- Manufacturing employment share, capital-labor ratio, output
- CPS, ACS, BRFSS, CDC Wonder mortality (drug overdose)
- Cross-region variation

## Identification
Cross-CZ shift-share IV:
```
Δemp_rate_cz = α + β·Δmanuf_share_cz + γX + ε
```
IV: ADH 2013-style instrument (Chinese imports, OECD)

## Main Result
- Manufacturing share 10 ppt 감소 → prime-age male employment rate -3.7 ppt, female -2.7 ppt
- 2000-2017 prime-age male employment 4.6 ppt 감소 의 1/3 ~ 1/2 가 manufacturing decline 이 설명
- **Opioid death link**: declining local manufacturing emp ↑ → local opioid use ↑, opioid death ↑
- Demand-side (manufacturing decline) 가 supply-side (opioid availability) 만큼 중요한 driver

## Connection to Trade × Mortality Korea
**역할: § 9 MECHANISM ANCHOR — manufacturing decline → drug death channel**

- Pierce-Schott 2020 AERI 의 NTR gap × suicide/opioid death 의 micro foundation
- 본 paper 의 mechanism (depression visit, F32/F33 진단률) 의 직접 anchor
- 한국에서는 opioid 가 미국 만큼 큰 issue 아님 (의약품 처방 strict regulation) — 본 paper 의 alcohol·suicide channel 이 더 직접적

## 본 paper § 9 인용 안
> "Charles, Hurst, and Schwartz (2019) show that manufacturing decline in the US is causally linked 
> to rising opioid mortality. We examine whether the inverse holds in Korea: does manufacturing 
> growth from trade exposure reduce alcohol-related mortality and suicide?"

## 본 paper 와의 차별화
- 한국 = manufacturing growth (US/EU 와 mirror image)
- Substance-specific: 한국은 alcohol-related (K70-K77) 와 suicide (X60-X84) 가 main channel, opioid 는 minor
- 본 paper 의 outcome heterogeneity 분석 (despair_total decomposition) 의 anchor

## Tier
- NBER Macro Annual (1+ tier) — 본 paper publication 시 cite
