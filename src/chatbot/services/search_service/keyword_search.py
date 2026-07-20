from pathlib import Path
from src.chatbot.services.search_service.base_search import BaseSearch
from src.loggers import main_logger
from src.chatbot.text_nomalizer import TextNormalizer
from src.chatbot.models.found_path_result import FoundPathResult


class KeywordSearch(BaseSearch):

    def __init__(self, root_path=None, text_normalizer=None):
        super().__init__(root_path)
        self.text_normalizer = text_normalizer or TextNormalizer()

    def search(self, query: str) -> list[dict]:
        list_rerank_path_result = []
        normalized_query = self.text_normalizer.normalize(query)
        query_tokens = normalized_query.split()
        for data in self.indexed_data:
            score = 0
            # So sánh tên nằm trong tên file
            if normalized_query == data.get('normalize_stem', ''):
                score += 150
            elif normalized_query in data.get('normalize_stem', ''):
                score += 100
            # So sánh tên nằm trong đường dẫn
            for folder in data.get('folders', []):
                if normalized_query in folder:
                    score += 30
            # So sánh từ ngữ nằm trong tên
            matched = set(query_tokens) & set(data.get('normalize_stem').split())
            score += len(matched) * 30

            if score > 0:
                rerank_path_result = FoundPathResult(
                    path=data.get('path', ''),
                    score=score
                )
                list_rerank_path_result.append(rerank_path_result.model_dump())

        return sorted(  # Sắp xếp kết quả giảm dần
            list_rerank_path_result,
            key=lambda x: x["score"],
            reverse=True
        )


if __name__ == '__main__':
    keyword_search = KeywordSearch()
    paths = keyword_search.search('Black hole')
    for path in paths:
        print(path)
