from dataclasses import dataclass
from typing import List
from pathlib import Path
import json

from router.classifier import TaskType


@dataclass
class BenchmarkSample:
    question: str
    task: TaskType
    reference: str


def load_jsonl(path: str) -> List[BenchmarkSample]:
    p = Path(path)
    if not p.exists():
        return []
    samples: List[BenchmarkSample] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            samples.append(
                BenchmarkSample(
                    question=obj["question"],
                    task=TaskType(obj["task"]),
                    reference=obj["reference"],
                )
            )
    return samples
