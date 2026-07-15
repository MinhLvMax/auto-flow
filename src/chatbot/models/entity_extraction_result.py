from pydantic import BaseModel, Field
from src.chatbot.models.llm_response_model import LLMResponseModel

class Entity(LLMResponseModel):
    name: str = Field(
        description="Tên chuẩn hoặc tên chính của thực thể được trích xuất từ câu hỏi."
    )
    aliases: list[str] = Field(
        default_factory=list,
        description=(
            "Các tên gọi khác của thực thể, bao gồm từ đồng nghĩa, "
            "cách viết khác, tên tiếng Anh, tên quốc tế hoặc các biến thể thường gặp."
        )
    )

    # @classmethod
    # def llm_schema(cls) -> str:
    #     return """
    # {
    #   "name": "string",
    #   "aliases": [
    #     "string"
    #   ]
    # }
    # """


class EntityExtractionResult(LLMResponseModel):
    entities: list[Entity] = Field(
        default_factory=list,
        description="Danh sách tất cả các thực thể được trích xuất từ câu hỏi của người dùng."
    )

    # @classmethod
    # def llm_schema(cls) -> str:
    #     return f"""
    # {{
    #   "entities": [
    #     {Entity.llm_schema()}
    #   ]
    # }}
    # """

if __name__ == '__main__':
    from pprint import pprint
    pprint(f'{Entity.llm_schema()}')
    pprint(f'{EntityExtractionResult.llm_schema()}')
