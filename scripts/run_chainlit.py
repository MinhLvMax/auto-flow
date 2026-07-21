from scripts.run_cmd_method import run
from scripts.config import venv_python

entry_point = 'main.py'  # sửa nếu có thay đổi entry point
run(str(venv_python), '-m', 'chainlit', 'run', entry_point)
