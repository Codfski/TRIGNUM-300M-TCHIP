# API Reference

## `trignum_core`

### `SubtractiveFilter`

**Path:** `src/trignum_core/subtractive_filter.py`

- `apply(data: Any) -> FilterResult`: Takes a string, list, or dict. Evaluates it against Universal Illogics. Returns a typed result.

### `Evaluator`

**Path:** `src/trignum_core/evaluator.py`

- `record(predicted_illogic: bool, actual_hallucination: bool) -> None`: Add a single test record.
- `compute_metrics() -> dict`: Returns F1, precision, recall, and accuracy.

### `HFDatasetFetcher`

**Path:** `src/trignum_core/dataset_connectors.py`

- `fetch(dataset_name: str, config: str, split: str, limit: int) -> List[Dict]`: Performs a REST call to HuggingFace Datasets API. Fallback manual fetching if library fails.

_(This reference will dynamically expand in Level 2)._
