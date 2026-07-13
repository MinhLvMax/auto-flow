import json
from typing import List, Dict
from groq import Groq
from pathlib import Path


class GroqModelName:
    COMPOUND = "groq/compound"
    COMPOUND_MINI = "groq/compound-mini"

    LLAMA_3_1_8B_INSTANT = "llama-3.1-8b-instant"
    LLAMA_3_3_70B_VERSATILE = "llama-3.3-70b-versatile"

    GPT_OSS_120B = "openai/gpt-oss-120b"
    GPT_OSS_20B = "openai/gpt-oss-20b"

    WHISPER_LARGE_V3 = "whisper-large-v3"
    WHISPER_LARGE_V3_TURBO = "whisper-large-v3-turbo"

    # Preview
    QWEN3_32B = 'qwen/qwen3-32b'
    QWEN_QWEN3_6_27B = 'qwen/qwen3.6-27b'

    META_LLAMA_LLAMA_4_SCOUT_17B_16E_INSTRUCT = 'meta-llama/llama-4-scout-17b-16e-instruct'
    META_LLAMA_LLAMA_PROMPT_GUARD_2_22M = 'meta-llama/llama-prompt-guard-2-22m'
    META_LLAMA_LLAMA_PROMPT_GUARD_2_86M = 'meta-llama/llama-prompt-guard-2-86m'

    OPENAI_GPT_OSS_SAFEGUARD_20B = 'openai/gpt-oss-safeguard-20b'


class GroqServices:
    def __init__(
            self,
            api_key: str
    ):
        self.client = Groq(api_key=api_key)

    def chat(
            self,
            text: str,
            model_name: str,
            system_prompt: str | None = None
    ) -> str:
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": text
        })

        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        return response.choices[0].message.content

    def chat_json(self, text, model_name, system_prompt=''):
        response = self.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt + " Trả về JSON."},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}  # Ép buộc trả về JSON
        )

        return response.choices[0].message.content

    def chat_history(
            self,
            model_name,
            messages: List[Dict[str, str]]
    ) -> str:
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        return response.choices[0].message.content

    # def summary(
    #         self,
    #         text,
    #         model_name,
    # ) -> str:
    #     formatted_prompt = SUMMARIZE_PROMPT.format(content=text)
    #     response = self.chat(formatted_prompt, model_name)
    #     return response


def build_tree(path, max_depth=None, current_depth=0):
    path = Path(path)

    if path.is_file():
        return None

    if max_depth is not None and current_depth >= max_depth:
        return {}

    return {
        child.name: build_tree(child, max_depth, current_depth + 1)
        for child in sorted(path.iterdir())
    }


IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    'profiles',
    '_internal'
}

def build_tree(path, max_depth=None, current_depth=0):
    path = Path(path)

    if path.is_file():
        return None

    if max_depth is not None and current_depth >= max_depth:
        return {}

    tree = {}

    for child in sorted(path.iterdir()):
        # Bỏ qua folder/file không cần thiết
        if child.name in IGNORE_DIRS:
            continue

        tree[child.name] = build_tree(
            child,
            max_depth,
            current_depth + 1
        )

    return tree

def read_json(path):
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def scan_directory(root: str | Path):
    root = Path(root).resolve()
    results = []

    for path in root.rglob("*"):
        # Bỏ qua thư mục không cần
        if any(part in IGNORE_DIRS for part in path.parts):
            continue

        # results.append({
        #     "path": str(path.relative_to(root)),
        #     "name": path.name,
        #     "type": "dir" if path.is_dir() else "file",
        # })

        results.append(str(path.relative_to(root)))
    return results


def system_notification(msg=None, separator_length=80):
    separator = '=' * separator_length
    return separator + '\n' + msg


SYSTEM_PROMPT = """
Bạn là trợ lý AI quản lý kho thư mục, bạn hiểu kiến trúc cây thư mục.

Nhiệm vụ của bạn là hỗ trợ người dùng tra cứu tài nguyên được trong thư mục.

Dữ liệu thư mục mà bạn quản lý: 
{data}
"""

if __name__ == '__main__':

    path = Path(r"C:\Users\Admin\Downloads")
    model_name = GroqModelName.LLAMA_3_1_8B_INSTANT

    TAG_USER = '- Người dùng hỏi: '
    TAG_SYSTEM = '- AI đáp:\n'

    current_file = Path(__file__).resolve()
    print(f'{current_file=}')
    index_file_path = current_file.parent / f'{path.stem}_index.json'
    if not index_file_path.exists():
        print(system_notification('Tiến hành quét nội dung thư mục...'))
        data = scan_directory(path)
        save_json(data, index_file_path)
    data = read_json(index_file_path)
    print(f'{index_file_path=}')
    from pprint import pprint

    pprint(data[:5])
    data = read_json(index_file_path)
    g = GroqServices()
    chat_history = [
        {
            'role': 'system',
            'content': SYSTEM_PROMPT.format(data=data[:100])
        }
    ]
    first_msg = g.chat_history(model_name, chat_history)
    print(system_notification(f'{TAG_SYSTEM} {first_msg}'))
    while True:
        user_input = input(system_notification(TAG_USER))
        if user_input == '':
            break
        chat_history.append({
            'role': 'user',
            'content': user_input
        })
        response = g.chat_history(model_name, chat_history)
        print(system_notification(f'{TAG_SYSTEM} {response}'))
    pass

    # Các lệnh gói
'''
cd src
cd chatbot
pyinstaller --onefile llm1.py
'''
