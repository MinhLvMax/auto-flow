import subprocess
from src.auto_flow.config import BASE_DIR
from datetime import datetime

user_commit = input("Nhập commit code: ")

if not user_commit:
    user_commit = datetime.now().strftime("Auto commit %Y-%m-%d %H:%M:%S")

commands = [
    ['git', 'add', '.'],
    ['git', 'commit', '-m', user_commit],
    ['git', 'push']
]

for cmd in commands:
    subprocess.run(cmd, cwd=BASE_DIR)