# Interface, 3.5.a-ids-signature-matcher (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(logs: list[dict], rules: list[dict]) -> list[str]
```

## Input (`logs`, `rules`)
- `logs`: list of dicts with keys:
  - `"id"` (str), unique packet/log entry identifier
  - `"dst_port"` (int), destination port
  - `"payload"` (str), packet payload text
- `rules`: list of dicts with keys:
  - `"port"` (int), destination port to match
  - `"keyword"` (str), substring to search for in payload

## Output (`result`)
A sorted `list[str]` of `id` values for log entries that match at least one rule.
Empty list if no entries match.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Keyword matching is case-insensitive (`keyword.lower() in payload.lower()`).
- An entry matching multiple rules appears only once (de-duplicated).
- Output is sorted ascending by `id` string value.
- A log entry matches a rule when its `dst_port == rule["port"]` AND `rule["keyword"].lower()` is a substring of `entry["payload"].lower()`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
