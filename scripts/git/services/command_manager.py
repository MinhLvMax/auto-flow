class CommandManager:
    def __init__(self):
        self.git_status = ["git", "-c", "color.status=always", "status"]
        self.git_add = ["git", "add", "."]
        self.git_pull = ["git", "pull"]
        self.git_push = ["git", "push"]
        self.git_log = ["git", "log"]

        self.pip_freeze = ["pip", "freeze"]
        pass

    @staticmethod
    def git_commit(message: str):
        return ["git", "commit", "-m", message]

command_manager = CommandManager()

__all__ = ['command_manager']