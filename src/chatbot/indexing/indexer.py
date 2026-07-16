from pathlib import Path
import json
import re
from tkinter import Tk, filedialog

from indexing.build_tree import select_folder
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

            index.append({
                "path": path,
                'normalize_stem': self.text_normalizer.normalize(p.stem),
                'suffix': p.suffix,
                "folders": [
                    self.text_normalizer.normalize(x)
                    for x in p.parts[:-1]  # loại tên file ra, chỉ lấy các thành phần trước đó tức là folder thôi
                ]
            })
        print(f'Lưu tại {output}')
        with open(output, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    def select_folder(self):
        root = Tk()
        root.withdraw()  # Ẩn cửa sổ chính

        folder = filedialog.askdirectory(
            title="Chọn thư mục cần build tree"
        )

        root.destroy()

        return folder if folder else None


if __name__ == '__main__':
    path = select_folder()
    indexer = Indexer()
    indexer.build_index(path, 'index.json')
    pass
