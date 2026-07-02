import pandas as pd
import json
from pathlib import Path
from pydantic import BaseModel
from src.auto_flow.schemas.scene_prompt_result import ScenePromptResult


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

    def read_scene_prompt(self, path):
        data = self.read_json(path)
        return ScenePromptResult(**data)

    def get_scenes_prompt_list(self, script_prompt_folder_path):
        scene_json_path = self.get_filepaths_in_folder(script_prompt_folder_path)
        scenes_prompt_list  = []
        for scene_json_path in scene_json_path:
            data = self.read_json(scene_json_path)
            scene_prompt = ScenePromptResult(**data)
            scenes_prompt_list.append(scene_prompt)
        return scenes_prompt_list

    def get_filepaths_in_folder(self, folder_path):
        file_paths = [path for path in folder_path.iterdir() if path.is_file()]
        return file_paths


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

if __name__ == '__main__':
    file_services = FileServices()
    # obj = file_services.read_scene_prompt(r'D:\minhlvfile\pythonproject\auto-flow\data\output\#13\INTRO.json')
    # print(obj)

    print(file_services.get_filepaths_in_folder(Path(r"D:\minhlvfile\pythonproject\auto-flow\data\output\#13")))
