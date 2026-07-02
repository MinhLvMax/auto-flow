from src.auto_flow.constants.script_columns import ScriptColumn
from src.auto_flow.services.groq_services import groq_services
from src.auto_flow.schemas.script import Script


class ScriptAnalyzer:
    def __init__(self, llm_services = groq_services):
        self.llm_services = llm_services

    def summary_script(self, script: Script, model_name) -> str:
        string_content = ''
        scenes = script.excel_content
        for scene in scenes:
            string_content += scene.get(ScriptColumn.SCRIPT)
        return self.llm_services.summary(string_content, model_name)

    # sau này thiết kế thêm các hàm phân tích tìm nhân vật chính hay cảnh chính thì viết thêm
