from src.auto_gen.context_factory import ContextFactory
from pathlib import Path
from src.auto_gen.pages.google_flow_page import GoogleFlowPage

context_factory_obj = ContextFactory()
gen_context = context_factory_obj.create_context(user_profile=Path('../profiles/user0'),
                                                 download_path=Path('../downloads'))
google_flow_page_obj = GoogleFlowPage(gen_context.new_page())
google_flow_page_obj.pause()
