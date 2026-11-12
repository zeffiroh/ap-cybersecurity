## 3. Scope it with search

Before you escalate, know how big it is. Which hosts talk to the odd domain, how many times, and did anything get past the proxy?

- [ ] Which client sends the most DNS queries? Is that normal for it? (dns_stats.csv)
- [ ] Who else asked for cloudmetric.example?
- [ ] What did the proxy let through and block for that laptop?
- [ ] Write the same scoping search in KQL

> Hint: The very long names all end in cloudmetric.example. Count by `src_ip` to see who asks for it.

```tool siem
{"q": "source=*dns.log | stats count by src_ip | sort - count", "n": 6, "files": ["dns.log"], "blank": ["q"]}
```

```tool siem
{"q": "source=*dns.log cloudmetric.example | stats count by src_ip", "n": 1, "files": ["dns.log"], "blank": ["q"]}
```

```tool siem
{"q": "source=*proxy.log src_ip=10.70.0.44 | table _time action url category", "n": 5, "files": ["proxy.log"], "blank": ["q"]}
```

```tool siem
{"q": "dns | where query endswith \"cloudmetric.example\" | summarize count() by src_ip", "lang": "kql", "n": 1, "files": ["dns.log"], "blank": ["q"]}
```

?> How many DNS queries did 10.70.0.44 send in dns.log? :: 59

?> How many different clients queried cloudmetric.example? :: 1

?> Which site did the proxy block? :: pastebox.example
