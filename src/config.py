from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import os

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
GROQ_API_KEY =os.getenv('GROQ_API_KEY')

BASE_DIR = Path(__file__).resolve().parents[1]  # Đường dẫn file chính của dự án
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PATH_FOLDER_LOG = BASE_DIR / 'logs'
PATH_FOLDER_LOG.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':

    print(f'{BASE_DIR=}')
