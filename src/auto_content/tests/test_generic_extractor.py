from pprint import pprint

from src.auto_content.provider.DuckDuckGoSearchProvider import DuckDuckGoSearchProvider
from src.auto_content.extractor.generic_html_extractor import GenericHtmlExtractor
from src.auto_content.interface.knowledge_provider import ResearchQuery


if __name__ == "__main__":
    provider = DuckDuckGoSearchProvider()
    extractor = GenericHtmlExtractor()

    query = ResearchQuery(
        keyword="Động Phong Nha Kẻ Bàng",
        limit=3,
    )

    hits = provider.search(query)

    first_hit = hits[0]

    print("HIT:")
    pprint(first_hit)

    print("=" * 80)

    if extractor.can_extract(first_hit):
        document = extractor.extract(first_hit)

        print("DOCUMENT TITLE:")
        print(document.title)

        print("DOCUMENT URL:")
        print(document.url)

        print("DOCUMENT CONTENT:")
        print(document.content[:2000])
    else:
        print("Extractor cannot handle this hit")