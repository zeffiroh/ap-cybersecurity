# Coding problem, 1.3.a: Classify adversary skill tier

**Skill:** Analyze Risk · **Maps to:** 1.3.A · **Language:** Python 3 (pytest)

## Problem
Security analysts use observable attacker behaviors to infer capability level. Given a profile of
an adversary's tools and behaviors, classify them as either a **low-skilled** or **high-skilled**
threat actor.

## Function contract
Implement `solve(adversary: dict) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).
Return `"low"` or `"high"` based on the classification rules defined in `interface.md`.

## Input
A dict with exactly these boolean keys:
- `uses_zero_day`, exploits an unpublished vulnerability
- `custom_tooling`, writes or substantially modifies their own tools
- `targets_specific_victim`, selects a specific high-value target
- `off_the_shelf_only`, relies solely on public tools without modification
- `adapts_to_defenses`, changes tactics when initial attempts fail

## Output
The string `"low"` or `"high"`.

## Classification rules (from interface.md)
1. If `uses_zero_day` OR `custom_tooling` -> `"high"`
2. If `targets_specific_victim` AND `adapts_to_defenses` -> `"high"`
3. Otherwise -> `"low"`

## Examples
```
{"uses_zero_day": True,  "custom_tooling": False, "targets_specific_victim": False,
 "off_the_shelf_only": False, "adapts_to_defenses": False}  ->  "high"

{"uses_zero_day": False, "custom_tooling": False, "targets_specific_victim": False,
 "off_the_shelf_only": True,  "adapts_to_defenses": False}  ->  "low"

{"uses_zero_day": False, "custom_tooling": False, "targets_specific_victim": True,
 "off_the_shelf_only": False, "adapts_to_defenses": True}   ->  "high"
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
