# Coding problem, 3.5.b: Traffic-anomaly detector

**Skill:** Detect Attacks · **Maps to:** 3.5.B · **Language:** Python 3 (pytest)

## Problem
Implement a simplified network traffic-anomaly detector. You are given a per-host **baseline**
(the normal profile for that host) and a window of **observed flow records**. Flag every host that
either exceeds its baseline byte-volume threshold or uses a destination port not in its baseline's
allowed-port set.

A **baseline** is a dict mapping host IP (str) to a dict with:
- `"max_bytes"`, integer, the maximum total outbound bytes this host normally sends in the window
- `"allowed_ports"`, list of integers, destination ports this host normally uses

An **observed flow record** is a dict with:
- `"host"`, source host IP string
- `"dst_port"`, destination port integer
- `"bytes"`, integer, bytes sent in this flow

A host may appear in multiple flow records within the same window; volumes accumulate.

## Function contract
Implement `solve(baseline, flows)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

- `baseline`, dict as described above
- `flows`, list of flow record dicts (any order)

Return a sorted `list[str]` of host IPs flagged as anomalous. A host is flagged if EITHER:
1. Its **total** bytes across all its flow records in this window exceeds `max_bytes`, OR
2. Any single flow record for that host uses a `dst_port` not present in `allowed_ports`.

A host not present in `baseline` at all is always flagged (unknown host, no baseline to compare
against, treated as an anomaly).

## Examples
```python
baseline = {
    "10.0.1.5": {"max_bytes": 500_000_000, "allowed_ports": [445, 139]},
    "10.0.2.9": {"max_bytes": 5_000_000, "allowed_ports": [80, 443]},
}
flows = [
    {"host": "10.0.1.5", "dst_port": 445, "bytes": 100_000_000},
    {"host": "10.0.1.5", "dst_port": 445, "bytes": 50_000_000},
    {"host": "10.0.2.9", "dst_port": 4444, "bytes": 1_000},   # unusual port -> flagged
]
solve(baseline, flows) == ["10.0.2.9"]
```

```python
baseline = {"10.0.3.1": {"max_bytes": 1_000_000, "allowed_ports": [443]}}
flows = [
    {"host": "10.0.3.1", "dst_port": 443, "bytes": 900_000},
    {"host": "10.0.3.1", "dst_port": 443, "bytes": 900_000},   # total 1.8M > 1M -> flagged
]
solve(baseline, flows) == ["10.0.3.1"]
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).
- Result is sorted, contains no duplicate host IPs.

## How to run
```
cd problem && python -m pytest tests.py -q
```
