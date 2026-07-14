from src.chatbot.graph.state import State
from src.chatbot.models.intent_classification import Intent
from src.chatbot.graph.nodes import NaturalChatNode, SearchNode

def classification_router(raw_state):
    state = State().model_validate(raw_state)
    if state.classification_results.intent == Intent.NATURAL_CHAT:
        return NaturalChatNode.__name__
    elif state.classification_results.intent == Intent.SEARCH:
        return SearchNode.__name__