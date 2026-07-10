import re

from src.auto_gen.constant import RatiosMode, ImageModelNameString, VideoGenerationMode, VideoModelNameString
from .base_page import BasePage
from playwright.sync_api import Page
from src.auto_gen.pages.components.setting_component import SettingComponent


class GoogleFlowProjectPage(BasePage):
    '''
    Đây là page khi mà mở vào trong một project
    '''
    url = None

    def __init__(self, page: Page):
        super().__init__(page)
        # entry tên project
        self.name_entry = page.get_by_role("textbox", name="Editable text")
        # nút hoàn tất đặt tên
        self.done_project_name_btn = page.get_by_role("button", name="done Done")
        # mục tất cả media
        self.all_media_btn = page.get_by_text("dashboardAll MediaAll Media")
        # thông báo hoạt động bất thường
        self.unusual_activity_notice = page.get_by_role("button", name="warning Failed We noticed")
        # mục chỉ ảnh
        self.images = page.get_by_text("imageView imagesImages")
        # mục chỉ video
        self.videos = page.get_by_text("videocamView videosVideos")
        # entry nhập prompt
        self.input_prompt = page.get_by_role("paragraph").filter(has_text="What do you want to create?")
        # nút chế độ tác nhân
        self.agent_btn = page.get_by_role("button", name="Tác nhân")
        # nút cài đặt
        self.setting_btn = page.locator("button").filter(
            has_text=re.compile(r"(Nano Banana|Video)")
        )
        # nút gửi prompt tạo
        self.send_btn = page.get_by_role("button", name="arrow_forward Create")

    def turn_off_agent_btn(self):
        pressed = self.agent_btn.get_attribute("aria-pressed")
        if pressed == 'true':
            print('Tắt chế độ tác nhân')
            self.agent_btn.click()

    def set_project_name(self, project_name: str):
        self.name_entry.click()
        self.name_entry.fill(project_name)
        self.done_project_name_btn.click()

    def _go_to_setting(self):
        self.setting_btn.click()
        return SettingComponent(self.page)

    def fill_prompt(self, prompt):
        self.input_prompt.fill(prompt)

    def turn_on_image_mode(self, ratio: RatiosMode = RatiosMode.R_16_9, quantity: int = 1, model_name: ImageModelNameString = ImageModelNameString.Nano_Banana_2):
        setting_component = self._go_to_setting()
        image_setting_component = setting_component.go_to_image_mode()
        image_setting_component.configure(ratio=ratio, quantity=quantity, model_name=model_name)

    def turn_on_video_mode(self, video_genaration_mode: VideoGenerationMode = VideoGenerationMode.INGREDIENTS,
                           ratio: RatiosMode = RatiosMode.R_16_9,
                           quantity = 1,
                           model_name: VideoModelNameString = VideoModelNameString.VEO_3_1_LITE_LOWER_PRIORITY,
                           duration=8):
        setting_component = self._go_to_setting()
        video_setting_component = setting_component.go_to_video_mode()
        video_setting_component.configure(video_genaration_mode, ratio, quantity, model_name, duration)
