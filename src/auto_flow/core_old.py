import re
from playwright.sync_api import sync_playwright, TimeoutError, Locator
from .config import FLOW_PROFILE, OUTPUT_DATA_DIR
from .loggers import main_logger
from data.input.prompts import pair_prompts

GOOGLE_FLOW_URL = 'https://labs.google/fx/vi/tools/flow'

def click_button(button: Locator):
    '''
    Chờ nút hiển thị ra thì bấm, nếu không có thì log lỗi ra
    :param button:
    :return:
    '''
    try:
        button.wait_for(state='visible', timeout=3000)
        button.click()
    except TimeoutError:
        main_logger.debug(f'Không tìm thấy nút {button=}')

def sap_xep_theo_cu_nhat(page):
    # Chọn xếp theo cũ nhất
    sap_xep_va_loc_btn = page.get_by_role("button", name="filter_list Sắp xếp và lọc")
    click_button(sap_xep_va_loc_btn)
    page.wait_for_timeout(1000)
    moi_nhat_radio = page.get_by_role("menuitem", name="radio_button_unchecked Cũ nhất")
    click_button(moi_nhat_radio)
    page.wait_for_timeout(1000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

def chuan_bi(page):
    image_setting_button = page.get_by_role("button", name="🍌 Nano Banana 2 crop_16_9 1x")
    if not image_setting_button.is_visible():
        tac_nhan_button = page.get_by_role("button", name="Tác nhân", exact=True)
        click_button(tac_nhan_button)
    button = page.get_by_role("button", name="Video · 8s crop_16_9 1x")
    click_button(button)

    image_mode_gen_button = page.get_by_role("tab", name="image Hình ảnh")
    if image_mode_gen_button.is_visible():
        click_button(image_mode_gen_button)

def run():
    with (sync_playwright() as p):
        context = p.chromium.launch_persistent_context(
            user_data_dir=FLOW_PROFILE,
            headless=False,
            channel='chrome',
            accept_downloads=True,
            # downloads_path=OUTPUT_DATA_DIR
        )

        page = context.new_page()
        page.goto(GOOGLE_FLOW_URL, wait_until='networkidle')

        # Giả sử đã tạo xong ảnh và video
        # page.goto('https://labs.google/fx/vi/tools/flow/project/8f14e9b5-2440-43d6-8c92-5a818e050a46',
        #           wait_until="networkidle")

        # Nút bắt đầu vào, nếu có thì ấn không có thì thôi
        Create_with_Google_Flow_button = page.get_by_role("button", name="Create with Google Flow")
        if Create_with_Google_Flow_button.is_visible():
            click_button(Create_with_Google_Flow_button)

        # Tạo mới project
        create_new_prj_button = page.get_by_role("button", name="add_2 Dự án mới")
        if create_new_prj_button.is_visible():
            click_button(create_new_prj_button)

        # Đặt tên project
        project_name_entry = page.locator("#flow-desktop-header > div > nav > div > div > input")
        project_name_entry.wait_for(state="attached", timeout=10000)
        project_name_entry.scroll_into_view_if_needed()
        if project_name_entry.is_visible():
            project_name_entry.fill('MinhNewProject')
            done_prj_name_button = page.get_by_role("button", name="done Xong")
            click_button(done_prj_name_button)
        page.wait_for_timeout(5000)

        page.pause()

        sap_xep_theo_cu_nhat(page)

        chuan_bi(page)



        button = page.get_by_role("button", name="🍌 Nano Banana 2 crop_16_9 1x")
        click_button(button)

        total_button = page.get_by_role("tab", name="1x")
        if total_button.is_visible():
            click_button(total_button)

        # # for pair_prompt in pair_prompts:
        # #     # Tạo ảnh
        # #     entry_fill_prompt = page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?")
        # #     entry_fill_prompt.fill(pair_prompt.get('image'))
        # #     button_create_image = page.get_by_role("button", name="arrow_forward Tạo")
        # #     click_button(button_create_image)
        # #
        # #     # Tạo video từ ảnh
        # #     page.pause()
        # #     image_item = page.get_by_role("link", name="Hình ảnh được tạo").first
        # #     menu_button = page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác").first
        # #     click_button(menu_button)

        # Duyệt hết để tạo ảnh trước
        for pair_prompt in pair_prompts:
            entry_fill_prompt = page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?")
            entry_fill_prompt.fill(pair_prompt.get('image'))
            button_create_image = page.get_by_role("button", name="arrow_forward Tạo")
            click_button(button_create_image)
            page.wait_for_timeout(1000)

        # Tạo các vid từ ảnh
        list_image_item = page.get_by_role("link", name="Hình ảnh được tạo")
        print(f'{list_image_item.count()=}')
        count_image_item = list_image_item.count()
        main_logger.info(f'Số lượng ảnh: {count_image_item=}.')
        for i in range(count_image_item):
            item_i = list_image_item.nth(i)
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            item_i.hover()
            three_dot_button = page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác")
            time.sleep(2)
            print(f'{three_dot_button.count()=}')
            click_button(three_dot_button.first)
            tao_anh_dong_button = page.get_by_role("menuitem", name="motion_blur Tạo ảnh động")
            click_button(tao_anh_dong_button)
            time.sleep(1)
            pair_prompt = pair_prompts[i]
            entry_fill_prompt = page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?")
            entry_fill_prompt.fill(pair_prompt.get('video'))
            time.sleep(1)
            button_create = page.get_by_role("button", name="arrow_forward Tạo")
            click_button(button_create)
            time.sleep(3)

        # Tự động tải về
        list_video_and_image = page.get_by_role("button").filter(has_text=re.compile(r"^$"))
        print(f'{list_video_and_image.count()=}')

        for i in range(list_video_and_image.count()):
            item_i = list_video_and_image.nth(i)
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            item_i.hover()
            three_dot_button = page.get_by_test_id("virtuoso-item-list").get_by_role("button", name="more_vert Khác")
            click_button(three_dot_button.first)
            page.wait_for_timeout(1000)

            download_option_btn = page.get_by_text("downloadTải xuống")
            click_button(download_option_btn.first)
            page.wait_for_timeout(1000)

            ref_1k_btn = page.get_by_role("menuitem", name="1K Kích thước gốc") # Nút này tải ảnh
            ref_1080p_btn = page.get_by_role("menuitem", name="1080p Đã tăng độ phân giải") # Nút này tải video

            # 2. Tạo một biến để chứa nút sẽ click
            target_button = None
            page.wait_for_timeout(1000)
            if ref_1k_btn.is_visible():
                target_button = ref_1k_btn.first
                print("-> Phát hiện nút 1K")
            elif ref_1080p_btn.is_visible():
                target_button = ref_1080p_btn.first
                print("-> Phát hiện nút 1080p")

            # 3. Tiến hành kích hoạt download CHÍNH XÁC nút đó
            if target_button:
                with page.expect_download() as download_info:
                    click_button(target_button)

                download = download_info.value
                filename = download.suggested_filename
                download.save_as(OUTPUT_DATA_DIR / f"{filename}.mp4")

        page.pause()
        input('Enter để đóng')