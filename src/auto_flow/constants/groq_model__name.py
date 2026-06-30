
class GroqModelName:
    COMPOUND = "groq/compound"
    COMPOUND_MINI = "groq/compound-mini"

    LLAMA_3_1_8B_INSTANT = "llama-3.1-8b-instant"
    LLAMA_3_3_70B_VERSATILE = "llama-3.3-70b-versatile"

    GPT_OSS_120B = "openai/gpt-oss-120b"
    GPT_OSS_20B = "openai/gpt-oss-20b"

    WHISPER_LARGE_V3 = "whisper-large-v3"
    WHISPER_LARGE_V3_TURBO = "whisper-large-v3-turbo"

    # Preview
    QWEN3_32B = 'qwen/qwen3-32b'
    QWEN_QWEN3_6_27B = 'qwen/qwen3.6-27b'

    META_LLAMA_LLAMA_4_SCOUT_17B_16E_INSTRUCT = 'meta-llama/llama-4-scout-17b-16e-instruct'
    META_LLAMA_LLAMA_PROMPT_GUARD_2_22M = 'meta-llama/llama-prompt-guard-2-22m'
    META_LLAMA_LLAMA_PROMPT_GUARD_2_86M = 'meta-llama/llama-prompt-guard-2-86m'

    OPENAI_GPT_OSS_SAFEGUARD_20B = 'openai/gpt-oss-safeguard-20b'

if __name__ == '__main__':
    def normalize_text(text: str) -> str:
        """
        Nhận vào một chuỗi.
        Trả về chuỗi viết hoa và thay ký tự đặc biệt bằng dấu cách.
        """
        result = ""

        for char in text:
            if char.isalnum():
                result += char
            else:
                result += "_"

        return result.upper()

    print(normalize_text('openai/gpt-oss-safeguard-20b'))