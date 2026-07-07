from playwright.sync_api import Page

class BasePage:
    def __init__(self, context):
        self.context = context
        self.page: Page = context.new_page()

    def close(self):
        self.page.close()