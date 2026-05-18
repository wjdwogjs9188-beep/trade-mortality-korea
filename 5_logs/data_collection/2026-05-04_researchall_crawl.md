# Probe — 2026-05-04T14:13:06.572427

URL: https://code.researchall.net/search_KSIC_HS_Link

- page 1: ✅ 1,272 chars
  - parsed rows: 0
- page 2: ✅ 1,272 chars
  - parsed rows: 0
- page 3: ✅ 1,272 chars
  - parsed rows: 0

## 자동 detect 결과

- total pages: ⚠️ detect 실패 (--max-pages 로 명시 필요)
- parser column: `⚠️ 표 추출 실패`

## 다음 step

1. `0_raw/hs_ksic_concordance/researchall_html/page_0001.html` 직접 열어서 표 구조 확인
2. parser column 이 HS code / KSIC code 와 매핑되는지 확인
3. 매핑 OK 면 `python 17_researchall_hs_ksic_crawl.py --crawl --max-pages 636` 실행
4. 매핑 fail 시 page_0001.html 의 일부를 R-A 에 paste → parser 수정
