from src.auto_prompt.llm.groq import GroqLLM
from src.auto_prompt.extractor.detector.LLMSentenceBoundaryDetector import LLMSentenceBoundaryDetector
from src.auto_prompt.services.sentence_detector_service import SentenceBoundaryService
from src.auto_flow.constants.groq_model__name import GroqModelName
from src.auto_prompt.script.reader.excel_parser import ExcelScriptParser

llm = GroqLLM()
detector = LLMSentenceBoundaryDetector(llm, GroqModelName.LLAMA_3_1_8B_INSTANT)
sentence_detector_service = SentenceBoundaryService(detector)
excel_script_parser = ExcelScriptParser()

script_path = r'D:\projects\auto-flow\data\input\scripts\#13.xlsx'
list_script_row = excel_script_parser.parse(script_path)
# print(list_script_row)

for row in list_script_row:
    paragraph = row.en
    data = sentence_detector_service.analyze(paragraph)
    print(data)
    break
