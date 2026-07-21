from scripts.run_cmd_method import run

entry_point = 'main.py' # sửa nếu có thay đổi entry point
run('python', '-m', 'chainlit', 'run', entry_point)