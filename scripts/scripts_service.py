import subprocess
from pathlib import Path

from src.config import BASE_DIR


class ScriptService:

    def __init__(self, workdir = None):
        self.workdir = Path(workdir) if workdir else BASE_DIR

        self.git_status = ["git", "-c", "color.status=always", "status"]
        self.git_pull = ["git", "pull"]
        self.git_push = ["git", "push"]
        self.git_add_all = ["git", "add", "."]
        self.git_commit = ["git", "commit", "-m"]
        self.git_log = ["git", "log", "--oneline", "-10"]

        self.install_requirements = [
            "python",
            "-m",
            "pip",
            "install",
            "-r",
            BASE_DIR / "requirements.txt",
        ]

        self.freeze_requirements = [
            "python",
            "-m",
            "pip",
            "freeze",
        ]

    def _run(self, command: list[str]) -> str:
        result = subprocess.run(
            command,
            cwd=self.workdir,
            text=True,
            # capture_output=True,
            check=False,
        )

        if result.returncode != 0:
            return result.stderr

        return result.stdout

    # ---------- Git ----------

    def cmd_git_status(self):
        return self._run(self.git_status)

    def cmd_git_pull(self):
        return self._run(self.git_pull)

    def cmd_git_push(self):
        return self._run(self.git_push)

    def cmd_git_add_all(self):
        return self._run(self.git_add_all)

    def cmd_git_commit(self, message: str):
        return self._run(
            self.git_commit + [message]
        )

    def cmd_git_log(self):
        return self._run(self.git_log)

    # ---------- Requirements ----------

    def cmd_install_requirements(self):
        return self._run(
            self.install_requirements
        )

    def cmd_freeze_requirements(self):
        return self._run(
            self.freeze_requirements
        )
