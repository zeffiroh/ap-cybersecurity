# Coding problem, 3.1.c: ARP spoofing detector

**Skill:** Analyze Risk · **Maps to:** 3.1.B · **Language:** Python 3 (pytest)

## Problem
You are building an arpwatch-style detector for Crestfield Analytics. Given a timestamp-ordered
log of observed ARP replies (each mapping an IP to a MAC), identify which IP addresses show the
ARP spoofing signature: the **first** reply seen for an IP establishes its trusted MAC binding. Any
**later** reply for the same IP with a **different** MAC is a spoofing indicator. A later reply
with the *same* MAC as the trusted binding is just a normal refresh and is not flagged.

## Function contract
Implement `solve(replies)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `replies`: `list[dict]`, each with:
  - `"ts"`: `int`, Unix timestamp (seconds) the reply was observed
  - `"ip"`: `str`, the IP address claimed in the reply
  - `"mac"`: `str`, the MAC address claimed for that IP

## Output
A `list[str]`, the distinct IP addresses that show the spoofing signature (at least one reply with
a MAC different from that IP's first-seen MAC), **sorted alphabetically**, with no duplicates.

## Examples
```python
replies = [
    {"ts": 100, "ip": "192.168.1.1", "mac": "aa:11:22:33:44:01"},
    {"ts": 130, "ip": "192.168.1.1", "mac": "aa:11:22:33:44:01"},
    {"ts": 145, "ip": "192.168.1.1", "mac": "de:ad:be:ef:00:99"},
]
solve(replies)  ->  ["192.168.1.1"]

replies2 = [
    {"ts": 100, "ip": "192.168.1.50", "mac": "11:22:33:44:55:66"},
]
solve(replies2)  ->  []
```

## Constraints
- Deterministic, offline, standard library only.
- `replies` may be given in any timestamp order in the list; use the `ts` field (not list
  position) to determine which reply for a given IP came first (the "trusted" binding).
- Test data never has two replies for the same IP with an identical minimum `ts`.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
