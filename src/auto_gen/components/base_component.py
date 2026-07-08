from playwright.sync_api import Page


class BaseComponent:
    def __init__(self, page: Page):
        self.page = page
