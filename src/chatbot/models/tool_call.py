from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool_name: str | None = None
    arguments: dict[str, str] = Field(
        default_factory=dict,
        description="Đối tượng chứa các tham số truyền vào tool. Các khóa và giá trị phải tuân theo schema của tool tương ứng."
    )
    answer: str | None = None


if __name__ == '__main__':
    from pprint import pprint

    pprint(ToolCall)
