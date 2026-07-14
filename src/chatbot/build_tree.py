from pathlib import Path

def build_tree(path, max_depth=None, current_depth=0):
    path = Path(path)

    if path.is_file():
        return None

    if max_depth is not None and current_depth >= max_depth:
        return {}

    return {
        child.name: build_tree(child, max_depth, current_depth + 1)
        for child in sorted(path.iterdir())
    }

if __name__ == '__main__':
    from src.chatbot.services.json_writer import JsonWriter
    json_writer = JsonWriter()
    tree = build_tree(Path('../chatbot'))
    json_writer.write(Path('.tree_dir.json'), tree)