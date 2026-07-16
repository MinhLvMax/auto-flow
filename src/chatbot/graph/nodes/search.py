from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.services.search_service.keyword_search import KeywordSearch
from src.chatbot.graph.state import State
from src.loggers import main_logger


class SearchNode(BaseNode):
    def __init__(self, search_service=None):
        super().__init__()
        self.search_service = search_service or KeywordSearch()

    def run(self, raw_state: dict):
        state = State.model_validate(raw_state)
        entities = state.entity_extraction_result.entities
        found_paths = []
        for entity in entities:
            if entity.name != '':
                paths = self.search_service.search(entity.name)
                found_paths.extend(paths)
            # for alias in entity.aliases:
            #     if alias != '':
            #         found_paths.extend(self.search_service.search(alias))
        # Lọc trùng
        seen = set()
        unique_results = []

        for item in found_paths:
            if item["path"] not in seen:
                seen.add(item["path"])
                unique_results.append(item)

        found_paths = unique_results
        self.loger.debug(found_paths)
        update_dict = State(
            found_paths=found_paths,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        return update_dict
