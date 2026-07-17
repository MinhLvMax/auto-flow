from src.chatbot.models.history import History
from src.chatbot.graph.workflows.orchestrator import build_workflow
from src.chatbot.graph.state import State
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.services.groq_llm_services import GroqServices
from src.loggers import main_logger


class ChatbotService:
    def __init__(self, workflow=None, prompt_service=None, llm_service = None):
        self.workflow = workflow or build_workflow()
        self.prompt_service = prompt_service or PromptService()
        self.llm_service = llm_service or GroqServices()

    def create_session(self):
        history = History()
        system_prompt = self.prompt_service.render(name="system")
        history.add(role='system', content=system_prompt)
        first_mess = self.llm_service.chat_history(history.to_messages())
        history.add(role='assistant', content=first_mess)
        return history

    def chat(self, history=None):
        main_logger.info('Chạy dịch vụ chat')
        state_dict = State(history=history).model_dump()
        last_state_dict = self.workflow.invoke(state_dict)
        last_state_obj = State.model_validate(last_state_dict)
        return last_state_obj.history, last_state_obj.found_paths
