from scripts.git.services.command_runner import command_runner
from datetime import datetime

command_runner.freeze_requirements()

user_commit = input("Nhập commit code: ")
if not user_commit:
    user_commit = datetime.now().strftime("Auto commit %Y-%m-%d %H:%M:%S")

command_runner.run(command_runner.command_manager.git_add)
command_runner.run(command_runner.command_manager.git_commit(user_commit))