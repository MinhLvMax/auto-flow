from dataclasses import dataclass, field


@dataclass
class SentenceInfo:
    text: str

    characters: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)
    objects: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)

    time: str | None = None