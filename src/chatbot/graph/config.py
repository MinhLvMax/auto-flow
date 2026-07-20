from src.chatbot.services.groq_llm_services import GroqModelName

class WorkFLowConfig:
    CLASSIFICATION_MODEL = GroqModelName.LLAMA_3_1_8B_INSTANT
    NATURAL_CHAT_MODEL = GroqModelName.LLAMA_3_1_8B_INSTANT
    EXTRACT_MODEL = GroqModelName.LLAMA_3_1_8B_INSTANT
    RETRIEVAL_MODEL = GroqModelName.LLAMA_3_1_8B_INSTANT