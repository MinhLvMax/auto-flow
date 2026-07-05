from abc import ABC, abstractmethod
from pydantic import BaseModel

class SentenceBoundaryDetectorBase(ABC):

    @abstractmethod
    def detect(self, sentence: str, context) -> BaseModel:
        """
        Return format:
        {
            "new_unit": bool,
            "reason": str
        }
        """
        pass