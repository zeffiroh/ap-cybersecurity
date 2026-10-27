# Interface, 2.1.a-cia-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data: list) -> dict:
```

## Input (`data`)
A list of dictionaries, where each dictionary represents a security incident report:
```python
[
    {"id": "INC-01", "description": "The customer database was leaked online."},
    {"id": "INC-02", "description": "A DDoS attack took the server down."}
]
```

## Output (`result`)
A dictionary mapping each incident ID to a sorted list of violated CIA pillars (`"Confidentiality"`, `"Integrity"`, `"Availability"`):
```python
{
    "INC-01": ["Confidentiality"],
    "INC-02": ["Availability"]
}
```

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- An incident description violates a pillar if it contains any of the following substring keywords (case-insensitive):
  - **Confidentiality**: `"leak"`, `"expose"`, `"disclose"`, `"intercept"`, `"steal"`, `"stole"`, `"read"`, `"password"`, `"credential"`
  - **Integrity**: `"modify"`, `"alter"`, `"change"`, `"corrupt"`, `"tamper"`, `"edit"`, `"forge"`, `"spoof"`
  - **Availability**: `"down"`, `"offline"`, `"unavailable"`, `"flood"`, `"crash"`, `"lock"`, `"ransomware"`, `"denial"`
- If no keywords match, the list of pillars for that incident is empty `[]`.
- The list of pillars for each incident ID must be sorted alphabetically (e.g. `["Availability", "Confidentiality"]`).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
