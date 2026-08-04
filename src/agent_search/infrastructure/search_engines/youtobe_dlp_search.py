import yt_dlp


class YoutubeDLPClient:
    def __init__(self):
        self.options = {
            "quiet": True,
            "extract_flat": True,
            "skip_download": True,
        }

    def search(self, keyword, limit=5):
        with yt_dlp.YoutubeDL(self.options) as ydl:
            result = ydl.extract_info(
                f"ytsearch{limit}:{keyword}",
                download=False
            )

        return result["entries"]


if __name__ == '__main__':
    from pprint import pprint
    # Sử dụng
    youtube = YoutubeDLPClient()
    videos = youtube.search("Tràng An", 10)
    pprint(videos)


