from src.auto_flow.utils.playwright_helpers import read_json
from src.auto_flow.config import INPUT_DATA_DIR
from src.auto_flow.schemas.script import Script

prompts = read_json(INPUT_DATA_DIR / "prompts.json")
script_prompts = Script(**prompts)

# Chắc là cần phải làm thêm cái giao diện nhập kịch bản, và các prompt thì llmgen cho theo công tắc


__all__ = ['script_prompts']
