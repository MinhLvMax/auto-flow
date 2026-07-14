from graph.nodes.base_node import BaseNode
from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqServices
from src.chatbot.graph.nodes.base_node import BaseNode

class NaturalChatNode(BaseNode):
    def __init__(self, llm_service = None):
        super().__init__()
        self.llm_service = llm_service or GroqServices()

    def __call__(self, raw_state: dict):
        state = State.model_validate(raw_state)

        history = state.history
        history.append({
            'role': 'user',
            'content': state.user_input,
        })
        system_output = self.llm_service.chat_history(history)
        new_state = State(
            sustem_output=system_output
        ).model_dump()
        self.loger.debug(new_state)
        return new_state

if __name__ == '__main__':
    data = {
        'user_input': 'Xin chào'
    }