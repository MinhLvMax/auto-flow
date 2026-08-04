import pprint
from pydantic import BaseModel
from groq import Groq
from typing import TypeVar
from src.agent_search.application.logger_service import LoggerService

T = TypeVar("T", bound=BaseModel)  # T là kiểu bất kì nhưng phải kế thừa BaseModel


class GroqLLM:
    def __init__(
        self,
        api_key,
        default_model="openai/gpt-oss-20b",
        logger: LoggerService | None = None,
    ):
        self.api_key = api_key
        self.default_model = default_model
        self.client = Groq(api_key=api_key)
        self.logger = logger

    def complete(
        self,
        messages: list[dict] | str,
        llm_model: str | None = None,
        response_model: type[T] | None = None,
    ) -> str | T:
        self.logger.info(f"{self.__class__.__name__}.{self.complete.__name__}")

        if llm_model is None:
            llm_model = self.default_model

        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        kwargs = {}
        if response_model is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "schema": response_model.model_json_schema(),
                },
            }

        response = self.client.chat.completions.create(
            model=llm_model or self.default_model,
            messages=messages,
            **kwargs,
        )

        content = response.choices[0].message.content

        if response_model is None:
            return content

        return response_model.model_validate_json(content)
