## 3. Finding 1: a login that trusts what you type

In the shop, the login puts the email straight into a SQL query inside quotes. End the quote and comment out the password check, and you're whoever you name. Prove it with **one** request in the web proxy, as admin, and stop there.

```tool proxy
{"m": "POST", "p": "/api/login", "h": "Content-Type: application/json", "b": "{\"email\": \"admin@nimbu.shop'--\", \"password\": \"x\"}", "s": 200, "blank": ["p", "b"]}
```

Then do the same in **Hack the shop** (mission "Log in as the admin"), and see the fix in the **SQL injection lab**: a parameterised query.

- [ ] The request, the response status and the role you got
- [ ] Why it works: the query the server built
- [ ] The fix, in one line a developer can follow
- [ ] The retest: the same request should now get 401

> Hint: `'--` closes the email's quote, and `--` starts a SQL comment, so `AND password = ...` is never checked.

?> Which HTTP status does the injected login get? :: 200
