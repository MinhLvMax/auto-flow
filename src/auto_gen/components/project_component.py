from playwright.sync_api import Page

from .base_component import BaseComponent

class ProjectComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.get_by_role("textbox", name="Editable text")
