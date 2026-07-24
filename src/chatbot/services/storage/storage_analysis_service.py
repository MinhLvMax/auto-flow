from pathlib import Path
import inspect
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.storage.token_analysis import TokenAnalysisService
from src.chatbot.services.storage.tree_analysis import TreeAnalysisService


import inspect
import json


def tool(description: str):
    def decorator(func):
        signature = inspect.signature(func)

        func.tool_desc = {
            "name": func.__name__,
            "description": description,
            "params": [
                p.name
                for p in signature.parameters.values()
                if p.name != "self"
            ]
        }

        return func

    return decorator


import inspect



class StorageAnalysisService:
    '''
    Cung cấp các cơ chế phân tích kho
    '''

    def __init__(self, token_analysis=None, tree_analysis=None, json_loader=None, llm_service=None):
        self.json_loader = json_loader or JsonReader()
        self.llm_service = llm_service or GroqService()
        self.token_analysis = token_analysis or TokenAnalysisService()
        self.tree_analysis = tree_analysis or TreeAnalysisService()

    @tool('Tìm kiếm paths theo query')
    def search(self, query):
        '''
        Tìm kiếm paths theo từ khóa
        :param query: Từ khóa cần tìm kiếm
        :return: Danh sách path tìm được
        '''
        return self.token_analysis.token_search(query)

    @tool('Lấy đường dẫn thư mục cha')
    def parent(self, id):
        '''
        Lấy đường dẫn thư mục cha của một path. Dùng khi cần quay lên cấp thư mục trước đó.
        :param id: ID của đường dẫn hiện tại.
        :return: Đường dẫn thư mục cha.
        '''
        return self.tree_analysis.get_parent(id)

    @tool('Lấy danh sách thư mục và file con trực tiếp')
    def children(self, id):
        '''
        Lấy danh sách thư mục và file con trực tiếp của path.
        :param id: ID của đường dẫn thư mục cần xem.
        :return: Danh sách đường dẫn các mục con.
        '''
        return self.tree_analysis.get_children(id)

    @tool('Lấy các thư mục và file cùng cấp')
    def siblings(self, id):
        '''
        Lấy các thư mục và file cùng cấp với path.
        :param id: ID đường dẫn hiện tại.
        :return: Danh sách đường dẫn các mục cùng cấp.
        '''
        return self.tree_analysis.get_siblings(id)

    def get_tool_definitions(selt):
        tools = []

        for _, method in inspect.getmembers(selt, inspect.ismethod):
            if hasattr(method, "tool_desc"):
                tools.append(method.tool_desc)

        return tools

if __name__ == '__main__':
    storage_analysis_service = StorageAnalysisService()
    print(storage_analysis_service.get_tool_definitions())
    pass
