import subprocess
from src.auto_flow.config import CHATGPT_PROFILE, CHROME_PATH

cmd = [
    CHROME_PATH,
    f"--user-data-dir={CHATGPT_PROFILE}"
]

subprocess.Popen(cmd)