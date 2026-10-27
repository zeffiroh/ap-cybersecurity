from typing import Any

def solve(data: Any) -> list[int]:
    """
    Identifies spoofed packets where the source IP is outside the expected subnet.

    Args:
        data: A list of dictionaries, each containing keys: "src_ip", "dst_ip", and "expected_subnet".
    Returns:
        A sorted list of integer indices of packets where the source IP is not in the expected subnet.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
