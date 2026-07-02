from yt_dlp import YoutubeDL

from src.auto_content.interface.knowledge_provider import (
    KnowledgeProvider,
    ResearchQuery,
    SourceHit,
    KnowledgeDocument,
)


class YouTubeSearchProvider(KnowledgeProvider):
    @property
    def source_name(self) -> str:
        return "youtube"

    def search(self, query: ResearchQuery) -> list[SourceHit]:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
            "noplaylist": True,
            "ignoreerrors": True,
        }

        search_text = f"ytsearch{query.limit}:{query.keyword}"

        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_text, download=False)

        entries = result.get("entries", []) if result else []

        hits: list[SourceHit] = []

        for item in entries:
            if not item:
                continue

            video_id = item.get("id")
            url = item.get("webpage_url")

            if not url and video_id:
                url = f"https://www.youtube.com/watch?v={video_id}"

            hits.append(
                SourceHit(
                    source_name=self.source_name,
                    title=item.get("title", ""),
                    url=url,
                    external_id=video_id,
                    snippet=item.get("description"),
                    raw={
                        "id": video_id,
                        "title": item.get("title"),
                        "url": url,
                        "channel": item.get("channel") or item.get("uploader"),
                        "view_count": item.get("view_count") or 0,
                        "duration": item.get("duration"),
                        "upload_date": item.get("upload_date"),
                        "description": item.get("description"),
                    },
                )
            )

        return hits

    def fetch(self, hit: SourceHit) -> KnowledgeDocument:
        raw = hit.raw or {}

        return KnowledgeDocument(
            source_name=self.source_name,
            title=hit.title,
            url=hit.url,
            content=hit.snippet or "",
            facts={
                "video_id": hit.external_id,
                "channel": raw.get("channel"),
                "view_count": raw.get("view_count"),
                "duration": raw.get("duration"),
                "upload_date": raw.get("upload_date"),
            },
            reliability_score=0.5,
            raw=hit.raw,
        )