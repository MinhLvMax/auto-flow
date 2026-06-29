import pandas as pd
import json
from pathlib import Path
from pydantic import BaseModel

class FileServices:
    def __init__(self):
        pass

    def read_excel(self, path):
        df = pd.read_excel(path)
        df = df.fillna('')  # Thay NaN bằng rỗng
        data = df.to_dict(orient="records")
        return data

    def read_json(self, file_path) -> dict:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, data, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def read_txt(self, path: Path) -> str:
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    def save_pydantic_json(self, data: BaseModel, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        json_data = data.model_dump(mode="json")
        with open(path, "w", encoding="utf-8") as f: json.dump(json_data, f, ensure_ascii=False, indent=4)