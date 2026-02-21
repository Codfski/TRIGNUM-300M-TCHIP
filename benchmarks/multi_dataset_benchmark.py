#!/usr/bin/env python3
"""
TRIGNUM-300M Level 1 Benchmark: Multi-Dataset Expansive Run

Tests the Subtractive Filter against multiple industry-standard
hallucination datasets, fetching samples dynamically from HuggingFace
to evaluate generalizability across domains (TruthfulQA, Medical, General Q&A).
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from trignum_core.subtractive_filter import SubtractiveFilter


@dataclass
class DatasetSample:
    id: str
    text: str
    has_hallucination: bool
    hallucination_type: str
    source: str


def fetch_hf_dataset(
    dataset: str, config: str, split: str, limit: int = 100
) -> List[Dict[str, Any]]:
    """Fetch rows from HuggingFace Datasets Server API."""
    url = f"https://datasets-server.huggingface.co/rows?dataset={dataset}&config={config}&split={split}&offset=0&length={limit}"
    print(f"  [↓] Fetching {dataset} ({config}/{split}) from HuggingFace...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            return [row["row"] for row in data.get("rows", [])]
    except Exception as e:
        print(f"  [!] Failed to fetch {dataset}: {e}")
        return []


def prepare_truthful_qa(limit: int = 100) -> List[DatasetSample]:
    """Prepare TruthfulQA samples (Truth vs Misconceptions)."""
    rows = fetch_hf_dataset(
        "truthfulqa/truthful_qa", "generation", "validation", limit=(limit // 2)
    )
    samples = []

    for i, row in enumerate(rows):
        question = row.get("question", "")
        best_answer = row.get("best_answer", "")
        incorrect_answers = row.get("incorrect_answers", [])

        # Add True Sample
        samples.append(
            DatasetSample(
                id=f"TQA-T-{i}",
                text=f"Q: {question}\nA: {best_answer}",
                has_hallucination=False,
                hallucination_type="clean",
                source="TruthfulQA",
            )
        )

        # Add Hallucination Sample
        if incorrect_answers:
            samples.append(
                DatasetSample(
                    id=f"TQA-H-{i}",
                    text=f"Q: {question}\nA: {incorrect_answers[0]}",
                    has_hallucination=True,
                    hallucination_type="misconception",
                    source="TruthfulQA",
                )
            )

    return samples


def prepare_medqa(limit: int = 100) -> List[DatasetSample]:
    """Prepare Medical Flashcards (Truthful Medical Data)."""
    rows = fetch_hf_dataset(
        "medalpaca/medical_meadow_medical_flashcards", "default", "train", limit=limit
    )
    samples = []

    for i, row in enumerate(rows):
        samples.append(
            DatasetSample(
                id=f"MED-T-{i}",
                text=f"Topic: {row.get('input', '')}\nDetail: {row.get('output', '')}",
                has_hallucination=False,
                hallucination_type="clean",
                source="MedHallu (Proxy)",
            )
        )
    return samples


def load_local_halueval(limit: int = 100) -> List[DatasetSample]:
    """Load from local HaluEval QA Data."""
    try:
        filepath = os.path.join(
            os.path.dirname(__file__), "halueval_data", "qa_data.json"
        )
        samples = []
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= (limit // 2):
                    break
                item = json.loads(line.strip())
                question = item.get("knowledge", "")

                # Hallucinated answer
                samples.append(
                    DatasetSample(
                        id=f"HE-H-{i}",
                        text=f"Context: {question}\nAnswer: {item.get('hallucinated_answer', '')}",
                        has_hallucination=True,
                        hallucination_type="qa_fabrication",
                        source="HaluEval QA",
                    )
                )

                # Right answer
                samples.append(
                    DatasetSample(
                        id=f"HE-T-{i}",
                        text=f"Context: {question}\nAnswer: {item.get('right_answer', '')}",
                        has_hallucination=False,
                        hallucination_type="clean",
                        source="HaluEval QA",
                    )
                )

        return samples
    except Exception as e:
        print(f"  [!] Failed to load local HaluEval: {e}")
        return []


def run_multi_benchmark():
    print("═" * 70)
    print("  🧲 TRIGNUM-300M PRE-FLIGHT EXPANSIVE BENCHMARK")
    print("═" * 70)

    print("\n  [1] Assembling Datasets...")
    dataset = []
    dataset.extend(prepare_truthful_qa(limit=60))  # ~60 samples
    dataset.extend(prepare_medqa(limit=30))  # ~30 samples
    dataset.extend(load_local_halueval(limit=60))  # ~60 samples

    if not dataset:
        print("\n  [!] Failed to assemble any data. Check network or API.")
        return

    print(f"  [✓] Assembled {len(dataset)} cross-domain samples.\n")
    print("  [2] Running Subtractive Filter Analysis...")

    sf = SubtractiveFilter()
    tp = tn = fp = fn = 0
    total_time = 0.0

    category_stats = {}

    for sample in dataset:
        start = time.perf_counter()
        res = sf.apply(sample.text)
        total_time += time.perf_counter() - start

        predicted_hallucination = (
            len(res.illogics_found) > 0 and res.subtraction_ratio > 0.01
        )
        actual = sample.has_hallucination

        if predicted_hallucination and actual:
            tp += 1
        elif predicted_hallucination and not actual:
            fp += 1
        elif not predicted_hallucination and actual:
            fn += 1
        else:
            tn += 1

        # Stats per source
        src = sample.source
        if src not in category_stats:
            category_stats[src] = {"total": 0, "correct": 0}
        category_stats[src]["total"] += 1

        if predicted_hallucination == actual:
            category_stats[src]["correct"] += 1

    # Metrics calculation
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-9)
    overall_acc = (tp + tn) / len(dataset)

    # ─── REPORT ───
    print("\n  " + "─" * 50)
    print("  📊 AGGREGATE RESULTS")
    print("  " + "─" * 50)
    print(f"  Total Samples Evaluated: {len(dataset)}")
    print(f"  Total Processing Time:   {total_time * 1000:.2f} ms")
    print(f"  Avg Time per Sample:     {(total_time * 1000) / len(dataset):.2f} ms\n")

    print(f"  Accuracy:   {overall_acc:6.2%}")
    print(f"  Precision:  {precision:6.2%}  (When filter flags, is it right?)")
    print(f"  Recall:     {recall:6.2%}  (Does it catch the actual hallucinations?)")
    print(f"  F1 Score:   {f1:6.2%}\n")

    print("  📂 PER-DATASET ACCURACY")
    print("  " + "─" * 50)
    for src, stats in category_stats.items():
        acc = stats["correct"] / max(stats["total"], 1)
        print(f"  {src:20s}  {stats['correct']}/{stats['total']}  ({acc:.1%})")

    print("\n  " + "═" * 50)
    if f1 > 0.6:
        print("  🟢 VERDICT: READY FOR FLIGHT (Generalizes across domains)")
    else:
        print("  🟡 VERDICT: CAUTION (Needs calibration for out-of-domain data)")
    print("  " + "═" * 50)


if __name__ == "__main__":
    run_multi_benchmark()
