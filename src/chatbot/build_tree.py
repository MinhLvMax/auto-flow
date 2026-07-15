from pathlib import Path
from tkinter import Tk, filedialog


def build_tree(
        path,
        max_depth=None,
        current_depth=0,
        ignore_dirs=None
):
    path = Path(path)

    if ignore_dirs is None:
        ignore_dirs = DEFAULT_IGNORE_DIRS

    if path.is_file():
        return None

    if max_depth is not None and current_depth >= max_depth:
        return {}

    tree = {}

    for child in sorted(path.iterdir()):

        # bỏ qua folder nằm trong blacklist
        if child.is_dir() and child.name in ignore_dirs:
            continue

        tree[child.name] = build_tree(
            child,
            max_depth,
            current_depth + 1,
            ignore_dirs
        )

    return tree


def select_folder():
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ chính

    folder = filedialog.askdirectory(
        title="Chọn thư mục cần build tree"
    )

    root.destroy()

    return Path(folder) if folder else None


if __name__ == '__main__':

    DEFAULT_IGNORE_DIRS = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
        '.obsidian'
    }

    from services.file_service.json_writer import JsonWriter

    json_writer = JsonWriter()
    path_folder = select_folder()
    tree = build_tree(path_folder)
    json_writer.write(Path('tree_dir.json'), tree)
