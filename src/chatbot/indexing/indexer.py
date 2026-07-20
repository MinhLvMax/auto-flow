from pathlib import Path
import json
# from tkinter import Tk, filedialog
# from src.chatbot.indexing.build_tree import select_folder
from src.chatbot.text_nomalizer import TextNormalizer


class Indexer:

    def __init__(self, text_normalizer=None):
        self.text_normalizer = text_normalizer or TextNormalizer()

    def build_list(self, root: str) -> list[str]:
        """
        Quét toàn bộ file trong folder
        """
        paths = []

        for path in Path(root).rglob("*"):
            if path.is_file():
                paths.append(str(path.resolve()))

        return paths

    def build_index(self, root: str, output: str):
        """
        Build file index json
        """

        paths = self.build_list(root)

        index = []

        for path in paths:
            p = Path(path)
            stat = p.stat()

            size_kb = stat.st_size / 1024
            size_mb = size_kb / 1024
            file_size_str = f"{size_mb:.2f} MB" if size_mb >= 1.0 else f"{size_kb:.1f} KB"

            index.append({
                "path": path,
                'normalize_stem': self.text_normalizer.normalize(p.stem),
                'suffix': p.suffix,
                "folders": [
                    self.text_normalizer.normalize(x)
                    for x in p.parts[:-1]  # loại tên file ra, chỉ lấy các thành phần trước đó tức là folder thôi
                ],
                'mtime': stat.st_mtime,
                "ctime": stat.st_ctime, # Ngày tạo
                'file_size': file_size_str,
                "preview": self._get_text_preview(p, max_chars=300)  # Đoạn trích nội dung
            })
        print(f'Lưu tại {output}')
        with open(output, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    def _get_text_preview(self, path_obj: Path, max_chars=300) -> str:
        """Đọc thử một đoạn nội dung ngắn nếu là file văn bản để làm preview"""
        # Chỉ đọc các file văn bản phổ biến
        text_suffixes = {".txt", ".md", ".json", ".csv"}
        if path_obj.suffix.lower() not in text_suffixes:
            return ""
        try:
            # Đọc tối đa số lượng ký tự quy định để tránh file quá nặng
            with open(path_obj, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(max_chars)
                # Dọn dẹp các ký tự xuống dòng dư thừa để lưu trữ gọn gàng
                return " ".join(content.split())
        except Exception:
            return ""

    # def select_folder(self):
    #     root = Tk()
    #     root.withdraw()  # Ẩn cửa sổ chính
    #
    #     folder = filedialog.askdirectory(
    #         title="Chọn thư mục cần build tree"
    #     )
    #
    #     root.destroy()
    #
    #     return folder if folder else None


if __name__ == '__main__':
    # path = select_folder()
    # indexer = Indexer()
    # indexer.build_index(path, 'index.json')
    pass
