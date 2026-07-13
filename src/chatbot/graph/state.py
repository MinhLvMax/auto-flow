from pydantic import BaseModel

class State(BaseModel):
    user_input: str
    sustem_output: str