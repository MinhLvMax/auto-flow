from pydantic import BaseModel
from src.auto_prompt.models.llm_output.sentence_boundary_decision_llm_result import SentenceBoundaryLLMResult

class SentenceBoundaryDecision(BaseModel):
    sentence: str
    decision: SentenceBoundaryLLMResult