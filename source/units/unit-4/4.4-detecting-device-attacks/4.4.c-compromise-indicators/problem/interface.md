# Interface, 4.4.c-ioc-scoring-engine (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(iocs: list) -> str
```

## Input (`iocs`)
A list of `str` IOC type identifiers observed on a single device. Duplicates may appear in the
list but each IOC type is counted at most once toward the total score.

## IOC weight table
```python
WEIGHTS = {
    "known_malicious_hash": 6,
    "av_disabled": 5,
    "new_admin_account": 4,
    "unusual_outbound_traffic": 3,
    "unexpected_scheduled_task": 3,
    "registry_run_key_added": 2,
    "failed_login_cluster": 1,
}
```
Any string not present in this table contributes a weight of `0`.

## Output (`result`)
One of `"clean"`, `"suspicious"`, `"compromised"`, based on the total score (sum of unique
matched weights):
- `score < 4` -> `"clean"`
- `4 <= score < 8` -> `"suspicious"`
- `score >= 8` -> `"compromised"`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only unless `blackbox.yaml: allow_deps` lists otherwise.
- Duplicate IOC type strings in the input are de-duplicated before scoring.
- Unrecognized IOC strings do not raise; they simply add 0 to the score.
- Thresholds are as specified above (lower bound inclusive, upper bound exclusive per band).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
