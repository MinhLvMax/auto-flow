from src.chatbot.graph.state import State
from src.chatbot.models.intent_classification import Intent
from src.chatbot.graph.nodes import NaturalChatNode, ExtractEntitiesNode, StorageAnalysisNode
from src.chatbot.graph.workflows import build_natural_graph, build_storage_analysis_graph, build_retrieval_graph
from src.loggers import main_logger

def classification_router(raw_state):
    state = State().model_validate(raw_state)
    if state.classification_results.intent == Intent.NATURAL_CHAT:
        return build_natural_graph.__name__
    elif state.classification_results.intent == Intent.SEARCH:
        return build_retrieval_graph.__name__
    elif state.classification_results.intent == Intent.STORAGE_ANALYSIS:
        return build_storage_analysis_graph.__name__