"""Starter code for 4.3.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""


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
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
