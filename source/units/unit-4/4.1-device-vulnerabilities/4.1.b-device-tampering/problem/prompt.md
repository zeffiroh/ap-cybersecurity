# Coding problem, 4.1.b: Device tampering and physical compromise

**Skill:** Analyze Risk · **Maps to:** 4.1.B · **Language:** Python 3 (pytest)

## Problem
In a physical security audit, we collect logs from system motherboards, BIOS events, and OS events. You must implement a parser that reads these logs and identifies all compromised devices.

A device is considered physically compromised if it triggers any of the following rules:
1.  **Chassis Intrusion:** `event_type == "chassis_intrusion"` and `details` contains `"open"` (case-insensitive).
2.  **Unauthorized Boot:** `event_type == "boot"` and `details` contains `"usb"`, `"external"`, or `"live"` (case-insensitive).
3.  **USB Rubber Ducky:** A `usb_insert` event with `"keyboard"` or `"hid"` in `details` (case-insensitive) followed by a `command` event on the same device within 3 seconds, where the command `details` contains `"powershell"`, `"cmd.exe"`, or `"download"` (case-insensitive).

## Function contract
Implement `solve(logs: list) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).
Return the sorted list of compromised device IDs.

## Input
A list of dicts:
```python
[
    {
        "timestamp": "2026-06-25T12:00:00Z",
        "device_id": "laptop_01",
        "event_type": "boot",
        "details": "Booted from external USB drive"
    }
]
```

## Output
A list of strings, e.g. `["laptop_01"]`, sorted alphabetically.

## Examples
```python
solve([
    {"timestamp": "2026-06-25T10:00:00Z", "device_id": "pc_01", "event_type": "chassis_intrusion", "details": "chassis opened detected"}
]) -> ["pc_01"]

solve([
    {"timestamp": "2026-06-25T10:00:00Z", "device_id": "pc_02", "event_type": "usb_insert", "details": "USB Keyboard connected"},
    {"timestamp": "2026-06-25T10:00:02Z", "device_id": "pc_02", "event_type": "command", "details": "powershell -nop -w hidden -c Get-Process"}
]) -> ["pc_02"]
```

## Constraints
- Pure function, offline, standard library only.
- Timestamps are ISO-8601 strings.
- Sorted return list with unique elements.
