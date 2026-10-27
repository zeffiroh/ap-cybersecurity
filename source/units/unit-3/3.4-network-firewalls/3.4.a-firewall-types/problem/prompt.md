# Coding problem, 3.4.a: Stateless vs. stateful packet classifier

**Skill:** Mitigate Risk · **Maps to:** 3.4.A · **Language:** Python 3 (pytest)

## Problem
You will implement two firewall decision functions that together illustrate the core difference
between stateless and stateful packet filtering.

A **packet** is a dict with these string keys:
- `"src"`, source IP string (e.g. `"203.0.113.10"`)
- `"dst"`, destination IP string
- `"sport"`, source port integer
- `"dport"`, destination port integer
- `"proto"`, protocol string, one of `"tcp"` / `"udp"` / `"icmp"`
- `"flags"`, TCP flag string: one of `"SYN"`, `"SYN-ACK"`, `"ACK"`, `"RST"`, `"FIN"`, `"DATA"`
  (non-TCP packets use `""`)

A **rule** is a dict with:
- `"action"`, `"allow"` or `"drop"`
- `"proto"`, protocol to match (`"tcp"`, `"udp"`, `"icmp"`, or `"any"`)
- `"dport"`, destination port to match (integer) or `0` meaning any port

Rules are evaluated top-to-bottom; the first match decides.  If no rule matches, the implicit
verdict is `"drop"`.

## Function contract
Implement `solve(rules, packets, mode)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

- `rules`, list of rule dicts (ordered, first-match)
- `packets`, list of packet dicts (process in order)
- `mode`, string: `"stateless"` or `"stateful"`

Return a `list[str]` of verdicts (`"allow"` or `"drop"`), one per packet, in order.

## Stateless mode
For each packet, walk the rule list. A rule matches when:
1. `rule["proto"]` is `"any"` OR equals `packet["proto"]`
2. `rule["dport"]` is `0` OR equals `packet["dport"]`

Return the matched rule's action, or `"drop"` if nothing matches.

## Stateful mode
Same rule matching applies, but also maintain an in-memory connection-tracking table (a dict).
The table key is `(src, dst, sport, dport, proto)` (tuple of the five fields above).

Additional stateful logic for TCP packets only:
- **SYN**: if the packet passes rules, add `(src, dst, sport, dport, "tcp")` to the table with
  state `"SYN_SENT"`. Verdict = `"allow"`.
- **SYN-ACK**: look up the *reverse* key `(dst, src, dport, sport, "tcp")` in the table (the
  original SYN entry). If found, update its state to `"ESTABLISHED"`. Verdict = `"allow"`.
  If the reverse key is not in the table, verdict = `"drop"`.
- **ACK / DATA**: if the packet's key OR its reverse is in the table with state `"ESTABLISHED"`,
  verdict = `"allow"`. Otherwise verdict = `"drop"` (no established session for this endpoint
  pair, a stateful firewall drops it even though a static rule might otherwise permit the port).
- **RST / FIN**: if the key or reverse is in the table, remove the entry. Verdict = `"allow"`.
  Otherwise `"drop"`.

Non-TCP packets (UDP, ICMP) are decided by rule matching only (no state tracking).

The table starts empty at the beginning of each `solve()` call.

## Input
```python
rules = [
    {"action": "allow", "proto": "tcp", "dport": 443},
    {"action": "allow", "proto": "tcp", "dport": 80},
    {"action": "drop",  "proto": "any", "dport": 0},
]
packets = [
    {"src": "203.0.113.10", "dst": "10.0.0.5", "sport": 55001, "dport": 443, "proto": "tcp", "flags": "SYN"},
    {"src": "10.0.0.5",     "dst": "203.0.113.10", "sport": 443, "dport": 55001, "proto": "tcp", "flags": "SYN-ACK"},
    {"src": "198.51.100.7", "dst": "10.0.0.5", "sport": 44000, "dport": 443, "proto": "tcp", "flags": "ACK"},
]
```

## Output
```
stateless: ["allow", "drop", "allow"]   # SYN-ACK (dport 55001) matches no rule
stateful:  ["allow", "allow", "drop"]   # third packet: ACK with no prior SYN
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).
- The connection table is local to each `solve()` call (not persisted between calls).

## How to run
```
cd problem && python -m pytest tests.py -q
```
