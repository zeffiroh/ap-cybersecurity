# Interface, 3.4.a-firewall-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(rules: list[dict], packets: list[dict], mode: str) -> list[str]
```

## Input

### `rules`, list of rule dicts, evaluated top-to-bottom (first match wins)
Each rule dict has:
- `"action"` (str): `"allow"` or `"drop"`
- `"proto"` (str): `"tcp"`, `"udp"`, `"icmp"`, or `"any"`
- `"dport"` (int): destination port to match, or `0` meaning any port

### `packets`, list of packet dicts, processed in order
Each packet dict has:
- `"src"` (str): source IP address
- `"dst"` (str): destination IP address
- `"sport"` (int): source port
- `"dport"` (int): destination port
- `"proto"` (str): `"tcp"`, `"udp"`, or `"icmp"`
- `"flags"` (str): TCP flag, one of `"SYN"`, `"SYN-ACK"`, `"ACK"`, `"RST"`, `"FIN"`, `"DATA"`,
  or `""` for non-TCP

### `mode`, `"stateless"` or `"stateful"`

## Output (`result`)
`list[str]` of verdicts, one per packet, each `"allow"` or `"drop"`, in the same order as
`packets`.

## Rule matching (both modes)
A rule matches a packet when BOTH conditions hold:
1. `rule["proto"] == "any"` OR `rule["proto"] == packet["proto"]`
2. `rule["dport"] == 0` OR `rule["dport"] == packet["dport"]`
Implicit default if no rule matches: `"drop"`.

## Stateful TCP tracking (stateful mode only)
- Connection table key: `(src, dst, sport, dport, proto)`, all five fields.
- **SYN**: passes rules -> add key with state `"SYN_SENT"` -> `"allow"`.
- **SYN-ACK**: reverse key `(dst, src, dport, sport, proto)` in table -> update to
  `"ESTABLISHED"` -> `"allow"`. Reverse key not found -> `"drop"`.
- **ACK / DATA**: key or reverse in table with state `"ESTABLISHED"` -> `"allow"`.
  Otherwise -> `"drop"` (no established session for this endpoint pair).
- **RST / FIN**: key or reverse in table -> remove entry -> `"allow"`. Not found -> `"drop"`.
- Non-TCP packets (UDP, ICMP): rule matching only; no state tracking.

## Guarantees / rules
- Pure function; deterministic; no I/O; no network access.
- Connection table is initialized empty at the start of each `solve()` call.
- Standard library only.

## Acceptance
`python -m pytest tests.py -q` passes all visible and hidden cases.
