from pydantic import BaseModel

class State(BaseModel):
    user_input: str | None = None
    sustem_output: str | None = None
    classification_results: dict | None = None