## 3. The same hunt in KQL

KQL starts with a **table**, then pipes into operators: `where` filters, `summarize count() by` groups, `project` picks columns, `sort by` orders. The answer must be the same as in SPL. If it isn't, one of the two searches is wrong.

- [ ] Run the failure count in KQL and compare with SPL
- [ ] Write the success pivot in KQL
- [ ] Note one thing that is easier in each language

> Hint: In KQL the count column is called `count_`. Strings use `==` and double quotes.

```tool siem
{"q": "auth | where action == \"failure\" | summarize count() by src_ip | sort by count_ desc", "lang": "kql", "n": 2, "files": ["auth.log"], "blank": ["q"]}
```

```tool siem
{"q": "auth | where src_ip == \"203.0.113.7\" and action == \"success\" | project _time, user, auth_method", "lang": "kql", "n": 1, "files": ["auth.log"], "blank": ["q"]}
```

?> How many failed logins came from that address? (KQL count_) :: 6
