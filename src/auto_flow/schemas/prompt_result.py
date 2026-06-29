from pydantic import BaseModel
from src.auto_flow.constants.enums.prompt_result_type import PromptResultType
from src.auto_flow.constants.enums.prompt_result_status import PromptResultStatus

class PromptResult(BaseModel):
    sentence: str
    type: PromptResultType
    prompt: str = None
    status: PromptResultStatus = PromptResultStatus.PENDING