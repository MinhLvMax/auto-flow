from scripts.config import PROJECT_PATH
from scripts.install_requirements.for_py_embed.setup_py_embed import python_embed_extract_dir

# Cài package
from scripts.run_cmd_method import run

python_path = python_embed_extract_dir / "python.exe"
run(python_path, '-m', 'pip', 'install', '-r', "requirements.txt",)

