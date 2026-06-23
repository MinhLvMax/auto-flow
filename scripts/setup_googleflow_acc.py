import subprocess
from src.auto_flow.config import FLOW_PROFILE, CHROME_PATH

cmd = [
    CHROME_PATH,
    f"--user-data-dir={FLOW_PROFILE}"
]

subprocess.Popen(cmd)