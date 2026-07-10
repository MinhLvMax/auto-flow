from playwright.sync_api import Page
from .base_component import BaseComponent
from src.auto_gen.pages.components.image_setting_component import ImageSettingComponent
from src.auto_gen.pages.components.video_setting_component import VideoSettingComponent


class SettingComponent(BaseComponent):
    '''
    Ô wiget xuất hiện khi ấn vào setting
    '''
    def __init__(self, page: Page):
        super().__init__(page)
        # Nút tab ảnh
        self.images_tab = page.get_by_role("tab", name="image Image")
        # Nút tạo video
        self.video_tab = page.get_by_role("tab", name="play_circle Video")

    def go_to_image_mode(self):
        self.images_tab.click()
        return ImageSettingComponent(self.page)

    def go_to_video_mode(self):
        self.video_tab.click()
        return VideoSettingComponent(self.page)
