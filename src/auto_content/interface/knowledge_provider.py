from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ResearchQuery:
    keyword: str
    language: str = "en"
    limit: int = 10
    country: str | None = None
    category: str | None = None


@dataclass
class SourceHit:
    source_name: str
    title: str
    url: str | None = None
    external_id: str | None = None
    snippet: str | None = None
    raw: dict[str, Any] | None = None


@dataclass
class KnowledgeDocument:
    source_name: str
    title: str
    content: str
    url: str | None = None
    facts: dict[str, Any] | None = None
    visual_keywords: list[str] | None = None
    published_at: datetime | None = None
    reliability_score: float = 0.5
    raw: dict[str, Any] | None = None


class KnowledgeProvider(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str:
        pass

    @abstractmethod
    def search(self, query: ResearchQuery) -> list[SourceHit]:
        pass

    @abstractmethod
    def fetch(self, hit: SourceHit) -> KnowledgeDocument:
        pass