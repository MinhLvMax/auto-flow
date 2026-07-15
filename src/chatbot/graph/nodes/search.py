from src.chatbot.graph.nodes.base_node import BaseNode
from src.chatbot.services.search_service.keyword_search import KeywordSearch
from src.chatbot.graph.state import State

class SearchNode(BaseNode):
    def __init__(self, search_service = None):
        super().__init__()
        self.search_service = search_service or KeywordSearch()

    def __call__(self, raw_state: dict):
        state = State.model_validate(raw_state)

        entities = state.entity_extraction_result.entities

        found_paths = []

        for entity in entities:
            if entity.name != '':
                found_paths.extend(self.search_service.search(entity.name))
            for alias in entity.aliases:
                if alias != '':
                    found_paths.extend(self.search_service.search(alias))
        # Lọc trùng
        found_paths = list(set(found_paths))
        update_dict = State(
            found_paths=found_paths,
        ).model_dump(
            exclude_none=True,
            exclude_defaults=True
        )
        self.loger.debug(update_dict)
        return update_dict
