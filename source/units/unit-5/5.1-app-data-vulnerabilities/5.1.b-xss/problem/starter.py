import html  # noqa: F401  (you will need this to fix the function)


def render_comment(username: str, comment: str) -> str:
    """
    Return the HTML card that displays a visitor's comment:

        <div class="c"><b>USERNAME</b>: COMMENT</div>

    VULNERABLE starter: it concatenates the username and comment straight into
    the HTML, so a comment like <script>steal()</script> is sent to the next
    visitor's browser as a real script tag (reflected XSS).

    Fix it with context-aware OUTPUT ENCODING: HTML-encode each user value
    (html.escape(value, quote=True)) before placing it into the template, so the
    browser can never parse user input as markup. Do not strip or blocklist input;
    keep the structural <div>/<b> tags as real HTML.
    """
    return '<div class="c"><b>' + username + "</b>: " + comment + "</div>"
