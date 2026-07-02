from src.auto_flow.schemas.script_prompt_result import ScriptPromptResult
from src.auto_flow.services.file_services import FileServices


class Script:
    def __init__(self, path, file_services = FileServices()):
        self.file_services = file_services
        self.path = path
        self.name = path.stem
        self.summary = ''
        # self.prompts: list[ScriptPromptResult] = []

    @property
    def excel_content(self):
        return self.file_services.read_excel(self.path)
