import json
from typing import Any, Dict, List


def format_metrics(metrics: Dict[str, float]) -> str:
    """Formats a metrics dictionary into a readable string."""
    return f"Precision: {metrics.get('precision', 0):.4f} | Recall: {metrics.get('recall', 0):.4f} | F1: {metrics.get('f1', 0):.4f}"

def serialize_results(filepath: str, data: List[Dict[str, Any]]) -> None:
    """Serializes benchmark results to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
def parse_markdown_table(markdown_str: str) -> List[Dict[str, str]]:
    """Helper to parse markdown tables into Python dictionaries."""
    # Placeholder utility for documentation generation
    pass
