# Interface, 4.1.b-device-tampering-detector (blackbox contract)

Any implementation that satisfies this interface must pass `tests.py` unchanged.

## Entry point
```python
def solve(logs: list[dict]) -> list[str]
```

## Input (`logs`)
A list of log dictionaries, sorted chronologically. Each log contains:
- `timestamp`: ISO-8601 string (e.g. `"2026-06-25T12:00:00Z"`)
- `device_id`: string identifier (e.g. `"workstation_01"`)
- `event_type`: string representing the log event type
- `details`: string containing incident or event details

## Output (`result`)
A list of strings representing the `device_id`s flagged as physically compromised, sorted alphabetically with no duplicates.

## Detection Rules (Case-Insensitive)
1.  **Chassis Intrusion:** Any log entry where `event_type == "chassis_intrusion"` and the word `"open"` is present in the `details`.
2.  **Unauthorized Boot:** Any log entry where `event_type == "boot"` and the `details` contains the words `"usb"`, `"external"`, or `"live"`.
3.  **USB Rubber Ducky (Keystroke Injection):** A log entry where `event_type == "usb_insert"` and `details` contains `"keyboard"` or `"hid"`, which is followed by a `command` log entry on the *same* device such that:
    - The command's timestamp `t_cmd` is greater than or equal to the USB insertion's timestamp `t_usb`.
    - The time difference `(t_cmd - t_usb).total_seconds() <= 3`.
    - The command's `details` contains the words `"powershell"`, `"cmd.exe"`, or `"download"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Timestamps can be parsed using `datetime.fromisoformat(ts.replace("Z", "+00:00"))`.
