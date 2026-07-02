from pydantic import BaseModel, ConfigDict
from src.auto_flow.constants.enums.prompt_result_type import PromptResultType
from src.auto_flow.constants.enums.prompt_result_status import PromptResultStatus

class PromptResult(BaseModel):
    sentence: str
    type: PromptResultType
    content: str = None
    status: PromptResultStatus = PromptResultStatus.PENDING

    model_config = ConfigDict(use_enum_values=True)