## 5. SQL over the same logs

Every log is also a table. The SQL tool names each table after its file (`auth`, `access`, `security`) and makes a column for each field. SQL is the language behind most data lakes, so it is worth having in your pocket.

- [ ] Count requests per client address in the shop's web log
- [ ] Find every request with UNION in it
- [ ] Join the idea back to the SSH hunt: same address?

> Hint: `GROUP BY clientip ORDER BY hits DESC` is the SQL version of `stats count by clientip | sort - count`. `LIKE '%UNION%'` finds the word anywhere in a column.

```tool sql
{"q": "SELECT clientip, COUNT(*) AS hits FROM access GROUP BY clientip ORDER BY hits DESC", "n": 10, "files": ["access.log"], "blank": ["q"]}
```

```tool sql
{"q": "SELECT clientip, status, uri FROM access WHERE uri LIKE '%UNION%'", "n": 3, "files": ["access.log"], "blank": ["q"]}
```

?> How many requests did 203.0.113.45 make to the shop? :: 12
