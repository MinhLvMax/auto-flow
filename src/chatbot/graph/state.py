from pydantic import BaseModel
from src.chatbot.models.intent_classification import IntentClassification
from src.chatbot.models.entity_extraction_result import EntityExtractionResult

class State(BaseModel):
    user_input: str = ''
    sustem_output: str = ''
    classification_results: IntentClassification = None
    entity_extraction_result: EntityExtractionResult = None
    history: list[dict] = []