from pathlib import Path

class PromptService:

    def __init__(self, prompt_dir = None):
        self.prompt_dir = Path(prompt_dir) or Path('../prompts')
        self.cache = {}

    def render(self, name, **kwargs):

        if name not in self.cache:
            path = self.prompt_dir / f"{name}.txt"
            self.cache[name] = path.read_text("utf-8-sig")

        return self.cache[name].format(**kwargs)