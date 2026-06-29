from pydantic import BaseModel, Field
from src.auto_flow.schemas.prompt_result import PromptResult

class ScenePromptResult(BaseModel):
    name: str
    prompts: list[PromptResult] = Field(default_factory=list)