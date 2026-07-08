from .base_page import BasePage
from playwright.sync_api import Page


class GoogleFlowProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.get_by_role("textbox", name="Editable text")
        self.all_media_btn = page.get_by_text("dashboardAll MediaAll Media")
        self.unusual_activity_notice = page.get_by_role("button", name="warning Failed We noticed")
        self.images = page.get_by_text("imageView imagesImages")
        self.videos = page.get_by_text("videocamView videosVideos")

        self.input_prompt = page.get_by_role("paragraph").filter(has_text="What do you want to create?")
        self.agent_btn = page.get_by_role("button", name="Tác nhân")

    def turn_off_agent_btn(self):
        pressed = self.agent_btn.get_attribute("aria-pressed")
        if pressed == 'true':
            print('Tắt chế độ tác nhân')
            self.agent_btn.click()

    

