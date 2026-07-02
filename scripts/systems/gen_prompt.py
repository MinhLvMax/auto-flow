from src.auto_flow.config import INPUT_DATA_DIR
from src.auto_flow.services.prompt_flow import PromptFlow

# Đường dẫn đến excel kịch bản
script_path = INPUT_DATA_DIR / 'scripts' / '#13.xlsx'
# Đường dẫn style lock
style_lock_path = INPUT_DATA_DIR / 'style_lock.txt'

pflow = PromptFlow(script_path=script_path, style_lock_path=style_lock_path)
pflow.run(2, 5)