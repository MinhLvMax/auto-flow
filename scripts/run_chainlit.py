from scripts.run_cmd_method import run
import sys

entry_point = 'main.py' # sửa nếu có thay đổi entry point
run(sys.executable, '-m', 'chainlit', 'run', entry_point)