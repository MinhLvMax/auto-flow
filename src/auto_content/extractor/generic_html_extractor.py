import requests
from bs4 import BeautifulSoup
from src.auto_content.interface.content_extractor import ContentExtractor
from src.auto_content.interface.knowledge_provider import SourceHit, KnowledgeDocument


class GenericHtmlExtractor(ContentExtractor):
    @property
    def extractor_name(self) -> str:
        return "generic_html"

    def can_extract(self, hit: SourceHit) -> bool:
        if not hit.url:
            return False

        return hit.url.startswith("http://") or hit.url.startswith("https://")

    def extract(self, hit: SourceHit) -> KnowledgeDocument:
        if not hit.url:
            raise ValueError("Cannot extract content because hit.url is empty")

        response = requests.get(
            hit.url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        self._remove_noise_tags(soup)

        title = self._extract_title(soup, hit)
        content = self._extract_main_content(soup)

        return KnowledgeDocument(
            source_name=hit.source_name,
            title=title,
            url=hit.url,
            content=content,
            reliability_score=0.6,
            raw={
                "extractor": self.extractor_name,
                "search_raw": hit.raw,
                "status_code": response.status_code,
                "html_length": len(response.text),
                "content_length": len(content),
            },
        )

    def _remove_noise_tags(self, soup: BeautifulSoup) -> None:
        noise_tags = [
            "script",
            "style",
            "noscript",
            "nav",
            "footer",
            "header",
            "aside",
            "form",
            "iframe",
            "svg",
        ]

        for tag in soup(noise_tags):
            tag.decompose()

    def _extract_title(self, soup: BeautifulSoup, hit: SourceHit) -> str:
        if hit.title:
            return hit.title

        if soup.title and soup.title.string:
            return soup.title.string.strip()

        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        return ""

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        main = (
                soup.find("article")
                or soup.find("main")
                or soup.find("div", {"role": "main"})
                or soup.body
        )

        if main is None:
            return ""

        paragraphs = main.find_all("p")

        lines = []

        for paragraph in paragraphs:
            text = paragraph.get_text(separator=" ", strip=True)

            if not text:
                continue

            if len(text) < 50:
                continue

            lines.append(text)

        return "\n\n".join(lines)