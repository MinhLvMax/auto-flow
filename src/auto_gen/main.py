from src.auto_gen.context_factory import ContextFactory
from pathlib import Path
from src.auto_gen.pages.google_flow_page import GoogleFlowPage
from src.config import BASE_DIR

context_factory_obj = ContextFactory()
user_profile = BASE_DIR / r'src\auto_gen\profiles\user0'
gen_context = context_factory_obj.create_context(user_profile=user_profile,
                                                 download_path=Path('../downloads'))
google_flow_page_obj = GoogleFlowPage(gen_context.new_page())
google_flow_page_obj.goto()
google_flow_project_page_obj = google_flow_page_obj.open_project_page('minhb15p17')
google_flow_project_page_obj.pause()
