from typing import Dict, List
from tqdm import tqdm

from router.models import load_models
from router.classifier import TaskType
from router.dynamic_router import ModelStats
from .dataset import load_jsonl, BenchmarkSample
from .metrics import  always_true, numeric_match, relaxed_match


def run_offline_benchmark(data_paths: List[str]) -> Dict[str, Dict[str, ModelStats]]:
    models = load_models("config/models.yaml")
    stats: Dict[str, Dict[str, ModelStats]] = {}

    all_samples: List[BenchmarkSample] = []
    for path in data_paths:
        all_samples.extend(load_jsonl(path))

    for sample in tqdm(all_samples, desc="Benchmarking"):
        for m in models:
            pred = m(sample.question)

            eval_method = getattr(sample, "eval", "exact")
            if eval_method == "numeric":
                score = numeric_match(sample.reference, pred)
            elif eval_method == "relaxed":
                score = relaxed_match(sample.reference, pred)
            elif eval_method == "auto_pass":
                score = True
            else:
                score = always_true(sample.reference, pred)

            task_key = sample.task.value
            stats.setdefault(task_key, {})
            s = stats[task_key].setdefault(m.name, ModelStats())
            s.trials += 1
            s.successes += score
        

    return stats
