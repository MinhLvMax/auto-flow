from playwright.sync_api import Page, Locator


class BasePage:
    url = None

    def __init__(self, page):
        self.page: Page = page

    def pause(self):
        self.page.pause()

    def close(self):
        self.page.close()

    def goto(self):
        if self.url is None:
            raise NotImplementedError("Page phải khai báo url")
        self.page.goto(self.url, wait_until='load')
        self.wait_util_loaded()

    def wait_util_loaded(self):
        print("Loading page...")
        self.page.wait_for_load_state("networkidle")

    def debug_locator(self, locator: Locator):
        count = locator.count()

        print("=" * 80)
        print(f"Count: {count}")

        for i in range(count):
            item = locator.nth(i)

            print(f"\n[{i}]")
            print("tag:", item.evaluate("e => e.tagName"))
            print("text:", repr(item.text_content()))
            print("html:", item.evaluate("e => e.outerHTML"))