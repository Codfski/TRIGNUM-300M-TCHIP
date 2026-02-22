from trignum_core.evaluator import Evaluator
from trignum_core.subtractive_filter import SubtractiveFilter


def run_preflight(samples):
    sf = SubtractiveFilter()
    tp = fp = tn = fn = 0

    for sample in samples:
        result = sf.apply(sample["text"])
        predicted = len(result.illogics_found) > 0
        actual = sample.get("has_hallucination", False)

        if predicted and actual: tp += 1
        elif predicted and not actual: fp += 1
        elif not predicted and actual: fn += 1
        else: tn += 1

    metrics = Evaluator.compute_metrics(tp, fp, tn, fn)
    print(metrics)

if __name__ == "__main__":
    # Placeholder sample
    samples = [{"text": "All cats are dogs.", "has_hallucination": True}]
    run_preflight(samples)
