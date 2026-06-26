import subprocess
from scripts.git.schemas.command_manager import command_manager
from src.auto_flow.config import BASE_DIR
from pathlib import Path

class CommandRunner:
    def __init__(self, command_manager = command_manager, cwd=BASE_DIR):
        self.cwd = cwd
        self.command_manager = command_manager

    def run(self, cmd, **kwargs):
        return subprocess.run(cmd, cwd=self.cwd, check=True, **kwargs)

    def freeze_requirements(self):
        with open(Path(self.cwd) / "requirements.txt", "w", encoding='utf-8') as f:
            self.run(self.command_manager.pip_freeze, stdout=f)

command_runner = CommandRunner()

__all__ = ['command_runner']