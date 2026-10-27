"""Reference solution for 4.4.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""

INTERPRETERS = {"powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe", "mshta.exe"}
SAFE_PARENT = "explorer.exe"
TRANSFER_THRESHOLD = 1000000


def solve(events: list) -> list:
    """Flag EDR process events showing a living-off-the-land parent-child pair or an
    unusually large outbound data transfer.

    Args:
        events: list of dicts with keys pid (int), process (str), parent_process (str),
            external_connection (bool), bytes_transferred (int).

    Returns:
        Sorted list of unique pids (int) flagged by either detection rule.
    """
    flagged = set()
    for ev in events:
        pid = ev["pid"]
        process = ev.get("process", "").lower()
        parent = ev.get("parent_process", "").lower()
        external = ev.get("external_connection", False)
        transferred = ev.get("bytes_transferred", 0)

        if process in INTERPRETERS and parent != SAFE_PARENT:
            flagged.add(pid)
            continue
        if external and transferred > TRANSFER_THRESHOLD:
            flagged.add(pid)
            continue

    return sorted(flagged)
