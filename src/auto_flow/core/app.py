from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page
from src.auto_flow.services.file_services import FileServices
from src.auto_flow.schemas.scene_prompt_result import ScenePromptResult
from src.config import FLOW_PROFILE, OUTPUT_DATA_DIR
from src.auto_flow.managers.action_manager import ActionManager


class FlowCreateImageVideo:

    def __init__(self, page: Page, scene_prompt: ScenePromptResult):
        self.page = page
        # self.locator_manager = LocatorManager(page)
        self.action_manager = ActionManager(page)
        self.file_services = FileServices()
        self.scene = scene_prompt
        self.project_name = scene_prompt.scene_name
        self.pair_prompts = scene_prompt.pairs_prompts
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
            self.action_manager.create_a_image(pair.image_prompt.content)
            number_of_images_created = self.action_manager.get_images_count()
            first_image = self.action_manager.find_first_image(number_of_images_created)
            self.action_manager.download_item(first_image, SCENE_DIR)

            self.action_manager.create_a_video(pair.video_prompt.content, first_image)
            number_of_videos_created = self.action_manager.get_videos_count()
            first_video = self.action_manager.find_first_video(number_of_videos_created)
            self.action_manager.download_item(first_video, SCENE_DIR)


def orchestrator(script_prompt_folder_path, start_index, end_index):
    with (sync_playwright() as p):
        print('Khoi tao context')

        flow_context = p.chromium.launch_persistent_context(  # Khởi tạo context
            user_data_dir=FLOW_PROFILE,  # Sử dụng 1 profile
            headless=False,  # ẩn trình duyệt
            channel='chrome',  # Dùng kênh chrome
            accept_downloads=True,  # Cho phép downdload
            # downloads_path=OUTPUT_DATA_DIR # Folder download mặc định
        )

        file_services = FileServices()

        page_flow = flow_context.new_page()  # Tạo 1 page
        list_scene_prompts = file_services.get_scenes_prompt_list(script_prompt_folder_path)
        selected_scenes = list_scene_prompts[start_index:end_index] # Kiểm soát theo index
        for scene in selected_scenes:
            flowmanager = FlowCreateImageVideo(page_flow, scene)
            flowmanager.run_main_flow()


if __name__ == '__main__':
    script_prompt_path = OUTPUT_DATA_DIR / '#13'
    orchestrator(script_prompt_path)
    pass
