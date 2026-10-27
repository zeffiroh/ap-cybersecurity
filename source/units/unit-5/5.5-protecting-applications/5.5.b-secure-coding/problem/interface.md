# Interface, 5.5.b-secure-coding-auditor (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(config: dict) -> list
```

## Input (`config`)
`dict` of application settings. Any key may be missing (missing keys never trigger a violation).
Recognized keys:
- `"debug_mode"`: `bool`
- `"db_query_style"`: `str` (`"parameterized"` or `"concatenated"`)
- `"secrets_in_code"`: `bool`
- `"error_verbosity"`: `str` (`"generic"` or `"verbose"`)
- `"dependencies_pinned"`: `bool`
- `"runs_as"`: `str` (e.g. `"app_user"` or `"root"`)
- `"code_review_required"`: `bool`

## Output (`result`)
Sorted `list[str]` of violated rule names. Only rules that fail appear.

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

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- A missing key never counts as a violation (only an explicit disqualifying value does).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
