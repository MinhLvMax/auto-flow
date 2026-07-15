from pydantic import BaseModel, Field
from src.chatbot.models.intent_classification import IntentClassification
from src.chatbot.models.entity_extraction_result import EntityExtractionResult
from src.chatbot.models.history import History

class State(BaseModel):
    classification_results: IntentClassification | None = None
    entity_extraction_result: EntityExtractionResult | None = None
    history: History = Field(default_factory=History)
    found_paths: list[str] = Field(default_factory=list)
