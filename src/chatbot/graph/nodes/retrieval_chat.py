from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqServices
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.graph.nodes.base_node import BaseNode
from src.loggers import main_logger


class RetrievalChatNode(BaseNode):
    def __init__(self, llm_service=None, prompt_service=None):
        super().__init__()
        self.llm_service = llm_service or GroqServices()
        self.prompt_service = prompt_service or PromptService()

    def __call__(self, raw_state: dict):
        state = State.model_validate(raw_state)

        context = self.prompt_service.render('search_context', paths=state.found_paths[:20])
        retrieval_instruction = self.prompt_service.render('retrieval')
        system_prompt = '\n\n'.join([retrieval_instruction, context])

        msg = state.history.to_messages(system_prompt=system_prompt, last_n=10)
        system_output = self.llm_service.chat_history(msg)

        state.history.add('assistant', system_output)

        update_dict = State(
            history=state.history,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )

        self.loger.debug(update_dict)
        return update_dict
