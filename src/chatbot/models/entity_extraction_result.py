from pydantic import BaseModel, Field


class Entity(BaseModel):
    name: str = Field(
        description="Tên chuẩn hoặc tên chính của thực thể được trích xuất từ câu hỏi."
    )
    # aliases


class EntityExtractionResult(BaseModel):
    entities: list[Entity] = Field(
        default_factory=list,
        description="Danh sách tất cả các thực thể được trích xuất từ câu hỏi của người dùng."
    )
