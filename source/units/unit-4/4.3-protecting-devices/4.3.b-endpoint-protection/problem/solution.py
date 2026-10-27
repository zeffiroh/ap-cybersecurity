"""Reference solution for 4.3.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


def solve(data: dict) -> list:
    """Flag processes that match a known-malware signature or exceed behavioral thresholds.

    Args:
        data: dict with keys "signatures" (list[str]), "behavioral_rules" (dict with
            "max_file_modifications" and "max_network_connections"), and "processes"
            (list of dicts with pid, name, hash, file_modifications, network_connections).

    Returns:
        Sorted list of PIDs (int) for every process that matches a signature or
        exceeds a behavioral threshold.
    """
    signatures = {s.lower() for s in data.get("signatures", [])}
    rules = data.get("behavioral_rules", {})
    max_files = rules.get("max_file_modifications", 0)
    max_net = rules.get("max_network_connections", 0)

    flagged = set()
    for proc in data.get("processes", []):
        pid = proc["pid"]
        if proc.get("hash", "").lower() in signatures:
            flagged.add(pid)
            continue
        if proc.get("file_modifications", 0) > max_files:
            flagged.add(pid)
            continue
        if proc.get("network_connections", 0) > max_net:
            flagged.add(pid)
            continue

    return sorted(flagged)
