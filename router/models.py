from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List
import yaml

from .classifier import TaskType

import http.client
import json



import os
from openai import OpenAI

# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

@dataclass
class ModelClient:
    name: str
    call_fn: Callable[[str, Dict[str, Any]], str]
    strengths: List[TaskType]
    cost: float = 1.0
    provider: str = "dummy"

    def __call__(self, prompt: str, **opts) -> str:
        return self.call_fn(prompt, opts)




# def call_openai_gpt4(prompt: str, opts: Dict[str, Any]) -> str:
#     response = client.chat.completions.create(
#         model="gpt-4o",  # or "gpt-4.1" depending on your model list
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=512,
#         temperature=0.7,
#     )
#     return response.choices[0].message.content.strip()

def call_openai_gpt4(prompt: str, opts: Dict[str, Any]) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def call_rapid_api(prompt: str, opts: Dict[str, Any] = {}) -> str:
    conn = http.client.HTTPSConnection(
        "chatgpt-42.p.rapidapi.com"
    )

    payload = json.dumps({
        "text": prompt
        })

    

    headers = {
    'x-rapidapi-key': "395871067emshf9082b1d8a615bbp1da357jsn28416e7a4c3c",
    'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
    'Content-Type': "application/json"
}

    conn.request("POST", "/aitohuman", payload, headers)

    res = conn.getresponse()
    data = res.read()
    # print(data)
    return data


def image_generation(prompt: str, opts: Dict[str, Any] = {}) -> bytes:
    conn = http.client.HTTPSConnection(
        "chatgpt-42.p.rapidapi.com"
    )

    payload = json.dumps({
        "text": prompt,
        "width":512,"height":512
        })

    

    headers = {
    'x-rapidapi-key': "395871067emshf9082b1d8a615bbp1da357jsn28416e7a4c3c",
    'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
    'Content-Type': "application/json"
    }

    conn.request("POST", "/texttoimage", payload, headers)

    res = conn.getresponse()
    data = res.read()
    # print(data)
    return data

def call_per_plexity_ai(prompt: str, opts: Dict[str, Any]) -> str:
    conn = http.client.HTTPSConnection("perplexity2.p.rapidapi.com")

    payload = json.dumps({
        "content": prompt
        })

    headers = {
    'x-rapidapi-key': "395871067emshf9082b1d8a615bbp1da357jsn28416e7a4c3c",
    'x-rapidapi-host': "perplexity2.p.rapidapi.com",
    'Content-Type': "application/json"
}
    conn.request("POST", "/", payload, headers)

    res = conn.getresponse()
    raw_data = res.read().decode("utf-8")
    data = json.loads(raw_data)
    print( data["choices"]["content"]["parts"][0]["text"])
    return data["choices"]["content"]["parts"][0]["text"]




_PROVIDER_FN = {
    "openai": {
        "openai-gpt4": call_rapid_api,
        "image_gen": image_generation,
    },
    "perplexity": {
        "perplexity-ai": call_per_plexity_ai,  
    }

}


def _load_yaml(path: str):
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_models(config_path: str) -> List[ModelClient]:
    cfg = _load_yaml(config_path)
    models_cfg = cfg.get("models", [])
    models: List[ModelClient] = []

    for m in models_cfg:
        name = m["name"]
        provider = m.get("provider")
        strengths = [TaskType(s) for s in m.get("strengths", [])]
        cost = float(m.get("cost", 1.0))

        call_fn = _PROVIDER_FN.get(provider, {}).get(name)
        if call_fn is None:
            raise ValueError(f"No call_fn registered for provider={provider}, name={name}")

        models.append(
            ModelClient(
                name=name,
                call_fn=call_fn,
                strengths=strengths,
                cost=cost,
                provider=provider,
            )
        )
    return models