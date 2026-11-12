## 5. Parse a raw log into fields

Searches only work on fields someone parsed. When a new log arrives that your SIEM doesn't know, you write the parser. The log parser uses `%{TYPE:name}` pieces, the same idea as Grok in log pipelines.

The pattern below parses SSH login lines. Lines it can't parse are shown in red: decide whether that is right.

- [ ] Run the pattern on auth.log
- [ ] Which line doesn't parse, and why is that fine?
- [ ] Write a second pattern for the sudo line

> Hint: The sudo line has a different shape: `sudo:   deploy : TTY=... ; COMMAND=...`. Start with `%{SYSLOGTIMESTAMP:time} %{HOSTNAME:host} sudo: +%{USER:user} : %{GREEDYDATA:rest}`.

```tool parse
{"file": "case/auth.log", "pat": "%{SYSLOGTIMESTAMP:time} %{HOSTNAME:host} sshd\\[%{INT:pid}\\]: %{WORD:result} %{WORD:method} for (?:invalid user )?%{USER:user} from %{IP:src_ip} port %{INT:src_port}%{GREEDYDATA:rest}", "n": 11, "blank": ["pat"]}
```

?> How many of the 12 lines does the SSH pattern parse? :: 11
