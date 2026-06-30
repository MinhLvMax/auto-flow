from pydantic import BaseModel, Field
from src.auto_flow.schemas.prompt_result import PromptResult

class ScenePromptResult(BaseModel):
    scene_name: str
    prompt_result: list[PromptResult] = Field(default_factory=list)