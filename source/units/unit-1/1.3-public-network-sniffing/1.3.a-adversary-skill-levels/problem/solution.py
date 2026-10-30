def solve(adversary: dict) -> str:
    if adversary["uses_zero_day"] or adversary["custom_tooling"]:
        return "high"
    if adversary["targets_specific_victim"] and adversary["adapts_to_defenses"]:
        return "high"
    return "low"
