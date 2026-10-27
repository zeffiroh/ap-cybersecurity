# Coding problem, 5.5.b: Secure-coding configuration auditor

**Skill:** Mitigate Risk · **Maps to:** 5.5.A, 5.5.B · **Language:** Python 3 (pytest)

## Problem
Build a lightweight policy-as-code auditor: given an application's configuration, flag every
secure-coding practice it violates, exactly the checks a code reviewer or CI gate would run.

## Function contract
Implement `solve(config: dict) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
`config`: `dict` of settings. Any key may be missing.

## Output
Sorted `list[str]` of violated rule names.

## Rule set
| condition | violation |
|---|---|
| `debug_mode is True` | `"debug-mode-enabled"` |
| `db_query_style == "concatenated"` | `"non-parameterized-query"` |
| `secrets_in_code is True` | `"hardcoded-secret"` |
| `error_verbosity == "verbose"` | `"verbose-error-messages"` |
| `dependencies_pinned is False` | `"unpinned-dependencies"` |
| `runs_as == "root"` | `"excessive-privilege"` |
| `code_review_required is False` | `"no-code-review"` |

## Examples
```
{"debug_mode": True}                         ->  ["debug-mode-enabled"]
{"db_query_style": "parameterized"}          ->  []
{"runs_as": "root", "secrets_in_code": True} ->  ["excessive-privilege", "hardcoded-secret"]
```

## Constraints
- Deterministic, offline, standard library only.
- A missing key never triggers a violation.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
