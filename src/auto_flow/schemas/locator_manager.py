import re
from playwright.sync_api import Locator, Error

class LocatorManager:
    '''Định nghĩa các nút bấm'''

    def __init__(self, page):
        self.page = page

    def get_16_9_btn(self):
        return self.page.get_by_role("tab", name="crop_16_9 16:")

    def get_thanh_phan_video_mode(self):
        return self.page.get_by_role("tab", name="chrome_extension Thành phần")

    def get_create_video_mod_btn(self):
        return self.page.get_by_role("tab", name="play_circle Video")

    def get_nanobanana2_btn(self):
        return self.page.get_by_role("button", name="🍌 Nano Banana 2")

    def get_more_drop_down_btn(self):
        return self.page.get_by_role("button").filter(
                has_text="arrow_drop_down"
            )

    def get_tab_x1(self):
        return self.page.get_by_role("tab", name="1x")

    def get_image_tab(self):
        return self.page.get_by_role("tab", name="image Hình ảnh")

    def get_setup_btn(self):
        '''
        Nút cài đặt chuyển các chế độ
        :return:
        '''
        return self.page.locator("button").filter(
            has_text=re.compile(r"(Nano Banana|Video)")
        )

    def get_close_notif_btn(self):
        return self.page.get_by_role("button", name="Đóng")

    def get_upscaled_notif(self):
        return self.page.get_by_text("check_circleĐã tăng độ phân")

    def get_update_notif(self):
        return self.page.get_by_text("check_circleQuá trình nâng cấ")

    def get_deleted_notif(self):
        return self.page.get_by_text("check_circleĐã xoá dự ánĐóng").first

    def get_latest_radio(self):
        return self.page.get_by_role("menuitem", name="radio_button_unchecked Cũ nhất")

    def get_sort_and_filter_btn(self):
        return self.page.get_by_role("button", name="filter_list Sắp xếp và lọc")

    def get_images(self):
        return self.page.get_by_role("link", name="Hình ảnh được tạo")

    def get_videos(self):
        return self.page.locator('div:has(> a > button > video)')

    def get_input_prompt_entry(self):
        return self.page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?")

    def get_create_button(self):
        return self.page.get_by_role("button", name="arrow_forward Tạo")

    def get_project_btn(self, prject_name):
        return self.page.locator(f"div:has-text('{prject_name}') > a")

    def get_create_new_project_btn(self) -> Locator:
        return self.page.locator(
            '#__next > div.sc-c7ee1759-1.jhwuTJ > div > div > button')

    def get_project_name_entry(self):
        return self.page.get_by_role("textbox", name="Văn bản có thể chỉnh sửa")

    def get_done_project_name_btn(self):
        return self.page.get_by_role("button", name="done Xong")

    def get_agent_mode_btn(self):
        return self.page.get_by_role("button", name="Tác nhân", exact=True)

    def get_create_amimation_btn(self):
        return self.page.get_by_role("menuitem", name="motion_blur Tạo ảnh động")