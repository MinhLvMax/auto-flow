from src.auto_flow.services.groq_services import groq_services
from src.auto_flow.constants.string_format.prompt_format import GEN_IMAGE_PROMPT, GEN_VIDEO_PROMPT


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
    ) -> str:
        prompt = GEN_IMAGE_PROMPT.format(
            sentence=sentence,
            context=context,
            script_summary=script_summary,
            style_lock=style_lock,
        )
        return self.llm_services.chat(prompt, model_name).strip()

    def gen_video_prompt(
            self,
            image_prompt: str,
            sentence: str,
            context: str,
            script_summary: str,
            style_lock: str,
            model_name: str,
    ) -> str:
        prompt = GEN_VIDEO_PROMPT.format(
            image_prompt=image_prompt,
            sentence=sentence,
            context=context,
            script_summary=script_summary,
            style_lock=style_lock,
        )

        return self.llm_services.chat(prompt, model_name).strip()

if __name__ == '__main__':
    pass
