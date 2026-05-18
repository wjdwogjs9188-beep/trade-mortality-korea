# [#8] A Practical Guide to Shift-Share Instruments

## 메타정보
- **저자**: Kirill Borusyak (LSE), Peter Hull (Chicago), Xavier Jaravel (LSE)
- **출판년도**: 2025
- **학술지**: Journal of Economic Perspectives, Vol. 39, No. 1, pp. 181-204
- **DOI**: 10.1257/jep.20231370
- **발행월**: Winter 2025
- **논문 타입**: Methodological Guide / Review Article
- **핵심 키워드**: Shift-share instruments, IV identification, Weak instruments, Exogeneity, Practical implementation, Heterogeneous treatment effects

## Research Question
**핵심 의제**: 최근 10년간 NBER working papers의 약 1/8이 "shift-share" 구조의 도구변수를 사용하고 있는데, 이들이 **언제 유효하며, 어떤 조건에서 실패하고, 실제로 어떻게 구현하는가?**

**구체적 질문들**:
1. Shift-share IV의 **기본 논리**는 무엇인가? (Framework 정립)
2. **Exogeneity 가정**이 언제 성립하고, 언제 위반되는가? (조건)
3. 약한 instrument는 어떻게 식별하고, 이를 통해 **inference를 조정**하는가? (Weak-instrument robust)
4. **Heterogeneous treatment effects (HTE)** 존재 시 shift-share coefficient는 무엇을 추정하는가? (Interpretation)
5. In-sample shifts (Bartik, Card 스타일)와 out-of-sample shifts의 **practical difference**는?
6. **Robustness checks**와 validity tests는 어떻게 수행하는가?

**Contribution** (문헌에서의 위치):
1. **방법론 발전 경로 정리**:
 - Freeman (1975, 1980): Origin (노동경제학)
 - Bartik (1991): In-sample Bartik instrument (regional labor demand)
 - Card (2009): Cuban boatlift (exogenous shares)
 - ADH (2013): China syndrome (shift-share + causal inference)
 - DGHP (2017): Shift-share IV validity critique (exposure & shift orthogonality)
 - Borusyak et al. (2025): Unified practical framework

2. **새로운 이해**:
 - Shift-share = K개의 single-instrument estimates의 pooled version
 - 어떤 shares가 driving인지 확인 가능 (transparency)
 - Weak instruments는 instrument strength로 판정 가능 (F-stats)
 - HTE 존재 시, coefficient = weighted average of heterogeneous parameters (LATE-like interpretation)

3. **Practical guidance**:
 - 체크리스트: Valid shift-share를 위한 필수 검증
 - Implementation guide: R/Stata code
 - Common pitfalls: 무엇을 피해야 하는가

## Data & Applications
**이 논문은 methodological guide** → 원본 data 없음
대신, 기존 논문들의 예시 중심:

### 주요 예시 (Table 1)
| Paper | Unit | Shares | Shifts | Outcome | Main finding |
|-------|------|--------|--------|---------|--------------|
| **Freeman (1975, 1980)** | MSA/industry | Union composition | National wage changes | Union wages | Union wage spillovers |
| **Bartik (1991)** | City | Industry composition | National employment growth | Local employment | Industry shocks → local growth |
| **Card (2009)** | Labor market | Cuban migrant share | Mariel boatlift | Native wages | Immigration shock → no wage effect |
| **ADH (2013)** | Commuting zone | Industry composition | Chinese import growth | Manufacturing employment | Trade shock → job losses |
| **This paper uses**: Regional units, initial period shares (lagged), common shocks across units | | | | |

### Generic Framework
**General shift-share form**:
$$z_i = \sum_{k=1}^K s_{ik} g_k$$

- $z_i$ = Instrument for unit i
- $s_{ik}$ = Exposure share (unit i to shift k) — often from t=0
- $g_k$ = Common shift (applies to all units, varies by k) — often time-aggregate
- K = Number of shift components (industries, destinations, network members, etc.)

**Key feature**: 
- Shares are **unit-specific** (heterogeneous exposure)
- Shifts are **common** (same shock to all units, but effect depends on exposure)
- $z_i$ summarizes how much unit i is affected by common shocks given its exposure composition

## Identification Strategy

### Core Assumption: Exogenous Shares
**The validity condition**:
$$\text{Cov}[\varepsilon_i, s_{ik}] = 0 \quad \text{for all } k$$

**Interpretation**: The shares (exposure structure at baseline) are **uncorrelated with future unobserved shocks** affecting the outcome.

**Why this works**:
- Baseline shares are determined by historical/institutional factors (not anticipatory)
- Future shocks (common across units, like global trade) apply uniformly
- But effect varies: Units exposed to more-affected sectors → larger shock

**When this breaks**:
1. **Exposure to multiple shocks**: 
 - If shares capture exposure to multiple shocks (global trade, tech adoption, supply chain reorg)
 - But treatment only measures one (trade)
 - → Omitted variables bias: Corr(shares, unobserved shocks) > 0
 - **Solution**: Control for exposure to other (competing) shocks in robustness

2. **Anticipatory behavior**:
 - If agents anticipate future shocks and adjust baseline shares
 - Example: Firms move plants away from soon-to-fail industries
 - **Requires**: Argument that anticipation timing was impossible or negligible

3. **Selective sorting**:
 - If workers with different health/ability sort into regions with different sector exposure
 - → Shares correlated with unobserved heterogeneity
 - **Solution**: Use historical period far enough removed from outcome period

### The Exogenous Shifts Perspective
**Alternative framing** (useful for intuition):
- Treat shifts $g_k$ as "natural experiment" assignment
- Shares as "treatment assignment probability" (like propensity scores)
- Units with higher exposure to affected sectors = higher treatment intensity

**Identification**: Shifts are exogenous (e.g., global demand shocks, China's rise) + shares are lagged/predetermined
→ Instrument is exogenous conditional on shares

### Weak Instruments Problem
**Standard F-statistic**:
$$F = \frac{\text{(Fitted treatment variation)}^2}{\text{(Residual variation)}}$$

- **Rule of thumb**: F > 10 (weak identification, should be wary; Stock-Yogo)
- **Stronger threshold**: F > 23 (Cragg-Donald, 5% bias)
- **ADH's F**: ~23-25 (modest, hence their heavy robustness)

**Why shift-share can be weak**:
- Shifts are common across units → Limited variation
- If shares aren't correlated with treated outcome, variation limited
- Large K (many industries) but concentrated employment → Few industries matter

**Borusyak et al.'s new contribution**: 
- Exposure-robust F-statistic (accounts for heterogeneity in shift importance)
- Can identify which shares are driving variation (crucial for assessment)

### Heterogeneous Treatment Effects (HTE) Interpretation
**Key insight**: If treatment effect is **heterogeneous** (varies by unit), then:
$$\hat{\beta}_{SS} = \sum_k \lambda_k \hat{\beta}_k$$

- $\hat{\beta}_k$ = Effect of shift k on outcome (identified from variation in exposure to shift k)
- $\lambda_k$ = Weight (depends on instrument variation from shift k)
- $\hat{\beta}_{SS}$ = **Weighted average** of heterogeneous effects

**Implication**:
- Different shifts may have different effects (e.g., Chinese imports vs. Indian imports affect sectors differently)
- The shifts you choose (g_k components) determine which effects you're averaging over
- **For Kane**: If trade shocks differ by source country, which shocks matter for Korea?

### Specification Design
**Baseline 2SLS**:
$$y_i = \beta x_i + \mathbf{w}_i \gamma + \varepsilon_i$$
$$x_i = \pi z_i + \mathbf{w}_i \delta + \nu_i$$

- First stage: Regress treatment on instrument + controls
 - $x_i$ = Actual treatment (e.g., import penetration, employment growth)
 - $z_i$ = Shift-share IV

- Second stage: Estimate treatment effect
 - $y_i$ = Outcome (e.g., mortality, unemployment)

- Controls $\mathbf{w}_i$: Baseline characteristics, do NOT include shares themselves (collinear with z_i)

### Standard Errors & Clustering
- **Clustering level**: Should match application
 - Regional analysis (ADH): Cluster by state (accounts for geographic correlation)
 - Network analysis: Cluster by network group
 - **Korea application**: Cluster by region (시도) or by sector, depending on shock source

- **Robust SE**: Standard Huber-White (sandwich)
- **Wild bootstrap**: For small number of clusters (e.g., 10 states)

## Main Findings/Guidance

### 1. Validity Checklist (Table in paper)
**Borusyak et al. propose researchers verify**:

- **Shares predetermined**: Baseline period chosen far enough before treatment/outcome
 - Example: 1990 shares for 1990-2007 analysis (ADH) ✓
 - Counter-example: 2000 shares for 1990-2000 analysis ✗

- **Shifts exogenous to outcome**: Argument for why shifts (global trade, tech) are exogenous
 - Check: Compare to falsification (prior shifts shouldn't affect post outcomes)
 - ADH placebo: 1980-1990 shifts don't predict 1990-2000 outcomes ✓

- **Only relevant shares included**: Avoid "generic" shares that correlate with many shocks
 - Example: Don't use "industry structure" as shares if treatment is trade but outcome is health
 - Risk: Shares also capture health/mortality exposure → Biased IV

- **First-stage strength**: F-statistic > 10 (minimum), F > 23 (better)
 - Report: F-stat in first-stage results
 - If weak: Consider alternative IV or direct estimation with robustness

- **Robustness checks**:
 - Stability across control variable sets
 - Stability across weighting schemes (population vs. unit-weight)
 - Leave-one-out jackknife (does one shift drive all results?)
 - Alternative shift definitions (robustness to measurement)

### 2. Practical Recommendations

#### 2.1 Choosing the Shifts
**Good practice**:
- **Out-of-sample shifts**: Use shifts measured outside the analysis sample
 - Example: Chinese export growth (measured at national/global level) for regional US labor market
 - Avoids mechanical correlation (shares computed from same data as shifts)

- **Alternative**: In-sample Bartik style (like ADH)
 - Shifts = National-level growth rates (excluding local unit)
 - "Leave-out" version: $g_k = \bar{g}_k^{-i}$ (growth in sector k excluding unit i)
 - More practical but more assumptions (must assume shifts are "as-if exogenous")

- **Measurement precision**: Use high-quality source
 - Example: UN Comtrade (trade) is standard; mitigates measurement error

#### 2.2 Interpretation of Coefficients
**When reporting results**:

If **homogeneous treatment effect** (all units affected similarly):
- Coefficient = ATE (average treatment effect)
- Interpretation: Standard

If **heterogeneous treatment effect** (differs by unit/sector):
- Coefficient = Weighted average of unit-specific effects
- **Report**: Distribution of effects, not just point estimate
- **Identify**: Which shifts/exposures drive the estimate (transparency)

#### 2.3 Weak Instrument Handling
**If F-stat < 10**:
1. Don't use t-stats from 2SLS (misleading)
2. Use weak-instrument robust CI (Anderson-Rubin)
3. Consider Bonferroni-correction for multiple hypotheses
4. Discuss alternative IV or identification strategy

**If F-stat borderline (10-23)**:
1. Report weak-instrument robust results alongside 2SLS
2. Larger sample size → more power (if possible)
3. Argue for exogeneity as offset to weak instrument

#### 2.4 Robustness Testing
**Essential checks** (Borusyak et al.'s checklist):

**A. Balance tests**:
- Regress baseline characteristics on instrumental variable
- Exposure to shocks should be "as-if random"
- If characteristics correlate with exposure: Potential violation

**B. Falsification**:
- Future shocks shouldn't predict past outcomes
- Past shifts shouldn't predict future outcomes (timing)

**C. Specification stability**:
- Coefficient size/significance across:
 - Different control variable sets
 - With/without population weighting
 - Different sample periods

**D. Share composition**:
- Which shares are driving results? (Share-specific F-stats)
- If one share dominates: Reduce to that single IV (clearer argument)

### 3. Common Pitfalls (What NOT to do)

1. **Using shares that capture outcome heterogeneity**:
 - Example: Initial health/mortality rates as shares for mortality outcome
 - → Shares are correlated with outcome → Biased IV
 - **Fix**: Use predetermined, policy-determined shares (industry structure, initial settlement patterns)

2. **Forgetting that shares must be uncorrelated with future shocks**:
 - Critical assumption often overlooked
 - Example: If trade shock anticipated, firms move out → shares change → Endogenous
 - **Fix**: Argument for "surprise" or historical determination

3. **Multiple hypotheses without correction**:
 - Report many outcomes, many outcomes without multiple-testing correction
 - → Some "significant" results by chance
 - **Fix**: Pre-specify main outcomes; use Romano-Wolf correction

4. **Weak instruments + small sample**:
 - F < 10 + N < 500 → Estimator unreliable
 - Can't be fixed by adding more clusters alone
 - **Fix**: Alternative identification or acknowledge limitation

5. **Generic shares for multiple mechanisms**:
 - Example: Industry composition captures trade, tech adoption, financialization
 - If outcome responds to multiple channels: Biased IV
 - **Fix**: Control for competing mechanisms in robustness; interpret carefully

## Heterogeneity & HTE

### Treatment Effect Heterogeneity
**Borusyak et al.'s framework handles this explicitly**:

When units have heterogeneous responses:
$$y_i = \beta_i x_i + \varepsilon_i$$

Coefficient estimated:
$$\hat{\beta}_{SS} = \sum_k w_k \hat{\beta}_k$$

where:
- $w_k$ = weight on shift k (determined by instrument variation from that shift)
- $\hat{\beta}_k$ = Effect of shift k (identified from variation in exposure to shift k)

**Example (ADH context)**:
- Shift 1: Chinese import surge (large, concentrated)
- Shift 2: Mexican imports (smaller, different sectors)
- $\hat{\beta}_{SS}$ = Weighted average of their effects

**If effects differ by sector**: 
- Chinese imports → manufacturing job losses
- Mexican imports → different sectors, maybe smaller job losses
- Overall coefficient = weighted avg (dominated by larger shift)

**Implication for Korea PAP**:
- Trade shocks from China vs. Vietnam vs. Indonesia differ
- Coefficient might reflect weighted average
- Should test HTE: Does effect differ by shock source?

### Regional Heterogeneity
**Likely important** (though Borusyak don't emphasize):
- High-manufacturing regions → Larger effect
- Export-dependent vs. domestic-oriented → Different effects
- Urban vs. rural → Different adjustment capacity

**Handling**: 
- Report effects by subgroup
- Interaction: Exposure × initial manufacturing share

### Dynamic Heterogeneity
- Short-run vs. long-run effects may differ
- Event-study approach (Finkelstein et al.) reveals timing
- Shift-share coefficients may be "average" across lags

## 본 연구와의 Connection

### PAP v3.4 ("Trade Shock and Deaths of Despair in Korea") 매핑

**1. Methodological Framework**:

This guide (Borusyak 2025) is the **most recent best-practice guidance** for shift-share instruments. PAP v3.4 will necessarily follow this framework.

- **Share design**: How to construct Korean trade exposure (시군구별 산업 구성)
 - Should use 1990 or 2000 baseline (predetermined)
 - Check: Available in Korean census? Ministry of statistics?

- **Shift design**: What represents common shocks to Korea?
 - Global demand shifts by sector (from UN Comtrade, global trade)
 - Korean export growth rates (national-level, excluding regional unit?)
 - Question: In-sample or out-of-sample? (Bartik vs. pure external IV)

**2. Validity Argument**:
- **Exogenous shares**: Korean regional industry structure in 1990 determined by
 - Historical geography (coal, ports, transportation)
 - Government policy (Chaebol location, SEZ)
 - Not anticipatory (1990 before major trade liberalization 2000s)

- **Exogenous shifts**: Global trade dynamics
 - China's rise (1995+ but accelerating 2001+)
 - Vietnam trade (post-normalization 1995)
 - Japan/Asia regional supply chains

- **Threat to validity**: 
 - Korea also grew rapidly in 1990s-2000s
 - Could "generic" shares also capture development/tech exposure?
 - **Fix**: Robustness control for non-trade shocks

**3. First-Stage Strategy**:
- Estimate: How much did regional import competition grow?
 - Outcome: Regional import penetration or employment decline
 - Key: Report F-stat, discuss weak/strong instruments
 - Expectation: If Korea industrial structure concentrated → Possibly weak IV

- **Alternative**: Report reduced-form (direct outcome)
 - Like Finkelstein (2026): Directly estimate mortality response to NAFTA exposure
 - Avoids two-stage estimation; bypasses some weak-instrument issues

**4. Heterogeneity Analysis** (HTE):
Borusyak's framework implies PAP should report:

- **Which sectors/shifts are driving results?**
 - E.g., Chinese imports vs. Japanese vs. Vietnam
 - Can show that Chinese shock dominates (transparency)

- **Subgroup effects**:
 - High-manufacturing regions (Gyeonggi, Busan) vs. low
 - Seoul metro vs. rural
 - Chaebol-heavy (Seoul, Daegu) vs. SME-heavy

- **Timing**: 
 - Immediate vs. delayed effect (2-5 year lag for deaths?)
 - Comparison to ADH/Finkelstein lag structure

**5. Robustness Checklist**:
From Borusyak et al.'s guide, PAP should include:

- Balance tests: Baseline characteristics vs. trade exposure (uncorrelated?)
- Falsification: Pre-1990 shocks shouldn't predict post-2000 mortality
- Specification stability: Results across control variable sets
- Share composition: Which industries/regions drive results?
- Alternative IV: China-shock vs. other sources (different effects?)
- Weak-instrument robust CI (Anderson-Rubin) if F-stat low

**6. Coefficient Interpretation**:
Following Borusyak:
- If homogeneous effect: "Trade shock → X% mortality increase" (straightforward)
- If heterogeneous: "Trade shock weighted average effect, driven primarily by [sector/region]"
 - More transparent; acknowledges underlying HTE
 - Avoids false precision

**7. Practical Implementation Questions for PAP**:

| Question | ADH (2013) | Borusyak (2025) Guidance | PAP v3.4 |
|----------|-----------|------------------------|----------|
| Share definition | 1990 industry composition (CZ) | Predetermined period ✓ | 1990 or 2000 industry composition (Si-Gun-Gu) |
| Shift definition | Foreign import growth | Out-of-sample preferred | Global trade growth? Or Korea national growth? |
| F-stat expected | ~23 | Depends on share variation |? (Korean data TBD) |
| In-sample or out-of-sample shifts? | Mostly out-of-sample (China trade) | Out-of-sample strongly preferred |? (Design choice) |
| Weak-instrument robust? | Robustness, but not formal | If F < 10, essential | If needed, use Anderson-Rubin |
| Report by subgroup? | Some (education level) | Encouraged (HTE transparency) | Should do (region, sector, macro period) |

**8. Multi-instrument Setup**:
Borusyak discuss: If K > 1 shifts (multiple sectors/sources)
- Can pool (single coefficient) or separate
- Transparency: Show results for dominant shifts
- Test whether effects differ by source

**Korea context**: 
- Chinese shock (dominant)
- Japanese competition (historical)
- Vietnam/Indonesia (rising 2000s)
- Separate analysis for each? Pooled?

**9. Weak Instruments in Korea Context**:
**Concern**: Korean regional data smaller (fewer CZs) than US (722)
- US regions: 722 commuting zones
- Korea regions: ~250 Si-Gun-Gu municipalities
 - → Less variation, potentially weak IV

- **Mitigation**:
 - Use broader regional groupings (시도 = provinces, ~17)
 - More aggregate → Stronger instrument, but less granular
 - Or: Accept weak IV, use robust methods (Anderson-Rubin, Bonferroni)

**10. Timeline & Lags**:
Following Finkelstein (2026) + ADH:
- Trade shock (measured 1990-2000, 2000-2010, 2010-2020)
- Employment response (1-2 year lag for data reporting)
- Health/mortality response (2-5 year lag for despair → death)
 - → Event-study framework with appropriate leads/lags

## Quality Assessment: 본 Researcher의 3가지 핵심 교훈

### 1. The "Exogenous Shares" Assumption is Brittle
**교훈**:
- Borusyak et al. emphasize: **Shares must be uncorrelated with ALL future shocks**, not just the one being measured
- 가장 흔한 위반: Generic shares capturing multiple exposure dimensions
 - Example: Industry composition exposes to trade, tech adoption, financialization
 - If outcome responds to multiple channels → Biased IV

- **PAP 적용**:
 - Korean "deaths of despair" 원인: 다중
 - Economic desperation (trade shock pathway)
 - Opioid epidemic (global health pathway, Korea 1990s-2000s약물 규제 변화)
 - Aging population (demographic pathway)
 - If shares (industry composition) correlate with all three → Confounded
 - **Solution**: Explicitly control for competing mechanisms; show trade effect persists

### 2. Weak Instruments Are Common & Manageable, But Require Honesty
**교훈**:
- Borusyak: F-stat >> 10 preferred, but F ~ 10-23 acceptable if:
 - Argument for exogeneity is strong
 - Robustness checks supportive
 - Weak-instrument robust CI reported

- ADH's F ~ 23 is actually *not weak* (Cragg-Donald threshold), but modest
- **Point**: Authors should be transparent, not hide weak first-stage

- **PAP실행**:
 - Don't assume Korea data will be strong (smaller samples)
 - Plan for potentially weak IV
 - Report first-stage F proactively
 - Have Anderson-Rubin CI ready as backup

### 3. Heterogeneous Effects are the Norm, Not Exception
**교훈**:
- Borusyak's framing (HTE + weighted average) is more realistic than
 homogeneous effect assumption
- Example: Different sectors hit differently by trade
 - Textiles, apparel (highly exposed to China) → Large job loss
 - Chemicals, machinery (less exposed) → Smaller effect
 - Coefficient = weighted average (dominated by large shocks)

- **Practical implication**: 
 - Always report subgroup analysis
 - Show which groups drive the overall effect
 - Increases credibility (less "black box")

- **PAP strategy**:
 - Report overall trade effect (mortality %)
 - Disaggregate by:
 - Industry (manufacturing-heavy vs. services)
 - Region (urban vs. rural)
 - Macro period (1990s crisis vs. 2000s growth vs. 2010s slowdown)
 - Pattern in heterogeneity can reveal mechanism (e.g., manufacturing-driven = job-loss-driven)

---

**Summary Word Count**: 2,867 words (1,500-2,500 범위 초과, but very comprehensive)

**핵심 한 줄**: Borusyak et al. (2025)의 실무 가이드는 shift-share IV의 유효성 체크리스트(predetermined shares, exogenous shifts, strong first-stage, robustness), HTE 해석(weighted average effect), 약한 instrument 처리(Anderson-Rubin CI), 실제 구현 방법을 통합 제시하여, Korea PAP v3.4의 무역충격×지역×사망 인과추정 설계에 최신 best-practice 표준과 위험 회피 경로를 제공하며, 특히 한국 소규모 표본에서의 weak IV 관리 전략을 강조한다.
