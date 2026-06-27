import json
import pandas as pd
from src.auto_flow.config import RUNTIME_DIR

def read_excel(path):
    df = pd.read_excel(path)
    df = df.fillna('') # Thay NaN bằng rỗng
    data = df.to_dict(orient="records")
    return data

def read_json(file_path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    save_json(read_excel(r'/data/input/scripts/#11.xlsx'), RUNTIME_DIR / '#11.json')

