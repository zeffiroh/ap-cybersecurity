# Interface, 3.1.c-arp-spoof-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(replies: list[dict]) -> list[str]
```

## Input (`replies`)
`list[dict]` where each dict has:
- `"ts"`: `int`, Unix timestamp in seconds the reply was observed
- `"ip"`: `str`, IP address claimed in the reply
- `"mac"`: `str`, MAC address claimed for that IP

## Output (`result`)
A `list[str]` of distinct IP addresses that show the ARP spoofing signature, **sorted
alphabetically**, with no duplicate entries.

## Detection rule
1. For each IP, find the reply with the smallest `ts`, this establishes the trusted MAC binding
   for that IP.
2. If any other reply for that same IP has a `mac` different from the trusted binding, the IP is
   flagged (spoofed).
3. IPs with only one observed reply, or where every reply agrees on the same MAC, are not flagged.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `replies` may arrive in any order; use `ts` (not list position) to determine the trusted (first)
  binding.
- Test data never has two replies for the same IP with a tied minimum `ts`.
- Output is sorted alphabetically with no duplicates.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
