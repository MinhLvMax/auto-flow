from pathlib import Path
from src.auto_flow.utils.helpers import read_excel, save_json
from src.auto_flow.config import SCRIPTS_DIR

class ScriptManager:
    def __init__(self, script_folder_path):
        self.script_folder_path = script_folder_path
        pass

    def get_paths(self):
        folder = Path(self.script_folder_path)
        return [p for p in folder.iterdir() if p.is_file()]

    def create_jsons_paths(self):
        paths = []
        for input_path in self.get_paths():
            data = read_excel(input_path)
            output_path = SCRIPTS_DIR / f'{input_path.stem}.json'
            save_json(data, output_path)
            paths.append(output_path)
        return paths

if __name__ == '__main__':
    sm = ScriptManager(r'D:\minhlvfile\pythonproject\auto-flow\data\input\scripts')
    sm.create_jsons_paths()