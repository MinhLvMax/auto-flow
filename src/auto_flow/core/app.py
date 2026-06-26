import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError, Locator, Error
from playwright.sync_api._generated import Page
from schemas import action_manager
from src.auto_flow.config import FLOW_PROFILE, OUTPUT_DATA_DIR, CHATGPT_PROFILE
from src.auto_flow.loggers import main_logger
from src.auto_flow.utils.prompts_reader import script_prompts
from src.auto_flow.utils.playwright_helpers import debug_locator
from src.auto_flow.schemas.action_manager import ActionManager


class FlowManager:

    def __init__(self, page: Page, scene):
        self.page = page
        # self.locator_manager = LocatorManager(page)
        self.action_manager = ActionManager(page)
        self.scene = scene
        self.project_name = scene.scene_name
        self.pair_prompts = scene.pair_prompts
        self.url = 'https://labs.google/fx/vi/tools/flow'
        self.gen_time_sleep = 20000
        self.check_time_sleep = 10000

    def run_main_flow(self):
        self.page.goto(self.url, wait_until='networkidle')  # Di chuyển đến URL FLOW

        self.action_manager.navigate_to_project(self.scene.scene_name)

        # Tạo folder lưu phân cảnh nếu chưa có
        SCENE_DIR = OUTPUT_DATA_DIR / self.project_name
        SCENE_DIR.mkdir(parents=True, exist_ok=True)

        for pair in self.pair_prompts:
            self.action_manager.create_a_image(pair.image)
            number_of_images_created = self.action_manager.get_images_count()
            first_image = self.action_manager.find_first_image(number_of_images_created)
            self.action_manager.download_item(first_image, SCENE_DIR)

            self.action_manager.create_a_video(pair.video, first_image)
            number_of_videos_created = self.action_manager.get_videos_count()
            first_video = self.action_manager.find_first_video(number_of_videos_created)
            self.action_manager.download_item(first_video, SCENE_DIR)


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

        page_flow = flow_context.new_page()  # Tạo 1 page
        for scene in script_prompts.scenes:
            flowmanager = FlowManager(page_flow, scene)
            flowmanager.run_main_flow()


if __name__ == '__main__':
    orchestrator()
    pass
