import random
import time
from pathlib import Path
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
from src.auto_flow.config import OUTPUT_DATA_DIR
# Khai báo các biến tĩnh

# Đường dẫn đến kịch bản
b12_path = Path(r'D:\minhlvfile\pythonproject\auto-flow\data\input\scripts\#12.xlsx')
# Đường dẫn style lock
style_lock_path = Path(r'D:\minhlvfile\pythonproject\auto-flow\data\input\style_lock')
# Đường dẫn đến folder chứa prompt kịch bản
output_prompt_path = Path(fr'D:\minhlvfile\pythonproject\auto-flow\data\output\{b12_path.stem}.json')

# Khai báo các dịch vụ

# Khai báo kịch bản
script = Script(b12_path)
# Khai báo prompt_engneer dịch vụ
prompt_engineer = PromptEngineer()
# Khai báo nhà phân tích nội dung
script_analyzer = ScriptAnalyzer()
# Khai báo file services
file_services = FileServices()

# Chuẩn bị dữ liệu

# Nội dung các phân cảnh
scenes = script.content[1:]
# Tóm tắt kịch bản
script.summary = script_analyzer.summary_script(script, GroqModelName.LLAMA_3_1_8B_INSTANT)
# Đọc style lock
style_lock = file_services.read_txt(style_lock_path)

# Chạy thử nhiệm

# Khởi tạo kết quả prompt kịch bản
script_prompt_result = ScriptPromptResult(name=script.name)
# Duyệt phân cảnh tạo prompt
for scene in scenes:
    # Lấy tên phân cảnh là giá trị cột index
    scene_name = scene.get(ScriptColumn.INDEX)
    print(f'{scene_name=}')
    # Khai báo đối tượng kết quả prompt phân cảnh
    scene_prompt_result = ScenePromptResult(name=str(scene_name))
    # Lấy bối cảnh là nội dung phân cảnh
    context = scene.get(ScriptColumn.SCRIPT)
    # Chia thành danh sách câu
    sentences = split_sentences(context)
    # Duyệt danh sách câu
    for sentence in sentences:
        print(f'{sentence=}')
        # Khai báo đối tượng kết quả prompt đơn lẻ cho ảnh
        prompt_image_result = PromptResult(
            sentence=sentence,
            type=PromptResultType.IMAGE,
        )
        try:
            # Tạo prompt ảnh
            image_prompt = prompt_engineer.gen_image_prompt(sentence, context, script.summary, style_lock, GroqModelName.LLAMA_3_1_8B_INSTANT)
            # Gán prompt vào thuộc tính prompt kết quả
            prompt_image_result.prompt = image_prompt
            # Set trạng thái tạo là success
            prompt_image_result.status = PromptResultStatus.SUCCESS
            print(f'{image_prompt=}')
        except Exception as e:
            print(e)
            # Nếu gặp lỗi thì set trạng thái tạo là failed
            prompt_image_result.status = PromptResultStatus.FAILED

        # Dù thành công hay thất bại thì cũng đưa prompt ảnh vừa tạo ra vào kết quả prompt phân cảnh
        scene_prompt_result.prompts.append(prompt_image_result)

        # Khai báo đối tượng kết quả prompt đơn lẻ cho video
        prompt_video_result = PromptResult(
            sentence=sentence,
            type=PromptResultType.VIDEO,
        )

        time.sleep(random.randint(15, 20))

        try:
            # Tạo prompt video
            video_prompt = prompt_engineer.gen_image_prompt(sentence, context, script.summary, style_lock,
                                                            GroqModelName.LLAMA_3_1_8B_INSTANT)
            # Đưa prompt video vào thuộc tính của prompt kết quả
            prompt_video_result.prompt = video_prompt
            # Set trạng thái thành công
            prompt_video_result.status = PromptResultStatus.SUCCESS
            print(f'{video_prompt=}')
        except Exception as e:
            print(e)
            # Lỗi thì set trạng thái thất bại
            prompt_video_result.status = PromptResultStatus.FAILED

        # Dù thất bại hay thành công thì cũng đưa prompt video vừa tạo ra vào kết quả prompt phân cảnh
        scene_prompt_result.prompts.append(prompt_video_result)

        time.sleep(random.randint(15, 20))


    # Đẩy phân cảnh vào kết quả prompt kịch bản
    script_prompt_result.scenes_prompts.append(scene_prompt_result)
    file_services.save_pydantic_json(script_prompt_result, output_prompt_path)

