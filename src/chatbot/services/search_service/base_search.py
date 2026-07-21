from abc import ABC, abstractmethod
from src.chatbot.services.storage_analysis_service import StorageAnalysisService


class BaseSearch(ABC):
    def __init__(self, storage_service=None):
        # Inject dịch vụ phân tích kho làm đơn vị cung cấp dữ liệu index sạch
        self.storage_service = storage_service or StorageAnalysisService()

        # Nhận dữ liệu đã nạp sẵn từ bộ nhớ của dịch vụ phân tích
        self.files_index_data = self.storage_service.files_data
        self.folders_index_data = self.storage_service.folders_data

    @abstractmethod
    def search(self, query) -> list[str]:
        pass