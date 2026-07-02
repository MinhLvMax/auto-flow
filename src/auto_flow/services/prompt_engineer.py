from constants.enums.prompt_result_status import PromptResultStatus
from constants.enums.prompt_result_type import PromptResultType
from src.auto_flow.schemas.pair_prompt import PairPromptResult
from src.auto_flow.schemas.prompt_result import PromptResult
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

    def gen_image_prompt_result_obj(self, sentence, context, script_summary, style_lock,
                                    gen_image_model_name) -> PromptResult:
        print(f'{sentence=}')
        # Khai báo đối tượng kết quả prompt đơn lẻ cho ảnh
        prompt_result = PromptResult(
            sentence=sentence,
            type=PromptResultType.IMAGE,
        )
        try:
            # Tạo prompt ảnh
            image_prompt = self.gen_image_prompt(sentence, context, script_summary, style_lock,
                                                 gen_image_model_name)
            # Gán prompt vào thuộc tính prompt kết quả
            prompt_result.content = image_prompt
            # Set trạng thái tạo là success
            prompt_result.status = PromptResultStatus.SUCCESS
            print(f'{image_prompt=}')
        except Exception as e:
            print(e)
            # Nếu gặp lỗi thì set trạng thái tạo là failed
            prompt_result.status = PromptResultStatus.FAILED
        return prompt_result

    def gen_video_prompt_result_obj(self,
                                    image_prompt: str,
                                    sentence: str,
                                    context: str,
                                    script_summary: str,
                                    style_lock: str,
                                    model_name: str, ) -> PromptResult:

        # Khai báo đối tượng kết quả prompt đơn lẻ cho video
        prompt_result = PromptResult(
            sentence=sentence,
            type=PromptResultType.VIDEO,
        )

        try:
            # Tạo prompt video
            video_prompt = self.gen_video_prompt(image_prompt=image_prompt, sentence=sentence,
                                                 context=context, script_summary=script_summary,
                                                 style_lock=style_lock,
                                                 model_name=model_name)
            # Đưa prompt video vào thuộc tính của prompt kết quả
            prompt_result.content = video_prompt
            # Set trạng thái thành công
            prompt_result.status = PromptResultStatus.SUCCESS
            print(f'{video_prompt=}')
        except Exception as e:
            print(e)
            # Lỗi thì set trạng thái thất bại
            prompt_result.status = PromptResultStatus.FAILED
        return prompt_result

    def gen_pair_prompt(self, sentence, context, script_summary, style_lock,
                        gen_image_model_name, gen_video_model_name) -> PairPromptResult:
        image_prompt = self.gen_image_prompt_result_obj(sentence, context, script_summary, style_lock,
                                                        gen_image_model_name)
        video_prompt = self.gen_video_prompt_result_obj(image_prompt.content, sentence, context, script_summary,
                                                        style_lock, gen_video_model_name)
        pair_prompt = PairPromptResult()
        pair_prompt.image_prompt = image_prompt
        pair_prompt.video_prompt = video_prompt
        return pair_prompt


if __name__ == '__main__':
    pass
