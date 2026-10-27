"""Starter code for 4.1.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""


def solve(device: dict) -> str:
    """Audit an IoT device dict and return its single dominant vulnerability verdict.

    Args:
        device: dict with keys default_password (bool), firmware_outdated (bool),
            open_ports (list[int]), unauthenticated_api (bool), encrypted_traffic (bool).
            Missing keys default to the "safe" value for that key.

    Returns:
        One of: "default_credentials", "outdated_firmware", "exposed_port",
        "unauthenticated_api", "unencrypted_traffic", "secure".
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
