## 4. The process tree: from a shell to the keys

Every program has a parent. The process tree shows who started what, so you can follow the attacker's hands on each machine. The tool flags the usual tells: programs in folders anyone can write to, hidden PowerShell, downloads, deleting backups.

```tool proctree
{"marks": ["eng-ws14|6344", "eng-ws14|6402", "eng-ws14|6418", "eng-ws14|6440", "eng-ws14|6511", "eng-ws14|6630", "eng-ws14|6711", "eng-ws14|6790", "fs02|4410", "fs02|4422", "fs02|4512", "fs02|4514", "fs02|4530", "fs02|4601"], "n": 14, "files": ["process.csv"], "blank": ["marks"]}
```

- [ ] On eng-ws14: what did the attacker run from the RDP session's cmd.exe, in order?
- [ ] Which process read lsass's memory, and with which DLL?
- [ ] On fs02: what started the encryption, and what ran just before it?
- [ ] Mark every attacker process

> Hint: comsvcs.dll is a real Windows DLL; its MiniDump function writes a process's memory to a file. Attackers use it because it's already on every machine.

?> Which DLL was used to dump lsass's memory? :: comsvcs.dll

?> Which service started the programs on fs02? :: WinUpdSvc
