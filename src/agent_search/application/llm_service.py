from typing import Protocol


class LLM(Protocol):
    def complete(self, messages: list[dict] | str, llm_model=None, response_model=None):
        pass
