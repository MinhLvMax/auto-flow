import json
from .base import Reader

class JsonReader(Reader):
    def parse(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)