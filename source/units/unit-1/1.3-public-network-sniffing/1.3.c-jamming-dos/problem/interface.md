# Interface, 1.3.c-jamming-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(samples: list[int]) -> bool
```

## Input (`samples`)
A list of integers, each representing one noise-floor measurement from a wireless monitor.
Values are >= 0. The list may be empty.

## Output (`result`)
`True` if the series contains a sustained jamming event; `False` otherwise.

## Detection rule
**Threshold T = 80 (strictly greater than). Minimum consecutive window N = 5.**

A series is flagged as jamming if it contains a run of at least N = 5 consecutive samples
where every sample in the run is strictly greater than T = 80.

A run is interrupted as soon as any sample is <= T. The run counter resets to zero.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- T and N are fixed constants (T=80, N=5); do not parameterize them.
- An empty list returns False.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
