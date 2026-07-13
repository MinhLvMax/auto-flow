from enum import StrEnum
from pydantic import BaseModel, Field


class Intent(StrEnum):
    NATURAL_CHAT = "NATURAL_CHAT"
    SEARCH = "SEARCH"


class IntentClassification(BaseModel):
    intent: Intent = Field(
        description="""
Loại ý định của người dùng.

Chỉ được chọn một trong hai giá trị:
- NATURAL_CHAT: Trò chuyện thông thường, không cần tra cứu dữ liệu.
- SEARCH: Cần tìm kiếm thông tin trong hệ thống hoặc thư mục.
"""
    )

    reason: str = Field(
        description="Giải thích ngắn gọn lý do chọn nhãn."
    )
