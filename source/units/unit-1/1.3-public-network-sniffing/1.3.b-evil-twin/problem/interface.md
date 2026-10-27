# Interface, 1.3.b-evil-twin-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(aps: list[dict]) -> list[str]
```

## Input (`aps`)
A list of access-point dicts. Each dict has exactly these keys:
- `ssid` (str), human-readable network name
- `bssid` (str), hardware MAC address, uppercase, colon-separated (e.g. `"AA:BB:CC:11:22:33"`)
- `security` (str), one of `"OPEN"`, `"WEP"`, `"WPA"`, `"WPA2"`, `"WPA3"`
- `signal` (int), dBm (negative integer; e.g. -55)

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of suspicious BSSIDs. Empty list if no anomaly.

## Detection rules (both are OR-combined per AP)
1. **Duplicate SSID**: an SSID appears with more than one distinct BSSID in the scan.
   All BSSIDs for that SSID are flagged.
2. **Security downgrade**: an SSID appears with multiple security levels. Any AP for that
   SSID whose security level is not the maximum (strongest) for that SSID is flagged.

Security strength order (weakest to strongest):
`OPEN` < `WEP` < `WPA` < `WPA2` < `WPA3`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- BSSIDs in input are already uppercase.
- Output is always sorted ascending and de-duplicated.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
