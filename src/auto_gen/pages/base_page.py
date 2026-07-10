from playwright.sync_api import Page, Locator
import random


class BasePage:
    url = None

    def __init__(self, page):
        self.page: Page = page

    def pause_page(self):
        self.page.pause()

    def close_page(self):
        self.page.close()

    def go_to_this_page(self):
        '''
        Tự di chuyển đến chính nó, khi nhảy nhiều page quá thì muốn quay lại page chính nó thì gọi hàm này
        '''
        if self.url is None:
            raise NotImplementedError("Page phải khai báo url")
        self.page.goto(self.url, wait_until='load')
        self.wait_util_loaded()

    def wait_util_loaded(self):
        print("Loading page...")
        self.page.wait_for_load_state("networkidle")

    def random_time_click(
            self,
            locator: Locator,
            min_delay: float = 0.2,
            max_delay: float = 1.0,
    ):
        self.page.wait_for_timeout(
            random.uniform(min_delay, max_delay) * 1000
        )
        locator.click()

    def click_random_order(self, *locators: Locator):
        locators = list(locators)
        random.shuffle(locators)
        for locator in locators:
            locator.click()

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
