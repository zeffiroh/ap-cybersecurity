"""Starter code for 5.6.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def solve(entries: List[Dict[str, object]], threshold: int, window_seconds: int) -> List[str]:
    """Flag source IPs whose failed-login (401) count reaches >= threshold within some
    rolling window of window_seconds — the brute-force SIEM rule from the lesson.

    Args:
        entries: list of {"ip": str, "ts": int, "status": int} log entries. `ts` is seconds
            since the start of the log; `status` is an HTTP status code.
        threshold: minimum number of 401s within the window to flag the IP.
        window_seconds: inclusive rolling window size, in seconds.
    Returns:
        sorted, de-duplicated list[str] of flagged IP addresses.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
