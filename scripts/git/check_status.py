import subprocess
from src.auto_flow.config import BASE_DIR

cmd = [
    'git',
    'status'
]

subprocess.run(cmd, cwd=BASE_DIR)