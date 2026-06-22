from playwright.sync_api import sync_playwright, TimeoutError, Locator
from playwright.sync_api._generated import Page
from src.auto_flow.config import THIS_PROFILE, OUTPUT_DATA_DIR
from src.auto_flow.loggers import main_logger
from src.auto_flow.utils.prompts_reader import script_prompts

GOOGLE_FLOW_URL = 'https://labs.google/fx/vi/tools/flow'
PROJECT_NAME = 'testproject'
GEN_IMAGE_TIME_SLEEP = 15 * 1000 # ms
this_scene = script_prompts.scenes[0]

def create_images(page: Page):
    # Nếu chế độ tạo video đang bật thì chuyển thành chế độ tạo ảnh
    setup_video_btn = page.get_by_role("button", name="Video · 8s crop_16_9 1x")
    if setup_video_btn.is_visible():
        setup_video_btn.click()
        page.get_by_role("tab", name="image Hình ảnh").click()
        page.get_by_role("tab", name="1x")
        page.get_by_role("button", name="🍌 Nano Banana 2 arrow_drop_down").click()
        page.get_by_role("button", name="🍌 Nano Banana 2")
        page.keyboard.press('Escape')

    # 

    page.pause()

    # Nếu đang ở chế độ tạo ảnh sẵn rồi thì tiến hành tạo ảnh

    for pair_prompt in this_scene.pair_prompts:
        page.get_by_role("paragraph").filter(has_text="Bạn muốn tạo gì?").fill(pair_prompt.image)
        page.get_by_role("button", name="arrow_forward Tạo").click()
        page.wait_for_timeout(GEN_IMAGE_TIME_SLEEP)

def create_videos(page: Page):
    # Nếu chế độ tạo ảnh đang bật thì chuyển sang chế độ tạo video
    setup_image_btn = page.get_by_role("button", name="🍌 Nano Banana 2 crop_16_9 1x")
    if setup_image_btn.is_visible():
        setup_image_btn.click()

        create_video_mod_btn = page.get_by_role("tab", name="play_circle Video")
        create_video_mod_btn.wait_for()
        create_video_mod_btn.click()

        thanh_phan_mode_btn = page.get_by_role("tab", name="chrome_extension Thành phần")
        thanh_phan_mode_btn.click()

        chon_ty_le_btn = page.get_by_role("tab", name="crop_16_9 16:")
        chon_ty_le_btn.click()

        chon_so_luong = page.get_by_role("tab", name="1x")
        chon_so_luong.click()

        page.pause()

        danh_sach_mo_hinh_btn = page.locator('button[aria-haspopup="menu"]')
        danh_sach_mo_hinh_btn.click()

        chon_mo_hinh_btn = page.get_by_role("button", name="volume_up Veo 3.1 - Lite [")
        chon_mo_hinh_btn.wait_for()
        chon_mo_hinh_btn.click()

        chon_thoi_gian_btn = page.get_by_role("tab", name="8s")
        chon_thoi_gian_btn.wait_for()
        chon_thoi_gian_btn.click()

        page.keyboard.press("Escape")

    page.pause()





    pass

def main_script():
    with (sync_playwright() as p):
        context = p.chromium.launch_persistent_context( # Khởi tạo context
            user_data_dir=THIS_PROFILE, # Sử dụng 1 profile
            headless=False, # Không ẩn trình duyệt
            channel='chrome', # Dùng kênh chrome
            accept_downloads=True, # Cho phép downdload
            # downloads_path=OUTPUT_DATA_DIR # Folder download mặc định
        )
        page = context.new_page() # Tạo 1 page
        page.goto(GOOGLE_FLOW_URL, wait_until='networkidle') # Di chuyển đến URL FLOW

        # Nếu có dự án với tên đó rồi thì vào, không thì tạo mới
        project = page.locator("div:has-text('testproject') > a")
        if project.is_visible():
            ## Vào dự án để làm việc tiếp
            project.click()
        else:
            ## Tạo mới 1 dự án và đặt tên
            print('Tạo mới 1 dự án.')
            page.locator('#__next > div.sc-c7ee1759-1.jhwuTJ > div > div > button').click() # Nút tạo mới project
            print('Đặt tên dự án.')
            page.get_by_role("textbox", name="Văn bản có thể chỉnh sửa").fill(PROJECT_NAME)
            page.get_by_role("button", name="done Xong").click()



        #Kiểm tra và tắt chế độ tác nhân nếu đang bật
        tac_nhan_btn = page.get_by_role("button", name="Tác nhân", exact=True)
        pressed = tac_nhan_btn.get_attribute("aria-pressed")
        page.pause()
        if pressed == 'true':
            tac_nhan_btn.click()

        create_images(page)
        create_videos(page)

        print("Xóa dự án.")
        page.pause()
        page.locator(r'xpath=/html/body/div[1]/div[1]/div[2]/div[1]/nav/div/button[2]').click()
        delete_btn = page.locator(r'xpath=/html/body/div[3]/div/button[3]')
        delete_btn.wait_for()
        delete_btn.click()
        confirm_btn = page.locator(r'/html/body/div[1]/div[2]/div[2]/div/button[2]')
        confirm_btn.wait_for()
        confirm_btn.click()
        page.pause()


if __name__ == '__main__':
    main_script()
    pass