#!/usr/bin/env python3
"""
TRIGNUM-300M FULL BENCHMARK: All HaluEval Data

Tests the Subtractive Filter against the COMPLETE HaluEval dataset.
No sample limits. Every single row.

Datasets:
  - qa_data.json:           ~10,000 samples
  - dialogue_data.json:     ~10,000 samples  
  - summarization_data.json: ~10,000 samples
  - general_data.json:       ~5,000 samples
"""

import sys
import os
import json
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trignum_core.subtractive_filter import SubtractiveFilter

BASE_URL = "https://raw.githubusercontent.com/RUCAIBox/HaluEval/main/data"
CACHE_DIR = os.path.join(os.path.dirname(__file__), "halueval_data")


def download_dataset(name):
    """Download and cache a HaluEval dataset file."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, name)

    if os.path.exists(cache_path):
        print(f"     📂 Cached: {name}")
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    url = f"{BASE_URL}/{name}"
    print(f"     📥 Downloading: {name}...")
    try:
        response = urllib.request.urlopen(url, timeout=60)
        data = response.read().decode("utf-8")
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(data)
        return data
    except Exception as e:
        print(f"     ⚠ Failed: {e}")
        return None


def parse_qa(raw):
    """Parse QA format: right_answer + hallucinated_answer."""
    samples = []
    for line in raw.strip().split("\n"):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "right_answer" in row and "hallucinated_answer" in row:
            samples.append({
                "text": row["right_answer"],
                "has_hallucination": False,
                "task": "qa",
            })
            samples.append({
                "text": row["hallucinated_answer"],
                "has_hallucination": True,
                "task": "qa",
            })
    return samples


def parse_dialogue(raw):
    """Parse dialogue format."""
    samples = []
    for line in raw.strip().split("\n"):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "right_response" in row and "hallucinated_response" in row:
            samples.append({
                "text": row["right_response"],
                "has_hallucination": False,
                "task": "dialogue",
            })
            samples.append({
                "text": row["hallucinated_response"],
                "has_hallucination": True,
                "task": "dialogue",
            })
    return samples


def parse_summarization(raw):
    """Parse summarization format."""
    samples = []
    for line in raw.strip().split("\n"):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "right_summary" in row and "hallucinated_summary" in row:
            samples.append({
                "text": row["right_summary"],
                "has_hallucination": False,
                "task": "summarization",
            })
            samples.append({
                "text": row["hallucinated_summary"],
                "has_hallucination": True,
                "task": "summarization",
            })
    return samples


def parse_general(raw):
    """Parse general format."""
    samples = []
    for line in raw.strip().split("\n"):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        # General format may vary
        if "right_answer" in row and "hallucinated_answer" in row:
            samples.append({
                "text": row["right_answer"],
                "has_hallucination": False,
                "task": "general",
            })
            samples.append({
                "text": row["hallucinated_answer"],
                "has_hallucination": True,
                "task": "general",
            })
        elif "right_response" in row and "hallucinated_response" in row:
            samples.append({
                "text": row["right_response"],
                "has_hallucination": False,
                "task": "general",
            })
            samples.append({
                "text": row["hallucinated_response"],
                "has_hallucination": True,
                "task": "general",
            })
    return samples


def load_all_data():
    """Load ALL available HaluEval datasets."""
    all_samples = []

    datasets = [
        ("qa_data.json", parse_qa),
        ("dialogue_data.json", parse_dialogue),
        ("summarization_data.json", parse_summarization),
        ("general_data.json", parse_general),
    ]

    for filename, parser in datasets:
        raw = download_dataset(filename)
        if raw:
            samples = parser(raw)
            print(f"     ✓ {filename}: {len(samples)} samples ({len(samples)//2} pairs)")
            all_samples.extend(samples)

    return all_samples


def run_benchmark(samples):
    """Run SubtractiveFilter on ALL samples."""
    sf = SubtractiveFilter()

    tp = fp = tn = fn = 0
    per_task = {}
    example_tps = []
    example_fps = []
    example_fns = []

    start = time.perf_counter()

    for sample in samples:
        text = sample["text"]
        task = sample["task"]
        if not text or len(text.strip()) < 5:
            continue

        result = sf.apply(text)

        predicted = len(result.illogics_found) > 0 and result.subtraction_ratio > 0
        actual = sample["has_hallucination"]

        if predicted and actual:
            tp += 1; outcome = "TP"
            if len(example_tps) < 10:
                example_tps.append({"text": text[:120], "task": task})
        elif predicted and not actual:
            fp += 1; outcome = "FP"
            if len(example_fps) < 10:
                example_fps.append({"text": text[:120], "task": task})
        elif not predicted and actual:
            fn += 1; outcome = "FN"
            if len(example_fns) < 5:
                example_fns.append({"text": text[:120], "task": task})
        else:
            tn += 1; outcome = "TN"

        # Per-task tracking
        if task not in per_task:
            per_task[task] = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
        per_task[task][outcome.lower()] += 1

    elapsed = (time.perf_counter() - start) * 1000
    n = tp + fp + tn + fn

    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-9)
    accuracy = (tp + tn) / max(n, 1)

    return {
        "total": n, "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": precision, "recall": recall, "f1": f1,
        "accuracy": accuracy, "time_ms": elapsed,
        "per_task": per_task,
        "example_tps": example_tps,
        "example_fps": example_fps,
        "example_fns": example_fns,
    }


def print_report(r):
    """Print full report."""
    print()
    print("═" * 70)
    print("  🧲 TRIGNUM-300M — FULL HaluEval BENCHMARK")
    print("  ALL datasets. ALL samples. No limits.")
    print("═" * 70)
    print()
    print(f"  Total Samples:       {r['total']:,}")
    print(f"  Processing Time:     {r['time_ms']:.1f} ms ({r['time_ms']/1000:.2f}s)")
    print(f"  Throughput:          {r['total']/(r['time_ms']/1000):,.0f} samples/sec")
    print()

    print("  📋 CONFUSION MATRIX")
    print("  " + "─" * 50)
    print(f"                         Predicted")
    print(f"                    Halluc.    Clean")
    print(f"  Actual Halluc.  │ {r['tp']:5d} TP │ {r['fn']:5d} FN │")
    print(f"  Actual Clean    │ {r['fp']:5d} FP │ {r['tn']:5d} TN │")
    print()

    def bar(v): return "█" * int(v * 30)

    print("  🎯 METRICS")
    print("  " + "─" * 50)
    print(f"  Precision:  {r['precision']:6.2%}  {bar(r['precision'])}")
    print(f"  Recall:     {r['recall']:6.2%}  {bar(r['recall'])}")
    print(f"  F1 Score:   {r['f1']:6.2%}  {bar(r['f1'])}")
    print(f"  Accuracy:   {r['accuracy']:6.2%}  {bar(r['accuracy'])}")
    print()

    # Per-task breakdown
    print("  📂 PER-TASK BREAKDOWN")
    print("  " + "─" * 50)
    for task, counts in sorted(r['per_task'].items()):
        t_tp = counts['tp']; t_fp = counts['fp']
        t_tn = counts['tn']; t_fn = counts['fn']
        t_total = t_tp + t_fp + t_tn + t_fn
        t_prec = t_tp / max(t_tp + t_fp, 1)
        t_rec = t_tp / max(t_tp + t_fn, 1)
        t_f1 = 2 * t_prec * t_rec / max(t_prec + t_rec, 1e-9)
        print(f"  {task:20s}  n={t_total:5d}  P={t_prec:.2%}  R={t_rec:.2%}  F1={t_f1:.2%}  TP={t_tp} FP={t_fp}")
    print()

    if r['example_tps']:
        print(f"  ✅ CAUGHT ({r['tp']} total, showing examples):")
        print("  " + "─" * 50)
        for ex in r['example_tps'][:5]:
            print(f"    [{ex['task']}] \"{ex['text'][:80]}...\"")
        print()

    if r['example_fps']:
        print(f"  ❌ FALSE ALARMS ({r['fp']} total, showing examples):")
        print("  " + "─" * 50)
        for ex in r['example_fps'][:5]:
            print(f"    [{ex['task']}] \"{ex['text'][:80]}...\"")
        print()

    print("  " + "═" * 50)
    print(f"  📈 F1 = {r['f1']:.2%} on FULL HaluEval ({r['total']:,} samples)")
    print(f"  ⚡ Speed: {r['total']/(r['time_ms']/1000):,.0f} samples/second")
    print("  " + "═" * 50)
    print()


if __name__ == "__main__":
    print()
    print("  🧲 TRIGNUM-300M — FULL HaluEval BENCHMARK")
    print("  Loading ALL available datasets...")
    print()

    samples = load_all_data()
    if not samples:
        print("  ❌ No data loaded.")
        sys.exit(1)

    hallu = sum(1 for s in samples if s['has_hallucination'])
    clean = sum(1 for s in samples if not s['has_hallucination'])
    tasks = set(s['task'] for s in samples)

    print(f"\n  📊 TOTAL: {len(samples):,} samples loaded")
    print(f"     Hallucinated: {hallu:,}")
    print(f"     Clean:        {clean:,}")
    print(f"     Tasks:        {', '.join(sorted(tasks))}")
    print()

    results = run_benchmark(samples)
    print_report(results)

    # Save full results
    save_data = {
        "benchmark": "TRIGNUM-300M Full HaluEval",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total": results["total"],
        "tp": results["tp"], "fp": results["fp"],
        "tn": results["tn"], "fn": results["fn"],
        "precision": results["precision"],
        "recall": results["recall"],
        "f1": results["f1"],
        "accuracy": results["accuracy"],
        "time_ms": results["time_ms"],
        "throughput_per_sec": results["total"] / (results["time_ms"] / 1000),
        "per_task": results["per_task"],
        "example_tps": results["example_tps"],
        "example_fps": results["example_fps"],
    }
    outpath = os.path.join(os.path.dirname(__file__), "full_halueval_results.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)
    print(f"  📁 Full results saved: {outpath}")
