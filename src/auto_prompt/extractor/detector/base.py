from abc import ABC, abstractmethod
from pydantic import BaseModel

class SentenceBoundaryDetectorBase(ABC):

    @abstractmethod
    def detect(self, sentence: str, context) -> BaseModel:
        '''
        Dùng để nhận diện câu có phải là bắt đầu phân cảnh mới hay không
        :param sentence:
        :param context:
        :return:
        '''
        """
        Return format:
        {
            "new_unit": bool,
            "reason": str
        }
        """
        return BaseModel()