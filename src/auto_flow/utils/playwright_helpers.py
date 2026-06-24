import json
import re
from pathlib import Path
from playwright.sync_api import Locator, Page, Error


def read_json(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


#
# def create_images(page: Page):
#     # Chuyển thành chế độ tạo ảnh
#     setup_btn = page.locator("button").filter(
#         has_text=re.compile(r"(Nano Banana|Video)")
#     )
#     if setup_btn.is_visible():
#         setup_btn.click()
#         btn_image_tab = page.get_by_role("tab", name="image Hình ảnh")
#         btn_image_tab.wait_for()
#         btn_image_tab.click()
#         page.get_by_role("tab", name="1x").click()
#         model_drop_down_btn = page.get_by_role("button").filter(
#             has_text="arrow_drop_down"
#         )
#         model_drop_down_btn.click()
#         page.get_by_role("button", name="🍌 Nano Banana 2")
#         page.keyboard.press('Escape')
#
#     # Tiến hành tạo ảnh
#     for pair_prompt in this_scene.pair_prompts:
#         page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?").fill(pair_prompt.image)
#         page.get_by_role("button", name="arrow_forward Tạo").click()
#         page.wait_for_timeout(GEN_TIME_SLEEP)
#
#
# def create_videos(page: Page):
#     # Chuyển thành chế độ tạo video
#     setup_btn = page.locator("button").filter(
#         has_text=re.compile(r"(Nano Banana|Video)")
#     )
#     if setup_btn.is_visible():
#         setup_btn.click()
#
#         create_video_mod_btn = page.get_by_role("tab", name="play_circle Video")
#         create_video_mod_btn.wait_for()
#         create_video_mod_btn.click()
#
#         thanh_phan_mode_btn = page.get_by_role("tab", name="chrome_extension Thành phần")
#         thanh_phan_mode_btn.click()
#
#         chon_ty_le_btn = page.get_by_role("tab", name="crop_16_9 16:")
#         chon_ty_le_btn.click()
#
#         chon_so_luong = page.get_by_role("tab", name="1x")
#         chon_so_luong.click()
#
#         model_drop_down_btn = page.get_by_role("button").filter(
#             has_text="arrow_drop_down"
#         )
#         model_drop_down_btn.click()
#
#         chon_mo_hinh_btn = page.get_by_role("button", name="volume_up Veo 3.1 - Lite [")
#         chon_mo_hinh_btn.wait_for()
#         chon_mo_hinh_btn.click()
#
#         chon_thoi_gian_btn = page.get_by_role("tab", name="8s")
#         chon_thoi_gian_btn.wait_for()
#         chon_thoi_gian_btn.click()
#
#         page.keyboard.press("Escape")
#
#         # Duyệt và tạo video
#         images = page.get_by_role("link",
#                                   name="Hình ảnh được tạo")  # Hình ảnh chưa được tạo xong hết thì đã chạy tạo ảnh => sẽ bị thiếu
#
#         # Bổ sung thêm cơ chế chờ đủ ảnh được tạo mới tạo video
#         while True:
#             images_count = images.count()
#             if images_count == len(this_scene.pair_prompts):
#                 print("Đã đủ số lượng ảnh cần tạo, bắt đầu quá trình tạo video.")
#                 break
#             page.wait_for_timeout(5000)
#             print("Chưa đủ ảnh, chưa bắt đầu quá trình tạo video.")
#
#         image_count = images.count()
#         for i, pair_prompt in zip(range(image_count), this_scene.pair_prompts):
#             print(f'{images.count()=}', f'{i=}')
#
#             # Ép trang cuộn xuống dưới cùng và ngược lại để tất cả phần tử được render vào DOM
#             # page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             # page.wait_for_timeout(1000)
#             # page.evaluate("window.scrollTo(0, 0)")
#             # page.wait_for_timeout(1000)
#
#             item_i = images.nth(i)
#             print(f'{item_i=}')
#             page.keyboard.press("Escape")
#             # item_i.scroll_into_view_if_needed()
#             item_i.hover()
#             page.wait_for_timeout(1000)  # Tạm nghỉ để nó đóng thằng hover trước đó
#             more_btn = page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác")
#             try:
#                 more_btn.click()
#             except Error as e:
#                 for idx in range(more_btn.count()):
#                     print(
#                         idx,
#                         more_btn.nth(idx).bounding_box()
#                     )
#                 debug_locator(more_btn)
#                 print(e)
#                 print('Dừng và kiểm tra lỗi')
#                 page.pause()
#                 return
#             tao_anh_dong_btn = page.get_by_role("menuitem", name="motion_blur Tạo ảnh động")
#             tao_anh_dong_btn.wait_for()
#             tao_anh_dong_btn.click()
#             input_prompt = page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?")
#             input_prompt.fill(pair_prompt.video)
#             create_btn = page.get_by_role("button", name="arrow_forward Tạo")
#             create_btn.click()
#             page.wait_for_timeout(GEN_TIME_SLEEP)

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


def debug_locator(locator: Locator):
    print(f"\n🔍 Total: {locator.count()} elements\n")

    for i in range(locator.count()):
        el = locator.nth(i)

        print(f"\n===== [{i}] =====")

        print("TEXT:")
        print(el.text_content())

        print("\nINNER TEXT:")
        print(el.inner_text())

        print("\nTAG:")
        print(el.evaluate("e => e.tagName"))

        print("\nATTRIBUTES:")
        print("class:", el.get_attribute("class"))
        print("id:", el.get_attribute("id"))
        print("role:", el.get_attribute("role"))
        print("aria-label:", el.get_attribute("aria-label"))
        print("aria-haspopup:", el.get_attribute("aria-haspopup"))

        print("\nOUTER HTML (preview):")
        html = el.evaluate("e => e.outerHTML")
        print(html[:300])  # cắt để khỏi spam console

        print("\n--------------------")


def close_notifications(page: Page):
    notifications = [
        page.get_by_text("check_circleĐã xoá dự ánĐóng").first,
        page.get_by_text("check_circleQuá trình nâng cấ"),
        page.get_by_text("check_circleĐã tăng độ phân"),
    ]
    for notification in notifications:
        if notification.is_visible():
            page.get_by_role("button", name="Đóng").click()
            page.wait_for_timeout(2000)


def safe_click(locator: Locator, page):
    close_notifications(page)
    try:
        locator.click()
    except:
        close_notifications(page)
        locator.click()


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
