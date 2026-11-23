## 3. Contain, then escalate

10.20.0.14 is hr-pc07, Priya Nair's HR laptop, and malware is running on it. **Contain first, investigate second.** In the Hacker Room, isolate hr-pc07 from the network (Remote desktop, or pull its cable in the Server room), then escalate alert AL-2203 with a note that says what you found and what you did.

If nobody contains it, at 09:41 the malware walks the file server and renames the HR share's files to `.kestrel-locked`.

- [ ] Isolate hr-pc07 before 09:41, and leave it switched on
- [ ] Escalate AL-2203: what fired, what you found, what you did, what you don't know yet

> Hint: Don't switch the laptop off: memory holds evidence. Isolating keeps it running but cut off.

?> Which alert should you escalate? (its ID) :: AL-2203

The full simulation, with Labs, goes further: who else received it, the download the proxy blocked, the process chain in Task Manager, ending the malware, and the hand-over to your lead, on a real-speed clock.
