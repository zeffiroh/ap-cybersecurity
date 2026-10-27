"""Reference solution for 4.4.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""

WINDOW_SECONDS = 60
MIN_FAILURES = 5


def solve(entries: list) -> list:
    """Flag usernames showing a brute-force pattern: 5+ FAILED attempts within any
    60-second window.

    Args:
        entries: list of dicts with keys ts (int), user (str), result ("SUCCESS"/"FAILED").
            Not guaranteed sorted by timestamp.

    Returns:
        Alphabetically sorted list of unique usernames flagged for brute-force.
    """
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
