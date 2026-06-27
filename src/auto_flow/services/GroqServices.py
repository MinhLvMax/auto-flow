from typing import List, Dict
from groq import Groq
import time
import json
from src.auto_flow.config import GROQ_API_KEY

class GroqServices:
    def __init__(
            self,
            api_key: str = GROQ_API_KEY
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


if __name__ == '__main__':
    g = GroqServices()
    r = g.chat("Chào bạn", 'llama-3.1-8b-instant')
    print(r)
    pass
