from groq import Groq
from pydantic import BaseModel
from src.chatbot.text_reader import TextReader
from src.chatbot.services.prompt_service import PromptService
from src.config import GROQ_API_KEY


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
            api_key: str = None,
            prompt_services = None,
    ):
        self.api_key = api_key or GROQ_API_KEY
        self.client = Groq(api_key=self.api_key)
        self.prompt_service = prompt_services or PromptService()

    def chat(
            self,
            text: str,
            model_name: str = GroqModelName.LLAMA_3_1_8B_INSTANT,
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

    def chat_json(
            self,
            text: str,
            response_model: type[BaseModel],
            model_name: str = GroqModelName.LLAMA_3_1_8B_INSTANT,
            system_prompt: str | None = None
    ) -> BaseModel:
        schemas_describle = {
            field_name: field_info.description
            for field_name, field_info in response_model.model_fields.items()
        }
        prompt = self.prompt_service.render('json_output', text=text, schema=schemas_describle)
        response = self.chat(prompt, model_name, system_prompt, {'type': 'json_object'})
        return response_model.model_validate_json(response)

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
