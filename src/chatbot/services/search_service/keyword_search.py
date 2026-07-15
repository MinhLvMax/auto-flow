from src.chatbot.services.search_service.base_search import BaseSearch


class KeywordSearch(BaseSearch):

    def __init__(self, tree_path=None):
        super().__init__(tree_path)

    def search(self, query: str) -> list[str]:
        results = []

        self._recursive_search(
            self.tree_data,
            [],
            query.lower(),
            results
        )

        return results

    def _recursive_search(
            self,
            node: dict,
            path: list[str],
            query: str,
            results: list[str]
    ):
        for name, value in node.items():
            current_path = path + [name]

            if query in name.lower():
                results.append(
                    "/" + "/".join(current_path)
                )

            if isinstance(value, dict):
                self._recursive_search(
                    value,
                    current_path,
                    query,
                    results
                )

if __name__ == '__main__':
    keyword_search = KeywordSearch()
    print(keyword_search.search('Vũ trụ'))