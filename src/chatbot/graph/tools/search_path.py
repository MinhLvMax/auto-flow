from src.chatbot.graph.tools.base import BaseTool
from src.chatbot.services.storage.storage_analysis_service import StorageAnalysisService


class SearchPathTool(BaseTool):
    def __init__(self, storage_analysis=None):
        self.storage_analysis = storage_analysis or StorageAnalysisService()

    def run(self, **kargs):
        paths = self.storage_analysis.search(**kargs)
        return paths

    def description(self):
        return self.storage_analysis.search.__doc__

    @property
    def name(self):
        return self.storage_analysis.search.__name__