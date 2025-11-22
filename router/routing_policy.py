from typing import Dict
from .classifier import TaskType
from .dynamic_router import ModelStats

def best_fit_model(stats: Dict[str, Dict[str, ModelStats]]) -> Dict[TaskType, str]:
    routing = {}
    for task_str, model_dict in stats.items():
        best_name, best_stat = None, None
        for name, s in model_dict.items():
            if best_stat is None or s.mean > best_stat.mean:
                best_name, best_stat = name, s
        routing[TaskType(task_str)] = best_name
    return routing