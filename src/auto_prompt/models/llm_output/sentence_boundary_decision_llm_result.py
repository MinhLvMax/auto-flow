from pydantic import BaseModel, Field


class SentenceBoundaryLLMResult(BaseModel):
    new_unit: bool = Field(..., description="Whether this sentence starts a new scene/unit")
    reason: str = Field(..., description="Short explanation for the decision")
