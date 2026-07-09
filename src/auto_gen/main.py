from src.auto_gen.context_factory.chrome_context_factory import ChromeContextFactory
from pathlib import Path
from src.auto_gen.pages.google_flow_page import GoogleFlowPage
from src.config import BASE_DIR

context_factory_obj = ChromeContextFactory()
user_profile = BASE_DIR / r'src\auto_gen\profiles\user0'
gen_context = context_factory_obj.create_context(user_profile=user_profile,
                                                 download_path=Path('../downloads'))
google_flow_page_obj = GoogleFlowPage(gen_context.new_page())
google_flow_page_obj.pause()
google_flow_page_obj.goto()
google_flow_page_obj.create_with_google_flow()
google_flow_project_page_obj = google_flow_page_obj.get_or_create_new_project('minhb15outro')
google_flow_project_page_obj.pause()
