import html


def render_comment(username: str, comment: str) -> str:
    safe_user = html.escape(username, quote=True)
    safe_comment = html.escape(comment, quote=True)
    return '<div class="c"><b>' + safe_user + "</b>: " + safe_comment + "</div>"
