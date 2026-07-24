from src.chatbot.graph.tools.base import BaseTool
from src.chatbot.services.storage.storage_analysis_service import StorageAnalysisService


class GetParentTool(BaseTool):
    def __init__(self, storage_analysis=None):
        self.storage_analysis = storage_analysis or StorageAnalysisService()

    def run(self, **kargs):
        path = self.storage_analysis.parent(**kargs)
        return path

    def description(self):
        return self.storage_analysis.parent.__doc__

    @property
    def name(self):
        return self.storage_analysis.parent.__name__