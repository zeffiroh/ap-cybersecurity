## 7. Write the shift handover

Rewrite "quiet night" as a handover that leaves nothing behind: every open item by ID with the next step and owner, what you closed, what to watch, who you called and when, and every temporary change with a review date.

- [ ] Every open item by ID, with next step and owner
- [ ] Closed items in one line each
- [ ] Things to watch on the next shift
- [ ] Calls and messages with times
- [ ] Temporary blocks or exceptions, with a review date

```tool report
{"tpl": "handover", "title": "Shift handover: morning to afternoon, 10 Nov", "text": "# Shift handover: morning to afternoon, 10 Nov\n\n## Still open\n\n- INC-0312 (from AL-3303, AL-3304, AL-3305, AL-3307, AL-3309, AL-3311): ransomware on acct-lt04 and fs02. Contained at 11:14 UTC. Next: incident lead decides on restoring the Accounts and Purchase shares; IT ops owns it.\n- AL-3301: same campaign. Next: confirm whether kiran.joshi opened the archive. Owner: afternoon analyst, by 14:00 UTC.\n- AL-3310: 5 failed VPN logons from 198.51.100.77 at 11:19 UTC for svc_sync and Administrator. Next: confirm svc_sync is disabled everywhere. Owner: IT ops.\n\n## Closed this shift\n\n- AL-3302: benign, the Frankfurt address is the company's cloud VPN gateway.\n- AL-3306: benign, the erp01 backup finished 40 minutes late but was complete and verified.\n- AL-3308: benign, a barcode scanner on the asset list plugged into wh-pc02.\n\n## Watch for\n\n- Any connection from any host to 198.51.100.77 or files-cdn-sync.example.\n- Any sign-in or new account named svc_sync.\n- New files ending in .saffron-locked on any share.\n\n## Calls and messages\n\n- 11:16 UTC: escalated to the incident lead by phone; answered, incident INC-0312 opened.\n- 11:22 UTC: messaged IT ops about the shares and the VPN account; answered at 11:25 UTC.\n\n## Tools and access\n\nTemporary proxy block on swiftroute-delivery.example and files-cdn-sync.example added at 10:34 and 11:16 UTC. Review it on 17 Nov; do not remove it without the incident lead.\n", "n": 5, "blank": ["text"]}
```
