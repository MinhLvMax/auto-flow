import re
from src.auto_prompt.models.sentence_boundary_decision import SentenceBoundaryDecision
from src.auto_prompt.extractor.detector.base import SentenceBoundaryDetectorBase
from pydantic import BaseModel


class SentenceBoundaryService:

    def __init__(
            self,
            detector: SentenceBoundaryDetectorBase,
    ):
        self.detector = detector

    def analyze(
            self,
            paragraph: str,
    ) -> list[dict]:
        results = []

        previous = None
        sentences = self._split_to_list_sentence(paragraph)
        for sentence in sentences:
            decision = self.detector.detect(
                sentence=sentence,
                context=previous,
            )
            results.append(
                SentenceBoundaryDecision(
                    sentence=sentence,
                    decision=decision,
                ).model_dump()
            )
            previous = sentence

        return results

    def _split_to_list_sentence(self, paragraph: str) -> list[str]:
        if not paragraph.strip():
            return []

        sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
        return [s.strip() for s in sentences if s.strip()]
