from src.auto_prompt.repository.reader.script_parser.excel_parser import ExcelScriptParser

path = r'D:\projects\auto-flow\data\input\scripts\#13.xlsx'
esp = ExcelScriptParser()
data = esp.parse(path)
from pprint import pprint
pprint(data)