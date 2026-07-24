from pathlib import Path
import os
from src.chatbot.services.text_nomalizer import TextNormalizer
from src.chatbot.services.file_service.json_writer import JsonWriter
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.config import TREE_INDEX_PATH, TOKEN_INDEX_PATH, PATH_ID_INDEX, DEDAULT_ROOT_PATH


class Indexer:

    def __init__(self, text_normalizer=None, json_writer=None, json_reader=None):
        self.text_normalizer = text_normalizer or TextNormalizer()
        self.json_writer = json_writer or JsonWriter()
        self.json_reader = json_reader or JsonReader()
        self.ignore = [
            ".idea",
            ".git",
            ".venv",
            "__pycache__",
        ]

    def build_tree_index(self, root_path: str=DEDAULT_ROOT_PATH, output_path: str = TREE_INDEX_PATH):
        result = {}
        i = 0
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in self.ignore]
            result[dirpath] = {
                'id': str(i),
                'dirnames': dirnames,
                'filenames': filenames,
            }
            i += 1
            for filename in filenames: # Duyệt để lấy luôn các path của file nữa vì hàm os đi bộ chỉ duyệt đến folder
                filename_path = Path(dirpath) / Path(filename)
                result[str(filename_path)] = {
                    'id': str(i),
                    'dirnames': [],
                    'filenames': [],
                }
                i += 1
        self.json_writer.write(output_path, result)

    def build_token_index(self, root_path=DEDAULT_ROOT_PATH, tree_indexed_path=TREE_INDEX_PATH, output_path=TOKEN_INDEX_PATH):
        data = self.json_reader.read(tree_indexed_path)
        inverted_index = {}
        for path, node in data.items():
            targets = [path]
            # Thêm các path của file nằm trong path đó vào list mục tiêu
            targets.extend(  # chỉ cần token thêm filenames là được, vì dirnames đã được chuyển hết lên path khi index
                str(Path(path) / filename)
                for filename in node["filenames"]
            )
            for target in targets:
                relative_path = Path(target).relative_to(root_path)
                tokens = set(self.text_normalizer.normalize(str(relative_path)).split())
                for token in tokens:
                    if token not in inverted_index:
                        inverted_index[token] = set()
                    inverted_index[token].add(target)
        inverted_index = {  # Chuyển từ set về list trước khi lưu json
            k: list(v)
            for k, v in inverted_index.items()
        }
        self.json_writer.write(output_path, inverted_index)

    def build_path_id_index(self, tree_indexed_path=TREE_INDEX_PATH, output_path=PATH_ID_INDEX):
        data = self.json_reader.read(tree_indexed_path)
        result = {}
        for k, v in data.items():
            result[v["id"]] = k
        self.json_writer.write(output_path, result)

    def build_index(self):
        self.build_tree_index()
        self.build_token_index()
        self.build_path_id_index()


if __name__ == '__main__':
    indexer = Indexer = Indexer()
    root_path = r'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE'
    indexer.build_index()
    # reader = JsonReader()
    # data = reader.read(TOKEN_INDEX_PATH)
    # print(len(data))
    pass
