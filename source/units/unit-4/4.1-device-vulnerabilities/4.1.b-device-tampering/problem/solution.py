from datetime import datetime


def solve(logs: list) -> list:
    compromised = set()
    if not logs:
        return []

    def parse_time(ts_str):
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

    usb_inserts = []

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

        if event_type == "chassis_intrusion" and "open" in details_lower:
            compromised.add(device_id)

        elif event_type == "boot" and any(k in details_lower for k in ["usb", "external", "live"]):
            compromised.add(device_id)

        elif event_type == "usb_insert" and any(k in details_lower for k in ["keyboard", "hid"]):
            usb_inserts.append((ts_dt, device_id))

        elif event_type == "command":
            for usb_ts, usb_dev in usb_inserts:
                if usb_dev == device_id:
                    time_diff = (ts_dt - usb_ts).total_seconds()
                    if 0 <= time_diff <= 3:
                        if any(k in details_lower for k in ["powershell", "cmd.exe", "download"]):
                            compromised.add(device_id)

    return sorted(list(compromised))
