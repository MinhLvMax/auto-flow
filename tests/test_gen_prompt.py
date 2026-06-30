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

# Khai báo các biến tĩnh

# Đường dẫn đến kịch bản
b12_path = INPUT_DATA_DIR / 'scripts' / '#13.xlsx'
# Đường dẫn style lock
style_lock_path = INPUT_DATA_DIR / 'style_lock.txt'

# Đường dẫn đến folder chứa prompt kịch bản
output_prompt_path = OUTPUT_DATA_DIR / f'{b12_path.stem}.json'
summary_model_name = GroqModelName.LLAMA_3_1_8B_INSTANT
gen_image_model_name = GroqModelName.META_LLAMA_LLAMA_4_SCOUT_17B_16E_INSTRUCT
gen_video_model_name = GroqModelName.META_LLAMA_LLAMA_4_SCOUT_17B_16E_INSTRUCT

# Khai báo các dịch vụ

# Khai báo kịch bản
script = Script(b12_path)
# Tạo thư mục kết quả dựa trên tên kịch bản
prompt_file_dir = OUTPUT_DATA_DIR / b12_path.stem
prompt_file_dir.mkdir(parents=True, exist_ok=True)
# Khai báo prompt_engneer dịch vụ
prompt_engineer = PromptEngineer()
# Khai báo nhà phân tích nội dung
script_analyzer = ScriptAnalyzer()
# Khai báo file services
file_services = FileServices()

# Chuẩn bị dữ liệu

# Nội dung các phân cảnh
start_scene = 5  # Lấy con số này trừ đi 2 sẽ ra phân cảnh bắt đầu thật sự
# end_scene = len(script.content)
end_scene = start_scene + 1

scenes = script.content[start_scene:end_scene]

# Tóm tắt kịch bản
script.summary = script_analyzer.summary_script(script, summary_model_name)
# Đọc style lock
style_lock = file_services.read_txt(style_lock_path)

# Chạy thử nhiệm

# Khởi tạo kết quả prompt kịch bản
script_prompt_result = ScriptPromptResult(script_name=script.name)
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
        # Khai báo đối tượng kết quả prompt đơn lẻ cho ảnh
        prompt_image_result = PromptResult(
            sentence=sentence,
            type=PromptResultType.IMAGE,
        )
        try:
            # Tạo prompt ảnh
            image_prompt = prompt_engineer.gen_image_prompt(sentence, context, script.summary, style_lock,
                                                            gen_image_model_name)
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
        scene_prompt_result.prompt_result.append(prompt_image_result)

        # Khai báo đối tượng kết quả prompt đơn lẻ cho video
        prompt_video_result = PromptResult(
            sentence=sentence,
            type=PromptResultType.VIDEO,
        )

        time.sleep(random.randint(15, 20))

        try:
            # Tạo prompt video
            video_prompt = prompt_engineer.gen_video_prompt(image_prompt=prompt_image_result.prompt, sentence=sentence,
                                                            context=context, script_summary=script.summary,
                                                            style_lock=style_lock,
                                                            model_name=gen_video_model_name)
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
        scene_prompt_result.prompt_result.append(prompt_video_result)

        time.sleep(random.randint(15, 20))

        output_path = prompt_file_dir / f'{scene_name}.json'
        print(f'{output_path=}')
        file_services.save_pydantic_json(scene_prompt_result, output_path)

    # Đẩy phân cảnh vào kết quả prompt kịch bản
    # script_prompt_result.scene_prompt_result.append(scene_prompt_result)
    # file_services.save_pydantic_json(script_prompt_result, output_prompt_path)
