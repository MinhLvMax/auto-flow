import os
from pathlib import Path
from tkinter import Tk, filedialog

# Gộp tất cả thư mục, tên file, đuôi file cần bỏ qua vào một nơi duy nhất
IGNORE_LIST = {
    # Thư mục cần bỏ qua
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    ".obsidian",
    "build",
    "dist",
    ".chainlit",
    ".files",
    ".profiles",
    "profiles",
    "python_embed",
    'python-embed',
    "envato_browser_profile",
    'logs',

    # File cụ thể cần bỏ qua
    ".env",
    ".gitignore",
    "codebase_context.txt",  # Tránh tự đọc chính file output nếu chạy lại
    'README.md',

    # Đuôi file cần bỏ qua
    ".json",
    ".png",
    ".jpg",
    ".jpeg",
    ".mp4",
    ".zip",
    ".txt",
    ".pyc",
    ".db",
}


def should_ignore(path: Path, ignore_set: set) -> bool:
    """Kiểm tra đường dẫn có thuộc danh sách bỏ qua hay không"""
    # 1. Kiểm tra nếu có bất kỳ thư mục cha nào trong đường dẫn nằm trong danh sách ignore
    if any(part in ignore_set for part in path.parts):
        return True

    # 2. Kiểm tra tên file hoặc thư mục hiện tại
    if path.name in ignore_set or path.name.lower() in ignore_set:
        return True

    # 3. Kiểm tra đuôi file (suffix)
    if path.suffix.lower() in ignore_set:
        return True

    return False


def generate_tree_string(path: Path, prefix: str = "", ignore_set=None) -> str:
    """Tạo chuỗi sơ đồ cây thư mục trực quan"""
    if ignore_set is None:
        ignore_set = IGNORE_LIST

    tree_str = ""
    # Lọc bỏ các thư mục và file nằm trong danh sách ignore
    children = sorted([
        c for c in path.iterdir()
        if not (c.name in ignore_set or c.suffix.lower() in ignore_set)
    ])

    for i, child in enumerate(children):
        is_last = (i == len(children) - 1)
        connector = "└── " if is_last else "├── "

        tree_str += f"{prefix}{connector}{child.name}\n"

        if child.is_dir():
            indent = "    " if is_last else "│   "
            tree_str += generate_tree_string(child, prefix + indent, ignore_set)

    return tree_str


def read_file(path: Path) -> str:
    """Đọc nội dung file văn bản, bỏ qua lỗi giải mã"""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def select_folder():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Chọn thư mục dự án")
    root.destroy()
    return Path(folder) if folder else None


if __name__ == "__main__":
    # folder = select_folder() # Chọn đường dẫn cụ thể
    from src.config import BASE_DIR
    folder = BASE_DIR # Gán luôn bằng đường dẫn dự án
    if folder is None:
        exit()

    output_file = Path("codebase_context.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        # 1. Ghi tiêu đề và sơ đồ cây thư mục ở đầu file
        f.write("# TỔNG QUAN KIẾN TRÚC DỰ ÁN (DIRECTORY TREE)\n")
        f.write("```text\n")
        f.write(f"{folder.name}/\n")
        f.write(generate_tree_string(folder))
        f.write("```\n\n")
        f.write("=" * 80 + "\n\n")

        # 2. Quét và ghi nội dung từng file code
        f.write("# CHI TIẾT MÃ NGUỒN CÁC FILE\n\n")

        for path in sorted(folder.rglob("*")):
            # Bỏ qua nếu nằm trong danh sách ignore (áp dụng cho cả file và thư mục)
            if should_ignore(path, IGNORE_LIST):
                continue

            # Chỉ xử lý file, bỏ qua thư mục
            if not path.is_file():
                continue

            relative_path = path.relative_to(folder)
            content = read_file(path)

            if content.strip():
                # Xác định ngôn ngữ lập trình để hiển thị cú pháp
                lang = path.suffix.lstrip(".")
                if lang == "py":
                    lang = "python"

                f.write(f"## FILE: `{relative_path}`\n")
                f.write(f"```{lang}\n")
                f.write(content)
                if not content.endswith("\n"):
                    f.write("\n")
                f.write("```\n\n")
                f.write("-" * 40 + "\n\n")

    print(f"Đã xuất toàn bộ mã nguồn ra file: {output_file.absolute()}")