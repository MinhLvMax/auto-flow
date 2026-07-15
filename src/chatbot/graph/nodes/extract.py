from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqServices
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.models.entity_extraction_result import EntityExtractionResult
from src.loggers import main_logger


class ExtractEntitiesNode(BaseNode):
    def __init__(self, llm_service = None, promp_service = None):
        super().__init__()
        self.llm_service = llm_service or GroqServices()
        self.prompt_service = promp_service or PromptService()

    def __call__(self, raw_state: dict):
        state = State.model_validate(raw_state)
        messages = state.history.to_messages(last_n=3)
        instruction = self.prompt_service.render('extract_entities_instruction')
        result = self.llm_service.chat_json(messages, EntityExtractionResult, system_prompt=instruction)

        update_dict = State(
            entity_extraction_result=result.model_dump()
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        self.loger.debug(update_dict)
        return update_dict

if __name__ == '__main__':
    state = State()
    state.history.add('user', 'Tôi từng làm về mặt trăng chưa?')
    main_logger.debug(state.model_dump())
    classification_node = ExtractEntitiesNode()
    print(classification_node.__call__(state.model_dump()))