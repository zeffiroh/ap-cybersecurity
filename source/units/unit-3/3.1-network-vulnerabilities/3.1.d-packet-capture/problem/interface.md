# Interface, 3.1.d-packet-leak-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(packets: list[dict]) -> list[str]
```

## Input (`packets`)
`list[dict]` where each dict has:
- `"port"`: `int`, destination port
- `"payload"`: `str`, captured payload text

## Output (`result`)
A `list[str]` the same length as `packets`, in the **same order as the input**, where each element
is one of `"LEAK"`, `"SAFE"`.

## Classification rules
1. If `port` is `443` or `22`, result is `"SAFE"` (encrypted; payload content is never checked).
2. Else if `port` is `80`, `23`, or `21`: result is `"LEAK"` if `payload` contains any of the
   substrings `"password="`, `"Password:"`, `"PASS "`; otherwise `"SAFE"`.
3. Else (any other port), result is `"SAFE"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Output order matches input order exactly.
- Substring checks are case-sensitive exact matches of the three literal strings above.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
