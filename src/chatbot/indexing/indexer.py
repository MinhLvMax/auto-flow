from pathlib import Path
import os
from services.text_nomalizer import TextNormalizer
from src.chatbot.services.file_service.json_writer import JsonWriter
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.config import TREE_INDEX_PATH, TOKEN_INDEX_PATH


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

    def build_index(self, root_path: str, output_path: str):
        result = {}
        for id, (dirpath, dirnames, filenames) in enumerate(os.walk(root_path)):
            dirnames[:] = [d for d in dirnames if d not in self.ignore]
            result[id] = {
                'dirpath': dirpath,
                'dirnames': dirnames,
                'filenames': filenames,
            }
        self.json_writer.write(output_path, result)

    def build_token_index(self, root_path, indexed_path=None, output_path=None):
        data = self.json_reader.read(indexed_path)
        inverted_index = {}
        for path, node in data.items():
            targets = [path]
            # index file với full path
            targets.extend( # chỉ cần token thêm filenames là được, vì dirnames đã được chuyển hết lên path khi index
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
        inverted_index = { # Chuyển từ set về list trước khi lưu json
            k: list(v)
            for k, v in inverted_index.items()
        }
        self.json_writer.write(output_path, inverted_index)


if __name__ == '__main__':
    indexer = Indexer = Indexer()
    root_path = r'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE'
    indexer.build_index(root_path, TREE_INDEX_PATH)
    indexer.build_token_index(root_path, TREE_INDEX_PATH, TOKEN_INDEX_PATH)

    # reader = JsonReader()
    # data = reader.read(TOKEN_INDEX_PATH)
    # print(len(data))
    pass
