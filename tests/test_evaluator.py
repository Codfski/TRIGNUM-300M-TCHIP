import pytest

from trignum_core.evaluator import Evaluator


def test_evaluator_initialization():
    evaluator = Evaluator()
    assert evaluator.tp == 0
    assert evaluator.fp == 0
    assert evaluator.tn == 0
    assert evaluator.fn == 0

def test_evaluator_metrics_computation():
    evaluator = Evaluator()
    evaluator.record(predicted_illogic=True, actual_hallucination=True)    # TP
    evaluator.record(predicted_illogic=True, actual_hallucination=False)   # FP
    evaluator.record(predicted_illogic=False, actual_hallucination=False)  # TN
    evaluator.record(predicted_illogic=False, actual_hallucination=True)   # FN
    
    metrics = evaluator.compute_metrics()
    assert metrics["precision"] == 0.5   # 1 / (1 + 1)
    assert metrics["recall"] == 0.5      # 1 / (1 + 1)
    assert metrics["f1"] == 0.5
    assert metrics["accuracy"] == 0.5    # (1 + 1) / 4

def test_evaluator_perfect_scores():
    evaluator = Evaluator()
    for _ in range(10):
        evaluator.record(predicted_illogic=True, actual_hallucination=True)   # 10 TP
        evaluator.record(predicted_illogic=False, actual_hallucination=False) # 10 TN
        
    metrics = evaluator.compute_metrics()
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0
    assert metrics["accuracy"] == 1.0
