from pydantic import BaseModel, Field


class SentenceBoundaryLLMResult(BaseModel):
    new_unit: bool = Field(..., description="Whether this sentence starts a new scene/unit")
    reason: str | None = Field(default='', description="Short explanation for the decision")
