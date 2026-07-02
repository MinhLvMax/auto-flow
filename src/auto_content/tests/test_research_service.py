from src.auto_content.interface.knowledge_provider import ResearchQuery
from src.auto_content.provider.DuckDuckGoSearchProvider import DuckDuckGoSearchProvider
from src.auto_content.extractor.generic_html_extractor import GenericHtmlExtractor
from src.auto_content.services.research_service import ResearchService


if __name__ == "__main__":
    provider = DuckDuckGoSearchProvider()
    extractor = GenericHtmlExtractor()

    research_service = ResearchService(
        provider=provider,
        extractor=extractor,
    )

    query = ResearchQuery(
        keyword="Abuna Yemata Guh",
        limit=5,
    )

    documents = research_service.research(query)

    for document in documents:
        print("=" * 80)
        print("TITLE:")
        print(document.title)

        print("URL:")
        print(document.url)

        print("CONTENT:")
        print(document.content)