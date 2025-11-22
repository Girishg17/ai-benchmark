from pathlib import Path
from router.dynamic_router import DynamicRouter, ModelStats
from router.models import load_models
from benchmark.offline_bench import run_offline_benchmark
from utils.io import write_json
import yaml


def main():
   
    with Path("config/routing.yaml").open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    stats_path = cfg["storage"]["stats_path"]


    data_paths = [
        "benchmark/data/coding.jsonl",
        "benchmark/data/math.jsonl",
        "benchmark/data/reasoning.jsonl",
        "benchmark/data/general.jsonl",
        "benchmark/data/image_generation.jsonl",
    ]

    stats = run_offline_benchmark(data_paths)


    out = {}
    for task_key, model_dict in stats.items():
        out[task_key] = {
            name: {"successes": s.successes, "trials": s.trials}
            for name, s in model_dict.items()
        }
    write_json(stats_path, out)


    models = load_models("config/models.yaml")
    router = DynamicRouter(models, stats_path=stats_path, exploration=0.1)
    print("Offline benchmark completed; router stats initialized.")


if __name__ == "__main__":
    main()
