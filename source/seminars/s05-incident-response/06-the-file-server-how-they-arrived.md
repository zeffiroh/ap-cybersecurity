## 6. The file server: how they arrived

On fs02 the same night looks like an administrator logging on over the network and installing a service. Read it in fs02's own logs, then compare with the Hayabusa and Velociraptor output the team captured.

```tool events
{"file": "eventlogs/fs02-Security.jsonl", "ids": "4624, 4672, 5140", "q": "adm.rjoshi", "n": 3, "blank": ["ids", "src", "q"]}
```

```tool events
{"file": "eventlogs/fs02-System.jsonl", "ids": "7045", "n": 1, "blank": ["ids", "src", "q"]}
```

- [ ] When did adm.rjoshi log on, from where, with which package (Kerberos or NTLM)?
- [ ] Which share was used to copy the service file?
- [ ] Which service was installed, running as whom?
- [ ] What did Hayabusa flag as critical?

> Hint: An administrator normally logs on with Kerberos. NTLM from a design workstation at 23:20 on a Friday, six seconds before a new service, is the pass-the-hash pattern.

?> From which IP address did adm.rjoshi log on to fs02? :: 10.50.2.14

?> Which command deleted the shadow copies? :: vssadmin delete shadows /all /quiet
