import json
from pathlib import Path
from playwright.sync_api import Locator, Page


def read_json(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def debug_locator(locator: Locator):
    print(f"\n🔍 Total: {locator.count()} elements\n")

    for i in range(locator.count()):
        el = locator.nth(i)

        print(f"\n===== [{i}] =====")

        print("TEXT:")
        print(el.text_content())

        print("\nINNER TEXT:")
        print(el.inner_text())

        print("\nTAG:")
        print(el.evaluate("e => e.tagName"))

        print("\nATTRIBUTES:")
        print("class:", el.get_attribute("class"))
        print("id:", el.get_attribute("id"))
        print("role:", el.get_attribute("role"))
        print("aria-label:", el.get_attribute("aria-label"))
        print("aria-haspopup:", el.get_attribute("aria-haspopup"))

        print("\nOUTER HTML (preview):")
        html = el.evaluate("e => e.outerHTML")
        print(html[:300])  # cắt để khỏi spam console

        print("\n--------------------")


def close_notifications(page: Page):
    notifications = [
        page.get_by_text("check_circleĐã xoá dự ánĐóng").first,
        page.get_by_text("check_circleQuá trình nâng cấ"),
        page.get_by_text("check_circleĐã tăng độ phân"),
    ]
    for notification in notifications:
        if notification.is_visible():
            page.get_by_role("button", name="Đóng").click()
            page.wait_for_timeout(2000)


def safe_click(locator: Locator, page):
    close_notifications(page)
    try:
        locator.click()
    except:
        close_notifications(page)
        locator.click()
