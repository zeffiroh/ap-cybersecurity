## 4. Scope it with search

Before you escalate, know how big it is. Which laptop sent the most data out, where did it go, did anyone else talk to the same places, and what did the firewall stop?

- [ ] Which host sent the most bytes out? Is that normal for it?
- [ ] Who sends data to storage.cloudbox.example, and how much? (check intel.json: is that site allowed?)
- [ ] Who else asked DNS for ledgerpro-support.example?
- [ ] What did the firewall deny?
- [ ] Write the cloud-storage search in KQL

> Hint: `stats sum(bytes_out) as sent by src_host` adds up the bytes per laptop. Reception sends files to clients through cloud storage every day; compare its numbers with acc-lt03's.

```tool siem
{"q": "source=*fw_sessions.csv | stats sum(bytes_out) as sent by src_host | sort - sent", "n": 6, "files": ["fw_sessions.csv"], "blank": ["q"]}
```

```tool siem
{"q": "source=*fw_sessions.csv dst_host=storage.cloudbox.example | stats count sum(bytes_out) as sent by src_host", "n": 2, "files": ["fw_sessions.csv"], "blank": ["q"]}
```

```tool siem
{"q": "source=*dns.log ledgerpro-support.example | stats count by src_ip", "n": 1, "files": ["dns.log"], "blank": ["q"]}
```

```tool siem
{"q": "source=*fw_sessions.csv action=deny | table _time src_host dst_host dport app", "n": 2, "files": ["fw_sessions.csv"], "blank": ["q"]}
```

```tool siem
{"q": "fw_sessions | where dst_host == \"storage.cloudbox.example\" | summarize sum(bytes_out) by src_host", "lang": "kql", "n": 2, "files": ["fw_sessions.csv"], "blank": ["q"]}
```

?> Which host sent the most data out? :: acc-lt03

?> How many hosts sent data to storage.cloudbox.example? :: 2

?> Which site did the firewall block for acc-lt03? :: filedrop.example
