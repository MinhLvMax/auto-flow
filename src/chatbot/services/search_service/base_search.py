from abc import ABC, abstractmethod

from src.config import BASE_DIR
from src.chatbot.services.file_service.json_reader import JsonReader
from src.loggers import main_logger


class BaseSearch(ABC):
    default_path = BASE_DIR / 'src' / 'chatbot' / 'indexing' / 'index.json'

    def __init__(self, root_path=None):
        self.root_path = root_path or self.default_path
        self.indexed_data = self._load_index()

    def _load_index(self):
        if not self.root_path.exists():
            return {}

        return JsonReader().read(self.root_path) or {}

    @abstractmethod
    def search(self, query) -> list[str]:
        pass

