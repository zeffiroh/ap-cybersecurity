"""Starter code for 2.4.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict


def solve(events: List[Dict], exit_delay_sec: int = 45, verify_window_sec: int = 120) -> List[str]:
    """Classify each alarm event as SUPPRESSED, FALSE_ALARM, LOCAL_ONLY, or DISPATCH.

    Args:
        events: list of dicts with keys 'ts' (int), 'zone' (str), 'sensor' (str: 'contact',
                'glass_break', or 'panic'), 'arm_state' (str: 'DISARMED', 'ARMED_AWAY',
                'ARMED_STAY'), 'since_armed_sec' (int).
        exit_delay_sec: grace period in seconds after arming (default 45).
        verify_window_sec: max gap in seconds between two different-zone real trips for
                cross-zone verification (default 120).
    Returns:
        List of classification strings, same length and order as `events`, each one of
        "SUPPRESSED", "FALSE_ALARM", "LOCAL_ONLY", "DISPATCH".
        See prompt.md and interface.md for the exact rules.
    """
    # TODO: implement the classification rules per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
