from src.chatbot.graph.tools.base import BaseTool
from src.chatbot.services.storage.storage_analysis_service import StorageAnalysisService


class GetSiblingsTool(BaseTool):
    def __init__(self, storage_analysis=None):
        self.storage_analysis = storage_analysis or StorageAnalysisService()

    def run(self, **kargs):
        paths = self.storage_analysis.get_siblings(**kargs)
        return paths

    def description(self):
        return self.storage_analysis.get_siblings.__doc__

    @property
    def name(self):
        return self.storage_analysis.get_siblings.__name__