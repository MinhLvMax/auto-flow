from abc import ABC, abstractmethod
from pydantic import BaseModel

class LLM(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def chat(
            self,
            user_prompt: str,
            model_name: str,
            system_prompt: str,
    ) -> str:
        """Basic chat interface"""
        pass

    def chat_json(
            self,
            text: str,
            model_name: str,
            response_model: type[BaseModel],
            system_prompt: str | None = None
    ) -> BaseModel:
        pass
