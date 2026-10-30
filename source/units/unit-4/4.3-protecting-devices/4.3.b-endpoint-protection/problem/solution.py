def solve(data: dict) -> list:
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
