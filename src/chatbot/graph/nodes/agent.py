
from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.graph.tools import get_tool_definitions

class Agent(BaseNode):
    def __init__(self, llm_service=None):
        super().__init__()
        self.llm_service = llm_service or GroqService()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)

        update_dict = State(

        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        return update_dict


if __name__ == '__main__':
    pass
