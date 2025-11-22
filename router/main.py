import yaml
from pathlib import Path
import json

from .dynamic_router import DynamicRouter
from .models import load_models
from utils.logger import get_logger

logger = get_logger(__name__)


def load_config():
    with Path("config/routing.yaml").open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_router() -> DynamicRouter:
    cfg = load_config()
    models = load_models("config/models.yaml")
    stats_path = cfg["storage"]["stats_path"]
    exploration = float(cfg["router"].get("exploration", 0.1))
    router = DynamicRouter(models=models, stats_path=stats_path, exploration=exploration)
    return router


# def interactive_cli():
#     router = build_router()
#     print("Interactive router. Type 'exit' to quit.")
#     while True:
#         q = input("Question> ")
#         if q.strip().lower() in {"exit", "quit"}:
#             break
#         result = router.route(q)
#         print(f"[task={result['task_type']}] [model={result['model']}]")
#         print(result["answer"])
#         fb = input("Was this good? (y/n, empty=skip) > ").strip().lower()
#         if fb in {"y", "n"}:
#             from .classifier import TaskType
#             reward = 1.0 if fb == "y" else 0.0
#             router.record_feedback(TaskType(result["task_type"]), result["model"], reward)
def interactive_cli():
    router = build_router()
    print("Interactive router. Type 'exit' to quit.")
    while True:
        q = input("Question> ")
        if q.strip().lower() in {"exit", "quit"}:
            break
        result = router.route(q)

        
        ans = result["answer"]
        if isinstance(ans, bytes):
            ans = ans.decode("utf-8")
        try:
            
            parsed = json.loads(ans)
            
            if isinstance(parsed, dict) and "result" in parsed:
                ans = "\n".join(parsed["result"]).strip()
            else:
                
                ans = json.dumps(parsed, indent=2)
        except (json.JSONDecodeError, TypeError):
            
            pass

        print(f"[task={result['task_type']}] [model={result['model']}]")
        print(ans)

        fb = input("Was this good? (y/n, empty=skip) > ").strip().lower()
        if fb in {"y", "n"}:
            from .classifier import TaskType
            reward = 1.0 if fb == "y" else 0.0
            router.record_feedback(TaskType(result["task_type"]), result["model"], reward)


if __name__ == "__main__":
    interactive_cli()
