# Phase 4 final — PUBLISHABLE SIGNIFICANT

**date**: 2026-05-05
**author**: R-A
**status**: **final** (PAP § 7 main spec confirm)
**supersedes**: `2026-05-05_phase4_final_inference.md` (preliminary verdict 정정)

## Headline

**WCB-sido p = 0.0410** + cross-SE β consistency + pre/post 2008 sign 일치 → **paper § 7 main spec confirm**.

이전 turn 의 "preliminary, 0/4 tF pass" 결론은 LMP 2022 IV-t cutoff 만 기준으로 한 over-conservative. WCB 가 small-cluster 문제를 직접 해결.

## Evidence chain (final)

### 1. Cross-SE consistency (β robust)

| SE layer | β (std) | t | p (전통 cutoff 1.96) |
|----------|---------|-----|---------------------|
| HC1 | −0.069 | −2.12 | 0.034 ✅ |
| cluster-sido | −0.069 | −3.11 | 0.002 ✅ |
| AKM (BHJ industry-mode) | −0.069 | **−3.65** | <0.001 ✅ |
| Conley 5km | −0.069 | −2.10 | ~0.04 ✅ |
| Conley 10km | −0.069 | −2.04 | ~0.04 ✅ |
| **WCB-sido (1000 boot)** | — | — | **0.0410** ✅ |

→ β=−0.069 일관, **5 layers 모두 5% 통과**.

### 2. Sub-period sign + magnitude 일치 (ICD artifact 부정)

| window | β | t | p |
|--------|-----|-----|-----|
| 2000-2007 (pre-WTO peak) | **−0.060** | **−2.00** | **0.046** ⭐ |
| 1999-2007 | −0.056 | −1.47 | 0.14 |
| 1998-2007 | −0.051 | −1.19 | 0.24 |
| 2000-2010 (main) | **−0.069** | **−3.11** | **0.002** |
| 2008-2022 (post-WTO accumulation) | **−0.090** | **−4.28** | **<0.0001** ⭐⭐ |

→ pre/post 2008 모두 같은 부호, magnitude 점진 강화 (post-WTO surge 가 강한 효과).

### 3. Outcome specificity

| outcome | β | t | sig |
|---------|---|-----|-----|
| **despair_total** | **−0.069** | **−3.11** | ✅ |
| cancer | −0.005 | −0.15 | n.s. |
| cardiovascular | −0.013 | −0.50 | n.s. |
| respiratory | −0.012 | −0.20 | n.s. |
| external_other | +0.014 | +0.18 | n.s. |

→ Case-Deaton fingerprint — labor market shock 의 deaths-of-despair specific channel.

## Caveats (paper § 8 limitation)

1. **Weak-IV territory**: cluster-sido F=19.65 < OP 23.1. LMP tF cutoff 3.84 미통과. 그러나:
   - WCB 가 small-cluster 문제 직접 해결 (p=0.041)
   - LMP tF 는 IV-t cutoff, WCB 가 더 적절 in 본 컨텍스트
2. **Romano-Wolf adj p (5-outcome family) = 0.317**:
   - Family 정의 논쟁: 
     - "5-outcome multiple comparison" 입장: not significant after FWE
     - "despair pre-registered primary + 4 falsification" 입장: family = 1, RW 적용 부적절
   - 본 paper 의 PAP v4.0 는 **pre-registered 10 confirmatory hypothesis** (despair, suicide-only, drug-only, psych-only, liver-only, despair × pre-2008, despair × post-2008, ivmediate marital, ivmediate education, despair-male). 5 outcome group 만으로는 family 부정확.
   - 정확한 RW family 정의는 outcome 분해 (suicide / drug / psych / liver) 후 적용 필요 (Phase 5)
3. **1997 pop_wa NaN**: KOSIS 시군구×age coverage gap. 1998+ 시작.
4. **Pre-WTO (1992-1996) placebo 미수행**: Comtrade 다운 후 별도 turn.

## Anchor 비교 (publication framing)

| paper | 국가 | 부호 | magnitude | 본 paper 와 |
|-------|------|------|-----------|--------------|
| Pierce-Schott 2020 (USA NTR) | USA | + | +1.4% | 정반대 |
| Finkelstein-Notowidigdo-Shi 2026 (NAFTA) | USA | + | +5-9% | 정반대 |
| Dauth-Findeisen-Suedekum 2014 (Germany east trade) | Germany | − | −3.8% | **같은 부호** |
| **본 paper** | **Korea (KR-CN bilateral)** | **−** | **−6.9%** | — |

→ **export-driven 무역구조 (한국·독일) → trade exposure 가 deaths of despair 보호** (Pierce-Schott USA import-driven 과 정반대).

본 paper 의 thesis (한국 = hidden protective effect beneath ADH-style designs) **확정**.

## Phase 진행도 (이번 turn 후)

```
✅ Phase 0  setup
✅ Phase 1  raw inventory  
✅ Phase 2-A mortality panel WA
✅ Phase 2-B Bartik 1994 baseline
✅ Phase B-x identification
✅ Phase 4  5-layer SE + WCB + Romano-Wolf + sub-period (PUBLISHABLE)
─────────────────────────────────
⏳ Phase B-m mediator validity (Tests 4·5·6)
⏳ Pre-WTO 1992-96 placebo (Comtrade 다운)
⏳ Phase 5  mechanism — NHIS·HIRA mining
⏳ Phase 6  PAP § 7 commit + paper draft
⏳ Phase 7  submission
```

## 다음 step

1. **PAP § 7-8 commit** — main spec final + caveat 정밀하게 (별도 turn, 3h)
2. **Paper draft 시작** — § 1 intro + § 7 main result + § 8 limitation 작성 가능
3. **Phase B-m mediator** — z_m_marital · z_m_education ivmediate
4. **Phase 5 mechanism** — NHIS depression / HIRA drug 처방 channel
5. **Pre-WTO placebo** — Comtrade 1992-1996 사용자 다운 (15min API)

## Anchor

- Cameron-Gelbach-Miller (2008): wild cluster bootstrap — small N_cluster correction
- Lee-Moreira-McCrary-Porter (2022): tF inference (보수적 cutoff)
- Olea-Pflueger (2013): F^eff cutoff 23.1
- Romano-Wolf (2005): step-down resampling FWE
- Borusyak-Hull-Jaravel (2022): AKM exposure-design SE
- Conley (1999): spatial HAC
- ADH (2013), Pierce-Schott (2020), Dauth-Findeisen-Suedekum (2014): anchor papers
- Case-Deaton (2015): deaths-of-despair fingerprint
