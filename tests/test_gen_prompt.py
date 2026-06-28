from pathlib import Path
from src.auto_flow.services.file_services import FileServices
from src.auto_flow.services.prompt_engineer import PromptEngineer
from src.auto_flow.services.script_analyzer import ScriptAnalyzer
from src.auto_flow.schemas.script import Script
from src.auto_flow.utils.helpers import split_sentences
from src.auto_flow.constants.groq_model__name import GroqModelName

# Khai báo các biến tĩnh

# Đường dẫn đến kịch bản
b12_path = Path(r'D:\projects\auto-flow\data\input\scripts\#12.xlsx')
# Đường dẫn style lock
style_lock_path = Path(r'D:\projects\auto-flow\data\input\style_lock.txt')

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

# Duyệt phân cảnh tạo prompt
for scene in scenes:
    # Lấy nội dung phân cảnh
    context = scene.get('DỊCH')
    # Chia thành danh sách câu
    sentences = split_sentences(context)
    # Duyệt danh sách câu
    for sentence in sentences:
        image_prompt = prompt_engineer.gen_image_prompt(sentence, context, script.summary, style_lock, GroqModelName.LLAMA_3_1_8B_INSTANT)
        print(image_prompt)
        breakpoint()
