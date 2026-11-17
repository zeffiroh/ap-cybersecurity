## 7. Hunt the web attack in SPL and KQL

The SSH password guessing failed. So how did the attacker have catalog's password 40 minutes later? Look at the web log. `uri_path` is the page without the query string, which makes grouping easy.

- [ ] Which tool did the attacker use? (look at the user agent)
- [ ] Which database table did the injection read?
- [ ] What did they do in the admin pages, and how big was it?
- [ ] Write both searches into your hunt pack

> Hint: `%20` is a space, `%27` is a quote and `%3D` is `=` in a URL. CyberChef's URL Decode makes the requests readable.

```tool siem
{"q": "sourcetype=access_combined useragent=sqlmap* | table _time clientip uri status", "n": 7, "files": ["access.log"], "blank": ["q"]}
```

```tool siem
{"q": "sourcetype=access_combined clientip=203.0.113.45 uri_path=/admin* | table _time method uri status bytes", "n": 4, "files": ["access.log"], "blank": ["q"]}
```

```tool siem
{"q": "access | where clientip == \"203.0.113.45\" and uri_path startswith \"/admin\" | project _time, method, uri, status, bytes", "lang": "kql", "n": 4, "files": ["access.log"], "blank": ["q"]}
```

?> Which scanner's name is in the user agent? :: sqlmap

?> Which table held the staff passwords? :: staff_users

?> Which admin page did the attacker download? (the path, without ?from=...) :: /admin/orders/export
