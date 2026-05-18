# Reference Library Deep Reading - Complete Index ## 📋 Overview 이 폴더는 SSCI Paper "Trade Shock and Deaths of Despair in Korea"의 **20개 reference 논문**에 대한 체계적인 요약 및 매핑을 포함합니다. **주요 산출물**:
1. **reference_library_metadata_v01.md** - 20개 논문의 구조화된 메타정보
2. **paper_summaries/** - 각 논문의 깊이 있는 요약 (진행 중)
3. **REFERENCE_LIBRARY_DEEP_SUMMARIES_STATUS.md** - 작업 진행 상황 및 계획 --- ## 📁 파일 목록 ### 최상위 문서 (먼저 읽기) | 파일 | 용도 | 읽기 시간 |
|------|------|---------|
| `reference_library_metadata_v01.md` | 20개 논문 분류, 저자, 연도, 핵심 기여, 본 paper와의 매핑 | 10-15분 |
| `REFERENCE_LIBRARY_DEEP_SUMMARIES_STATUS.md` | 전체 작업 상황 및 다음 예정 | 5분 | ### 세부 요약 (paper_summaries/) | # | 논문 | 저자 | 상태 | 길이 |
|---|------|------|------|------|
| 1 | Pierce & Schott 2020 AERI | Pierce, Schott | ✅ 완료 | 2,300단어 |
| 2 | Finkelstein et al. 2026 | FNS | ⏳ 예정 | - |
| 3 | Borusyak et al. 2025 | BHJ | ⏳ 예정 | - |
| 4 | Adão-Kolesár-Morales 2019 | AKM | ⏳ 예정 | - |
| 5-20 | 나머지 논문들 | - | 📋 Metadata only | - | --- ## 🚀 빠른 시작 (Quick Start) ### Step 1: Orientation (5분)
`reference_library_metadata_v01.md` 열기 → **Tier별 분류 확인** 본 paper의 다음 section에서 어떤 논문이 필요한지 빠르게 파악:
- § 3 Data → Pierce-Schott, Finkelstein
- § 6 Identification Strategy → AKM, BHJ, GPS, ASS
- § 4 Mechanism → Sufi 2023, Mian-Sufi ### Step 2: Deep Dive (1시간)
`paper_02_pierce_schott_2020_aeri.md` 읽기 가장 직접적인 벤치마크 논문:
- U.S. county-level DID specification
- Trade shock → labor market → mortality pathway
- 본 paper Korea 적용 시 methodology reference ### Step 3: 다음 논문들 (다음 session)
Finkelstein 2026 (벤치마크 effect size) → BHJ 2025 (IV 방법) → AKM 2019 (SE 이론) --- ## 📊 20개 논문 분류 ### Tier 1: 벤치마크 (본 paper 직접 비교)
- Finkelstein-Notowidigdo-Shi 2026 (NAFTA→mortality)
- Pierce-Schott 2020 (PNTR→deaths of despair) ✅ 요약 완료
- Pierce-Schott 2016 (FEDS WP, extended version) ### Tier 2: 방법론 (IV/Shift-Share/SE)
- Borusyak-Hull-Jaravel 2025 (practical guide) ⏳
- Adão-Kolesár-Morales 2019 (clustered SE) ⏳
- Goldsmith-Pinkham et al. 2020 (Rotemberg weights)
- Andrews-Stock-Sun 2019 (weak IV)
- Borusyak-Hull-Jaravel 2020 (orthogonality) ### Tier 3: 응용 & 기초
- Autor-Dorn-Hanson 2013 (China Syndrome)
- Dauth-Findeisen-Suedekum 2014 (Germany trade)
- Case-Deaton 2015 (deaths of despair)
- Sufi 2023 (Korea household debt)
- Mian-Sufi-Verner (debt cycles) ### Tier 4: 메커니즘
- Autor-Dorn-Hanson 2018 (marriage value)
- Dix-Carneiro et al. 2017 (trade→crime Brazil)
- Dow et al. 2019 (policies→deaths of despair) ### Tier 5: 확장
- DFS IZA DPs 2017-2018 (Germany detailed) ### Tier 6: OCR 필요
- NBER Tech WP 151, NBER WP 5570 (스캔본) --- ## 🎯 본 Paper와의 매핑 (가장 중요) ### Pierce-Schott 2020 ↔ 본 Paper | 차원 | Pierce-Schott | 본 Paper | 매핑 |
|------|-------------|---------|------|
| Geography | 3,122 US counties | 시군구 (227) | Analogous but smaller N |
| Outcome | Drug overdoses (primary) | Suicide (primary) | Opposite cause mix |
| Shock | PNTR 2000 (discrete) | China trade (continuous) | Different timing structure |
| Mechanism | Unemployment → disability → opioid | Unemployment → debt → family → suicide | Korea-specific pathway |
| Method | State-clustered SE | 5-layer SE (AKM+Rotemberg+BHJ+Romano) | More advanced inference |
| Innovation | First trade→deaths link | Family-mediated channel + Korea focus | Novelty claim | ### 인용 방법 **Benchmark effect size**:
> "Pierce and Schott (2020) find that areas more exposed to China import competition experience 2-3 additional drug overdose deaths per 100,000 per year. In Korea's context with lower opioid prevalence, suicide is expected to be the primary response." **Methodology**:
> "Following Pierce and Schott (2020), we employ a shift-share instrumental variable approach, using county-level variation in sectoral trade exposure..." **Heterogeneity**:
> "Consistent with Pierce and Schott's finding that working-age males are most affected by trade shocks, we expect gender-differential effects in Korea's manufacturing-concentrated regions." --- ## 📖 추천 읽기 순서 ### 새 사용자 (1-2시간)
1. `reference_library_metadata_v01.md` (15분)
2. `paper_02_pierce_schott_2020_aeri.md` § 1-5 (45분)
3. `paper_02_pierce_schott_2020_aeri.md` § 10 "본 paper와의 연결" (15분) ### 깊이 있는 학습 (4-5시간)
1. Metadata (완료)
2. Pierce-Schott 전체 (1시간)
3. Finkelstein 2026 (1.5시간) ← 다음 priority
4. BHJ 2025 Practical Guide (1시간)
5. AKM 2019 (1.5시간) ### 완전한 습득 (10시간)
위의 5개 + GPS 2020 + ASS 2019 + ADH 2013 + 추가 응용 논문들 --- ## ⚙️ 기술 정보 ### 데이터 소스 | 항목 | Pierce-Schott | Finkelstein | 본 Paper |
|------|-------------|-------------|---------|
| Mortality | CDC death certificates | CDC microdata + SEER | KOSIS |
| Population | SEER | SEER | 통계청 |
| Trade data | Tariff schedule, import statistics | Similar | 관세청 |
| Employment | County Business Patterns | CBP | 광업제조업통계 | ### 코드 & 재현성 - **Pierce-Schott**: Replication package (Div. of Research & Statistics, Federal Reserve)
- **BHJ**: GitHub repository (ssaggregate R package)
- **AKM**: Code not published (implementation needed) ### 소프트웨어 추천:
- **Stata** (main): shift-share IV, clustering, event studies
- **R** (보조): BHJ::ssaggregate, sandwich (clustered SE), {did} (event study)
- **Python** (시각화): seaborn, plotnine --- ## 🔍 각 論文의 한국 적용성 ### ✅ 높은 적용성
- Pierce-Schott 2020 (일반적 methodology)
- AKM 2019 (theoretical foundation)
- BHJ 2025 (practical implementation)
- Sufi 2023 (Korea-specific household debt data) ### ⚠️ 중간 적용성
- Finkelstein 2026 (NAFTA ≠ China shock, but benchmark useful)
- ADH 2013 (baseline shift-share, but China shock structure different) ### ❌ 낮은 적용성
- Case-Deaton 2015 (US trends, Korea 자살률 훨씬 높음)
- ARLD related papers (Korea 음주사망은 다른 패턴) --- ## 📝 작성 기준 & 품질 관리 각 요약은 다음을 포함합니다:
- ✅ 메타정보 (저자, 출판, DOI)
- ✅ Research question (명확히)
- ✅ Data: sample, geographic unit, time period, size
- ✅ Identification strategy (식 포함)
- ✅ Main findings (구체적 coefficient magnitude)
- ✅ Robustness (alternative specs)
- ✅ Heterogeneity (subgroup analysis)
- ✅ Mechanism (proposed pathways)
- ✅ 본 paper와의 연결 (명시적 매핑)
- ✅ 강점/한계 (critical assessment) --- ## 📞 질문 & 피드백 ### 이 요약들이 충분한가?
- **빠른 understanding**: Metadata만으로 충분
- **논문 인용**: Pierce-Schott 요약 참고
- **방법론 구현**: BHJ + AKM 요약 필요 (현재 예정)
- **한국 맥락**: Sufi 2023 metadata + Pierce-Schott = 충분 ### 다른 논문도 깊게 읽어주나?
- **다음 session**: Finkelstein 2026 (가장 중요)
- **그 다음**: BHJ 2025 + AKM 2019 (방법론)
- **Tier 3**: 필요하면 주문 (metadata로도 충분할 가능성 높음) ### 원본 PDF 접근?
논문별 접근 정보:
- **Open access**: Pierce-Schott 2020 AERI (AER 웹사이트)
- **Restricted**: Finkelstein (BFI, possibly upon request)
- **Working papers**: NBER, IZA 웹사이트 (free) --- ## 📚 최종 추천 **지금 읽을 것 (오늘)**:
1. `reference_library_metadata_v01.md` (10분)
2. `paper_02_pierce_schott_2020_aeri.md` (1시간) **다음 주**:
3. Finkelstein 2026 요약 (본 paper 벤치마크 확인)
4. BHJ 2025 + AKM 2019 (IV 방법론 깊게 이해) **이후**:
5. 필요한 추가 논문들 JIT (just-in-time) 읽기 --- **생성**: automated tooling Agent **최종 업데이트**: 2026-05-04 **버전**: v1.0 (Pierce-Schott 완료, Finkelstein 등 예정) 