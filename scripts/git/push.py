import subprocess
from src.auto_flow.config import BASE_DIR

commands = [
    ['git', 'push']
]

for cmd in commands:
    subprocess.run(cmd, cwd=BASE_DIR)
