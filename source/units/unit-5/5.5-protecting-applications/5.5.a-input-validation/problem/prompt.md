# Coding problem, 5.5.a: Field validator (allowlist + injection detector)

**Skill:** Mitigate Risk · **Maps to:** 5.5.A · **Language:** Python 3 (pytest)

## Problem
Build the server-side validation gate described in the lesson: given a batch of submitted form
field values, classify each as SAFE or BLOCKED using **allowlist rules per field type** plus
detection of known **injection meta-characters/keywords**, the same two checks a real
input-validation layer runs before any value reaches a database query, HTML page, or shell.

## Function contract
Implement `solve(submissions: list) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
`submissions`: `list[dict]`, each `{"field": str, "type": str, "value": str}`. `type` is one of
`"zip"`, `"email"`, `"quantity"`, `"username"`.

## Output
`list[str]` of the `value`s that are BLOCKED, in the same order they appeared in the input.

## Allowlist rules (per `type`)
- `zip`: exactly 5 digits.
- `email`: `local@domain.tld` shape.
- `quantity`: integer string `1`-`99`.
- `username`: 3-20 letters/digits/underscore.

A value is also BLOCKED (even if it matches the allowlist shape) if it contains a known
injection signature: `--`, `;`, `<script`, `UNION SELECT`, `OR 1=1`, `' OR '`, `DROP TABLE`,
`../`, `%3B`, `%2F` (case-insensitive).

## Examples
```
[{"field":"zip","type":"zip","value":"94107"}]                    ->  []
[{"field":"zip","type":"zip","value":"9410"}]                     ->  ["9410"]
[{"field":"u","type":"username","value":"admin'--"}]               ->  ["admin'--"]
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
