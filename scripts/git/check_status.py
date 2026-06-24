import subprocess
from src.auto_flow.config import BASE_DIR

cmd = ["git", "-c", "color.status=always", "status"]

subprocess.run(cmd, cwd=BASE_DIR)
