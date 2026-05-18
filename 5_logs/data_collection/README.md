# data_collection/ — Phase 1 data fetch progress log

_총 12 file. Phase 1 의 ECOS·KOSIS·researchall·WEO·centroid 수집 archive_

본 폴더는 Phase 1 의 외부 source 다운로드 progress note. ECOS API 7 version (v01-v08), KOSIS 출생·인구, researchall crawl, WEO IMF, centroid 등의 fetch progress 와 trouble-shooting log.

---

## 12 fetch log (2026-05-04 기준)

### ECOS API (7 file)

| file | 내용 |
|------|------|
| `2026-05-04_phase1_ecos.md` | ECOS API v01 1차 수집. 5 통계표 |
| `2026-05-04_phase1_ecos_v03.md` | v03 patch (lib.ecos_api 직접 사용) |
| `2026-05-04_phase1_ecos_v04.md` | v04 추가 통계표 |
| `2026-05-04_phase1_ecos_stat_search.md` | StatisticSearch endpoint probe |
| `2026-05-04_phase1_ecos_v05.md` | v05 |
| `2026-05-04_phase1_ecos_v07.md` | v07 |
| `2026-05-04_phase1_ecos_v08.md` | ⭐ v08 final — 16 통계표 fetch 완료 (132Y001/003 산업별대출, 161Y001 M1, 161Y006 M2, 102Y002 본원통화, 301Y015 지역경상수지, 403Y001/002 국가별 수출입, 722Y001 기준금리, 731Y004 환율, 901Y009 CPI + 5 연체율) |

### KOSIS (2 file)

| file | 내용 |
|------|------|
| `2026-05-04_phase1_kosis_birth.md` | KOSIS 출생성비 fetch (z_m_marital input) |

### researchall (2 file)

| file | 내용 |
|------|------|
| `2026-05-04_researchall_crawl.md` | researchall 사이트 crawl 시도 |
| `2026-05-04_researchall_api.md` | researchall API endpoint probe |

### IMF WEO (1 file)

| file | 내용 |
|------|------|
| `2026-05-04_phase0_weo.md` | WEO forecast surprise (Phase B-x Test 1b input) |

### Centroid (1 file)

| file | 내용 |
|------|------|
| `2026-05-04_phase1_centroid.md` | 시군구 centroid (Conley spatial HAC + z_m_education distance) |

---

## ⭐ 핵심 mark file

`2026-05-04_phase1_ecos_v08.md` — ECOS final 16 통계표. v01→v08 의 7 차례 시행착오 lessons (StatisticSearchList vs StatisticItemList endpoint 차이, item 정확 호출, 한도 우회, lib.ecos_api 직접 사용 등) 가 archive.

---

## reset 시 다시 발견 필요한 함정

| 시행착오 | file | 함정 |
|---------|------|------|
| ECOS endpoint 차이 | v03 → v04 | StatisticSearchList vs StatisticItemList |
| 정확 item 호출 | v06 → v08 | item code dependency |
| API 일일 한도 | (Comtrade 별도) | 4 keys rotation |
| KOSIS UI 다운 4분할 | `2026-05-04_phase1_kosis_birth.md` 관련 | API 한도 → UI 다운 + cp949→utf-8 |
| WEO vintage 식별 | `2026-05-04_phase0_weo.md` | forecast surprise 의 vintage 정합 |

reset 시 위 5건 시행착오 반복 risk.
