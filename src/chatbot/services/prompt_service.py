from pathlib import Path
from src.config import BASE_DIR

class PromptService:
    default_prompt_dir = BASE_DIR / 'src' / 'chatbot' / 'prompts'

    def __init__(self, prompt_dir = None):
        self.prompt_dir = Path(prompt_dir or self.default_prompt_dir)
        self.cache = {}

    def render(self, name, **kwargs):

        if name not in self.cache:
            path = self.prompt_dir / f"{name}.txt"
            self.cache[name] = path.read_text("utf-8-sig")

        return self.cache[name].format(**kwargs)