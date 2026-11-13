## 5. Memory: what the RAM remembered

The incident team took a memory image of eng-ws14 at 01:14 and ran Volatility on it. We can't re-run Volatility in the browser, but we can read its saved output. Memory shows things logs can miss: exited processes, the command lines, network connections and who was in which session.

- [ ] Which PID is lsass, and which process dumped it?
- [ ] What did nt.exe do with the dump?
- [ ] Which account and password hash did px.exe use, against which server?
- [ ] Which session were they in, and whose was the other one?

> Hint: In px.exe's command line, -H is an NTLM hash. Using a hash instead of a password is "pass the hash". The netscan line shows the connection it made.

?> What is lsass's PID on eng-ws14? :: 724

?> Which account did px.exe use on fs02? :: adm.rjoshi

?> In which RDP session number was the attacker? :: 3
