from src.auto_flow.schemas.prompt import Prompt
from src.auto_flow.services.groq_services import groq_services
from src.auto_flow.constants.string_format.prompt_format import GEN_IMAGE_PROMPT


class PromptEngineer:
    def __init__(self, llm_services=groq_services):
        self.llm_services = llm_services
        pass

    def gen_image_prompt(
            self,
            sentence: str,
            context: str,
            script_summary: str,
            style_lock: str,
            model_name: str
    ) -> Prompt:
        prompt = GEN_IMAGE_PROMPT.format(
            sentence=sentence,
            context=context,
            script_summary=script_summary,
            style_lock=style_lock,
            schema=Prompt.get_llm_schema(),
        )

        return self.llm_services.chat_json(prompt, model_name)

if __name__ == '__main__':
    pass
