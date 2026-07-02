from pydantic import BaseModel, Field

from schemas.pair_prompt import PairPromptResult
from src.auto_flow.schemas.prompt_result import PromptResult

class ScenePromptResult(BaseModel):
    scene_name: str
    pairs_prompts: list[PairPromptResult] = Field(default_factory=list)