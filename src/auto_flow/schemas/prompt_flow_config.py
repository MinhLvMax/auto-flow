from pydantic import BaseModel
from pathlib import Path

class PromptFlowConfig:
    script_path: Path
    style_lock_path: Path
