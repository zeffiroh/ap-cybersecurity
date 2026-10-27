# Coding problem, 5.1.a: Fix the Injectable Login

**Skill:** Mitigate Risk · **Maps to:** 5.1.A, 5.1.B · **Language:** Python 3 (pytest, sqlite3)

## The situation
The `authenticate` function below is the login check for a small app. It works for normal
users, but it builds its SQL query by **concatenating** the username and password straight
into the query text. That is the exact flaw that makes SQL injection possible: an attacker
who types SQL syntax instead of a username can change what the query *means*.

The starter code is the vulnerable version. Run the tests and you will see the injection
cases fail: inputs like `admin'--` and `' OR '1'='1` log in **without the real password**.

## Your task
Rewrite `authenticate` so that user input can never change the structure of the query. Use a
**parameterized query** (a prepared statement): pass the SQL template with `?` placeholders and
the user values as a separate tuple, and let the database driver bind them as data.

```python
cur.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
```

When you do this, the injection inputs are treated as ordinary (non-existent) usernames, so
they return no row, while genuine credentials still succeed.

## Function contract
Implement `authenticate(users, username, password) -> str | None` in `starter.py`:
- `users` is a list of `(username, role, password)` tuples to load into an in-memory table.
- Return the matching user's `role` if (and only if) both username and password match a row.
- Return `None` for any failed or injected login.

Do **not** filter or blocklist the input, and do **not** compare the lists in Python. The whole
point is that the *database query itself* must be safe. Use `sqlite3` with `:memory:`.

## How to run
```
cd problem && python -m pytest tests.py -q
```
A correct solution passes every test, including the injection cases. A string-concatenation
version will fail them, because the injected input logs in.
