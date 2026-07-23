from src.chatbot.models.history import History
from src.chatbot.graph.workflows.orchestrator import build_workflow
from src.chatbot.graph.state import State
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.services.groq_llm_services import GroqService
from services.storage.storage_analysis_service import StorageAnalysisService
from src.loggers import main_logger


class ChatbotService:
    def __init__(self, workflow=None, prompt_service=None, llm_service=None, storage_service=None):
        self.workflow = workflow or build_workflow()
        self.prompt_service = prompt_service or PromptService()
        self.llm_service = llm_service or GroqService()
        self.storage_service = storage_service or StorageAnalysisService()

    def create_session(self, **kwargs):
        history = History()
        dir_summary = self.storage_service.get_warehouse_summary_prompt()
        system_prompt = self.prompt_service.render(name="system", summary=dir_summary)
        # Tạo payload tạm thời để hỏi LLM câu chào đầu tiên
        initial_payload = [{"role": "system", "content": system_prompt}]
        first_mess = self.llm_service.chat_history(initial_payload)
        history.add(role='assistant', content=first_mess)
        return history

    # def _get_directory_summary(self, root_path) -> str:
    #     """Đọc nhanh file index và lấy danh sách các thư mục/chủ đề chính hiện có"""
    #     index_path = Path(root_path)
    #     if not index_path.exists():
    #         return "Hiện tại chưa có dữ liệu nào được lập chỉ mục."
    #     try:
    #         with open(index_path, "r", encoding="utf-8") as f:
    #             data = json.load(f)
    #
    #         # Lấy ra các tên thư mục con cấp 1 (ngay sau thư mục gốc) để làm danh mục chính
    #         main_categories = set()
    #         for item in data:
    #             folders = item.get("folders", [])
    #             if len(folders) > 0:
    #                 # Lấy folder đầu tiên trong chuỗi phân cấp làm danh mục chính
    #                 main_categories.add(folders[-1])
    #
    #         if main_categories:
    #             return "Các danh mục chính bạn đang quản lý bao gồm: " + ", ".join(list(main_categories)[:15])
    #         return "Thư mục hiện tại đang trống hoặc chưa được phân loại."
    #     except Exception as e:
    #         main_logger.error(f"Lỗi khi đọc tóm tắt thư mục: {e}")
    #         return "Không thể tải cấu trúc thư mục."

    def chat(self, history=None):
        main_logger.info('Chạy dịch vụ chat')
        state_dict = State(history=history).model_dump()
        last_state_dict = self.workflow.invoke(state_dict)
        last_state_obj = State.model_validate(last_state_dict)
        return last_state_obj.history, last_state_obj.found_paths
