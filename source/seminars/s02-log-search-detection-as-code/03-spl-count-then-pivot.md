## 3. SPL: count, then pivot

SPL reads left to right: a search, then a pipe `|`, then a command that works on the results. `stats count by src_ip` groups the failures by address, and `sort - count` puts the biggest first.

Then **pivot**: take what you found and search again from a new angle. First the address, then the account it reached, then what that account did.

- [ ] Run the failure count and read the table
- [ ] Find the Accepted login from the same address
- [ ] Find where that account normally logs in from
- [ ] Find what it did with sudo, and compare with its normal sudo use

> Hint: Field names come from the parsed log: `action`, `src_ip`, `user`, `auth_method`, `process`, `command`. Click any field name in the results to add it to the search.

```tool siem
{"q": "sourcetype=syslog action=failure | stats count by src_ip | sort - count", "n": 2, "files": ["auth.log"], "blank": ["q"]}
```

```tool siem
{"q": "Accepted src_ip=203.0.113.45 | table _time user auth_method", "n": 1, "files": ["auth.log"], "blank": ["q"]}
```

```tool siem
{"q": "process=sshd user=catalog | table _time src_ip action", "n": 5, "files": ["auth.log"], "blank": ["q"]}
```

```tool siem
{"q": "process=sudo | table _time user run_as command", "n": 3, "files": ["auth.log"], "blank": ["q"]}
```

?> Which address failed most often? :: 203.0.113.45

?> Which account did that address log in as? :: catalog

?> From which address does that account normally log in? :: 10.30.0.30

?> Which program did the attacker run with sudo to copy every database? (program name) :: mysqldump
