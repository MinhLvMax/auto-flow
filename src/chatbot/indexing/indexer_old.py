from pathlib import Path
import json
import os
# from tkinter import Tk, filedialog
# from src.chatbot.indexing.build_tree import select_folder
from services.text_nomalizer import TextNormalizer
from src.chatbot.services.file_service.json_writer import JsonWriter
from src.chatbot.config import FILES_INDEX_PATH, FOLDERS_INDEX_PATH
import uuid
from datetime import datetime


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

    def build_index_v3(
            self,
            root_path: str | Path,
            output_path: str | Path | None = None
    ) -> list[str]:
        """
        Quét toàn bộ cây thư mục và ghi file + folder vào một file JSON duy nhất.

        Mỗi node gồm:
            id
            type
            name
            normalized_name
            path
            relative_path
            parent_id
            depth
            extension
            size
            modified_at

        :param root_path: Folder gốc cần index.
        :param output_path: Đường dẫn file JSON đầu ra.
        :return: Danh sách các đường dẫn không thể index.
        """

        print(self.build_index_v3.__name__)

        root = Path(root_path).expanduser()

        if not root.exists():
            raise FileNotFoundError(f"Không tìm thấy thư mục: {root}")

        if not root.is_dir():
            raise NotADirectoryError(f"Đường dẫn không phải thư mục: {root}")

        # Chuyển root thành đường dẫn tuyệt đối.
        root = root.resolve()

        # Nếu không truyền output_path thì tạo directory_index.json
        # cùng thư mục với files_index.json hiện tại.
        if output_path is None:
            output_path = FILES_INDEX_PATH.with_name("directory_index.json")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        nodes: list[dict] = []
        error_paths: list[str] = []

        def normalize_relative_path(path: Path) -> str:
            """
            Chuẩn hóa relative path về dạng dùng dấu /.

            Root folder sẽ có relative_path là chuỗi rỗng.
            """
            path_string = path.as_posix()

            if path_string == ".":
                return ""

            return path_string

        def create_node_id(node_type: str, relative_path: str) -> str:
            """
            Tạo ID ổn định từ loại node và relative path.

            Cùng một relative_path sẽ tạo ra cùng một ID
            khi chạy index lại.
            """
            path_key = relative_path.casefold() or "__root__"
            value = f"{node_type}:{path_key}"

            generated_uuid = uuid.uuid5(
                uuid.NAMESPACE_URL,
                value
            )

            return f"{node_type}_{generated_uuid.hex}"

        def handle_walk_error(error: OSError):
            """
            Nhận lỗi do os.walk gặp phải, ví dụ folder không có quyền đọc.
            """
            error_path = getattr(error, "filename", None) or str(error)

            print(f"Không thể quét: {error_path}")
            error_paths.append(str(error_path))

        for current_path, subfolders, files in os.walk(
                root,
                topdown=True,
                onerror=handle_walk_error,
                followlinks=False
        ):
            # Sắp xếp để thứ tự node ổn định giữa các lần index.
            subfolders.sort(key=str.casefold)
            files.sort(key=str.casefold)

            current_path_obj = Path(current_path)

            try:
                relative_folder_obj = current_path_obj.relative_to(root)
            except ValueError:
                print(f"Đường dẫn nằm ngoài root, bỏ qua: {current_path_obj}")
                error_paths.append(str(current_path_obj))
                continue

            relative_folder_path = normalize_relative_path(
                relative_folder_obj
            )

            folder_id = create_node_id(
                node_type="folder",
                relative_path=relative_folder_path
            )

            # Root không có parent.
            if relative_folder_path == "":
                parent_id = None
                depth = 0
            else:
                parent_relative_path = normalize_relative_path(
                    relative_folder_obj.parent
                )

                parent_id = create_node_id(
                    node_type="folder",
                    relative_path=parent_relative_path
                )

                depth = len(relative_folder_obj.parts)

            try:
                folder_stat = current_path_obj.stat()
                folder_modified_at = int(folder_stat.st_mtime)
            except OSError as error:
                print(
                    f"Không thể đọc metadata folder "
                    f"{current_path_obj}: {error}"
                )
                error_paths.append(str(current_path_obj))
                folder_modified_at = None

            # Ghi node folder.
            folder_record = {
                "id": folder_id,
                "type": "folder",
                "name": current_path_obj.name,
                "normalized_name": self.text_normalizer.normalize(
                    current_path_obj.name
                ),
                "path": str(current_path_obj),
                "relative_path": relative_folder_path,
                "parent_id": parent_id,
                "depth": depth,
                "extension": None,
                "size": None,
                "modified_at": folder_modified_at
            }

            nodes.append(folder_record)

            # Ghi các file nằm trực tiếp trong folder hiện tại.
            for filename in files:
                file_path = current_path_obj / filename

                try:
                    file_stat = file_path.stat()
                    relative_file_obj = file_path.relative_to(root)
                except OSError as error:
                    print(
                        f"Không thể index file {file_path}: {error}"
                    )
                    error_paths.append(str(file_path))
                    continue
                except ValueError:
                    print(
                        f"File nằm ngoài root, bỏ qua: {file_path}"
                    )
                    error_paths.append(str(file_path))
                    continue

                relative_file_path = normalize_relative_path(
                    relative_file_obj
                )

                file_id = create_node_id(
                    node_type="file",
                    relative_path=relative_file_path
                )

                file_record = {
                    "id": file_id,
                    "type": "file",
                    "name": file_path.name,

                    # Dùng stem để tên tìm kiếm không chứa extension.
                    # Ví dụ video_01.mp4 -> video 01
                    "normalized_name": self.text_normalizer.normalize(
                        file_path.stem
                    ),

                    "path": str(file_path),
                    "relative_path": relative_file_path,

                    # Folder hiện tại chính là parent trực tiếp của file.
                    "parent_id": folder_id,

                    # File nằm sâu hơn folder hiện tại một cấp.
                    "depth": len(relative_file_obj.parts),

                    "extension": file_path.suffix.lower(),
                    "size": file_stat.st_size,
                    "modified_at": int(file_stat.st_mtime)
                }

                nodes.append(file_record)

        root_id = create_node_id(
            node_type="folder",
            relative_path=""
        )

        index_data = {
            "schema_version": 0,
            "root_id": root_id,
            "root_path": str(root),
            "indexed_at": datetime.now().astimezone().isoformat(
                timespec="seconds"
            ),
            "node_count": len(nodes),
            "error_count": len(error_paths),
            "nodes": nodes
        }

        # Ghi ra file tạm trước, sau đó mới thay thế file index chính.
        # Cách này giảm nguy cơ index chính bị hỏng nếu chương trình
        # bị dừng giữa lúc đang ghi.
        temporary_output_path = output_path.with_suffix(
            output_path.suffix + ".tmp"
        )

        self.json_writer.write(
            temporary_output_path,
            index_data
        )

        os.replace(
            temporary_output_path,
            output_path
        )

        print(f"Đã lưu index tại: {output_path}")
        print(f"Tổng số node: {len(nodes)}")
        print(f"Số đường dẫn lỗi: {len(error_paths)}")

        return error_paths


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

    # result = indexer.build_index_v2(r'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE')
    #
    # output_file = Path("error_files.txt")
    # with output_file.open("w", encoding="utf-8") as f:
    #     for item in result:
    #         f.write(f"{item}\n")
    #
    # print(f"Đã lưu danh sách lỗi vào: {output_file.resolve()}")

    # result = indexer.build_index_v3(
    #     root_path=r'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE',
    #     output_path=Path("directory_index.json"))

    pass
