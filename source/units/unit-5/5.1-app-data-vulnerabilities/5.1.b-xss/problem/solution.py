import html


def render_comment(username: str, comment: str) -> str:
    """
    Context-aware output encoding: each user value is HTML-encoded before it is
    placed into the template, so user input is always rendered as text and can
    never be parsed as markup. The structural tags are the app's own HTML.
    """
    safe_user = html.escape(username, quote=True)
    safe_comment = html.escape(comment, quote=True)
    return '<div class="c"><b>' + safe_user + "</b>: " + safe_comment + "</div>"
