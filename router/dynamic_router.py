from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List
import math
import random

from .classifier import TaskType, classify_task
from .models import ModelClient
from utils.io import read_json, write_json
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ModelStats:
    successes: float = 0.0
    trials: int = 0

    @property
    def mean(self) -> float:
        if self.trials == 0:
            return 0.0
        return self.successes / self.trials


class DynamicRouter:
    def __init__(
        self,
        models: List[ModelClient],
        stats_path: str,
        exploration: float = 0.1,
        ucb_confidence: float = 2.0,
    ):
        self.models: Dict[str, ModelClient] = {m.name: m for m in models}
        self.stats_path = stats_path
        self.exploration = exploration
        self.ucb_confidence = ucb_confidence
        self.stats: Dict[str, Dict[str, ModelStats]] = self._load_stats()

        
        for t in TaskType:
            self.stats.setdefault(t.value, {})
            for name in self.models:
                self.stats[t.value].setdefault(name, ModelStats())

    def _load_stats(self) -> Dict[str, Dict[str, ModelStats]]:
        raw = read_json(self.stats_path, default={})
        stats: Dict[str, Dict[str, ModelStats]] = {}
        for task_str, model_dict in raw.items():
            stats[task_str] = {}
            for model_name, v in model_dict.items():
                stats[task_str][model_name] = ModelStats(
                    successes=float(v.get("successes", 0.0)),
                    trials=int(v.get("trials", 0)),
                )
        return stats

    def _save_stats(self):
        out = {}
        for task_str, model_dict in self.stats.items():
            out[task_str] = {
                m: {"successes": s.successes, "trials": s.trials}
                for m, s in model_dict.items()
            }
        write_json(self.stats_path, out)

    def register_model(self, model: ModelClient, initial_score: float = 0.5):
        logger.info(f"Registering new model: {model.name}")
        self.models[model.name] = model
        for t in TaskType:
            task_key = t.value
            self.stats.setdefault(task_key, {})
            if model.name not in self.stats[task_key]:
                self.stats[task_key][model.name] = ModelStats(
                    successes=2.0 * initial_score,
                    trials=2,
                )
        self._save_stats()

    def _total_trials_for_task(self, task_key: str) -> int:
        return sum(stat.trials for stat in self.stats[task_key].values())

    def _ucb_score(self, mean: float, trials: int, total_trials: int) -> float:
        if trials == 0:
            
            return float("inf")
        return mean + self.ucb_confidence * math.sqrt(math.log(max(total_trials,1)) / trials)

    def _choose_model_for_task(self, task: TaskType) -> ModelClient:
        task_key = task.value
        task_stats = self.stats.setdefault(task_key, {})

        
        available_models = [m for m in self.models.values() if task in m.strengths]

        
        for m in available_models:
            task_stats.setdefault(m.name, ModelStats())

        total_trials = self._total_trials_for_task(task_key)

        # Epsilon-greedy exploration
        if random.random() < self.exploration:
            model = random.choice(available_models)
            logger.info(f"[EXPLORE] Chose model={model.name} for task={task_key}")
            return model

        # UCB 
        best_model = None
        best_score = -float("inf")
        for model in available_models:
            stat = task_stats[model.name]
            score = self._ucb_score(stat.mean, stat.trials, total_trials)
            if score > best_score:
                best_score = score
                best_model = model

        logger.info(f"[UCB] Chose model={best_model.name} (score={best_score:.3f}) for task={task_key}")
        return best_model

    def route(self, question: str, **opts) -> Dict[str, Any]:
        task = classify_task(question)
        model = self._choose_model_for_task(task)
        answer = model(question, **opts)
        return {
            "task_type": task.value,
            "model": model.name,
            "answer": answer,
        }

    def record_feedback(self, task: TaskType, model_name: str, reward: float):
        task_key = task.value
        self.stats.setdefault(task_key, {})
        stat = self.stats[task_key].setdefault(model_name, ModelStats())
        stat.trials += 1
        stat.successes += float(reward)
        logger.info(f"Feedback for task={task_key}, model={model_name}: reward={reward}, mean={stat.mean:.3f}")
        self._save_stats()
