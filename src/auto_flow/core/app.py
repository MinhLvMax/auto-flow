import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError, Locator, Error
from playwright.sync_api._generated import Page
from src.auto_flow.config import FLOW_PROFILE, OUTPUT_DATA_DIR, CHATGPT_PROFILE
from src.auto_flow.loggers import main_logger
from src.auto_flow.utils.prompts_reader import script_prompts
from src.auto_flow.utils.playwright_helpers import debug_locator, turn_on_create_image_mode, turn_on_create_video_mode, \
    download_item
from src.auto_flow.utils.playwright_helpers import safe_click, close_notifications


class FlowManager:

    def __init__(self, page: Page, scene):
        self.page = page
        self.scene = scene
        self.project_name = scene.scene_name
        self.pair_prompts = scene.pair_prompts
        self.url = 'https://labs.google/fx/vi/tools/flow'
        self.gen_time_sleep = 20000
        self.check_time_sleep = 10000

    def find_first_image(self, number_of_images_created: int):
        while True:
            images = self.page.get_by_role("link", name="Hình ảnh được tạo")
            if images.count() == number_of_images_created:
                print('Ảnh mới nhất chưa tạo xong, vui lòng chờ.')
                self.page.wait_for_timeout(self.check_time_sleep)
            else:
                break

        first_image = images.first

        return first_image

    def find_first_video(self, number_of_videos_created: int):
        while True:
            videos = self.page.locator('div:has(> a > button > video)')
            if videos.count() == number_of_videos_created:
                print('Video mới nhất chưa tạo xong, vui lòng chờ.')
                self.page.wait_for_timeout(self.check_time_sleep)
            else:
                break
        first_video = videos.first

        return first_video

    def create_a_image(self, prompt: str):
        turn_on_create_image_mode(self.page)
        self.page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?").fill(prompt)
        self.page.get_by_role("button", name="arrow_forward Tạo").click()

    def create_a_video(self, prompt: str, first_image: Locator):
        turn_on_create_video_mode(self.page)
        first_image.hover()
        more_btn = self.page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác")
        more_btn.click()
        tao_anh_dong_btn = self.page.get_by_role("menuitem", name="motion_blur Tạo ảnh động")
        tao_anh_dong_btn.wait_for()
        tao_anh_dong_btn.click()
        self.page.keyboard.press("Escape")
        self.page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?").fill(prompt)
        self.page.get_by_role("button", name="arrow_forward Tạo").click()

    def navigate_to_project(self):
        print('Goto Google Flow Url')
        self.page.goto(self.url, wait_until='networkidle')  # Di chuyển đến URL FLOW
        self.page.keyboard.press("Escape")

        # Nếu có dự án với tên đó rồi thì vào, không thì tạo mới
        project = self.page.locator(f"div:has-text('{self.project_name}') > a")
        if project.is_visible():
            ## Vào dự án để làm việc tiếp
            print('Du an da co san, vao lam viec tiep')
            project.click()
        else:
            ## Tạo mới 1 dự án và đặt tên
            print('Tạo mới 1 dự án.')
            self.page.locator(
                '#__next > div.sc-c7ee1759-1.jhwuTJ > div > div > button').click()  # Nút tạo mới project
            print('Đặt tên dự án.')
            self.page.get_by_role("textbox", name="Văn bản có thể chỉnh sửa").fill(self.project_name)
            self.page.get_by_role("button", name="done Xong").click()

    def set_agent_mode(self):
        # Kiểm tra và tắt chế độ tác nhân nếu đang bật
        tac_nhan_btn = self.page.get_by_role("button", name="Tác nhân", exact=True)
        pressed = tac_nhan_btn.get_attribute("aria-pressed")
        if pressed == 'true':
            print('Tat che do tac nhan')
            tac_nhan_btn.click()

    def run_main_flow(self):
        # Tạo folder lưu phân cảnh nếu chưa có
        SCENE_DIR = OUTPUT_DATA_DIR / self.project_name
        SCENE_DIR.mkdir(parents=True, exist_ok=True)

        for pair in self.pair_prompts:
            self.create_a_image(pair.image)
            number_of_images_created = self.page.get_by_role("link",
                                                             name="Hình ảnh được tạo").count()
            first_image = self.find_first_image(number_of_images_created)
            download_item(self.page, first_image, SCENE_DIR)

            self.create_a_video(pair.video, first_image)
            number_of_videos_created = self.page.locator('div:has(> a > button > video)').count()
            first_video = self.find_first_video(number_of_videos_created)
            download_item(self.page, first_video, SCENE_DIR)


def orchestrator():
    with (sync_playwright() as p):
        print('Khoi tao context')

        flow_context = p.chromium.launch_persistent_context(  # Khởi tạo context
            user_data_dir=FLOW_PROFILE,  # Sử dụng 1 profile
            headless=False,  # ẩn trình duyệt
            channel='chrome',  # Dùng kênh chrome
            accept_downloads=True,  # Cho phép downdload
            # downloads_path=OUTPUT_DATA_DIR # Folder download mặc định
        )

        print('Tao page')
        page_flow = flow_context.new_page()  # Tạo 1 page

        scene = script_prompts.scenes[0]
        flowmanager = FlowManager(page_flow, scene)
        flowmanager.navigate_to_project()
        flowmanager.run_main_flow()


if __name__ == '__main__':
    orchestrator()
    pass
