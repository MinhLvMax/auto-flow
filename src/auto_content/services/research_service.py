from src.auto_content.interface.knowledge_provider import (
    KnowledgeProvider,
    ResearchQuery,
    SourceHit,
    KnowledgeDocument,
)
from src.auto_content.interface.content_extractor import ContentExtractor


class ResearchService:
    def __init__(
        self,
        provider: KnowledgeProvider,
        extractor: ContentExtractor,
    ):
        self.provider = provider
        self.extractor = extractor

    def search(self, query: ResearchQuery) -> list[SourceHit]:
        """
        Chỉ tìm danh sách nguồn.
        Ví dụ: DuckDuckGo trả về title, url, snippet.
        """
        return self.provider.search(query)

    def research(self, query: ResearchQuery) -> list[KnowledgeDocument]:
        """
        Luồng chính:
        1. Search ra SourceHit
        2. Dùng extractor để bóc nội dung thật
        3. Trả về list KnowledgeDocument
        """
        hits = self.search(query)

        documents: list[KnowledgeDocument] = []

        for hit in hits:
            try:
                document = self._extract_hit(hit)

                if document.content.strip():
                    documents.append(document)

            except Exception as error:
                print(f"Cannot extract: {hit.url} | {error}")

        return documents

    def _extract_hit(self, hit: SourceHit) -> KnowledgeDocument:
        """
        Ưu tiên dùng extractor để bóc nội dung thật.

        Nếu extractor không xử lý được, tạm fallback về provider.fetch().
        provider.fetch() hiện tại của bạn đang lấy snippet, nên chỉ là phương án dự phòng.
        """
        if self.extractor.can_extract(hit):
            return self.extractor.extract(hit)

        return self.provider.fetch(hit)