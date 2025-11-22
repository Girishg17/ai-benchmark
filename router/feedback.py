from dataclasses import dataclass
from typing import Literal
from .classifier import TaskType


@dataclass
class Feedback:
    task: TaskType
    model_name: str
    reward: float     
    source: Literal["user", "benchmark"] = "user"
    comment: str | None = None
