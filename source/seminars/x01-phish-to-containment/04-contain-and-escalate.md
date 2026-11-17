## 4. Contain, then escalate

You know enough: hr-pc07 opened a macro document, and malware is running on it. **Contain first, investigate second.** In the Hacker Room, isolate hr-pc07 from the network (Remote desktop, or shut its switch port in the Server room), end the malware's process, and escalate alert AL-2203 with a note that says what you found and what you did.

If nobody contains it, at 09:41 the malware walks the file server and renames the HR share's files to `.kestrel-locked`. `share_listing.txt` shows what that looks like.

- [ ] Isolate hr-pc07 before 09:41
- [ ] End svchost-upd.exe
- [ ] Escalate AL-2203: what fired, what you found, what you did, what you don't know yet

> Hint: Don't switch the laptop off: memory holds evidence. Isolating keeps it running but cut off.

?> Which alert should you escalate? (its ID) :: AL-2203
