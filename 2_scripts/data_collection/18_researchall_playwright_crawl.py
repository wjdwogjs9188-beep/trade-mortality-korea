"""
researchall.net SPA 크롤러 — Playwright headless 브라우저 사용.
(A) API endpoint 발견 path 가 fail 시 fallback.

JS 렌더링 후 표 scrape. 한 페이지 ~3초 (JS 실행 + sleep) → 636 페이지 = 약 30-50분.

선결: pip install playwright + playwright install chromium

산출 동일:
  0_raw/hs_ksic_concordance/researchall_HS6_to_KSIC_link.csv
"""
from __future__ import annotations
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from lib.config import RAW_DIR, LOGS_DIR
except ImportError:
    PROJECT = Path(__file__).resolve().parents[2]
    RAW_DIR = PROJECT / "0_raw"
    LOGS_DIR = PROJECT / "5_logs"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "https://code.researchall.net/search_KSIC_HS_Link"

OUT_DIR = RAW_DIR / "hs_ksic_concordance"
PARSED_CSV = OUT_DIR / "researchall_HS6_to_KSIC_link.csv"
LOG = LOGS_DIR / "data_collection" / f"{datetime.now():%Y-%m-%d}_researchall_playwright.md"


def main(max_pages: int, headless: bool) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] playwright 미설치. 다음 두 명령 실행:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    log = [f"# Playwright crawl — {datetime.now().isoformat()}\n\n"]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        ctx = browser.new_context()
        page = ctx.new_page()

        page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
        time.sleep(2.0)

        # 첫 페이지 표 column 자동 식별
        # site 의 정확 selector 는 probe 후 채워야 — 우선 generic <table>/<tr>
        table_selector = "table"
        page.wait_for_selector(table_selector, timeout=10000)

        # 페이지네이션 진단
        # 본 사이트의 페이지 클릭 방식 확정 못 했음 → 우선 첫 페이지만 dump → 사용자 확인
        first_html = page.content()
        Path(OUT_DIR / "playwright_page_0001.html").write_text(first_html, encoding="utf-8")
        print(f"[ok] 첫 페이지 다운 ({len(first_html):,} chars)")
        log.append(f"- 첫 페이지: {len(first_html):,} chars\n")

        # 표 첫 추출
        first_rows = page.evaluate("""() => {
            const rows = [];
            document.querySelectorAll('table tr').forEach(tr => {
                const cells = Array.from(tr.querySelectorAll('th,td')).map(c => c.innerText.trim());
                if (cells.length) rows.push(cells);
            });
            return rows;
        }""")
        print(f"[parse] {len(first_rows)} rows on first page")
        if first_rows:
            print(f"  header: {first_rows[0]}")
            print(f"  sample: {first_rows[1] if len(first_rows) > 1 else 'n/a'}")
        log.append(f"- 첫 페이지 추출 rows: {len(first_rows)}\n")

        # ⚠️ 페이지네이션 정확 selector 미확정 — 본 spike 는 첫 페이지만 다움
        # API path 가 발견되면 17_researchall_hs_ksic_crawl.py 의 API 호출 버전 사용 권장

        log.append(f"\n## 다음 step\n\n")
        log.append(f"1. `playwright_page_0001.html` 직접 열어서 표 selector 확인\n")
        log.append(f"2. 페이지 넘기기 element (button/a/input) 의 selector 확정\n")
        log.append(f"3. 본 스크립트의 페이지네이션 부분 (`# TODO`) 채운 후 풀 크롤\n")
        log.append(f"4. *권장*: API endpoint 발견 (DevTools Network) → 17_ 스크립트의 API 버전이 10배 빠름\n")

        browser.close()

    LOG.write_text("".join(log), encoding="utf-8")
    print(f"[log] {LOG}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--headless", action="store_true", default=True)
    parser.add_argument("--no-headless", dest="headless", action="store_false")
    args = parser.parse_args()

    sys.exit(main(args.max_pages, args.headless))
