from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqServices
from src.chatbot.intent_classification import IntentClassification

class ClassificationNode:
    def __init__(self, llm_service):
        self.llm_service = llm_service or GroqServices()

    def __call__(self, raw_state: dict):
        state = State.model_validate(raw_state)
        result = self.llm_service.chat_json(state.user_input, IntentClassification)
        return State(
            classification_results=result.model_dump()
        ).model_dump()