# Interface, 5.1.b-encoded-comment

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def render_comment(username: str, comment: str) -> str
```

## Input
- `username`: the commenter's display name (untrusted input).
- `comment`: the comment body (untrusted input).

## Output
A single HTML string, the comment card:
```
<div class="c"><b>USERNAME</b>: COMMENT</div>
```
where `USERNAME` and `COMMENT` are the HTML-encoded forms of the two inputs.

## Encoding rules
- User values are HTML-encoded with `html.escape(value, quote=True)` semantics:
  `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`, `'` → `&#x27;`.
- The structural markup the function itself emits (`<div class="c">`, `<b>`, `</b>`, `</div>`)
  is real HTML and is **not** encoded.
- No detection, stripping, or blocklisting of input. Encoding alone is the defense.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only (`html`).

## Acceptance
`python -m pytest tests.py -q` passes, including the injection cases, which succeed only when the
user values are encoded rather than concatenated raw.
