from src.auto_content.interface.knowledge_provider import KnowledgeProvider, ResearchQuery, SourceHit, KnowledgeDocument
from ddgs import DDGS

class DuckDuckGoSearchProvider(KnowledgeProvider):
    @property
    def source_name(self) -> str:
        return "duckduckgo"

    def search(self, query: ResearchQuery) -> list[SourceHit]:
        with DDGS() as ddgs:
            results = ddgs.text(
                query.keyword,
                max_results=query.limit,
            )

        hits: list[SourceHit] = []

        for item in results:
            hits.append(
                SourceHit(
                    source_name=self.source_name,
                    title=item.get("title", ""),
                    url=item.get("href"),
                    snippet=item.get("body"),
                    raw=item,
                )
            )

        return hits

    def fetch(self, hit: SourceHit) -> KnowledgeDocument:
        return KnowledgeDocument(
            source_name=self.source_name,
            title=hit.title,
            url=hit.url,
            content=hit.snippet or "",
            reliability_score=0.4,
            raw=hit.raw,
        )

if __name__ == '__main__':
    rq = ResearchQuery(
        keyword='Động phong nha kẻ bàng',
    )
    d = DuckDuckGoSearchProvider()
    infor =  d.search(rq)
    from pprint import pprint
    pprint(infor)

