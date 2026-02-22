"""
Metrics accuracy calculation utilities (Level 2 Extension placeholder).
"""
from typing import Dict


def compute_f1_score(precision: float, recall: float) -> float:
    """Computes F1 score from precision and recall."""
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def calculate_accuracy_matrix(tp: int, fp: int, tn: int, fn: int) -> Dict[str, float]:
    """Calculates all essential classification metrics."""
    total = tp + fp + tn + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = compute_f1_score(precision, recall)
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }
