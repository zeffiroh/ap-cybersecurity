"""Reference solution for 1.3.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


def solve(adversary: dict) -> str:
    """Classify an adversary as 'low' or 'high' skill based on their profile.

    Rules (first match wins):
      1. uses_zero_day OR custom_tooling                          -> 'high'
      2. targets_specific_victim AND adapts_to_defenses           -> 'high'
      3. otherwise                                                -> 'low'
    """
    if adversary["uses_zero_day"] or adversary["custom_tooling"]:
        return "high"
    if adversary["targets_specific_victim"] and adversary["adapts_to_defenses"]:
        return "high"
    return "low"
