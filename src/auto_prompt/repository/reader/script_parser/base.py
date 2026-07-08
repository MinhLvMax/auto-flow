from abc import ABC, abstractmethod

from src.auto_prompt.models.script_row import ScriptRow


class ScriptParser(ABC):

    @abstractmethod
    def parse(self, raw) -> list[ScriptRow]:
        """Convert any script format → sentences"""
        pass