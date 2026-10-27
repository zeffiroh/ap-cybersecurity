"""Reference solution for 2.3.b — Surveillance systems (CCTV, monitoring).
MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

solve(events) -> sorted, de-duplicated list of alert strings.

Alert rules:
  AFTER_HOURS:<camera_id>  — person detected outside authorized_hours UTC hour range
  GHOST_MOTION:<camera_id> — 3+ consecutive motion=True, person_detected=False on same camera
  CROWD_SERVER_ROOM        — person_detected=True in area='server_room' > 2 times in any 60s window

Hour from timestamp: hour = (ts % 86400) // 3600   (UTC)
authorized_hours = (start, end): authorized if start <= hour < end
"""
from __future__ import annotations
from collections import defaultdict


def solve(events: list[dict]) -> list[str]:
    """Analyze a camera event log and return sorted, de-duplicated alert strings."""
    if not events:
        return []

    alerts: set[str] = set()

    # --- Rule 1: AFTER_HOURS ---
    for ev in events:
        if ev["person_detected"]:
            hour = (ev["ts"] % 86400) // 3600
            start, end = ev["authorized_hours"]
            if not (start <= hour < end):
                alerts.add(f"AFTER_HOURS:{ev['camera_id']}")

    # --- Rule 2: GHOST_MOTION (3+ consecutive motion=T, person=F per camera) ---
    # Events are already sorted ascending by ts; group by camera to preserve order.
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

    # --- Rule 3: CROWD_SERVER_ROOM (>2 person_detected in server_room within any 60s window) ---
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
