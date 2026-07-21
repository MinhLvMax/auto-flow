from pathlib import Path
import json
import os
# from tkinter import Tk, filedialog
# from src.chatbot.indexing.build_tree import select_folder
from src.chatbot.text_nomalizer import TextNormalizer
from src.chatbot.services.file_service.json_writer import JsonWriter
from src.chatbot.config import FILES_INDEX_PATH, FOLDERS_INDEX_PATH


class Indexer:

    def __init__(self, text_normalizer=None, json_writer=None):
        self.text_normalizer = text_normalizer or TextNormalizer()
        self.json_writer = json_writer or JsonWriter()

    def build_list(self, root: str) -> list[str]:
        """
        Quét toàn bộ file trong folder
        """
        paths = []

        for path in Path(root).rglob("*"):
            print(f'Đang quét {path=}')
            if path.is_file():
                paths.append(str(path.resolve()))
        return paths

    def build_index(self, root: str, output: str):
        """
        Build file index json
        """

        paths = self.build_list(root)

        files_index = []

        for i, path in enumerate(paths):
            print(f'{i}/{len(paths)}, đang xử lý {path=}')
            file_index = self._build_file_index(path)
            files_index.append(file_index)

        print(f'Lưu tại {output}')
        with open(output, "w", encoding="utf-8") as f:
            json.dump(files_index, f, ensure_ascii=False, indent=2)

    def build_index_v2(self, root_path: Path):
        print(self.build_index_v2.__name__)
        files_index = []
        folders_index = []
        list_error_path = []

        for current_path, list_subfolders, list_files in os.walk(root_path):
            current_path_obj = Path(current_path)
            normalized_parts = [
                self.text_normalizer.normalize(x)
                for x in current_path_obj.parts[:-1]
            ]
            # Index folder
            folders_index.append({
                "path": str(current_path_obj),
                'normalize_stem': self.text_normalizer.normalize(current_path_obj.stem),
                "normalize_parts": normalized_parts,
                "depth": len(current_path_obj.parts) - 1,
                "file_count": len(list_files),
                "subfolder_count": len(list_subfolders),
            })

            # Index file
            for file in list_files:
                print(f'Đang xử lý {file=}')
                path = current_path_obj / file
                try:
                    stat = path.stat()
                except FileNotFoundError as e:
                    print(f'Không thể index {path} vì 1 lý do nào đó')
                    list_error_path.append(path)
                    continue
                preview = self._get_text_preview(path, max_chars=300)
                record = {
                    "path": str(path),
                    'normalize_stem': self.text_normalizer.normalize(path.stem),
                    'suffix': path.suffix.lower(),
                    "normalize_parts": normalized_parts,
                    "mtime": int(stat.st_mtime),
                    "ctime": int(stat.st_ctime),
                    "size": stat.st_size,
                }
                if preview:
                    record["preview"] = preview

                files_index.append(record)

        self.json_writer.write(FILES_INDEX_PATH, files_index)
        print(f'Đã lưu {FILES_INDEX_PATH=}')
        self.json_writer.write(FOLDERS_INDEX_PATH, folders_index)
        print(f'Đã lưu {FOLDERS_INDEX_PATH=}')
        return list_error_path

    def _build_file_index(self, path: str):
        p = Path(path)
        stat = p.stat()

        size_kb = stat.st_size / 1024
        size_mb = size_kb / 1024
        file_size_str = f"{size_mb:.2f} MB" if size_mb >= 1.0 else f"{size_kb:.1f} KB"

        return {
            "path": path,
            'normalize_stem': self.text_normalizer.normalize(p.stem),
            'suffix': p.suffix,
            "folders": [
                self.text_normalizer.normalize(x)
                for x in p.parts[:-1]  # loại tên file ra, chỉ lấy các thành phần trước đó tức là folder thôi
            ],
            'mtime': stat.st_mtime,
            "ctime": stat.st_ctime,  # Ngày tạo
            'file_size': file_size_str,
            "preview": self._get_text_preview(p, max_chars=300)  # Đoạn trích nội dung
        }


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
    indexer = Indexer()
    result = indexer.build_index_v2(r'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE')

    output_file = Path("error_files.txt")
    with output_file.open("w", encoding="utf-8") as f:
        for item in result:
            f.write(f"{item}\n")

    print(f"Đã lưu danh sách lỗi vào: {output_file.resolve()}")
    pass
