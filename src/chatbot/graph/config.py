from src.chatbot.services.groq_llm_services import GroqModelName


class WorkFLowConfig:
    CLASSIFICATION_MODEL = GroqModelName.LLAMA_3_1_8B_INSTANT #json
    NATURAL_CHAT_MODEL = GroqModelName.COMPOUND_MINI
    EXTRACT_MODEL = GroqModelName.GPT_OSS_20B #json
    RETRIEVAL_MODEL = GroqModelName.GPT_OSS_120B
