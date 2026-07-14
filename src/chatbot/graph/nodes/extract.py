from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqServices
from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.models.entity_extraction_result import EntityExtractionResult

class ExtractEntitiesNode(BaseNode):
    def __init__(self, llm_service = None):
        super().__init__()
        self.llm_service = llm_service or GroqServices()

    def __call__(self, raw_state: dict):
        state = State.model_validate(raw_state)
        messages = [
            *state.history[-5:],
            {
                'role': 'user',
                'content': state.user_input,
            }
        ]
        result = self.llm_service.chat_json(messages, EntityExtractionResult)
        new_state = State(
            entity_extraction_result=result.model_dump()
        ).model_dump()
        self.loger.debug(new_state)
        return new_state

if __name__ == '__main__':
    data = {
        'user_input': 'Kho dữ liệu của tôi có làm về sao mộc và sao hỏa chưa'
    }
    classification_node = ExtractEntitiesNode()
    print(classification_node.__call__(data))