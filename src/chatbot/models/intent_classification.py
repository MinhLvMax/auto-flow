from enum import StrEnum
from pydantic import BaseModel, Field
from src.chatbot.models.llm_response_model import LLMResponseModel


class Intent(StrEnum):
    NATURAL_CHAT = "NATURAL_CHAT"
    SEARCH = "SEARCH"
    STORAGE_ANALYSIS = "STORAGE_ANALYSIS"

    @classmethod
    def intent_values(self):
        return ", ".join(intent.value for intent in Intent)


class IntentClassification(LLMResponseModel):
    intent: Intent = Field(
        description=f'''
Phân loại ý định của người dùng.

Các loại ý định:

- {Intent.NATURAL_CHAT.value}: 
  Người dùng chỉ muốn trò chuyện, hỏi đáp hoặc trao đổi thông thường,
  không cần sử dụng dữ liệu nội bộ.

- {Intent.SEARCH.value}: 
  Người dùng muốn tìm kiếm thông tin cụ thể trong hệ thống,
  cây thư mục hoặc dữ liệu đã được lập chỉ mục.

- {Intent.STORAGE_ANALYSIS.value}: 
  Người dùng muốn biết thông tin tổng quan về kho dữ liệu,
  cấu trúc thư mục, thống kê, các nhóm dữ liệu hoặc kiến thức
  được tổng hợp từ toàn bộ kho.

Chỉ trả về đúng một trong các giá trị: {Intent.intent_values()}
'''
    )

    reason: str = Field(
        description="Giải thích ngắn gọn lý do chọn nhãn."
    )

    # @classmethod
    # def llm_schema(cls) -> str:
    #     return """
    # {
    #   "intent": "NATURAL_CHAT | SEARCH",
    #   "reason": "string"
    # }
    # """
