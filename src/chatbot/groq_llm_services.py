from groq import Groq

from src.chatbot.llm.base import BaseLLMService


class GroqServices(BaseLLMService):
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
            messages: list[dict[str, str]]
    ) -> str:
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        return response.choices[0].message.content
