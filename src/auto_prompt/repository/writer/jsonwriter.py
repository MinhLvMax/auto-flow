from .base import Writer
import json
import os

class JsonWriter(Writer):
    def save(self, data, output_dir: str) -> None:
        os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        with open(output_dir, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)