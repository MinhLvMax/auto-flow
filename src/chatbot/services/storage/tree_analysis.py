from pathlib import Path
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.config import TREE_INDEX_PATH
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.text_nomalizer import TextNormalizer


class TreeAnalysisService:
    def __init__(self, llm_service=None, tree_index_path=None, json_reader=None, text_normalizer=None):
        self.llmservice = llm_service or GroqService
        self.tree_index_path = tree_index_path or TREE_INDEX_PATH
        self.json_reader = json_reader or JsonReader()
        self.text_normalizer = text_normalizer or TextNormalizer()

    @property
    def tree_data(self):
        return self.json_reader.read(self.tree_index_path)

    def get_parent(self, path: str):
        return str(Path(path).parent)

    def get_children(self, path: str):
        node = self.tree_data.get(path)
        if node:
            children = []
            for dirname in node.get('dirnames', []):
                children.append(str(Path(path) / dirname))
            for filename in node.get('filenames', []):
                children.append(str(Path(path) / filename))
            return children
        return []

    def get_siblings(self, path: str):
        parent = self.get_parent(path)
        return self.get_children(parent)


if __name__ == '__main__':
    tas = TreeAnalysisService()
    query = 'Tìm kiếm các địa điểm trung quốc'
    path = r'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE\Nga'
    # print(tas.get_parent(path))
    # print(tas.get_children(path))
    # print(tas.get_siblings(path))

    # print(tas.get_parent.__doc__)
    # print(tas.get_children.__doc__)
    # print(tas.get_siblings.__doc__)
