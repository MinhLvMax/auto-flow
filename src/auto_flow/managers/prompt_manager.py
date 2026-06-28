from src.auto_flow.managers.script_manager import scripts_manager
from src.auto_flow.utils.helpers import read_json

class PromptManager:
    def __init__(self):
        self.scripts_manager = scripts_manager
        pass

    def get_prompts(self):
        data = []
        paths = scripts_manager.create_jsons_paths()
        for path in paths:
            data.append(read_json(path))
        return data

if __name__ == '__main__':
    pm = PromptManager()
    print(pm.get_prompts())