from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqServices
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.graph.config import WorkFLowConfig


class NaturalChatNode(BaseNode):
    def __init__(self, llm_service=None, prompt_service=None):
        super().__init__()
        self.llm_service = llm_service or GroqServices()
        self.prompt_service = prompt_service or PromptService()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)

        natural_instruction = self.prompt_service.render('natural', summary=state.dir_summary)
        msges = state.history.to_messages(last_n=4, system_prompt=natural_instruction)
        system_output = self.llm_service.chat_history(msges, WorkFLowConfig.NATURAL_CHAT_MODEL)

        state.history.add('assistant', system_output)

        update_dict = State(
            history=state.history,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )

        return update_dict
