## 5. From a service account to the domain

An hour later svc-sql logs on to app02. Follow it: what did it run, what was it after, and what happened on the domain controller next? On the DC, a 4662 with the replication rights is a **DCSync**: asking the DC for every password hash, the way another DC would. Only domain controllers should ever do that.

```tool events
{"file": "eventlogs/app02-Security.jsonl", "ids": "4624, 4672, 4688", "q": "svc-sql", "n": 5, "blank": ["ids", "src", "q"]}
```

```tool events
{"file": "eventlogs/dc01-Security.jsonl", "ids": "4662", "n": 5, "blank": ["ids", "src", "q"]}
```

- [ ] When did svc-sql log on to app02, from where?
- [ ] Why save the SECURITY and SYSTEM hives? (what's inside)
- [ ] What was the findstr looking for?
- [ ] Which 4662 events are DCSync by someone who isn't a DC?

> Hint: The SECURITY hive holds LSA secrets, including the saved password of every scheduled task. DC02$ is the other domain controller; its replication is normal.

?> Which account performed the DCSync? :: adm.k.nair

?> From which address did that account log on to dc01? :: 10.60.1.22
