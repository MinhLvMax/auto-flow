from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.config import INDEXED_DATA_PATH
from src.chatbot.services.groq_llm_services import GroqServices

class StorageAnalysisService:
    '''
    Cung cấp các cơ chế phân tích kho
    '''
    def __init__(self, indexed_path: None, json_loader = None, llm_service = None):
        self.indexed_path = indexed_path or INDEXED_DATA_PATH
        self.json_loader = json_loader or JsonReader()
        self.llm_service = llm_service or GroqServices()







