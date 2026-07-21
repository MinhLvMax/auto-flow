from scripts.run_cmd_method import run
from scripts.config import PROJECT_PATH
from scripts.config import venv_python

requirements = PROJECT_PATH / 'requirements.txt'

with requirements.open('w', encoding='utf-8') as f:
    run(str(venv_python), '-m', 'pip', 'freeze', stdout=f)