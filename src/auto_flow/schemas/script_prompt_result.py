from pydantic import BaseModel, Field
from src.auto_flow.schemas.scene_prompt_result import ScenePromptResult

class ScriptPromptResult(BaseModel):
    script_name: str
    scene_prompt_result: list[ScenePromptResult] = Field(default_factory=list)