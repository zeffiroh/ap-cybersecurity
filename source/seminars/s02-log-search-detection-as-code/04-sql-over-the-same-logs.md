## 4. SQL over the same logs

Every log is also a table. The SQL tool names each table after its file (`auth`, `access`, `security`) and makes a column for each field. SQL is the language behind most data lakes, so it is worth having in your pocket.

- [ ] Count requests per client address in the web log
- [ ] Find every request from 203.0.113.7 that got status 200
- [ ] Join the idea back to the SSH hunt: same attacker?

> Hint: `GROUP BY clientip ORDER BY hits DESC` is the SQL version of `stats count by clientip | sort - count`.

```tool sql
{"q": "SELECT clientip, COUNT(*) AS hits FROM access GROUP BY clientip ORDER BY hits DESC", "n": 3, "files": ["access.log"], "blank": ["q"]}
```

?> How many requests did 203.0.113.7 make to the web server? :: 9
