from src.auto_content.interface.knowledge_provider import (
    KnowledgeProvider,
    ResearchQuery,
    SourceHit,
)


class YouTubeRankingService:
    def __init__(self, provider: KnowledgeProvider):
        self.provider = provider

    def find_top_viewed(
            self,
            keyword: str,
            search_limit: int = 20,
            top_n: int = 5,
    ) -> list[SourceHit]:
        query = ResearchQuery(
            keyword=keyword,
            limit=search_limit,
        )

        hits = self.provider.search(query)

        youtube_hits = [
            hit for hit in hits
            if hit.url and "youtube.com/watch" in hit.url
        ]

        sorted_hits = sorted(
            youtube_hits,
            key=self._get_view_count,
            reverse=True,
        )

        return sorted_hits[:top_n]

    def _get_view_count(self, hit: SourceHit) -> int:
        if not hit.raw:
            return 0

        return int(hit.raw.get("view_count") or 0)
