import re
from .base_page import BasePage
from playwright.sync_api import Page


class GoogleFlowProjectPage(BasePage):
    '''
    Đây là page khi mà mở vào trong một project
    '''
    url = None
    def __init__(self, page: Page):
        super().__init__(page)
        # entry tên project
        self.name = page.get_by_role("textbox", name="Editable text")
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
        self.name.click()
        self.name.fill(project_name)
        self.done_project_name_btn.click()

    

