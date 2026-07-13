from pathlib import Path


class TextReader:
    def read(self, path: str | Path) -> str:
        path = Path(path)

        with path.open("r", encoding="utf-8") as f:
            return f.read()
