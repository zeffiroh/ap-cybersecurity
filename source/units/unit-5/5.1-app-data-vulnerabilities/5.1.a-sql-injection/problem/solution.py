import sqlite3


def authenticate(users, username, password):
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
