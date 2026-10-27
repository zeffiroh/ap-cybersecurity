# Coding problem, 4.3.b: Endpoint Detection Engine

**Skill:** Mitigate Risk · **Maps to:** 4.3.B · **Language:** Python 3 (pytest)

## Problem
Endpoint Protection Platforms (EPP) use a mixture of signature detection (known hashes) and behavioral heuristics (actions taken by the process, such as excessive file updates or network socket connections) to identify and suspend threats.

You are tasked with writing a process-auditing rule engine `solve(data)`. The engine evaluates a list of running processes against:
1. A database of known malicious file hashes (signatures).
2. Max thresholds on process behavior: `max_file_modifications` and `max_network_connections`.

The function must return a list of PIDs of all processes that violate any of these rules.

## Function contract
Implement `solve(data)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A dictionary containing security signatures, behavioral thresholds, and a list of active processes:
```json
{
  "signatures": ["d41d8cd98f00b204e9800998ecf8427e", "098f6bcd4621d373cade4e832627b4f6"],
  "behavioral_rules": {
    "max_file_modifications": 10,
    "max_network_connections": 5
  },
  "processes": [
    {
      "pid": 101,
      "name": "backup_agent.exe",
      "hash": "81dc9bdb52d04dc20036dbd8313ed055",
      "file_modifications": 8,
      "network_connections": 2
    },
    {
      "pid": 102,
      "name": "ransomware.exe",
      "hash": "d41d8cd98f00b204e9800998ecf8427e",
      "file_modifications": 2,
      "network_connections": 0
    },
    {
      "pid": 103,
      "name": "spam_sender.exe",
      "hash": "1f10c9aa0090ff91e90ff8a8bc8a9bcf",
      "file_modifications": 1,
      "network_connections": 12
    }
  ]
}
```

## Output
A list of integers representing the PIDs of flagged processes, sorted in ascending order.
For the example input above:
```json
[102, 103]
```
*(Explanation: PID 102 matches a known signature; PID 103 exceeds the network connections threshold)*

## Constraints
- Signature matching is case-insensitive (e.g., `"A1B2"` matches `"a1b2"`).
- Behavioral violations occur when a metric is *strictly greater* than the threshold (i.e. `file_modifications > max_file_modifications`).
- Standard library only.

## How to run
```
cd problem && python -m pytest tests.py -q
```
