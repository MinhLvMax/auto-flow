from abc import ABC, abstractmethod
from services.storage.storage_analysis_service import StorageAnalysisService


class BaseSearch(ABC):
    def __init__(self, storage_service=None):
        # Inject dịch vụ phân tích kho làm đơn vị cung cấp dữ liệu index sạch
        self.storage_service = storage_service or StorageAnalysisService()
