from pathlib import Path
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.storage.token_analysis import TokenAnalysisService
from src.chatbot.services.storage.tree_analysis import TreeAnalysisService


class StorageAnalysisService:
    '''
    Cung cấp các cơ chế phân tích kho
    '''

    def __init__(self, token_analysis=None, tree_analysis=None, json_loader=None, llm_service=None):
        self.json_loader = json_loader or JsonReader()
        self.llm_service = llm_service or GroqService()
        self.token_analysis = token_analysis or TokenAnalysisService()
        self.tree_analysis = tree_analysis or TreeAnalysisService()

    def search(self, query):
        '''
        Tìm kiếm paths theo từ khóa
        :param query: Từ khóa cần tìm kiếm
        :return: Danh sách path tìm được
        '''
        paths = [
            path
            for path, score in self.token_analysis.token_search(query)
        ]
        return paths

    def get_parent(self, path):
        '''
        Lấy đường dẫn thư mục cha của một path. Dùng khi cần quay lên cấp thư mục trước đó.
        :param path: Đường dẫn hiện tại.
        :return: Đường dẫn thư mục cha.
        '''
        return self.tree_analysis.get_parent(path)

    def get_children(self, path):
        '''
        Lấy danh sách thư mục và file con trực tiếp của path.
        :param path: Đường dẫn thư mục cần xem.
        :return: Danh sách đường dẫn các mục con.
        '''
        return self.tree_analysis.get_children(path)

    def get_siblings(self, path):
        '''
        Lấy các thư mục và file cùng cấp với path.
        :param path: Đường dẫn hiện tại.
        :return: Danh sách đường dẫn các mục cùng cấp.
        '''
        return self.tree_analysis.get_siblings(path)


if __name__ == '__main__':
    pass
