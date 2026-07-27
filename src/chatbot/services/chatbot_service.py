from src.chatbot.models.history import History
from src.chatbot.graph.state import State
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.storage.storage_analysis_service import StorageAnalysisService
from src.chatbot.graph.workflows.agent_graph import build_agent_graph


class ChatbotService:
    def __init__(self, workflow=None, prompt_service=None, llm_service=None, storage_service=None):
        self.workflow = workflow or build_agent_graph()
        self.prompt_service = prompt_service or PromptService()
        self.llm_service = llm_service or GroqService()
        self.storage_service = storage_service or StorageAnalysisService()

    def chat(self, history=None):
        state_dict = State(history=history).model_dump()
        last_state_dict = self.workflow.invoke(state_dict)
        last_state_obj = State.model_validate(last_state_dict)
        return last_state_obj.history, last_state_obj.tool_result
