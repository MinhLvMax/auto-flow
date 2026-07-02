import random
import time
from src.auto_flow.constants.enums.prompt_result_status import PromptResultStatus
from src.auto_flow.constants.enums.prompt_result_type import PromptResultType
from src.auto_flow.constants.groq_model__name import GroqModelName
from src.auto_flow.constants.script_columns import ScriptColumn
from src.auto_flow.services.file_services import FileServices
from src.auto_flow.services.prompt_engineer import PromptEngineer
from src.auto_flow.services.script_analyzer import ScriptAnalyzer
from src.auto_flow.schemas.prompt_result import PromptResult
from src.auto_flow.schemas.scene_prompt_result import ScenePromptResult
from src.auto_flow.schemas.script_prompt_result import ScriptPromptResult
from src.auto_flow.schemas.script import Script
from src.auto_flow.utils.helpers import split_sentences
from src.auto_flow.config import OUTPUT_DATA_DIR, INPUT_DATA_DIR

class PromptFlow:
    def __init__(self, script_path, style_lock_path):
        self.script_path = script_path
        self.output_prompt_path = OUTPUT_DATA_DIR / f'{script_path.stem}.json'
        self.summary_model_name = GroqModelName.LLAMA_3_1_8B_INSTANT
        self.gen_image_model_name = GroqModelName.META_LLAMA_LLAMA_4_SCOUT_17B_16E_INSTRUCT
        self.gen_video_model_name = GroqModelName.META_LLAMA_LLAMA_4_SCOUT_17B_16E_INSTRUCT
        self.script = Script(script_path)
        self.prompt_file_dir = OUTPUT_DATA_DIR / script_path.stem
        self.prompt_file_dir.mkdir(parents=True, exist_ok=True)
        # Khai báo prompt_engneer dịch vụ
        self.prompt_engineer = PromptEngineer()
        # Khai báo nhà phân tích nội dung
        self.script_analyzer = ScriptAnalyzer()
        # Khai báo file services
        self.file_services = FileServices()
        self.style_lock = self.file_services.read_txt(style_lock_path)
        pass

    def run(self, start_scene_idx, end_scene_idx):
        self.script.summary = self.script_analyzer.summary_script(self.script, self.summary_model_name)
        scenes = self.script.excel_content[start_scene_idx:end_scene_idx]

        # Khởi tạo kết quả prompt kịch bản
        script_prompt_result = ScriptPromptResult(script_name=self.script.name)
        # Duyệt phân cảnh tạo prompt
        for scene in scenes:
            # Lấy tên phân cảnh là giá trị cột index
            scene_name = scene.get(ScriptColumn.INDEX)
            print(f'{scene_name=}')
            # Khai báo đối tượng kết quả prompt phân cảnh
            scene_prompt_result = ScenePromptResult(scene_name=str(scene_name))
            # Lấy bối cảnh là nội dung phân cảnh
            context = scene.get(ScriptColumn.SCRIPT)
            # Chia thành danh sách câu
            sentences = split_sentences(context)
            # Duyệt danh sách câu
            for sentence in sentences:
                print(f'{sentence=}')

                pari_prompt = self.prompt_engineer.gen_pair_prompt(sentence=sentence,
                                                                   context=context,
                                                                   script_summary=self.script.summary,
                                                                   style_lock=self.style_lock,
                                                                   gen_image_model_name=self.gen_image_model_name,
                                                                   gen_video_model_name=self.gen_video_model_name)
                scene_prompt_result.pairs_prompts.append(pari_prompt)

                output_path = self.prompt_file_dir / f'{scene_name}.json'
                print(f'{output_path=}')
                self.file_services.save_pydantic_json(scene_prompt_result, output_path)

                # Dừng 30 giây
                sleep_time = 30
                for remaining in range(sleep_time, 0, -1):
                    print(f"Còn {remaining} giây...")
                    time.sleep(1)

if __name__ == '__main__':
    # Đường dẫn đến kịch bản
    script_path = INPUT_DATA_DIR / 'scripts' / '#13.xlsx'
    # Đường dẫn style lock
    style_lock_path = INPUT_DATA_DIR / 'style_lock.txt'
    pflow = PromptFlow(script_path=script_path, style_lock_path=style_lock_path)
    pflow.run(0,2)