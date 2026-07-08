from groq import Groq
from src.config import GROQ_API_KEY
from src.auto_prompt.llm.base import LLM
from pydantic import BaseModel
from src.auto_prompt.constant.prompt_format import JSON_RESPONSE_PROMPT


class GroqLLM(LLM):
    def __init__(self, api_key: str = GROQ_API_KEY):
        super().__init__()
        self.api_key = api_key
        self.client = Groq(api_key=api_key)

    def chat(
            self,
            text: str,
            model_name: str,
            system_prompt: str | None = None,
            response_format: dict | None = None
    ) -> str:
        kwargs = {}
        if response_format is not None:
            kwargs["response_format"] = response_format
        messages = []
        self.client = Groq(api_key=self.api_key)
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
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

    def chat_json(
            self,
            text: str,
            model_name: str,
            response_model: type[BaseModel],
            system_prompt: str | None = None
    ) -> BaseModel:
        schemas_describle = {
            field_name: field_info.description
            for field_name, field_info in response_model.model_fields.items()
        }
        prompt = JSON_RESPONSE_PROMPT.format(text=text, schema=schemas_describle)
        response = self.chat(prompt, model_name, system_prompt, {'type': 'json_object'})
        return response_model.model_validate_json(response)
