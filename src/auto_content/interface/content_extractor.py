from abc import ABC, abstractmethod
from src.auto_content.interface.knowledge_provider import SourceHit, KnowledgeDocument


class ContentExtractor(ABC):
    @property
    @abstractmethod
    def extractor_name(self) -> str:
        """
        Tên extractor, dùng để log/debug.
        Ví dụ: generic_html, wikipedia, youtube_transcript, pdf...
        """
        pass

    @abstractmethod
    def can_extract(self, hit: SourceHit) -> bool:
        """
        Kiểm tra extractor này có bóc được nội dung từ SourceHit này không.
        """
        pass

    @abstractmethod
    def extract(self, hit: SourceHit) -> KnowledgeDocument:
        """
        Bóc nội dung thật từ SourceHit và trả về KnowledgeDocument.
        """
        pass
