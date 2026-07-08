from pathlib import Path
from urllib.parse import quote_plus, urljoin
from datetime import datetime
import html
import re
import time
from src.auto_search.keywords import KEYWORDS
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# =========================
# CẤU HÌNH
# =========================



RESULTS_PER_KEYWORD = 5
time_str = datetime.now().strftime("%Y%m%d%H%M%S")

OUTPUT_HTML = Path(f"output/{time_str}.html")
OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)

HEADLESS = False

USER_DATA_DIR = "envato_browser_profile"

SEARCH_URL_TEMPLATE = "https://app.envato.com/search?itemType=stock-video&term={term}"


# Chỉ nhận link dạng:
# https://app.envato.com/stock-video/339e4510-12b6-45e6-970e-1369d851925c
STOCK_VIDEO_REGEX = re.compile(
    r"https?://app\.envato\.com/stock-video/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
    re.IGNORECASE
)

RELATIVE_STOCK_VIDEO_REGEX = re.compile(
    r"/stock-video/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
    re.IGNORECASE
)


# =========================
# HÀM PHỤ
# =========================

def build_search_url(keyword: str) -> str:
    term = quote_plus(keyword.strip())
    return SEARCH_URL_TEMPLATE.format(term=term)


def normalize_video_url(url: str) -> str:
    """
    Chuẩn hóa link về dạng https://app.envato.com/stock-video/uuid
    """
    if url.startswith("/stock-video/"):
        return urljoin("https://app.envato.com", url)

    # Cắt bỏ query phía sau nếu có
    return url.split("?")[0].split("#")[0]


def add_unique_video_link(links: list[str], seen: set[str], url: str) -> None:
    """
    Thêm link vào list nếu đúng dạng stock-video và chưa bị trùng.
    """
    if not url:
        return

    url = normalize_video_url(url)

    match = STOCK_VIDEO_REGEX.search(url)
    if not match:
        return

    clean_video_url = match.group(0)

    if clean_video_url not in seen:
        seen.add(clean_video_url)
        links.append(clean_video_url)


def extract_all_stock_video_links_from_dom(page, max_scan: int = 300) -> list[str]:
    """
    Lấy tất cả link stock-video từ DOM, giữ nguyên thứ tự xuất hiện.
    Không giới hạn 3 hay 5 link ở đây, vì cần nhiều candidate để lọc trùng.
    """
    links = []
    seen = set()

    anchors = page.locator('a[href*="/stock-video/"]')
    count = anchors.count()

    scan_count = min(count, max_scan)

    for i in range(scan_count):
        try:
            href = anchors.nth(i).get_attribute("href")
        except Exception:
            continue

        if not href:
            continue

        url = normalize_video_url(href)
        add_unique_video_link(links, seen, url)

    return links


def extract_all_stock_video_links_from_html(page) -> list[str]:
    """
    Quét toàn bộ HTML/JSON trong page để lấy link stock-video.
    """
    links = []
    seen = set()

    content = page.content()

    absolute_matches = STOCK_VIDEO_REGEX.findall(content)
    for url in absolute_matches:
        add_unique_video_link(links, seen, url)

    relative_matches = RELATIVE_STOCK_VIDEO_REGEX.findall(content)
    for relative_url in relative_matches:
        url = normalize_video_url(relative_url)
        add_unique_video_link(links, seen, url)

    return links


def extract_first_video_links(
    page,
    max_links: int = 5,
    excluded_links: set[str] | None = None
) -> list[str]:
    """
    Lấy link video, nhưng bỏ qua các link đã tồn tại trong excluded_links.
    Dùng để tránh trùng link giữa các keyword.
    """
    if excluded_links is None:
        excluded_links = set()

    final_links = []
    local_seen = set()

    dom_links = extract_all_stock_video_links_from_dom(page)
    html_links = extract_all_stock_video_links_from_html(page)

    candidates = dom_links + html_links

    for url in candidates:
        if url in local_seen:
            continue

        local_seen.add(url)

        # Bỏ qua link đã lấy ở keyword trước
        if url in excluded_links:
            continue

        final_links.append(url)

        if len(final_links) >= max_links:
            break

    return final_links


def wait_and_scroll_page(page):
    """
    Đợi trang load và cuộn xuống để Envato render thêm item.
    """
    time.sleep(4)

    for _ in range(4):
        page.mouse.wheel(0, 1200)
        time.sleep(1.5)

    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except PlaywrightTimeoutError:
        pass

    time.sleep(2)


def scrape_envato_links(keywords: list[str]) -> list[dict]:
    """
    Kết quả:
    [
        {
            "keyword": "...",
            "links": ["...", "...", "..."]
        }
    ]
    """
    final_results = []

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=HEADLESS,
            channel="chrome",
            viewport={"width": 1440, "height": 1000},
        )

        page = browser_context.new_page()

        for index, keyword in enumerate(keywords, start=1):
            print(f"\n[{index}/{len(keywords)}] Keyword: {keyword}")

            search_url = build_search_url(keyword)
            print(f"Search URL: {search_url}")

            links = []

            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=60000)

                wait_and_scroll_page(page)

                links = extract_first_video_links(
                    page,
                    max_links=RESULTS_PER_KEYWORD
                )

            except Exception as e:
                print(f"Lỗi khi xử lý keyword '{keyword}': {e}")

            print(f"Lấy được {len(links)} link video:")
            for link in links:
                print(" -", link)

            final_results.append({
                "keyword": keyword,
                "links": links,
            })

        browser_context.close()

    return final_results


def make_html(results: list[dict], output_path: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_parts = []

    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Envato Video Links</title>
<style>
    body {
        font-family: Arial, sans-serif;
        padding: 24px;
        background: #f5f5f5;
        color: #222;
    }

    h1 {
        margin-bottom: 8px;
    }

    .time {
        color: #666;
        margin-bottom: 24px;
    }

    .keyword-box {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 18px;
    }

    .keyword {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    ol {
        margin-top: 8px;
    }

    li {
        margin-bottom: 8px;
    }

    a {
        color: #0066cc;
        word-break: break-all;
    }

    .empty {
        color: #b00020;
        font-style: italic;
    }
</style>
</head>
<body>
""")

    html_parts.append("<h1>Envato Stock Video Links</h1>\n")
    html_parts.append(f'<div class="time">Generated at: {html.escape(now)}</div>\n')

    for item in results:
        keyword = item["keyword"]
        links = item["links"]

        html_parts.append('<div class="keyword-box">\n')
        html_parts.append(f'<div class="keyword">{html.escape(keyword)}</div>\n')

        if links:
            html_parts.append("<ol>\n")
            for link in links:
                safe_link = html.escape(link)
                html_parts.append(
                    f'<li><a href="{safe_link}" target="_blank">{safe_link}</a></li>\n'
                )
            html_parts.append("</ol>\n")
        else:
            html_parts.append('<div class="empty">Không lấy được link video nào.</div>\n')

        html_parts.append("</div>\n")

    html_parts.append("""
</body>
</html>
""")

    Path(output_path).write_text("".join(html_parts), encoding="utf-8")


# =========================
# CHẠY
# =========================

if __name__ == "__main__":
    results = scrape_envato_links(KEYWORDS)
    make_html(results, OUTPUT_HTML)

    print("\nHoàn tất.")
    print(f"File HTML đã tạo: {Path(OUTPUT_HTML).resolve()}")