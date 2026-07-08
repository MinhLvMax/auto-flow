from playwright.sync_api import Page

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
        self.page.goto(self.url)