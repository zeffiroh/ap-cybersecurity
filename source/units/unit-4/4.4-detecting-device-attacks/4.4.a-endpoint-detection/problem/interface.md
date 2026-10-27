# Interface, 4.4.a-edr-telemetry-analyzer (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(events: list) -> list
```

## Input (`events`)
A list of dicts, each describing one EDR process event:

| key | type | meaning |
|---|---|---|
| `pid` | int | process id |
| `process` | str | the process image name, e.g. `"powershell.exe"` |
| `parent_process` | str | the parent process image name, e.g. `"winword.exe"` |
| `external_connection` | bool | whether the process opened a connection to an external host |
| `bytes_transferred` | int | total bytes transferred over that connection (0 if none) |

## Output (`result`)
A de-duplicated, ascending-sorted list of `int` pids for every flagged event.

## Detection rules (flag if EITHER fires)
1. `process.lower()` is in `{"powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe",
   "mshta.exe"}` AND `parent_process.lower()` is not `"explorer.exe"`.
2. `external_connection` is `True` AND `bytes_transferred > 1000000`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only unless `blackbox.yaml: allow_deps` lists otherwise.
- Process/parent name matching is case-insensitive.
- The output list has no duplicate pids and is sorted ascending.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
