import subprocess

url = "https://www.facebook.com/stories/191635882440346/UzpfSVNDOjQ1NTU0MTE1NjE0NDc3NDA=/?view_single=false"

subprocess.run(
    [
        "yt-dlp",
        "-f", "bv*+ba/b",
        "--cookies-from-browser", "edge",  # Nếu cần đăng nhập
        "-o", "%(title)s.%(ext)s",  # Tên file đầu ra
        url,
    ],
    check=True
)
