import json
import re
import pandas as pd
from src.auto_flow.config import RUNTIME_DIR

#
# def read_excel(path):
#     df = pd.read_excel(path)
#     df = df.fillna('')  # Thay NaN bằng rỗng
#     data = df.to_dict(orient="records")
#     return data
#
#
# def read_json(file_path) -> dict:
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)
#
#
# def save_json(data, path):
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)


def split_sentences(text: str) -> list[str]:
    if not text:
        return []

    # Chuẩn hóa xuống dòng
    text = text.replace("\n", " ").strip()

    # Tách sau . ! ?
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Xóa khoảng trắng và câu rỗng
    return [s.strip() for s in sentences if s.strip()]
