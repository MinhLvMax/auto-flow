import json

from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.graph.state import State
from src.chatbot.services.groq_llm_services import GroqService, GroqModelName
from src.chatbot.services.prompt_service import PromptService
from src.chatbot.services.storage.storage_analysis_service import StorageAnalysisService
from src.chatbot.models.history import History
from src.chatbot.models.tool_call import ToolCall
from src.loggers import main_logger


class AgentNode(BaseNode):
    def __init__(self, llm_service=None, prompt_service=None, storage_analysis_service=None):
        super().__init__()
        self.llm_service = llm_service or GroqService()
        self.prompt_service = prompt_service or PromptService()
        self.storage_analysis_service = storage_analysis_service or StorageAnalysisService()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)
        tools_definition = json.dumps(
            self.storage_analysis_service.get_tool_definitions(),
            ensure_ascii=False,
            separators=(",", ":")
        )
        system_prompt = self.prompt_service.render('tool_call',
                                                   tools_definition=tools_definition)
        messages = state.history.to_messages(system_prompt, 3)
        new_history = state.history
        if state.tool_result is not None:
            filtered_results = [r for r in state.tool_result if r.get('score', 0) >= 2][:8]

            # Fallback nếu lọc xong không còn kết quả nào phù hợp
            if not filtered_results:
                filtered_results = state.tool_result[:3]

            # Đưa kết quả vào hội thoại dưới vai trò người dùng (user) hoặc hệ thống (system)
            new_dict ={
                "role": "user",
                "content": f"[Hệ thống] Kết quả truy vấn từ công cụ:\n{json.dumps(filtered_results, ensure_ascii=False)}"
            }

            messages.append(new_dict)
            new_history.add('user', new_dict['content'])

        response: ToolCall = self.llm_service.get_tool_schema(messages, GroqModelName.LLAMA_3_3_70B_VERSATILE)

        if response.answer:
            new_history.add('assistant', response.answer)
        elif response.tool_name:
            # Ghi nhận bước đi của Agent vào lịch sử trò chuyện để lượt sau nó nhớ được mình đã gọi gì
            new_history.add(
                'assistant',
                f"[Yêu cầu hệ thống] Tôi cần gọi công cụ '{response.tool_name}' với tham số: {json.dumps(response.arguments, ensure_ascii=False)}"
            )
        update_dict = State(
            history=new_history,
            tool_call=response,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        main_logger.debug(update_dict)
        return update_dict


if __name__ == '__main__':
    agent = AgentNode()
    messeges = [
        {
            "role": "user",
            "content": "thư mục id 2 cùng cấp với các thư mục nào"
        }
    ]
    raw_state = {
        'history': {
            'messages': messeges,
        },
    }
    # state = State().model_validate(raw_state)

    agent.run(raw_state)
    pass
