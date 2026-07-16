from pydantic import BaseModel

class FoundPathResult(BaseModel):
    path: str
    score: float | int