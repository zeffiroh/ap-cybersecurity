## 3. What ran on hr-pc07

10.20.0.14 is hr-pc07, Priya Nair's HR laptop. The EDR process list shows every program that started and which program started it. Follow the chain from Word.

- [ ] What did Word start?
- [ ] What did that start, and what was left running?

> Hint: Follow the `ppid` column: each process's parent is the row whose `pid` matches it.

?> Which program did Word start? :: cmd.exe

?> Which program was left running from C:\Users\Public? :: svchost-upd.exe
