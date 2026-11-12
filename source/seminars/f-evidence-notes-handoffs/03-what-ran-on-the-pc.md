## 3. What ran on the PC

"HR PC slow, maybe virus" is a guess. The process list says exactly what ran, when and which program started it. Follow the `ppid` column: each process names its parent.

- [ ] Which program started cmd.exe? Should it ever do that?
- [ ] Where does the program PowerShell started live? Where does the real svchost.exe live?
- [ ] When did that program reach the file share?

> Hint: The real svchost.exe is in C:\Windows\System32 and runs as SYSTEM. A file called svchost-upd.exe in C:\Users\Public is pretending.

?> Which program started cmd.exe? (file name) :: WINWORD.EXE

?> What is the PID of svchost-upd.exe started by PowerShell? :: 4810
