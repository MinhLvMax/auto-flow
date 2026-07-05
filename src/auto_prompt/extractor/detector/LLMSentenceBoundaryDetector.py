from pydantic import BaseModel
from src.auto_prompt.extractor.detector.base import SentenceBoundaryDetectorBase
from src.auto_prompt.llm.base import LLM
from src.auto_prompt.models.llm_output.sentence_boundary_decision_llm_result import SentenceBoundaryLLMResult
from src.auto_prompt.constant.prompt_format import SENTENCE_BOUNDARY_PROMPT


class LLMSentenceBoundaryDetector(SentenceBoundaryDetectorBase):

    def __init__(
            self,
            llm: LLM,
            model_name: str,
    ):
        self.llm = llm
        self.model_name = model_name

    def detect(
            self,
            sentence: str,
            context: str | None = None
    ) -> BaseModel:

        prompt = SENTENCE_BOUNDARY_PROMPT.format(
            sentence=sentence,
            context=context or "None",
        )

        return self.llm.chat_json(
            text=prompt,
            model_name=self.model_name,
            response_model=SentenceBoundaryLLMResult,
        )

