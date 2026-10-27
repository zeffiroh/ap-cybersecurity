# Coding problem, 1.5.a: AI reviewing security configurations

**Skill:** Mitigate Risk, Collaborate · **Maps to:** 1.5.A · **Language:** Python 3 (pytest)

## Problem
Build the rule-engine core of an AI-assisted configuration auditor. Given a list of configuration
file lines (as a real tool would read from `/etc/ssh/sshd_config` or a service config), return
the sorted set of security finding tags for every insecure directive detected. This mirrors exactly
what tools like Lynis and OpenSCAP do at their rule-evaluation layer.

## Function contract
Implement `solve(config_lines: list[str]) -> list[str]` in `starter.py`
(see `interface.md` / `blackbox.yaml`). Return a sorted, de-duplicated list of finding tag strings.

## Input
A `list[str]`, each element one line from a config file. Lines may be blank, start with `#`
(comments), or contain leading/trailing whitespace. Matching is case-insensitive.

Example input:
```python
[
    "# sshd_config for web01",
    "Port 22",
    "PermitRootLogin yes",
    "PasswordAuthentication yes",
    "X11Forwarding yes",
    "",
]
```

## Output
A sorted `list[str]` of finding tags. Tags are drawn from:
- `"insecure:PermitRootLogin"`
- `"insecure:PasswordAuthentication"`
- `"insecure:Port23"`
- `"insecure:SSLDisabled"`
- `"insecure:X11Forwarding"`
- `"insecure:PermitEmptyPasswords"`

## Examples
```
["PermitRootLogin yes", "Port 22"]
    -> ["insecure:PermitRootLogin"]

["PasswordAuthentication yes", "X11Forwarding yes", "PermitRootLogin yes"]
    -> ["insecure:PasswordAuthentication", "insecure:PermitRootLogin", "insecure:X11Forwarding"]

["port 23", "ssl false"]
    -> ["insecure:Port23", "insecure:SSLDisabled"]

["# all defaults", "Port 22", "PermitRootLogin no", ""]
    -> []
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
