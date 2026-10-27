# Coding problem, 3.1.b: DNS resolver race classifier

**Skill:** Analyze Risk, Detect Attacks · **Maps to:** 3.1.A, 3.1.B · **Language:** Python 3 (pytest)

## Problem
You are building triage logic for a resolver reply log at Crestfield Analytics. For each
outstanding query, the log records the replies that arrived, and, for each reply, who sent it
(`"authoritative"` or `"attacker"`), and the `tx_id`, `port`, and `qname` it carried. Classify each
query's outcome:

- **"REJECT"**, no reply is a valid candidate (none match the query's `tx_id`, `port`, AND
  `qname` all three), so nothing is cached. This also covers the case of zero replies.
- **"WIN"**, among the valid candidates (replies matching all three fields), the one with the
  smallest `arrival` number (i.e. the first to arrive) has `"from": "authoritative"`.
- **"POISON"**, among the valid candidates, the first-arriving one has `"from": "attacker"`.

## Function contract
Implement `solve(queries)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `queries`: `list[dict]`, each with:
  - `"qname"`: `str`, the domain name queried
  - `"tx_id"`: `int`, the transaction ID the resolver sent
  - `"port"`: `int`, the source port the resolver sent the query from
  - `"replies"`: `list[dict]`, each with `"from"` (`"authoritative"` or `"attacker"`),
    `"tx_id"` (`int`), `"port"` (`int`), `"qname"` (`str`), `"arrival"` (`int`, lower = earlier)

## Output
A `list[str]` of classifications, **one per input query, in the same order as the input**. Each
entry is one of `"WIN"`, `"POISON"`, `"REJECT"`.

## Examples
```python
queries = [
    {
        "qname": "bank.example", "tx_id": 48291, "port": 33412,
        "replies": [
            {"from": "attacker", "tx_id": 48291, "port": 33412, "qname": "bank.example", "arrival": 1},
            {"from": "authoritative", "tx_id": 48291, "port": 33412, "qname": "bank.example", "arrival": 2},
        ],
    },
]
solve(queries)  ->  ["POISON"]

queries2 = [
    {
        "qname": "shop.example", "tx_id": 11020, "port": 40500,
        "replies": [
            {"from": "attacker", "tx_id": 99999, "port": 40500, "qname": "shop.example", "arrival": 1},
            {"from": "authoritative", "tx_id": 11020, "port": 40500, "qname": "shop.example", "arrival": 2},
        ],
    },
]
solve(queries2)  ->  ["WIN"]
```

## Constraints
- Deterministic, offline, standard library only.
- A reply is a "valid candidate" only if `reply["tx_id"] == query["tx_id"]` AND
  `reply["port"] == query["port"]` AND `reply["qname"] == query["qname"]`.
- Among valid candidates, only the one with the minimum `arrival` value matters (test data never
  has ties on the minimum `arrival`).
- Replies may be given in any order in the list; use the `arrival` field, not list position, to
  determine which arrived first.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
