# Interface, 3.4.b-acl-evaluator (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(rules: list[dict], packets: list[dict]) -> list[str]
```

## Input

### `rules`, list of rule dicts, evaluated top-to-bottom (first match wins)
Each rule dict has:
- `"action"` (str): `"allow"` or `"deny"`
- `"src"` (str): source IP address, or `"any"`
- `"dst"` (str): destination IP address, or `"any"`
- `"port"` (int): destination port, or `0` meaning any port
- `"proto"` (str): `"tcp"`, `"udp"`, or `"any"`

### `packets`, list of packet dicts, evaluated independently, in order
Each packet dict has:
- `"src"` (str): source IP address
- `"dst"` (str): destination IP address
- `"port"` (int): destination port
- `"proto"` (str): `"tcp"` or `"udp"`

## Output (`result`)
`list[str]` of verdicts, one per packet, each `"allow"` or `"deny"`, in the same order as
`packets`.

## Rule matching
A rule matches a packet when ALL hold:
1. `rule["src"] == "any"` OR `rule["src"] == packet["src"]`
2. `rule["dst"] == "any"` OR `rule["dst"] == packet["dst"]`
3. `rule["port"] == 0` OR `rule["port"] == packet["port"]`
4. `rule["proto"] == "any"` OR `rule["proto"] == packet["proto"]`

Evaluation returns the **first** matching rule's action. If no rule matches, the implicit
deny-all applies: verdict = `"deny"`.

## Guarantees / rules
- Pure function; deterministic; no I/O; no network access.
- `rules` list is not mutated by `solve`.
- Standard library only.

## Acceptance
`python -m pytest tests.py -q` passes all visible and hidden cases.
