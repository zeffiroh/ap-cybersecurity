import sqlite3


def authenticate(users, username, password):
    """
    Return the role of the user whose username AND password both match a row,
    or None if the login fails.

    VULNERABLE starter: it concatenates user input into the SQL text, so an
    attacker can inject SQL. Rewrite the query to use parameter placeholders (?)
    with the values passed separately, so input can never change the query's
    structure. Do not blocklist input; fix the query itself.
    """
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (username TEXT, role TEXT, password TEXT)")
    cur.executemany("INSERT INTO users VALUES (?, ?, ?)", users)

    # --- the injectable part: user input is glued straight into the SQL text ---
    query = (
        "SELECT role FROM users WHERE username = '"
        + username + "' AND password = '" + password + "'"
    )
    try:
        cur.execute(query)
        row = cur.fetchone()
    except sqlite3.Error:
        row = None
    conn.close()
    return row[0] if row else None
