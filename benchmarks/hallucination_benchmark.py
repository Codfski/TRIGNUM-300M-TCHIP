#!/usr/bin/env python3
"""
TRIGNUM-300M Level 1 Benchmark: Hallucination Detection

Tests the Subtractive Filter against a curated dataset of
LLM outputs containing known hallucinations vs. truthful statements.

This benchmark measures:
- Precision: When filter says "illogic", how often is it correct?
- Recall: Of all real hallucinations, how many does it catch?
- F1 Score: Harmonic mean of precision and recall
- Subtraction Efficiency: Average ratio of noise removed
"""

import sys
import os
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trignum_core.subtractive_filter import SubtractiveFilter


# ═══════════════════════════════════════════════════════════════
# BENCHMARK DATASET
# Each entry has:
#   - text: The LLM output to analyze
#   - has_hallucination: Ground truth (True/False)
#   - hallucination_type: Category of the hallucination
#   - source: Where this pattern comes from
# ═══════════════════════════════════════════════════════════════

BENCHMARK_DATA = [
    # ─── CLEAN / TRUTHFUL STATEMENTS ───
    {
        "id": "T001",
        "text": "Water boils at 100 degrees Celsius at standard atmospheric pressure. This is due to the kinetic energy of molecules overcoming intermolecular forces.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "physics_fact",
    },
    {
        "id": "T002",
        "text": "The Python programming language was created by Guido van Rossum and first released in 1991. It emphasizes code readability with significant whitespace.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "tech_fact",
    },
    {
        "id": "T003",
        "text": "Machine learning models learn patterns from training data. The quality and diversity of training data significantly impacts model performance.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "ml_fact",
    },
    {
        "id": "T004",
        "text": "DNA carries genetic information using four nucleotide bases: adenine, thymine, guanine, and cytosine. These bases pair in specific combinations.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "biology_fact",
    },
    {
        "id": "T005",
        "text": "The speed of light in a vacuum is approximately 299,792,458 meters per second. This is considered a fundamental constant of nature.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "physics_fact",
    },
    {
        "id": "T006",
        "text": "Compound interest causes investments to grow exponentially over time. The formula is A equals P times the quantity one plus r to the power of n.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "finance_fact",
    },
    {
        "id": "T007",
        "text": "Photosynthesis converts carbon dioxide and water into glucose and oxygen using light energy. This process occurs in the chloroplasts of plant cells.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "biology_fact",
    },
    {
        "id": "T008",
        "text": "HTTP status code 404 indicates that the requested resource was not found on the server. This is one of the most commonly encountered error codes.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "tech_fact",
    },
    {
        "id": "T009",
        "text": "The cerebral cortex is the outermost layer of the brain. It plays a key role in memory, attention, perception, cognition, and language.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "neuroscience_fact",
    },
    {
        "id": "T010",
        "text": "Gravity causes objects to accelerate toward each other. On Earth, the gravitational acceleration is approximately 9.8 meters per second squared.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "physics_fact",
    },
    {
        "id": "T011",
        "text": "Neural networks consist of layers of interconnected nodes. Each connection has an associated weight that is adjusted during training.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "ml_fact",
    },
    {
        "id": "T012",
        "text": "The mitochondria are organelles found in eukaryotic cells. They are responsible for producing adenosine triphosphate through cellular respiration.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "biology_fact",
    },
    {
        "id": "T013",
        "text": "Regular exercise improves cardiovascular health by strengthening the heart muscle. It also helps regulate blood pressure and cholesterol levels.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "health_fact",
    },
    {
        "id": "T014",
        "text": "TCP provides reliable, ordered delivery of data between applications. It uses acknowledgments and retransmissions to ensure data integrity.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "tech_fact",
    },
    {
        "id": "T015",
        "text": "The periodic table organizes chemical elements by atomic number. Elements in the same group share similar chemical properties.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "chemistry_fact",
    },

    # ─── CONTRADICTION HALLUCINATIONS ───
    {
        "id": "H001",
        "text": "Water always boils at 100 degrees Celsius. However, water never boils at that temperature when altitude changes. The boiling point is always 100 degrees regardless of conditions.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "physics_hallucination",
    },
    {
        "id": "H002",
        "text": "All mammals are warm-blooded. No mammals are truly warm-blooded because body temperature varies. Therefore all mammals maintain constant temperature.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "biology_hallucination",
    },
    {
        "id": "H003",
        "text": "Python is always interpreted and never compiled. Python is sometimes compiled to bytecode. The language always runs directly from source code without any compilation.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "tech_hallucination",
    },
    {
        "id": "H004",
        "text": "The speed of light is always constant. In some materials, the speed of light is never the same as in vacuum. Therefore light always travels at the same speed everywhere.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "physics_hallucination",
    },
    {
        "id": "H005",
        "text": "All neural networks can learn any function. No neural network can truly generalize. Every model always perfectly captures the underlying pattern.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "ml_hallucination",
    },
    {
        "id": "H006",
        "text": "The human brain always processes information sequentially. The brain never processes information in parallel. All cognitive tasks are always handled one at a time.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "neuroscience_hallucination",
    },
    {
        "id": "H007",
        "text": "Antibiotics are always effective against all infections. Antibiotics are never effective against viral infections. Therefore antibiotics always cure every disease.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "health_hallucination",
    },
    {
        "id": "H008",
        "text": "Quantum computers can always solve any problem faster than classical computers. They never outperform classical machines. Therefore quantum supremacy is always achieved.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "tech_hallucination",
    },
    {
        "id": "H009",
        "text": "Climate change is caused by all human activity and none of it. The temperature is always rising and never changing. Therefore the climate always stays the same.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "science_hallucination",
    },
    {
        "id": "H010",
        "text": "Every encryption algorithm is always unbreakable. No encryption is ever truly secure. Therefore all data is always perfectly protected by encryption.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "security_hallucination",
    },

    # ─── CIRCULAR REFERENCE HALLUCINATIONS ───
    {
        "id": "H011",
        "text": "The model is accurate because the data is good. The data is good because the model is accurate. The model is accurate because the data is good.",
        "has_hallucination": True,
        "hallucination_type": "circular_reference",
        "source": "ml_hallucination",
    },
    {
        "id": "H012",
        "text": "The algorithm is fast because it uses efficient data structures. It uses efficient data structures because the algorithm is fast. The algorithm is fast because it uses efficient data structures.",
        "has_hallucination": True,
        "hallucination_type": "circular_reference",
        "source": "cs_hallucination",
    },
    {
        "id": "H013",
        "text": "The treatment works because patients improve. Patients improve because the treatment works. The treatment works because patients improve.",
        "has_hallucination": True,
        "hallucination_type": "circular_reference",
        "source": "health_hallucination",
    },
    {
        "id": "H014",
        "text": "This framework is innovative because it uses new concepts. It uses new concepts because the framework is innovative. This framework is innovative because it uses new concepts.",
        "has_hallucination": True,
        "hallucination_type": "circular_reference",
        "source": "tech_hallucination",
    },
    {
        "id": "H015",
        "text": "The economy grows because consumer confidence is high. Consumer confidence is high because the economy grows. The economy grows because consumer confidence is high.",
        "has_hallucination": True,
        "hallucination_type": "circular_reference",
        "source": "economics_hallucination",
    },

    # ─── NON-SEQUITUR HALLUCINATIONS ───
    {
        "id": "H016",
        "text": "Therefore the neural network achieves perfect accuracy",
        "has_hallucination": True,
        "hallucination_type": "non_sequitur",
        "source": "ml_hallucination",
    },
    {
        "id": "H017",
        "text": "Thus we can conclude that this approach solves all problems",
        "has_hallucination": True,
        "hallucination_type": "non_sequitur",
        "source": "cs_hallucination",
    },
    {
        "id": "H018",
        "text": "Therefore the patient will recover completely",
        "has_hallucination": True,
        "hallucination_type": "non_sequitur",
        "source": "health_hallucination",
    },
    {
        "id": "H019",
        "text": "Thus the algorithm runs in constant time",
        "has_hallucination": True,
        "hallucination_type": "non_sequitur",
        "source": "cs_hallucination",
    },
    {
        "id": "H020",
        "text": "Therefore quantum computing will replace classical computing entirely",
        "has_hallucination": True,
        "hallucination_type": "non_sequitur",
        "source": "tech_hallucination",
    },

    # ─── MIXED / COMPLEX HALLUCINATIONS ───
    {
        "id": "H021",
        "text": "All proteins fold into their correct structure and none of them ever misfold. The protein always finds its native state. Therefore protein folding is always solved and never needs research.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "biology_hallucination",
    },
    {
        "id": "H022",
        "text": "GPT models are always correct. GPT models never make mistakes. Therefore all GPT outputs are always true and all information is never wrong.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "ml_hallucination",
    },
    {
        "id": "H023",
        "text": "Security is ensured because encryption is used. Encryption is used because security is ensured. Therefore the system is always secure because encryption is used because security is ensured.",
        "has_hallucination": True,
        "hallucination_type": "circular_reference",
        "source": "security_hallucination",
    },
    {
        "id": "H024",
        "text": "The test passes because the code is correct. The code is correct because the test passes. The test passes because the code is correct. Therefore the software has no bugs.",
        "has_hallucination": True,
        "hallucination_type": "circular_reference",
        "source": "cs_hallucination",
    },
    {
        "id": "H025",
        "text": "All drugs are always safe and none are ever dangerous. Every medication never has side effects. Therefore pharmaceutical research always produces perfect results and never fails.",
        "has_hallucination": True,
        "hallucination_type": "contradiction",
        "source": "health_hallucination",
    },

    # ─── SUBTLE / BORDERLINE CASES ───
    {
        "id": "S001",
        "text": "Most machine learning models require large amounts of data. However, few-shot learning techniques can sometimes achieve reasonable performance with limited examples.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "ml_nuance",
    },
    {
        "id": "S002",
        "text": "While neural networks have achieved impressive results in many areas, they can sometimes produce confident but incorrect outputs, especially on out-of-distribution data.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "ml_nuance",
    },
    {
        "id": "S003",
        "text": "The human immune system is complex and adaptive. Some responses are immediate while others develop over time. Not all immune responses are equally effective.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "biology_nuance",
    },
    {
        "id": "S004",
        "text": "Database normalization reduces redundancy but may impact query performance. The optimal level of normalization depends on the specific use case and access patterns.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "tech_nuance",
    },
    {
        "id": "S005",
        "text": "Climate models have improved significantly over the decades. While they capture large-scale trends well, regional predictions remain challenging due to the complexity of atmospheric systems.",
        "has_hallucination": False,
        "hallucination_type": None,
        "source": "science_nuance",
    },
]


@dataclass
class BenchmarkResult:
    """Result of running the benchmark."""
    total_samples: int
    true_positives: int    # Correctly identified hallucinations
    true_negatives: int    # Correctly identified clean text
    false_positives: int   # Clean text flagged as hallucination
    false_negatives: int   # Missed hallucinations
    precision: float
    recall: float
    f1_score: float
    avg_subtraction_ratio: float
    avg_confidence: float
    processing_time_ms: float
    per_category: Dict[str, Dict[str, float]]
    details: List[Dict]


def run_benchmark(threshold: float = 0.0) -> BenchmarkResult:
    """
    Run the Subtractive Filter against the benchmark dataset.

    Args:
        threshold: Minimum subtraction ratio to classify as hallucination.
                   0.0 = any detection counts.

    Returns:
        BenchmarkResult with metrics.
    """
    sf = SubtractiveFilter()
    details = []

    tp = fp = tn = fn = 0
    total_sub_ratio = 0.0
    total_confidence = 0.0
    category_stats = {}

    start_time = time.perf_counter()

    for sample in BENCHMARK_DATA:
        result = sf.apply(sample["text"])

        # Prediction: hallucination if any illogics found above threshold
        predicted_hallucination = (
            len(result.illogics_found) > 0 and
            result.subtraction_ratio > threshold
        )
        actual_hallucination = sample["has_hallucination"]

        # Confusion matrix
        if predicted_hallucination and actual_hallucination:
            tp += 1
            outcome = "TP"
        elif predicted_hallucination and not actual_hallucination:
            fp += 1
            outcome = "FP"
        elif not predicted_hallucination and actual_hallucination:
            fn += 1
            outcome = "FN"
        else:
            tn += 1
            outcome = "TN"

        total_sub_ratio += result.subtraction_ratio
        total_confidence += result.confidence

        # Track per-category stats
        h_type = sample.get("hallucination_type") or "clean"
        if h_type not in category_stats:
            category_stats[h_type] = {"total": 0, "detected": 0}
        category_stats[h_type]["total"] += 1
        if predicted_hallucination and actual_hallucination:
            category_stats[h_type]["detected"] += 1
        elif not predicted_hallucination and not actual_hallucination:
            category_stats[h_type]["detected"] += 1  # Correct negative

        details.append({
            "id": sample["id"],
            "text_preview": sample["text"][:60] + "...",
            "actual": actual_hallucination,
            "predicted": predicted_hallucination,
            "outcome": outcome,
            "illogics_found": len(result.illogics_found),
            "subtraction_ratio": result.subtraction_ratio,
            "confidence": result.confidence,
            "hallucination_type": sample.get("hallucination_type"),
        })

    end_time = time.perf_counter()

    # Compute metrics
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-9)
    n = len(BENCHMARK_DATA)

    # Per-category accuracy
    per_cat = {}
    for cat, stats in category_stats.items():
        per_cat[cat] = {
            "total": stats["total"],
            "correct": stats["detected"],
            "accuracy": stats["detected"] / max(stats["total"], 1),
        }

    return BenchmarkResult(
        total_samples=n,
        true_positives=tp,
        true_negatives=tn,
        false_positives=fp,
        false_negatives=fn,
        precision=precision,
        recall=recall,
        f1_score=f1,
        avg_subtraction_ratio=total_sub_ratio / n,
        avg_confidence=total_confidence / n,
        processing_time_ms=(end_time - start_time) * 1000,
        per_category=per_cat,
        details=details,
    )


def print_report(result: BenchmarkResult):
    """Print a formatted benchmark report."""
    print()
    print("═" * 70)
    print("  🧲 TRIGNUM-300M LEVEL 1 BENCHMARK: HALLUCINATION DETECTION")
    print("═" * 70)
    print()

    # Overview
    print("  📊 OVERVIEW")
    print("  " + "─" * 50)
    print(f"  Total Samples:       {result.total_samples}")
    print(f"  Processing Time:     {result.processing_time_ms:.2f} ms")
    print(f"  Avg Subtraction:     {result.avg_subtraction_ratio:.4f}")
    print(f"  Avg Confidence:      {result.avg_confidence:.2%}")
    print()

    # Confusion Matrix
    print("  📋 CONFUSION MATRIX")
    print("  " + "─" * 50)
    print(f"                         Predicted")
    print(f"                    Halluc.    Clean")
    print(f"  Actual Halluc.  │  {result.true_positives:3d} (TP) │  {result.false_negatives:3d} (FN) │")
    print(f"  Actual Clean    │  {result.false_positives:3d} (FP) │  {result.true_negatives:3d} (TN) │")
    print()

    # Key Metrics
    print("  🎯 KEY METRICS")
    print("  " + "─" * 50)
    precision_bar = "█" * int(result.precision * 30)
    recall_bar = "█" * int(result.recall * 30)
    f1_bar = "█" * int(result.f1_score * 30)

    print(f"  Precision:  {result.precision:6.2%}  {precision_bar}")
    print(f"  Recall:     {result.recall:6.2%}  {recall_bar}")
    print(f"  F1 Score:   {result.f1_score:6.2%}  {f1_bar}")
    print()

    # Per-category results
    print("  📂 PER-CATEGORY ACCURACY")
    print("  " + "─" * 50)
    for cat, stats in sorted(result.per_category.items()):
        acc_bar = "█" * int(stats["accuracy"] * 20)
        icon = "✅" if stats["accuracy"] >= 0.8 else ("⚠️" if stats["accuracy"] >= 0.5 else "❌")
        print(f"  {icon} {cat:20s}  {stats['correct']:2d}/{stats['total']:2d}  "
              f"{stats['accuracy']:6.1%}  {acc_bar}")
    print()

    # Misclassifications
    misclassified = [d for d in result.details if d["outcome"] in ("FP", "FN")]
    if misclassified:
        print("  ⚠️  MISCLASSIFICATIONS")
        print("  " + "─" * 50)
        for d in misclassified:
            print(f"  [{d['outcome']}] {d['id']}: {d['text_preview']}")
            if d["outcome"] == "FN":
                print(f"       Type: {d['hallucination_type']} (MISSED)")
            else:
                print(f"       False alarm: detected {d['illogics_found']} illogics")
        print()

    # Verdict
    print("  " + "═" * 50)
    if result.f1_score >= 0.8:
        print("  🟡 VERDICT: STRONG — Subtractive Filter shows real capability")
    elif result.f1_score >= 0.6:
        print("  🔵 VERDICT: PROMISING — Filter detects patterns but needs tuning")
    elif result.f1_score >= 0.4:
        print("  ⚠️  VERDICT: DEVELOPING — Some detection, significant gaps")
    else:
        print("  🔴 VERDICT: EARLY STAGE — Needs fundamental improvements")

    print(f"  📈 F1 = {result.f1_score:.2%}")
    print("  " + "═" * 50)
    print()


def save_results(result: BenchmarkResult, filepath: str):
    """Save benchmark results to JSON."""
    data = {
        "benchmark": "TRIGNUM-300M Level 1: Hallucination Detection",
        "version": "v0.300.0",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "metrics": {
            "precision": result.precision,
            "recall": result.recall,
            "f1_score": result.f1_score,
            "total_samples": result.total_samples,
            "true_positives": result.true_positives,
            "true_negatives": result.true_negatives,
            "false_positives": result.false_positives,
            "false_negatives": result.false_negatives,
            "avg_subtraction_ratio": result.avg_subtraction_ratio,
            "avg_confidence": result.avg_confidence,
            "processing_time_ms": result.processing_time_ms,
        },
        "per_category": result.per_category,
        "details": result.details,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  📁 Results saved to: {filepath}")


if __name__ == "__main__":
    print("\n  🧲 Running TRIGNUM-300M Subtractive Filter Benchmark...\n")
    result = run_benchmark(threshold=0.0)
    print_report(result)

    # Save results
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    save_results(result, results_path)
