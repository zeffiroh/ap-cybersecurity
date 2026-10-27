# Interface, 1.4.b-prompt-injection-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(prompt_text: str) -> list[str]
```

## Input (`prompt_text`)
A single string of user-supplied text passed to an LLM application. May be empty string or
any casing. The function must not raise on empty or None input.

## Output (`list[str]`)
A sorted list of matched injection pattern names. Elements are drawn exclusively from the
following fixed vocabulary (exact spelling must be preserved in output):

```
"disregard"
"ignore previous instructions"
"reveal system prompt"
"system:"
"you are now"
```

Return `[]` if no patterns are detected.

## Pattern matching rules (case-insensitive substring, applied to `prompt_text.lower()`)

| Output name                      | Trigger                                                         |
|----------------------------------|-----------------------------------------------------------------|
| `"disregard"`                    | `"disregard"` in text                                           |
| `"ignore previous instructions"` | `"ignore previous"` in text                                     |
| `"reveal system prompt"`         | `"reveal"` in text **AND** `"system"` in text (checked separately) |
| `"system:"`                      | `"system:"` in text                                             |
| `"you are now"`                  | `"you are now"` in text                                         |

All five patterns are checked independently. Multiple patterns can match the same input.

## Return order
The returned list must be sorted (ascending, standard Python string sort order).

## Guarantees / rules
- Pure function, deterministic, no I/O, no network, no side effects.
- Standard library only (no external packages); see `blackbox.yaml: allow_deps`.
- Must handle empty string and None without raising an exception.
- Pattern names in the output must match the vocabulary exactly (spacing, punctuation).

## Acceptance
```
python -m pytest tests.py -q
```
All tests must pass (both visible cases and edge cases).
