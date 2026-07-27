from typing import Protocol
from src.chatbot.graph.state import State


class BaseTool(Protocol):

    def run(self, **kargs):
        ...

    def description(self):
        ...

    @property
    def name(self):
        ...
