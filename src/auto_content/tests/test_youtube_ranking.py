from src.auto_content.provider.YouTubeSearchProvider import YouTubeSearchProvider
from src.auto_content.services.youtube_ranking_service import YouTubeRankingService


if __name__ == "__main__":
    provider = YouTubeSearchProvider()

    service = YouTubeRankingService(
        provider=provider,
    )

    hits = service.find_top_viewed(
        keyword="Abuna Yemata Guh",
        search_limit=20,
        top_n=5,
    )

    for index, hit in enumerate(hits, start=1):
        raw = hit.raw or {}

        print("=" * 80)
        print(f"TOP {index}")
        print("TITLE:", hit.title)
        print("URL:", hit.url)
        print("CHANNEL:", raw.get("channel"))
        print("VIEWS:", raw.get("view_count"))
        print("DURATION:", raw.get("duration"))
        print("UPLOAD DATE:", raw.get("upload_date"))