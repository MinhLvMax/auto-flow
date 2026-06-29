from enum import StrEnum


class PromptResultStatus(StrEnum):
    PENDING = "pending"   # chưa
    SUCCESS = "success"   # thành công
    FAILED = "failed"     # thất bại