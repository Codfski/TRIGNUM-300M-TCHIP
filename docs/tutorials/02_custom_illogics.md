# Adding Custom Illogics

The core logic ruleset lives inside `src/trignum_core/subtractive_filter.py`.

To extend it, simply append to the `UNIVERSAL_ILLOGICS` set during initialization or subclass `SubtractiveFilter` and override the rules evaluation loop.

## Example:

```python
class MedicalIllogicFilter(SubtractiveFilter):
    def __init__(self):
        super().__init__()
        self.UNIVERSAL_ILLOGICS.update([
            "Prescribes contraindicated medication without warning",
            "Cites non-existent clinical trials"
        ])
```
