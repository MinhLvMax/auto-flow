from pydantic import BaseModel, Field
from src.chatbot.models.history import History
from src.chatbot.models.tool_call import ToolCall

class State(BaseModel):
    history: History = Field(default_factory=History)
    found_paths: list[dict] = Field(default_factory=list)
    tool_call: ToolCall | None = None
    tool_result: list[dict] | None = None
