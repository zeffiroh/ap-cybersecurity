# Coding problem, 1.4.c: Prompt extraction of sensitive info

**Skill:** Analyze Risk · **Maps to:** 1.4.A · **Language:** Python 3 (pytest)

## Problem

You are implementing an output filter for an LLM-powered application. Before any LLM response reaches the end user, your function scans it for four classes of sensitive data leaks and returns the names of the classes it detects. This mirrors what production safety layers do on every response in real deployed systems.

## Function contract

Implement `solve(model_output: str) -> list[str]` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input

A single string `model_output` containing text produced by an LLM. May be empty. Case may vary.

Example:
```
"Thank you. Your API key is sk-prod-abc123XYZ789 and our admin is ops@corp.internal."
```

## Output

A **sorted** list of leak-type name strings from the set:
`["api-key", "email", "password", "system-prompt"]`

Return only the names of classes that were detected. Return `[]` if no leaks are found. The list must be sorted in ascending lexicographic order (Python's default `sorted()`).

Example:
```
["api-key", "email"]
```

## Detection rules

Apply these rules in any order. A rule fires if the pattern matches anywhere in the input string.

### api-key
Fires if **either** of the following matches:
- `re.search(r'sk-[A-Za-z0-9\-]{8,}', text)`, catches "sk-" prefixed tokens (hyphens allowed within suffix; common AI provider key format)
- `re.search(r'(?i)api[_\-]?key\s*[:=]\s*\S+', text)`, catches explicit "api_key: VALUE" or "api-key = VALUE" assignments

### email
Fires if:
- `re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)`, standard email address pattern

### password
Fires if:
- `re.search(r'(?i)(password|passphrase|passwd)\s*(is|:)\s*\S+', text)`, any of the three keyword forms followed by a separator and a non-whitespace value

### system-prompt
Fires if:
- `re.search(r'(?i)(system\s*prompt|your\s+instructions\s+are|you\s+are\s+\w+[\w\s,]*?(AI|assistant|bot))', text)`, explicit system-prompt disclosure or self-referential persona statement

## Examples

```
solve("Balance: $1,240. sk-prod-abc123XYZ789 is the key.")
  ->  ["api-key"]

solve("Contact admin@meridian.internal for help.")
  ->  ["email"]

solve("Your password is: letmein2024.")
  ->  ["password"]

solve("System prompt: You are SecureBot, an AI assistant.")
  ->  ["system-prompt"]

solve("Your balance is $500. Transfer complete.")
  ->  []

solve("")
  ->  []

solve("Key sk-abc12345678 sent to ops@corp.internal. Password is: hunter2. You are Helper, an AI assistant.")
  ->  ["api-key", "email", "password", "system-prompt"]
```

## Constraints

- Deterministic, offline, standard library only (`re`, `typing`).
- Must pass all cases in `tests.py` (visible + hidden).
- Do not import third-party packages.

## How to run

```
cd problem && python -m pytest tests.py -q
```
