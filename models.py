from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    content: str
    task: str

class Action(BaseModel):
    action: str  # simple string (important for logging)

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool