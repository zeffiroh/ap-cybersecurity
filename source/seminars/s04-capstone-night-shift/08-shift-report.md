## 8. Shift report

Close your shift. Everything open, by ID, with an owner. Everything closed in one line. What the morning should watch. Who you called and when. How many hints you opened.

- [ ] Open items by ID with owners
- [ ] Closed items
- [ ] Watch list including your new rule
- [ ] Calls with times
- [ ] Hints opened

```tool report
{"tpl": "handover", "title": "Shift report: night shift, 5 Nov", "text": "# Shift report: night shift, 5 Nov\n\n## Still open\n\n- INC-0505 (AL-7301, AL-7303, AL-7304, AL-7306, AL-7308): DNS tunnel from fin-lt04. Escalated at 11:55 UTC. Next: client isolates the laptop; morning analyst rebuilds what was sent from the TXT names. Owner: morning shift lead.\n- AL-7312: anonymising relay from guest Wi-Fi. Needs more information: ask the client whether guest Wi-Fi keeps DHCP logs. Owner: morning analyst, by 04:30 UTC.\n\n## Closed this shift\n\n- AL-7302: benign, Finance opened a workbook from the issued encrypted USB key.\n- AL-7305: benign, the chat app's normal background start.\n- AL-7307: benign, VPN CPU during the update push.\n- AL-7309: benign, typing mistakes then a good logon from the same desk.\n- AL-7310: benign, service installed under change CHG-2291.\n- AL-7311: benign, printer looking for a retired share; the client's IT will fix the printer.\n\n## Watch for\n\n- Any host asking for cloudmetric.example or taxhelp-tools.example.\n- Any new task named TeamsUpdateCheck, or msteams-update.exe in AppData.\n- New rule \"TXT lookups from a program in the user profile\" goes live tonight in test mode: check its hits.\n\n## Calls and messages\n\n- 11:55 UTC: called the client duty manager; answered, approved isolation at 12:02 UTC.\n- 12:10 UTC: messaged the morning shift lead with the escalation; read at 12:12 UTC.\n\n## Tools and access\n\nWatch list entries for cloudmetric.example and taxhelp-tools.example added at 11:50 UTC; review on 12 Nov. Hints opened: 0.\n", "n": 5, "blank": ["text"]}
```
