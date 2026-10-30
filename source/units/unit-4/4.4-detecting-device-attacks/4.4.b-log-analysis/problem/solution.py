WINDOW_SECONDS = 60
MIN_FAILURES = 5


def solve(entries: list) -> list:
    failures_by_user = {}
    for entry in entries:
        if entry.get("result") == "FAILED":
            user = entry["user"]
            failures_by_user.setdefault(user, []).append(entry["ts"])

    flagged = set()
    for user, timestamps in failures_by_user.items():
        timestamps.sort()
        if len(timestamps) < MIN_FAILURES:
            continue
        for i in range(len(timestamps) - MIN_FAILURES + 1):
            span = timestamps[i + MIN_FAILURES - 1] - timestamps[i]
            if span <= WINDOW_SECONDS:
                flagged.add(user)
                break

    return sorted(flagged)
