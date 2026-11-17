## 3. One request, then stop

The login puts the email straight into a SQL query. Prove it with **one** POST to /api/login in the Web proxy, with the email `admin@nimbu.shop'--` and any password. Record the status and the role, and stop.

- [ ] The request, the status and the role you got
- [ ] Why it works, and the one-line fix
- [ ] The retest you'll ask for

> Hint: `'--` closes the quote and comments out the password check. The fix is a parameterised query.

?> Which HTTP status does the injected login get? :: 200
