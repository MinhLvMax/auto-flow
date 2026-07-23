from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.prompt_service import PromptService
from services.storage.storage_analysis_service import StorageAnalysisService
from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.graph.config import WorkFLowConfig


class StorageAnalysisNode(BaseNode):
    def __init__(self, llm_service=None, prompt_service=None, storage_service=None):
        super().__init__()
        self.llm_service = llm_service or GroqService()
        self.prompt_service = prompt_service or PromptService()
        self.storage_service = storage_service or StorageAnalysisService()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)

        # 1. Gọi dịch vụ phân tích kho để lấy cấu trúc cây thư mục và thông số tổng quan
        warehouse_summary = self.storage_service.get_warehouse_summary_prompt()

        # 2. Render Prompt hệ thống dành riêng cho phân tích kho
        system_prompt = self.prompt_service.render('storage_analysis', summary=warehouse_summary)

        # 3. Lấy hội thoại lịch sử kèm theo System Prompt mới nạp dữ liệu
        messages = state.history.to_messages(system_prompt=system_prompt, last_n=6)

        # 4. Gọi LLM để sinh câu trả lời cho khách hàng
        system_output = self.llm_service.chat_history(messages, model_name=WorkFLowConfig.NATURAL_CHAT_MODEL)

        # 5. Lưu phản hồi vào lịch sử trò chuyện
        state.history.add('assistant', system_output)

        update_dict = State(
            history=state.history
        ).model_dump(exclude_none=True, exclude_defaults=True)

        return update_dict