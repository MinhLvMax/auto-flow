from pydantic import BaseModel
from src.auto_flow.schemas.prompt import Prompt

class PairPrompt(BaseModel):
    image: Prompt
    video: Prompt