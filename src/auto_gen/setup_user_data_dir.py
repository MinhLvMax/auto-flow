import subprocess
from pathlib import Path
from src.config import BASE_DIR

CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
USER_DATA_DIR = BASE_DIR / r'src\auto_gen\profiles\user0'
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

cmd = [
    CHROME_PATH,
    f"--user-data-dir={USER_DATA_DIR}"
]

subprocess.Popen(cmd)