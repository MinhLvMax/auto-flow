from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # Đường dẫn file chính của dự án

PATH_FOLDER_LOG = BASE_DIR / 'logs'

DATA_DIR = BASE_DIR / 'data'
INPUT_DATA_DIR = DATA_DIR / 'input'
OUTPUT_DATA_DIR = DATA_DIR / 'output'

RUNTIME_DIR = BASE_DIR / 'runtime'
PROFILE_DIR = RUNTIME_DIR / 'profiles'
AUTH_DIR = RUNTIME_DIR / 'auth'
THIS_PROFILE = PROFILE_DIR / 'taikhoantaoradelamgi98' # Về sau nên cho nó nhận từ cli

if __name__ == '__main__':

    print(f'{BASE_DIR=}')
    print(f'{DATA_DIR=}')
    print(f'{INPUT_DATA_DIR=}')
    print(f'{OUTPUT_DATA_DIR=}')
    print(f'{RUNTIME_DIR=}')
