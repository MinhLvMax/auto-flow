import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError, Locator, Error
from playwright.sync_api._generated import Page
from src.auto_flow.config import FLOW_PROFILE, OUTPUT_DATA_DIR, CHATGPT_PROFILE
from src.auto_flow.loggers import main_logger
from src.auto_flow.utils.prompts_reader import script_prompts
from src.auto_flow.utils.helpers import debug_locator
from src.auto_flow.utils.helpers import safe_click, close_notifications

GOOGLE_FLOW_URL = 'https://labs.google/fx/vi/tools/flow'
GEN_TIME_SLEEP = 20 * 1000  # ms
CHECK_TIME_SLEEP = 10 * 1000
this_scene = script_prompts.scenes[0]
PROJECT_NAME = this_scene.scene_name
pair_prompts = this_scene.pair_prompts


def sap_xep_theo_cu_nhat(page: Page):
    # Chọn xếp theo cũ nhất
    print('Sap xep theo thu tu cu nhat den moi nhat tu tren xuong')
    sap_xep_va_loc_btn = page.get_by_role("button", name="filter_list Sắp xếp và lọc")
    sap_xep_va_loc_btn.click()
    moi_nhat_radio = page.get_by_role("menuitem", name="radio_button_unchecked Cũ nhất")
    moi_nhat_radio.wait_for()
    moi_nhat_radio.click()
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)  # Chờ cho nó đóng menu


def create_images(page: Page):
    # Chuyển thành chế độ tạo ảnh
    setup_btn = page.locator("button").filter(
        has_text=re.compile(r"(Nano Banana|Video)")
    )
    if setup_btn.is_visible():
        setup_btn.click()
        btn_image_tab = page.get_by_role("tab", name="image Hình ảnh")
        btn_image_tab.wait_for()
        btn_image_tab.click()
        page.get_by_role("tab", name="1x").click()
        model_drop_down_btn = page.get_by_role("button").filter(
            has_text="arrow_drop_down"
        )
        model_drop_down_btn.click()
        page.get_by_role("button", name="🍌 Nano Banana 2")
        page.keyboard.press('Escape')

    # Tiến hành tạo ảnh
    for pair_prompt in this_scene.pair_prompts:
        page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?").fill(pair_prompt.image)
        page.get_by_role("button", name="arrow_forward Tạo").click()
        page.wait_for_timeout(GEN_TIME_SLEEP)


def create_videos(page: Page):
    # Chuyển thành chế độ tạo video
    setup_btn = page.locator("button").filter(
        has_text=re.compile(r"(Nano Banana|Video)")
    )
    if setup_btn.is_visible():
        setup_btn.click()

        create_video_mod_btn = page.get_by_role("tab", name="play_circle Video")
        create_video_mod_btn.wait_for()
        create_video_mod_btn.click()

        thanh_phan_mode_btn = page.get_by_role("tab", name="chrome_extension Thành phần")
        thanh_phan_mode_btn.click()

        chon_ty_le_btn = page.get_by_role("tab", name="crop_16_9 16:")
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

        # Duyệt và tạo video
        images = page.get_by_role("link",
                                  name="Hình ảnh được tạo")  # Hình ảnh chưa được tạo xong hết thì đã chạy tạo ảnh => sẽ bị thiếu

        # Bổ sung thêm cơ chế chờ đủ ảnh được tạo mới tạo video
        while True:
            images_count = images.count()
            if images_count == len(this_scene.pair_prompts):
                print("Đã đủ số lượng ảnh cần tạo, bắt đầu quá trình tạo video.")
                break
            page.wait_for_timeout(5000)
            print("Chưa đủ ảnh, chưa bắt đầu quá trình tạo video.")

        image_count = images.count()
        for i, pair_prompt in zip(range(image_count), this_scene.pair_prompts):
            print(f'{images.count()=}', f'{i=}')

            # Ép trang cuộn xuống dưới cùng và ngược lại để tất cả phần tử được render vào DOM
            # page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            # page.wait_for_timeout(1000)
            # page.evaluate("window.scrollTo(0, 0)")
            # page.wait_for_timeout(1000)

            item_i = images.nth(i)
            print(f'{item_i=}')
            page.keyboard.press("Escape")
            # item_i.scroll_into_view_if_needed()
            item_i.hover()
            page.wait_for_timeout(1000)  # Tạm nghỉ để nó đóng thằng hover trước đó
            more_btn = page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác")
            try:
                more_btn.click()
            except Error as e:
                for idx in range(more_btn.count()):
                    print(
                        idx,
                        more_btn.nth(idx).bounding_box()
                    )
                debug_locator(more_btn)
                print(e)
                print('Dừng và kiểm tra lỗi')
                page.pause()
                return
            tao_anh_dong_btn = page.get_by_role("menuitem", name="motion_blur Tạo ảnh động")
            tao_anh_dong_btn.wait_for()
            tao_anh_dong_btn.click()
            input_prompt = page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?")
            input_prompt.fill(pair_prompt.video)
            create_btn = page.get_by_role("button", name="arrow_forward Tạo")
            create_btn.click()
            page.wait_for_timeout(GEN_TIME_SLEEP)


def turn_on_create_image_mode(page: Page):
    # Chuyển thành chế độ tạo ảnh
    setup_btn = page.locator("button").filter(
        has_text=re.compile(r"(Nano Banana|Video)")
    )
    if setup_btn.is_visible():
        setup_btn.click()
        btn_image_tab = page.get_by_role("tab", name="image Hình ảnh")
        btn_image_tab.wait_for()
        btn_image_tab.click()
        page.get_by_role("tab", name="1x").click()
        model_drop_down_btn = page.get_by_role("button").filter(
            has_text="arrow_drop_down"
        )
        model_drop_down_btn.click()
        page.get_by_role("button", name="🍌 Nano Banana 2")
        page.keyboard.press('Escape')

def download_item(page: Page, item: Locator, path: Path):
    close_notifications(page)
    page.keyboard.press('Escape')
    item.hover()

    # Click 3 chấm
    try:
        page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác").click()
    except Error as e:
        item.hover()
        page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác").click()

    # Click tải xuống
    page.get_by_text("downloadTải xuống").click()
    # Tìm nút
    ref_1k_btn = page.get_by_role("menuitem", name="1K Kích thước gốc")  # Nút này tải ảnh
    ref_1080p_btn = page.get_by_role("menuitem", name="1080p Đã tăng độ phân giải")  # Nút này tải video
    downloadbtn = None
    if ref_1k_btn.is_visible():
        downloadbtn = ref_1k_btn.first
        print("-> Phát hiện nút 1K")
    elif ref_1080p_btn.is_visible():
        downloadbtn = ref_1080p_btn.first
        print("-> Phát hiện nút 1080p")

    # Bắt sự kiện tải và lưu file ảnh
    with page.expect_download(timeout=0) as download_info:
        downloadbtn.click()
        download = download_info.value
        filename = download.suggested_filename
        download.save_as(path / f"{filename}")


def find_first_image(page: Page, number_of_images_created: int):
    while True:
        images = page.get_by_role("link", name="Hình ảnh được tạo")
        if images.count() == number_of_images_created:
            print('Ảnh mới nhất chưa tạo xong, vui lòng chờ.')
            page.wait_for_timeout(CHECK_TIME_SLEEP)
        else:
            break

    first_image = images.first

    # first_image.hover()
    # # Click 3 chấm
    # page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác").click()
    # # Click tải xuống
    # page.get_by_text("downloadTải xuống").click()
    # # Bắt sự kiện tải và lưu file ảnh
    # with page.expect_download() as download_info:
    #     page.get_by_role("menuitem", name="1K Kích thước gốc").click()
    #     download = download_info.value
    #     filename = download.suggested_filename
    #     download.save_as(scene_path / f"{filename}")
    return first_image


def find_first_video(page: Page, number_of_videos_created: int):
    while True:
        videos = page.locator('div:has(> a > button > video)')
        if videos.count() == number_of_videos_created:
            print('Video mới nhất chưa tạo xong, vui lòng chờ.')
            page.wait_for_timeout(CHECK_TIME_SLEEP)
        else:
            break
    first_video = videos.first

    return first_video


def create_a_image(page: Page, prompt: str):
    turn_on_create_image_mode(page)
    page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?").fill(prompt)
    page.get_by_role("button", name="arrow_forward Tạo").click()


def turn_on_create_video_mode(page: Page):
    # Chuyển thành chế độ tạo video
    setup_btn = page.locator("button").filter(
        has_text=re.compile(r"(Nano Banana|Video)")
    )
    if setup_btn.is_visible():
        setup_btn.click()

        create_video_mod_btn = page.get_by_role("tab", name="play_circle Video")
        create_video_mod_btn.wait_for()
        create_video_mod_btn.click()

        thanh_phan_mode_btn = page.get_by_role("tab", name="chrome_extension Thành phần")
        thanh_phan_mode_btn.click()

        chon_ty_le_btn = page.get_by_role("tab", name="crop_16_9 16:")
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


def create_a_video(page: Page, prompt: str, first_image: Locator):
    turn_on_create_video_mode(page)
    first_image.hover()
    more_btn = page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác")
    more_btn.click()
    tao_anh_dong_btn = page.get_by_role("menuitem", name="motion_blur Tạo ảnh động")
    tao_anh_dong_btn.wait_for()
    tao_anh_dong_btn.click()
    page.keyboard.press("Escape")
    page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?").fill(prompt)
    page.get_by_role("button", name="arrow_forward Tạo").click()


def main_flow(page: Page):
    # Tạo folder lưu phân cảnh nếu chưa có
    SCENE_DIR = OUTPUT_DATA_DIR / this_scene.scene_name
    SCENE_DIR.mkdir(parents=True, exist_ok=True)

    for pair in pair_prompts:
        create_a_image(page, pair.image)
        number_of_images_created = page.get_by_role("link",
                                  name="Hình ảnh được tạo").count()
        first_image = find_first_image(page, number_of_images_created)
        download_item(page, first_image, SCENE_DIR)

        create_a_video(page, pair.video, first_image)
        number_of_videos_created = page.locator('div:has(> a > button > video)').count()
        first_video = find_first_video(page, number_of_videos_created)
        download_item(page, first_video, SCENE_DIR)

    pass


def start_init():
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
        print('Goto Google Flow Url')
        page_flow.goto(GOOGLE_FLOW_URL, wait_until='networkidle')  # Di chuyển đến URL FLOW
        page_flow.keyboard.press("Escape")

        print("Dừng để xóa dự án")
        page_flow.pause()

        # Nếu có dự án với tên đó rồi thì vào, không thì tạo mới
        project = page_flow.locator(f"div:has-text('{this_scene.scene_name}') > a")
        if project.is_visible():
            ## Vào dự án để làm việc tiếp
            print('Du an da co san, vao lam viec tiep')
            project.click()
        else:
            ## Tạo mới 1 dự án và đặt tên
            print('Tạo mới 1 dự án.')
            page_flow.locator('#__next > div.sc-c7ee1759-1.jhwuTJ > div > div > button').click()  # Nút tạo mới project
            print('Đặt tên dự án.')
            page_flow.get_by_role("textbox", name="Văn bản có thể chỉnh sửa").fill(PROJECT_NAME)
            page_flow.get_by_role("button", name="done Xong").click()

        # Kiểm tra và tắt chế độ tác nhân nếu đang bật
        tac_nhan_btn = page_flow.get_by_role("button", name="Tác nhân", exact=True)
        pressed = tac_nhan_btn.get_attribute("aria-pressed")
        if pressed == 'true':
            print('Tat che do tac nhan')
            tac_nhan_btn.click()

        main_flow(page_flow)


if __name__ == '__main__':
    start_init()
    pass
