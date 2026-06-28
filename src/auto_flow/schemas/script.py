from src.auto_flow.schemas.pair_prompt import PairPrompt
from src.auto_flow.services.file_services import FileServices


class Script:
    def __init__(self, path, file_services = FileServices()):
        self.file_services = file_services
        self.path = path
        self.name = path.stem
        self.summary = ''
        self.prompts: list[PairPrompt] = []

    @property
    def content(self):
        return self.file_services.read_excel(self.path)
