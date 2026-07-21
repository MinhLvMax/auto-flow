import sys
from scripts.run_cmd_method import run

run(sys.executable, '-m', 'pip', 'list')