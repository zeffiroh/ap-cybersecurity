## 6. Hunt the web attack in SPL and KQL

The same address also hit the web server. Find the scanner, the SQL injection, and what came after it. `uri_path` is the page without the query string, which makes grouping easy.

- [ ] Which tool did the attacker use? (look at the user agent)
- [ ] Which page did they upload, and what commands did they run through it?
- [ ] Write both searches into your hunt pack

> Hint: `%20` is a space and `%27` is a quote in a URL. CyberChef's URL Decode makes the commands readable.

```tool siem
{"q": "sourcetype=access_combined useragent=sqlmap* | table _time clientip uri status", "n": 4, "files": ["access.log"], "blank": ["q"]}
```

```tool siem
{"q": "sourcetype=access_combined clientip=203.0.113.7 uri_path=/uploads/img.php | table _time uri status", "n": 3, "files": ["access.log"], "blank": ["q"]}
```

```tool siem
{"q": "access | where clientip == \"203.0.113.7\" and uri_path == \"/uploads/img.php\" | project _time, uri, status", "lang": "kql", "n": 3, "files": ["access.log"], "blank": ["q"]}
```

?> Which scanner's name is in the user agent? :: sqlmap

?> Which file did the attacker run commands through? (file name) :: img.php
