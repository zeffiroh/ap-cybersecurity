## 9. Shift report

Close your shift. Everything open, by ID, with an owner. Everything closed in one line. What the morning should watch. Who you called and when. How many hints you opened.

- [ ] Open items by ID with owners
- [ ] Closed items
- [ ] Watch list including your new rule
- [ ] Calls with times
- [ ] Hints opened

```tool report
{"tpl": "handover", "title": "Shift report: night shift, 11 to 12 Nov", "text": "# Shift report: night shift, 11 to 12 Nov\n\n## Still open\n\n- INC-1112 (AL-8401, AL-8403, AL-8404, AL-8406, AL-8408): client files copied from acc-lt03 to cloud storage through a remote access tool. Escalated at 01:18 UTC. Next: client isolates the laptop; morning analyst lists exactly which files were copied and helps the client decide who must be told. Owner: morning shift lead.\n- AL-8412: unknown device android-7f3a on the staff Wi-Fi. Needs more information: ask the client's office manager whether a staff member connected a new phone today. Owner: morning analyst, by 03:00 UTC.\n\n## Closed this shift\n\n- AL-8402: benign, a.nguyen's own inbox rule for tax-office letters, made in Outlook from the office.\n- AL-8405: benign, Windows Update restarts during the patch push CHG-0417.\n- AL-8407: benign, typing mistakes with Caps Lock on, then a good logon from the same desk.\n- AL-8409: benign, the monthly archive job CHG-0412.\n- AL-8410: benign, service installed during the patch window CHG-0418.\n- AL-8411: benign, new phone, MFA approved, from the office's own address.\n\n## Watch for\n\n- Any host contacting ledgerpro-support.example, relay.remotehelper.example or downloads.toolmirror.example.\n- Any RemoteHelper service, or any program whose OriginalFileName is rclone.exe.\n- New rule \"Renamed rclone\" goes live tonight in test mode: check its hits.\n\n## Calls and messages\n\n- 01:18 UTC: called the client's practice principal; answered, approved isolation at 01:24 UTC.\n- 01:35 UTC: messaged the morning shift lead with the escalation; read at 01:37 UTC.\n\n## Tools and access\n\nWatch list entries for the three domains added at 01:10 UTC; review on 19 Nov. Hints opened: 0.\n", "n": 5, "blank": ["text"]}
```
