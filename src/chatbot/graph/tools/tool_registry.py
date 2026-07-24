from src.chatbot.graph.tools.get_childrens import GetChildrensTool
from src.chatbot.graph.tools.get_parent import GetParentTool
from src.chatbot.graph.tools.get_siblings import GetSiblingsTool
from src.chatbot.graph.tools.search_path import SearchPathTool


class ToolRegistry:
    def __init__(self):
        self.tools = [
            GetChildrensTool(),
            GetParentTool(),
            GetSiblingsTool(),
            SearchPathTool(),
        ]

        self.tool_map = {
            tool.name: tool
            for tool in self.tools
        }

    def get(self, name):
        return self.tool_map.get(name)

    def definitions(self):
        return [
            {
                "name": tool.name,
                "description": tool.description()
            }
            for tool in self.tools
        ]