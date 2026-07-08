from src.config import OUTPUT_DATA_DIR
from src.auto_flow.core.app import orchestrator

# Đường dẫn tới folder prompt kịch bản
script_prompt_path = OUTPUT_DATA_DIR / '#13'
orchestrator(script_prompt_path, 0, 5)
pass
