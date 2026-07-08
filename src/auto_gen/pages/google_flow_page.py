import re

from playwright.sync_api import Page

from src.auto_gen.pages.base_page import BasePage
from src.auto_gen.pages.google_flow_project_page import GoogleFlowProjectPage

class GoogleFlowPage(BasePage):
    url = 'https://labs.google/fx/tools/flow'

    def __init__(self, page: Page):
        super().__init__(page)
        self.goto()
        self.create_with_google_flow_btn = page.get_by_role("button", name="Create with Google Flow")
        self.create_new_project_btn = page.get_by_role("button", name="add_2 New project")

    def create_with_google_flow(self):
        self.create_with_google_flow_btn.click()

    def create_new_project(self):
        self.create_new_project_btn.click()

    def open_project_page(self, project_name):
        span = self.page.get_by_text(f"{project_name}editEdit project")
        a = span.locator("xpath=ancestor::div[2]/a")
        # self.debug_locator(a)
        # url_project = a.get_attribute("href")
        a.click()
        project_page = GoogleFlowProjectPage(self.page)
        project_page.wait_util_loaded()
        return project_page

