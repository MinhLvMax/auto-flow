from enum import StrEnum
from pydantic import BaseModel, Field


class Intent(StrEnum):
    NATURAL_CHAT = "NATURAL_CHAT"
    SEARCH = "SEARCH"


class IntentClassification(BaseModel):
    intent: Intent = Field(
        description="""
Phân loại ý định của người dùng.

- NATURAL_CHAT: Người dùng chỉ muốn trò chuyện, hỏi đáp hoặc trao đổi thông thường, không cần tìm kiếm dữ liệu.
- SEARCH: Người dùng muốn tìm kiếm thông tin trong hệ thống, cây thư mục hoặc dữ liệu đã được lập chỉ mục.

Chỉ trả về đúng một trong hai giá trị: NATURAL_CHAT hoặc SEARCH.
"""
    )

    reason: str = Field(
        description="Giải thích ngắn gọn lý do chọn nhãn."
    )
