from pathlib import Path
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.config import TREE_INDEX_PATH, PATH_ID_INDEX
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.text_nomalizer import TextNormalizer
from src import log

logger = log.get_logger(__name__)

class TreeAnalysisService:
    def __init__(self, llm_service=None, tree_index_path=None, path_id_index=None, json_reader=None,
                 text_normalizer=None):
        self.llmservice = llm_service or GroqService
        self.tree_index_path = tree_index_path or TREE_INDEX_PATH
        self.path_id_index = path_id_index or PATH_ID_INDEX
        self.json_reader = json_reader or JsonReader()
        self.text_normalizer = text_normalizer or TextNormalizer()

    @property
    def tree_data(self):
        return self.json_reader.read(self.tree_index_path)

    @property
    def path_id_data(self):
        return self.json_reader.read(self.path_id_index)

    @log.log_call(logger)
    def get_parent(self, path_id: str):
        path = self.path_id_data.get(path_id, None)
        parent_path = Path(path).parent
        parent_obj = self.tree_data.get(str(parent_path), None)
        parent_id = parent_obj.get('id', None)
        # return str(parent_path), parent_id
        return [{
            'path': str(parent_path),
            'id': parent_id
        }]

    @log.log_call(logger)
    def get_children(self, path_id: str):
        path = self.path_id_data.get(path_id, None)
        path_obj = self.tree_data.get(path)
        if path_obj:
            childrens = []
            for dirname in path_obj.get('dirnames', []):
                dirname_path = str(Path(path) / dirname)
                dirname_path_id = self.tree_data.get(str(dirname_path), None).get('id', None)
                # childrens.append((dirname_path, dirname_path_id))
                childrens.append({
                    'path': dirname_path,
                    'id': dirname_path_id
                })
            for filename in path_obj.get('filenames', []):
                filename_path = str(Path(path) / filename)
                filename_path_id = self.tree_data.get(str(filename_path), None).get('id', None)
                # childrens.append((filename_path, filename_path_id))
                childrens.append({
                    'path': filename_path,
                    'id': filename_path_id
                })
            return childrens
        return []

    @log.log_call(logger)
    def get_siblings(self, path_id: str):
        this_path = self.path_id_data.get(path_id, None)
        parent = self.get_parent(path_id)
        siblings = self.get_children(parent[0].get('id'))
        siblings.remove({
            'path': this_path,
            'id': path_id
        })
        return siblings


if __name__ == '__main__':
    tas = TreeAnalysisService()
    query = 'Tìm kiếm các địa điểm trung quốc'
    # path = r'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE\England\Lindisfarne'
    # print(tas.get_parent('693'))
    # print(tas.get_children('693'))
    print(tas.get_siblings('693'))

    # print(tas.get_parent.__doc__)
    # print(tas.get_children.__doc__)
    # print(tas.get_siblings.__doc__)
