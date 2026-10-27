# Interface, 3.2.b-control-type-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def classify_controls(scenarios: list[dict]) -> list[str]
```

## Input (`scenarios`)
`list[dict]` where each dict has:
- `"id"`: `str`
- `"description"`: `str`, flavor text, not used for classification logic
- `"mechanism"`: `str`, one of `"policy_document"`, `"training_program"`,
  `"access_review_process"`, `"software_or_hardware_enforcement"`, `"physical_barrier"`

## Output (`result`)
A `list[str]` the same length as `scenarios`, in the **same order as the input**, where each
element is one of `"managerial"`, `"technical"`, `"physical"`.

## Classification rule
- `mechanism` in `{"policy_document", "training_program", "access_review_process"}` -> `"managerial"`
- `mechanism == "software_or_hardware_enforcement"` -> `"technical"`
- `mechanism == "physical_barrier"` -> `"physical"`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `"mechanism"` always contains one of the five listed values in test data (no invalid values).
- Output order matches input order exactly.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
