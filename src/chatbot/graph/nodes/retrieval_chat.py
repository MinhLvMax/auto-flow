from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.graph.config import WorkFLowConfig


class RetrievalChatNode(BaseNode):
    def __init__(self, llm_service=None, prompt_service=None):
        super().__init__()
        self.llm_service = llm_service or GroqService()
        self.prompt_service = prompt_service or PromptService()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)
        MIN_SCORE_THRESHOLD = 50
        valid_paths = [
            item for item in state.found_paths
            if item.get("score", 0) >= MIN_SCORE_THRESHOLD
        ]
        if not valid_paths:
            system_prompt = self.prompt_service.render('no_results', summary=state.dir_summary)
        else:
            paths = valid_paths[:10]  # Lấy một phần đầu để đưa vào llm nói
            retrieval_instruction = self.prompt_service.render('retrieval')
            context = self.prompt_service.render('search_context', paths=paths)
            system_prompt = '\n\n'.join([retrieval_instruction, context])

        msg = state.history.to_messages(system_prompt=system_prompt, last_n=10)
        system_output = self.llm_service.chat_history(msg, model_name=WorkFLowConfig.RETRIEVAL_MODEL)

        state.history.add('assistant', system_output)

        update_dict = State(
            history=state.history,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        return update_dict
