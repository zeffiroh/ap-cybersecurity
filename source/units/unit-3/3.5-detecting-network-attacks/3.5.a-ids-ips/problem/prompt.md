# Coding problem, 3.5.a: IDS signature matcher

**Skill:** Detect Attacks · **Maps to:** 3.5.A · **Language:** Python 3 (pytest)

## Problem
You are implementing the rule-matching core of a simple IDS. The sensor receives a stream of
packet-log entries. Each entry is a dict with the fields shown below. You are given a list of
signature rules; each rule has a destination port and a keyword that must appear (case-insensitive)
in the payload. A log entry matches a rule when BOTH the port AND the keyword condition are met.

Return the sorted list of `id` values for every log entry that matches at least one rule.

## Function contract
Implement `solve(logs: list[dict], rules: list[dict]) -> list[str]` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
- `logs`: list of dicts, each with keys:
  - `"id"` (str), unique entry identifier, e.g. `"pkt-001"`
  - `"dst_port"` (int), destination port of the packet
  - `"payload"` (str), packet payload (may be empty)
- `rules`: list of dicts, each with keys:
  - `"port"` (int), destination port to match
  - `"keyword"` (str), substring to find (case-insensitive) in the payload

## Output
A sorted `list[str]` of `id` values for entries that match at least one rule.
Empty list if no entries match.

## Examples
```
logs = [
    {"id": "pkt-001", "dst_port": 80,  "payload": "GET /admin/../etc/passwd HTTP/1.1"},
    {"id": "pkt-002", "dst_port": 443, "payload": "TLS handshake"},
    {"id": "pkt-003", "dst_port": 80,  "payload": "GET /index.html HTTP/1.1"},
    {"id": "pkt-004", "dst_port": 22,  "payload": "SSH-2.0-OpenSSH_8.9"},
]
rules = [
    {"port": 80, "keyword": "etc/passwd"},
    {"port": 22, "keyword": "libssh"},
]
solve(logs, rules)  ->  ["pkt-001"]

logs = []
solve(logs, rules)  ->  []
```

## Constraints
- Deterministic, offline, standard library only.
- Keyword matching is case-insensitive substring match.
- A log entry that matches multiple rules is included only once in the output.
- Output is sorted ascending by `id`.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
