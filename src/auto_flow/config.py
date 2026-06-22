from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # Đường dẫn file chính của dự án
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


PATH_FOLDER_LOG = BASE_DIR / 'logs'
PATH_FOLDER_LOG.mkdir(parents=True, exist_ok=True)

DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

INPUT_DATA_DIR = DATA_DIR / 'input'
INPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DATA_DIR = DATA_DIR / 'output'
OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)

RUNTIME_DIR = BASE_DIR / 'runtime'
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_DIR = RUNTIME_DIR / 'profiles'
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

AUTH_DIR = RUNTIME_DIR / 'auth'


THIS_PROFILE = PROFILE_DIR / 'taikhoantaoradelamgi98' # Về sau nên cho nó nhận từ cli, nên để là user1 user2 cho đỡ hiểu nhầm logic

if __name__ == '__main__':

    print(f'{BASE_DIR=}')
    print(f'{DATA_DIR=}')
    print(f'{INPUT_DATA_DIR=}')
    print(f'{OUTPUT_DATA_DIR=}')
    print(f'{RUNTIME_DIR=}')
