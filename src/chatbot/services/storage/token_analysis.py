from collections import Counter
from pathlib import Path
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.config import TOKEN_INDEX_PATH, TREE_INDEX_PATH
from src.chatbot.services.groq_llm_services import GroqService
from src.chatbot.services.text_nomalizer import TextNormalizer
from src import log

logger = log.get_logger(__name__)

class TokenAnalysisService:
    def __init__(self, llm_service=None, token_index_path=None, tree_index_path=None, json_reader=None,
                 text_normalizer=None):
        self.llmservice = llm_service or GroqService
        self.token_index_path = token_index_path or TOKEN_INDEX_PATH
        self.tree_index_path = tree_index_path or TREE_INDEX_PATH
        self.json_reader = json_reader or JsonReader()
        self.text_normalizer = text_normalizer or TextNormalizer()
        self._token_data = None
        self._tree_data = None

    @property
    def token_data(self):
        if self._token_data is None:
            return self.json_reader.read(self.token_index_path)
        else:
            return self._token_data

    @property
    def tree_data(self):
        if self._tree_data is None:
            return self.json_reader.read(self.tree_index_path)
        else:
            return self._tree_data

    @log.log_call(logger)
    def token_search(self, query: str): # Đang bị duyệt 3 lần
        scores = Counter()
        query_nomalizer = self.text_normalizer.normalize(query)
        query_tokens = set(self.text_normalizer.tokenize(query))

        for token in query_tokens:
            for path in self.token_data.get(token, []):
                scores[path] += 1

                path_obj = Path(path)
                path_normalizer = self.text_normalizer.normalize(path_obj.stem)
                if path_obj.suffix == '' and query_nomalizer in path_normalizer:  # Ưu tiên folder hơn để nó được xếp hàng lên cao hơn các file ở trong đó
                    depth_bonus = 1 / len(path_obj.parts)
                    scores[path] += depth_bonus  # folder ngắn hơn thì càng được ưu tiên hơn

        # print(scores)
        result = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
        {
            "path": path,
            "id": self.tree_data.get(path, {}).get("id"),
            "score": score
        }
        for path, score in result
    ]


if __name__ == '__main__':
    tas = TokenAnalysisService()
    query = 'trung quốc'
    candicates = tas.token_search(query)
    print(f'{len(candicates)=}')
    for candidate in candicates:
        print(candidate)
