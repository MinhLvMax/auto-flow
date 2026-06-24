from pydantic import BaseModel


class PairPrompt(BaseModel):
    image: str
    video: str


class Scene(BaseModel):
    scene_name: str
    pair_prompts: list[PairPrompt]


class Script(BaseModel):
    script_name: str
    scenes: list[Scene]