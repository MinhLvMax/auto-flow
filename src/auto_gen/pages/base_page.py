from playwright.sync_api import Page, Locator


class BasePage:
    url = None

    def __init__(self, page):
        self._page: Page = page

    def pause(self):
        self._page.pause()

    def close(self):
        self._page.close()

    def goto(self):
        '''
        Tự di chuyển đến chính nó, khi nhảy nhiều page quá thì muốn quay lại page chính nó thì gọi hàm này
        '''
        if self.url is None:
            raise NotImplementedError("Page phải khai báo url")
        self._page.goto(self.url, wait_until='load')
        self.wait_util_loaded()

    def wait_util_loaded(self):
        print("Loading page...")
        self._page.wait_for_load_state("networkidle")

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