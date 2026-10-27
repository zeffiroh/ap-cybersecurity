# Coding problem, 5.1.b: Fix the Reflected Comment

**Skill:** Mitigate Risk · **Maps to:** 5.1.A, 5.1.B · **Language:** Python 3 (pytest)

## The situation
`render_comment` builds the HTML that shows a visitor's comment on a page. It works for
ordinary text, but it drops the username and comment **straight into the HTML** by string
concatenation. That is reflected cross-site scripting (XSS): whatever the user typed is parsed
by the next visitor's browser as markup, so `<script>...</script>` in a comment becomes a live
script running in that visitor's session.

The starter is the vulnerable version. A comment of `<script>steal()</script>` comes back out
as a real `<script>` tag.

## Your task
Fix `render_comment` so user input can never be parsed as HTML. The correct defense is
**context-aware output encoding**: HTML-encode every user-supplied value before it goes into the
page, so `<` becomes `&lt;`, `>` becomes `&gt;`, `&` becomes `&amp;`, and the quote characters
are encoded too. Python's standard library does exactly this:

```python
import html
safe = html.escape(user_value, quote=True)
```

Encode the `username` and `comment` values, then place them into the same HTML template. Do
**not** detect, strip, or blocklist payloads — the point is that *encoded* input is harmless no
matter what it contains, while the app's own structural tags stay intact.

## Function contract
Implement `render_comment(username: str, comment: str) -> str`:
- Return the comment card HTML: `<div class="c"><b>USERNAME</b>: COMMENT</div>`, where
  `USERNAME` and `COMMENT` are the HTML-encoded user values.
- The structural tags (`<div class="c">`, `<b>`) are the app's own output and stay as real HTML.

## How to run
```
cd problem && python -m pytest tests.py -q
```
A correct solution passes every test, including the injection cases. The concatenation version
fails them because the raw `<script>` and `<img onerror=...>` payloads reach the output as markup.
