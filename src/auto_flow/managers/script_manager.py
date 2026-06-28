from pathlib import Path
from src.auto_flow.utils.helpers import read_excel, save_json
from src.auto_flow.config import RUN_TIME_SCRIPTS_DIR, INPUT_SCRIPTS_DIR

class ScriptManager:
    def __init__(self, script_folder_path = INPUT_SCRIPTS_DIR):
        self.script_input_folder_path = script_folder_path
        pass

    def get_paths(self):
        '''
        Lấy các path kịch bản đầu vào
        '''
        folder = Path(self.script_input_folder_path)
        return [p for p in folder.iterdir() if p.is_file()]

    def create_jsons_paths(self, scripts_dir = RUN_TIME_SCRIPTS_DIR):
        '''
        Tạo json từ các path kịch bản
        '''
        paths = []
        for input_path in self.get_paths():
            data = read_excel(input_path)
            output_path = scripts_dir / f'{input_path.stem}.json'
            save_json(data, output_path)
            paths.append(output_path)
        return paths

scripts_manager = ScriptManager()

if __name__ == '__main__':
    pass