# Coding problem, 3.4.b: ACL evaluator (first-match-wins)

**Skill:** Mitigate Risk · **Maps to:** 3.4.B, 3.4.C · **Language:** Python 3 (pytest)

## Problem
Implement a firewall ACL evaluator. Given an ordered list of rules and a list of packets, decide
the verdict ("allow" or "deny") for each packet using first-match-wins evaluation with an implicit
deny-all at the end of the list.

A **rule** is a dict with these string/number keys:
- `"action"`, `"allow"` or `"deny"`
- `"src"`, source IP string, or `"any"`
- `"dst"`, destination IP string, or `"any"`
- `"port"`, destination port integer, or `0` meaning any port
- `"proto"`, protocol string: `"tcp"`, `"udp"`, or `"any"`

A **packet** is a dict with:
- `"src"`, source IP string
- `"dst"`, destination IP string
- `"port"`, destination port integer
- `"proto"`, protocol string (`"tcp"` or `"udp"`)

## Function contract
Implement `solve(rules, packets)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

- `rules`, ordered list of rule dicts (evaluate top to bottom, first match wins)
- `packets`, list of packet dicts (evaluate independently, in order)

Return a `list[str]` of verdicts (`"allow"` or `"deny"`), one per packet, in the same order as
`packets`.

## Rule matching
A rule matches a packet when ALL of the following hold:
1. `rule["src"] == "any"` OR `rule["src"] == packet["src"]`
2. `rule["dst"] == "any"` OR `rule["dst"] == packet["dst"]`
3. `rule["port"] == 0` OR `rule["port"] == packet["port"]`
4. `rule["proto"] == "any"` OR `rule["proto"] == packet["proto"]`

Walk `rules` in order; return the **first** matching rule's `"action"`. If no rule in the list
matches, the verdict is `"deny"` (the implicit deny-all, you do not need a literal rule for this;
just return `"deny"` when nothing matches).

## Examples
```python
rules = [
    {"action": "allow", "src": "10.0.4.0", "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},
    {"action": "deny",  "src": "any",      "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},
]
packets = [
    {"src": "10.0.4.0", "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},   # matches rule 1 -> allow
    {"src": "10.0.9.9", "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},   # matches rule 2 -> deny
    {"src": "10.0.9.9", "dst": "10.0.1.5", "port": 22,   "proto": "tcp"},   # matches nothing -> deny
]
solve(rules, packets) == ["allow", "deny", "deny"]
```

## Shadowing example
```python
rules = [
    {"action": "allow", "src": "any", "dst": "any", "port": 22, "proto": "tcp"},   # too broad, placed first
    {"action": "deny",  "src": "203.0.113.0", "dst": "10.0.1.10", "port": 22, "proto": "tcp"},
]
packet = {"src": "203.0.113.0", "dst": "10.0.1.10", "port": 22, "proto": "tcp"}
# The broad rule 1 matches first, so the deny in rule 2 never fires:
solve(rules, [packet]) == ["allow"]
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
