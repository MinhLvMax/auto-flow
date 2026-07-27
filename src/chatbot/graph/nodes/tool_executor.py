import json

from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.graph.state import State
from src.chatbot.graph.tools.tool_registry import ToolRegistry
from src.chatbot.services.groq_llm_services import GroqService, GroqModelName
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.services.storage.storage_analysis_service import StorageAnalysisService
from src.chatbot.models.tool_call import ToolCall
from src import log

class ToolExecutorNode(BaseNode):
    def __init__(self, registry=None):
        super().__init__()
        self.registry = registry or ToolRegistry()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)
        tool = self.registry.get(state.tool_call.tool_name)
        if tool is None:
            raise ValueError(
                f"Unknown tool {state.tool_call.tool_name}"
            )
        result = tool.run(
            **state.tool_call.arguments
        )
        update_dict = State(
            tool_result=result,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        return update_dict


if __name__ == '__main__':
    pass
