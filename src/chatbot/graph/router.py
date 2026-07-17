from src.chatbot.graph.state import State
from src.chatbot.models.intent_classification import Intent
from src.chatbot.graph.nodes import NaturalChatNode, ExtractEntitiesNode
from src.chatbot.graph.workflows.natural_chat import build_natural_graph
from src.loggers import main_logger

def classification_router(raw_state):
    state = State().model_validate(raw_state)
    if state.classification_results.intent == Intent.NATURAL_CHAT:
        return build_natural_graph.__name__
    elif state.classification_results.intent == Intent.SEARCH:
        return ExtractEntitiesNode.__name__