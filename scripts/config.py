from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parents[1]
venv_path = PROJECT_PATH / '.venv'
venv_python = venv_path / "Scripts" / "python.exe"