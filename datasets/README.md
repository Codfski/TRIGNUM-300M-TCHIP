# TRIGNUM-300M Datasets Directory

This directory is the designated local storage path for all structured JSON/JSONL datasets used in the benchmark pipeline.

## Structure

- `halueval/` - Place HaluEval QA, Dialogue, and Summarization splits here.
- `truthfulqa/` - Place TruthfulQA validation splits here.
- `medhallu/` - Placeholder for medical knowledge logic benchmarks.

## Usage

When the `HFDatasetFetcher` inside `src/trignum_core/dataset_connectors.py` fails to reach the HuggingFace REST API due to network restrictions, the `Preflight` script will automatically look in this directory for local offline fallbacks.

Make sure `.gitignore` covers raw JSON data if you plan to deal with files larger than 100MB.
