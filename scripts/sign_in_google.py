import os
import subprocess
from src.auto_flow.config import THIS_PROFILE, CHROME_PATH

project_path = os.path.dirname(os.path.abspath(__file__))



cmd = [
    CHROME_PATH,
    f"--user-data-dir={THIS_PROFILE}"
]

subprocess.Popen(cmd)