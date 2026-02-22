import json
import urllib.request
from typing import Any, Dict, List


def fetch_hf_dataset(dataset: str, config: str, split: str, limit: int = 100) -> List[Dict[str, Any]]:
    url = f"https://datasets-server.huggingface.co/rows?dataset={dataset}&config={config}&split={split}&offset=0&length={limit}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            return [row["row"] for row in data.get("rows", [])]
    except Exception as e:
        print(f"Failed to fetch {dataset}: {e}")
        return []

def load_local_json(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(line.strip()) for line in f]
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        return []
