INTERPRETERS = {"powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe", "mshta.exe"}
SAFE_PARENT = "explorer.exe"
TRANSFER_THRESHOLD = 1000000


def solve(events: list) -> list:
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
