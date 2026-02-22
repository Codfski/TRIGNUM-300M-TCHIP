from dataclasses import dataclass
from typing import List


@dataclass
class EvalResult:
    dataset: str
    tp: int
    fp: int
    tn: int
    fn: int
    precision: float
    recall: float
    f1: float
    accuracy: float

class Evaluator:
    @staticmethod
    def compute_metrics(tp: int, fp: int, tn: int, fn: int) -> EvalResult:
        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-9)
        accuracy = (tp + tn) / max(tp + tn + fp + fn, 1)
        return EvalResult("unknown", tp, fp, tn, fn, precision, recall, f1, accuracy)
