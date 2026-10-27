"""Reference solution for 4.1.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from datetime import datetime


def solve(logs: list) -> list:
    """Analyze logs to detect physical tampering and device compromise.

    Args:
        logs: A list of log dictionaries, sorted chronologically.

    Returns:
        A list of compromised device IDs, sorted alphabetically.
    """
    compromised = set()
    if not logs:
        return []

    def parse_time(ts_str):
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

    # For fast lookup of USB insertions per device
    usb_inserts = []  # List of (timestamp_dt, device_id)

    # Process all events
    for event in logs:
        device_id = event.get("device_id")
        event_type = event.get("event_type", "")
        details = event.get("details", "")
        ts_str = event.get("timestamp", "")

        if not device_id or not ts_str:
            continue

        try:
            ts_dt = parse_time(ts_str)
        except ValueError:
            continue

        details_lower = details.lower()

        # Rule 1: Chassis Intrusion
        if event_type == "chassis_intrusion" and "open" in details_lower:
            compromised.add(device_id)

        # Rule 2: Unauthorized Boot
        elif event_type == "boot" and any(k in details_lower for k in ["usb", "external", "live"]):
            compromised.add(device_id)

        # Record USB insert for Rule 3
        elif event_type == "usb_insert" and any(k in details_lower for k in ["keyboard", "hid"]):
            usb_inserts.append((ts_dt, device_id))

        # Check Command for Rule 3
        elif event_type == "command":
            for usb_ts, usb_dev in usb_inserts:
                if usb_dev == device_id:
                    time_diff = (ts_dt - usb_ts).total_seconds()
                    if 0 <= time_diff <= 3:
                        if any(k in details_lower for k in ["powershell", "cmd.exe", "download"]):
                            compromised.add(device_id)

    return sorted(list(compromised))
