from playwright.sync_api import sync_playwright

class Main:
    def run_context(self):
        with (sync_playwright() as p):
            print('Khoi tao context')

            context = p.chromium.launch_persistent_context(  # Khởi tạo context
                user_data_dir='taikhoantaoradelamgi98',  # Sử dụng 1 profile
                headless=False,  # ẩn trình duyệt
                channel='chrome',  # Dùng kênh chrome
                accept_downloads=True,  # Cho phép downdload
                # downloads_path=OUTPUT_DATA_DIR # Folder download mặc định
            )
            # thực hiện logic
            context.close()
