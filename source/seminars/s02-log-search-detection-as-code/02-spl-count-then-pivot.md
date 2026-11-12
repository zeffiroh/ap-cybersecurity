## 2. SPL: count, then pivot

SPL reads left to right: a search, then a pipe `|`, then a command that works on the results. `stats count by src_ip` groups the failures by address, and `sort - count` puts the biggest first.

Then **pivot**: take the address you found and search for it again, this time for a success.

- [ ] Run the first search and read the table
- [ ] Change it to find the Accepted login from the same address
- [ ] Find what that user did with sudo

> Hint: Field names come from the parsed log: `action`, `src_ip`, `user`, `auth_method`. Click any field name in the results to add it to the search.

```tool siem
{"q": "sourcetype=syslog action=failure | stats count by src_ip | sort - count", "n": 2, "files": ["auth.log"], "blank": ["q"]}
```

```tool siem
{"q": "Accepted src_ip=203.0.113.7 | table _time user auth_method", "n": 1, "files": ["auth.log"], "blank": ["q"]}
```

```tool siem
{"q": "process=sudo | table _time user run_as command", "n": 1, "files": ["auth.log"], "blank": ["q"]}
```

?> Which address failed most often? :: 203.0.113.7

?> Which user did that address log in as? :: deploy

?> Which file did that user read with sudo? (full path) :: /etc/shadow
