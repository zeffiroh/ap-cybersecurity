## 7. Windows: the hop to reception

The reception PC saw those port 445 connections as **logons**. In the Security log, 4625 is a failed logon and 4624 a successful one; Logon Type 3 means over the network. 5140 is a share being opened and 5145 a file in it being read.

```tool events
{"file": "eventlogs/Security.jsonl", "ids": "4625", "q": "10.30.1.20", "n": 9, "blank": ["ids", "src", "q"]}
```

```tool events
{"file": "eventlogs/Security.jsonl", "ids": "4624, 5140, 5145", "q": "10.30.1.20", "n": 8, "blank": ["ids", "src", "q"]}
```

- [ ] How many failed logons came from appt01, for which account?
- [ ] When did the logon succeed, and with which Logon Type?
- [ ] Which share was opened, and which files were read?
- [ ] What kind of data is in that share? Why does that raise the stakes?

> Hint: The one 4625 on 5 Nov at 03:31 is the receptionist mistyping at the keyboard (Logon Type 2). It isn't part of this.

?> How many failed logons came from 10.30.1.20? :: 9

?> Which share did the attacker open on rcp-pc03? :: Scans

?> How many files were read from it? :: 6
