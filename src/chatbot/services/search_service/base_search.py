from abc import ABC, abstractmethod
from src.config import BASE_DIR
from src.chatbot.services.file_service.json_reader import JsonReader

class BaseSearch(ABC):
    default_path = BASE_DIR / 'src' / 'chatbot' / 'tree_dir.json'

    def __init__(self, tree_path=None):
        self.tree_path = tree_path or self.default_path
        self.tree_data = self._load_index()

    def _load_index(self):
        if not self.tree_path.exists():
            return {}

        return JsonReader().read(self.tree_path) or {}

    @abstractmethod
    def search(self, query) -> list[str]:
        pass

