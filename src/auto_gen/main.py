import time
from src.auto_gen.context_factory.chrome_context_factory import ChromeContextFactory
from pathlib import Path
from src.auto_gen.pages.google_flow_page import GoogleFlowPage
from src.config import BASE_DIR
from src.auto_gen.json_reader import JsonReader

context_factory_obj = ChromeContextFactory()
user_profile = BASE_DIR / r'src\auto_gen\profiles\user0'
gen_context = context_factory_obj.create_context(user_profile=user_profile,
                                                 download_path=Path('../downloads'))
# Trang chủ chứa các dự án
google_flow_page_obj = GoogleFlowPage(gen_context.new_page())
google_flow_page_obj.go_to_this_page()
google_flow_page_obj.create_with_google_flow()

# Trang của 1 dự án cụ thể
google_flow_project_page_obj = google_flow_page_obj.get_or_create_new_project('minhb15outro')

json_reader = JsonReader()
data = json_reader.read(path=Path('input.json'))

for pair in data:
    google_flow_project_page_obj.pause_page()
    google_flow_project_page_obj.turn_on_image_mode()
    time.sleep(1)
    google_flow_project_page_obj.fill_prompt(pair.get('image'))
    google_flow_project_page_obj.turn_on_video_mode()
    time.sleep(1)
    google_flow_project_page_obj.fill_prompt(pair.get('video'))
