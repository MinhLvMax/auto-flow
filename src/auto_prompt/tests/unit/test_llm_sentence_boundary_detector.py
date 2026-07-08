import time

from src.auto_prompt.llm.groq import GroqLLM
from src.auto_prompt.extractor.detector.LLMSentenceBoundaryDetector import LLMSentenceBoundaryDetector
from src.auto_prompt.repository.reader.json_reader import JsonReader
from src.auto_prompt.repository.writer.jsonwriter import JsonWriter
from src.auto_prompt.services.sentence_detector_service import SentenceBoundaryService
from src.auto_flow.constants.groq_model__name import GroqModelName
from src.auto_prompt.repository.reader.script_parser.excel_parser import ExcelScriptParser
from src.config import INTERMEDIATE_DATA_DIR, INPUT_DATA_DIR
from pathlib import Path

llm = GroqLLM()
detector = LLMSentenceBoundaryDetector(llm, GroqModelName.LLAMA_3_1_8B_INSTANT)
sentence_detector_service = SentenceBoundaryService(detector)
excel_script_parser = ExcelScriptParser()
reader = JsonReader()
writer = JsonWriter()


script_path = INPUT_DATA_DIR / 'scripts' / '#13.xlsx'
list_script_row = excel_script_parser.parse(script_path)
detected_result_path = INTERMEDIATE_DATA_DIR / 'sentence_detection' / script_path.stem / f'{script_path.stem}.json'

if detected_result_path.exists():
    paragraph_detected_list = reader.parse(detected_result_path)
    start_index = len(paragraph_detected_list)
else:
    paragraph_detected_list = []
    start_index = 0

for row in list_script_row[start_index:]:
    paragraph = row.en
    paragraph_detected = sentence_detector_service.analyze(paragraph)
    print(paragraph_detected)
    paragraph_detected_list.append(paragraph_detected)
    print('Sleeptime...')
    time.sleep(5)
    writer.save(paragraph_detected_list, detected_result_path)
