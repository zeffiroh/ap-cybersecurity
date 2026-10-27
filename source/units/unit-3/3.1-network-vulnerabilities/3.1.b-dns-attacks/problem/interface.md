# Interface, 3.1.b-dns-resolver-race-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(queries: list[dict]) -> list[str]
```

## Input (`queries`)
`list[dict]` where each dict has:
- `"qname"`: `str`, domain name queried
- `"tx_id"`: `int`, transaction ID the resolver sent
- `"port"`: `int`, source port the resolver sent the query from
- `"replies"`: `list[dict]`, each with:
  - `"from"`: `str`, `"authoritative"` or `"attacker"`
  - `"tx_id"`: `int`
  - `"port"`: `int`
  - `"qname"`: `str`
  - `"arrival"`: `int`, arrival order, lower arrives earlier

## Output (`result`)
A `list[str]` the same length as `queries`, in the **same order as the input**, where each element
is one of `"WIN"`, `"POISON"`, `"REJECT"`.

## Classification rules
1. A reply is a **valid candidate** iff its `tx_id`, `port`, and `qname` all equal the query's
   `tx_id`, `port`, and `qname`.
2. If there are no valid candidates (including an empty `replies` list), the result is `"REJECT"`.
3. Otherwise, take the valid candidate with the smallest `arrival` value (the first to arrive). If
   its `"from"` is `"authoritative"`, the result is `"WIN"`; if `"attacker"`, the result is
   `"POISON"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Output order matches input order exactly.
- Test data never has two valid candidates with an identical `arrival` value.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
