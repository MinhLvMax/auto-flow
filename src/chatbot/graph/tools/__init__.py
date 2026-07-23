from .get_childrens import GetChildrensTool
from .get_parent import GetParentTool
from .get_siblings import GetSiblingsTool
from .search_path import SearchPathTool
from .base import BaseTool

# Khởi tạo các tool (bạn có thể truyền StorageAnalysisService vào nếu cần cấu hình riêng)
# Hoặc để mặc định như code hiện tại của bạn
INSTALLED_TOOLS = [
    GetChildrensTool(),
    GetParentTool(),
    GetSiblingsTool(),
    SearchPathTool()
]

# Tạo một dictionary để tra cứu tool nhanh dựa trên tool.name
TOOL_REGISTRY = {tool.name: tool for tool in INSTALLED_TOOLS}

def get_tool_definitions():
    """
    Hàm này hỗ trợ lấy thông tin mô tả của các tool
    để gửi kèm trong prompt hệ thống hoặc cấu hình cho LLM.
    """
    return [
        {
            "name": tool.name,
            "description": tool.description()
        }
        for tool in INSTALLED_TOOLS
    ]