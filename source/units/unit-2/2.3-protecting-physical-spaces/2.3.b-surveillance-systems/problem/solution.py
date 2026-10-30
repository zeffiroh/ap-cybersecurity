from __future__ import annotations
from collections import defaultdict


def solve(events: list[dict]) -> list[str]:
    if not events:
        return []

    alerts: set[str] = set()

    for ev in events:
        if ev["person_detected"]:
            hour = (ev["ts"] % 86400) // 3600
            start, end = ev["authorized_hours"]
            if not (start <= hour < end):
                alerts.add(f"AFTER_HOURS:{ev['camera_id']}")

    cam_events: dict[str, list[dict]] = defaultdict(list)
    for ev in events:
        cam_events[ev["camera_id"]].append(ev)

    for cam_id, cam_evs in cam_events.items():
        streak = 0
        for ev in cam_evs:
            if ev["motion"] and not ev["person_detected"]:
                streak += 1
                if streak >= 3:
                    alerts.add(f"GHOST_MOTION:{cam_id}")
                    break
            else:
                streak = 0

    server_ts = sorted(
        ev["ts"] for ev in events
        if ev["person_detected"] and ev["area"] == "server_room"
    )
    n = len(server_ts)
    for i in range(n):
        count = 1
        for j in range(i + 1, n):
            if server_ts[j] - server_ts[i] <= 60:
                count += 1
                if count > 2:
                    alerts.add("CROWD_SERVER_ROOM")
                    break
            else:
                break
        if "CROWD_SERVER_ROOM" in alerts:
            break

    return sorted(alerts)
