from src.chatbot.graph.state import State
from langgraph.graph import END
from src.chatbot.models.intent_classification import Intent
from src.chatbot.graph.nodes.tool_executor import ToolExecutorNode

from src.loggers import main_logger


def agent_router(raw_state):
    state = State().model_validate(raw_state)
    if state.tool_call.answer:
        return END
    else:
        return ToolExecutorNode.__name__

if __name__ == '__main__':
    print(ToolExecutorNode.__name__)