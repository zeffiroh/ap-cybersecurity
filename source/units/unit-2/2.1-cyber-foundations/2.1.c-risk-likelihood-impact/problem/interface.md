# Interface, 2.1.c-risk-decisions (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data: list[dict]) -> dict[str, str]
```

## Input (`data`)
A list of dictionaries representing risks. Each dictionary contains:
- `name` (str): Unique name of the risk.
- `likelihood` (int): Likelihood of occurrence (1 to 5).
- `impact` (int): Financial or operational impact (1 to 5).
- `cost` (float/int): Cost to implement mitigation controls.
- `value` (float/int): Value of the asset being protected.

## Output (`result`)
A dictionary where keys are the `name` of each risk from the input and values are the decided risk treatment:
- `"Avoid"`
- `"Mitigate"`
- `"Transfer"`
- `"Accept"`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Rules prioritized in order:
  1. `likelihood * impact >= 20` and `cost > 0.6 * value` -> `"Avoid"`
  2. `likelihood * impact >= 15` and `cost <= 0.3 * value` -> `"Mitigate"`
  3. `likelihood * impact >= 15` -> `"Transfer"`
  4. `likelihood * impact >= 5` and `cost <= 0.1 * value` -> `"Mitigate"`
  5. Default -> `"Accept"`

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
