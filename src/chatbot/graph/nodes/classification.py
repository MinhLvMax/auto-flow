
from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.models.intent_classification import IntentClassification
from src.chatbot.graph.config import WorkFLowConfig
from src.loggers import main_logger


class ClassificationNode(BaseNode):
    def __init__(self, llm_service=None):
        super().__init__()
        self.llm_service = llm_service or GroqService()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)

        messages = state.history.messages[-5:]
        classif_result = self.llm_service.chat_json(messages, IntentClassification, model_name=WorkFLowConfig.CLASSIFICATION_MODEL)
        self.loger.debug(classif_result)
        update_dict = State(
            classification_results=classif_result,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        return update_dict


if __name__ == '__main__':
    data = {
        'user_input': 'Kho dữ liệu tôi làm về vũ trụ chưa'
    }
    classification_node = ClassificationNode()
    print(classification_node.__call__(data))
