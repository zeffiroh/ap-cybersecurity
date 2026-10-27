# Interface, 1.4.c-leak-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point

```python
def solve(model_output: str) -> list[str]
```

## Input (`model_output`)

A single `str`, the raw text output produced by an LLM before delivery to the end user.
May be empty string `""`. May contain mixed case. No guaranteed structure.

## Output (`result`)

A `list[str]` of leak-type names detected in `model_output`. Must be sorted in ascending
lexicographic order (as produced by Python's built-in `sorted()`). Return `[]` if no leaks
are found.

Valid leak-type names (exactly as spelled, lowercase with hyphen):
- `"api-key"`
- `"email"`
- `"password"`
- `"system-prompt"`

## Detection rules (exact regex, applied case-insensitively where noted)

### "api-key"
Fires if either pattern matches:
```
re.search(r'sk-[A-Za-z0-9\-]{8,}', text)
re.search(r'(?i)api[_\-]?key\s*[:=]\s*\S+', text)
```

### "email"
Fires if:
```
re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)
```

### "password"
Fires if:
```
re.search(r'(?i)(password|passphrase|passwd)\s*(is|:)\s*\S+', text)
```

### "system-prompt"
Fires if:
```
re.search(r'(?i)(system\s*prompt|your\s+instructions\s+are|you\s+are\s+\w+[\w\s,]*?(AI|assistant|bot))', text)
```

## Guarantees / rules

- Pure function, deterministic, no I/O, no network.
- Standard library only (`re`, `typing`).
- Output list must be sorted (ascending, lexicographic).
- An empty input `""` must return `[]`.
- Detection is independent per class, all matching classes are returned.

## Examples

| Input | Expected output |
|---|---|
| `"sk-prod-abc123XYZ789 is the key."` | `["api-key"]` |
| `"contact admin@corp.internal"` | `["email"]` |
| `"passphrase is: hunter2"` | `["password"]` |
| `"system prompt: You are SecureBot"` | `["system-prompt"]` |
| `"Balance: $500."` | `[]` |
| `""` | `[]` |
| text with all four patterns | `["api-key", "email", "password", "system-prompt"]` |

## Acceptance

`python -m pytest tests.py -q` passes (visible + hidden cases).
