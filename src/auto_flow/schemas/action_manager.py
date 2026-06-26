import random
import re
from cmath import nan
from pathlib import Path
from playwright.sync_api import Page
from src.auto_flow.schemas.locator_manager import LocatorManager, Locator

class ActionManager:
    '''Định nghĩa các loạt thao tác hành động thực hiện các nút trên giao diện'''

    def __init__(self, page):
        self.page = page
        self.locator_manager = LocatorManager(page)

    def get_videos_count(self):
        return self.locator_manager.get_videos().count()

    def get_images_count(self):
        return self.locator_manager.get_images().count()

    def find_first_image(self, number_of_images_created: int, time_sleep: int = 5000):
        while True:
            images = self.locator_manager.get_images()
            if images.count() == number_of_images_created:
                print('Ảnh mới nhất chưa tạo xong, vui lòng chờ.')
                self.page.wait_for_timeout(time_sleep)
            else:
                break

        first_image = images.first

        return first_image

    def find_first_video(self, number_of_videos_created: int, time_sleep: int = 5000):
        while True:
            videos = self.locator_manager.get_videos()
            if videos.count() == number_of_videos_created:
                print('Video mới nhất chưa tạo xong, vui lòng chờ.')
                self.page.wait_for_timeout(time_sleep)
            else:
                break
        first_video = videos.first
        return first_video

    def click_send_btn(self):
        send_btn = self.locator_manager.get_send_button()
        self.page.wait_for_timeout(random.randint(500, 2000))
        self.safe_click(send_btn)

    def create_a_image(self, prompt: str):
        self.turn_on_create_image_mode()
        self.locator_manager.get_input_prompt_entry().fill(prompt)
        self.click_send_btn()

    def create_a_video(self, prompt: str, first_image: Locator):
        self.turn_on_create_video_mode(self.page)
        self.click_more_btn(first_image)
        tao_anh_dong_btn = self.locator_manager.get_create_amimation_btn()
        self.safe_click(tao_anh_dong_btn)
        self.page.keyboard.press("Escape")

        input_entry = self.locator_manager.get_input_prompt_entry()
        input_entry.fill(prompt)

        self.click_send_btn()

    def navigate_to_project(self, project_name):
        self.page.keyboard.press("Escape")

        # Nếu có dự án với tên đó rồi thì vào, không thì tạo mới
        project = self.locator_manager.get_project_btn(project_name)
        if project.is_visible():
            ## Vào dự án để làm việc tiếp
            print('Du an da co san, vao lam viec tiep')
            project.click()
        else:
            ## Tạo mới 1 dự án và đặt tên
            print('Tạo mới 1 dự án.')
            create_new_prj_btn = self.locator_manager.get_create_new_project_btn()
            create_new_prj_btn.click()
            # Nút tạo mới project
            print('Đặt tên dự án.')
            self.locator_manager.get_project_name_entry().fill(project_name)
            self.locator_manager.get_done_project_name_btn().click()

    def set_agent_mode(self):
        # Kiểm tra và tắt chế độ tác nhân nếu đang bật
        tac_nhan_btn = self.locator_manager.get_agent_mode_btn()
        pressed = tac_nhan_btn.get_attribute("aria-pressed")
        if pressed == 'true':
            print('Tat che do tac nhan')
            tac_nhan_btn.click()

    def sap_xep_theo_cu_nhat(self):
        # Chọn xếp theo cũ nhất
        print('Sap xep theo thu tu cu nhat den moi nhat tu tren xuong')
        sap_xep_va_loc_btn = self.locator_manager.get_sort_and_filter_btn()
        sap_xep_va_loc_btn.click()
        moi_nhat_radio = self.locator_manager.get_latest_radio()
        moi_nhat_radio.wait_for()
        moi_nhat_radio.click()
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(1000)  # Chờ cho nó đóng menu

    def close_notifications(self):
        notifications = [
            self.locator_manager.get_deleted_notif(),
            self.locator_manager.get_update_notif(),
            self.locator_manager.get_upscaled_notif(),
        ]
        for notification in notifications:
            if notification.is_visible():
                self.locator_manager.get_close_notif_btn().click()
                self.page.wait_for_timeout(2000)

    def safe_click(self, locator: Locator):
        self.close_notifications()
        try:
            locator.click()
        except:
            self.close_notifications()
            locator.click()

    def turn_on_create_image_mode(self):
        # Chuyển thành chế độ tạo ảnh
        setup_btn = self.locator_manager.get_setup_btn()
        if setup_btn.is_visible():
            setup_btn.click()
            btn_image_tab = self.locator_manager.get_image_tab()
            btn_image_tab.wait_for()
            btn_image_tab.click()
            tab_x1 = self.locator_manager.get_tab_x1()
            tab_x1.click()
            model_drop_down_btn = self.locator_manager.get_more_drop_down_btn()
            model_drop_down_btn.click()
            nano_banana2_btn = self.locator_manager.get_nanobanana2_btn()
            self.page.keyboard.press('Escape')

    def turn_on_create_video_mode(self, page: Page):
        # Chuyển thành chế độ tạo video
        setup_btn = self.locator_manager.get_setup_btn()
        if setup_btn.is_visible():
            setup_btn.click()

            create_video_mod_btn = self.locator_manager.get_create_video_mod_btn()
            create_video_mod_btn.wait_for()
            create_video_mod_btn.click()

            thanh_phan_mode_btn = self.locator_manager.get_thanh_phan_video_mode()
            thanh_phan_mode_btn.click()

            chon_ty_le_btn = self.locator_manager.get_16_9_btn()
            chon_ty_le_btn.click()

            chon_so_luong = page.get_by_role("tab", name="1x")
            chon_so_luong.click()

            model_drop_down_btn = page.get_by_role("button").filter(
                has_text="arrow_drop_down"
            )
            model_drop_down_btn.click()

            chon_mo_hinh_btn = page.get_by_role("button", name="volume_up Veo 3.1 - Lite [")
            chon_mo_hinh_btn.wait_for()
            chon_mo_hinh_btn.click()

            chon_thoi_gian_btn = page.get_by_role("tab", name="8s")
            chon_thoi_gian_btn.wait_for()
            chon_thoi_gian_btn.click()

            page.keyboard.press("Escape")

    def click_more_btn(self, item: Locator):
        item.click(button='right')
        # self.page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác").first.click()

    def click_download_btn(self, item: Locator):
        self.click_more_btn(item)
        self.locator_manager.get_download_btn().click()

    def download_item(self, item: Locator, path: Path):
        self.close_notifications()
        self.page.keyboard.press('Escape')

        # Tải xuống
        self.click_download_btn(item)
        # Tìm nút
        ref_1k_btn = self.page.get_by_role("menuitem", name="1K Kích thước gốc")  # Nút này tải ảnh
        ref_1080p_btn = self.page.get_by_role("menuitem", name="1080p Đã tăng độ phân giải")  # Nút này tải video
        downloadtylebtn = None
        if ref_1k_btn.is_visible():
            downloadtylebtn = ref_1k_btn.first
            print("-> Phát hiện nút 1K")
        elif ref_1080p_btn.is_visible():
            downloadtylebtn = ref_1080p_btn.first
            print("-> Phát hiện nút 1080p")


        # Bắt sự kiện tải và lưu file ảnh
        with self.page.expect_download(timeout=0) as download_info:
            downloadtylebtn.click()
            # Cần làm hàm kiểm tra xem có đang tải không, nếu không thì ấn tải lại sau 10 giây
            download = download_info.value
            filename = download.suggested_filename
            download.save_as(path / f"{filename}")