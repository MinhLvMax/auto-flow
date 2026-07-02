from pydantic import BaseModel
from src.auto_flow.schemas.prompt_result import PromptResult

class PairPromptResult(BaseModel):
    image_prompt: PromptResult = None
    video_prompt: PromptResult = None