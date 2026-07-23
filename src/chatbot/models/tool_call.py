from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    name: str = Field(
        description="Tên của tool cần gọi. Phải khớp chính xác với một tool được cung cấp."
    )

    kargs: dict[str, str] = Field(
        description="Đối tượng chứa các tham số truyền vào tool. Các khóa và giá trị phải tuân theo schema của tool tương ứng."
    )

    

if __name__ == '__main__':
    from pprint import pprint
    pprint(ToolCall)