# Coding problem, 4.4.c: Weighted IOC-scoring engine

**Skill:** Detect Attacks · **Maps to:** 4.4.B, 4.4.C · **Language:** Python 3 (pytest)

## Problem
Each device under investigation reports a set of observed indicators of compromise (IOCs). Each
IOC type carries a fixed severity weight. Build the scoring engine that sums the weights of the
IOCs observed on a device and returns an overall compromise verdict.

## Function contract
Implement `def solve(iocs: list) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of strings, each an IOC type observed on one device. Duplicate entries in the list count
only once (an IOC type either is or is not present on the device).

## IOC weight table
| IOC type string | weight |
|---|---|
| `"known_malicious_hash"` | 6 |
| `"av_disabled"` | 5 |
| `"new_admin_account"` | 4 |
| `"unusual_outbound_traffic"` | 3 |
| `"unexpected_scheduled_task"` | 3 |
| `"registry_run_key_added"` | 2 |
| `"failed_login_cluster"` | 1 |

Any IOC type string not in this table contributes a weight of 0 (it is ignored, not an error).

## Output
One of the strings: `"clean"` (total score < 4), `"suspicious"` (4 <= total score < 8),
`"compromised"` (total score >= 8).

## Examples
```
["av_disabled", "new_admin_account"]
    -> "compromised"   # 5 + 4 = 9 >= 8

["failed_login_cluster"]
    -> "clean"          # 1 < 4

["new_admin_account", "failed_login_cluster"]
    -> "suspicious"      # 4 + 1 = 5, in [4, 8)
```

## Constraints
- Deterministic, offline, standard library only.
- Duplicate IOC types in the input list must not be double-counted.
- Unknown/unrecognized IOC type strings contribute 0 and must not raise an error.
- Thresholds are: `< 4` clean, `4 <= score < 8` suspicious, `>= 8` compromised.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
