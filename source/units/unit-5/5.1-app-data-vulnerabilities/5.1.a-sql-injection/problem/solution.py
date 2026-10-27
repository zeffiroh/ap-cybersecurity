import sqlite3


def authenticate(users, username, password):
    """
    Parameterized login: the SQL template is fixed and the user values are bound
    separately as data, so injected SQL syntax is treated as an ordinary (and
    non-existent) username rather than as part of the query structure.
    """
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (username TEXT, role TEXT, password TEXT)")
    cur.executemany("INSERT INTO users VALUES (?, ?, ?)", users)

    cur.execute(
        "SELECT role FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
