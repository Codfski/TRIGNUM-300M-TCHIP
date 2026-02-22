# Adding Custom Datasets

1. Drop your JSON or JSONL file into `datasets/`.
2. Update `src/preflight/preflight_config.yaml` with the file path.
3. If pulling from an API, extend the `HFDatasetFetcher` inside `src/trignum_core/dataset_connectors.py`.

Example:

```yaml
datasets:
  my_custom_domain:
    enabled: true
    source: "local"
    path: "datasets/custom/my_data.json"
```
