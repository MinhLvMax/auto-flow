from scripts.run_cmd_method import run
from scripts.config import venv_python

run(str(venv_python), "-m", "pip", "install", "-r", "requirements.txt", )
