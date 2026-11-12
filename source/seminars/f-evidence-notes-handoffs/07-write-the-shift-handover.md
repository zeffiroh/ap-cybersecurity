## 7. Write the shift handover

Rewrite last night's "all quiet" note as a handover that leaves nothing behind. List every open item **by ID** with the next step and who owns it, what you closed, what to watch, who you called and when, and any temporary change that must be undone later.

- [ ] Every open item by ID, with next step and owner
- [ ] Closed items in one line each
- [ ] Things to watch on the next shift
- [ ] Calls and messages with times
- [ ] Temporary blocks or exceptions, with a review date

> Hint: A temporary block nobody remembers becomes a permanent one. Write down who may remove it, and when it should be reviewed.

```tool report
{"tpl": "handover", "title": "Shift handover: morning to afternoon, 02 Nov", "text": "# Shift handover: morning to afternoon, 02 Nov\n\n## Still open\n\n- INC-0211 (from AL-2203, AL-2204, AL-2205, AL-2208, AL-2210): ransomware on hr-pc07 and fs01. Contained at 09:52 UTC. Next: incident lead decides on restore from snapshot s-1101; IT ops owns it.\n- AL-2201: same campaign. Next: confirm whether dev.kapoor and tomas.reyes opened the invoice. Owner: afternoon analyst, by 14:00 UTC.\n- AL-2207: 6 failed network logons from 198.51.100.140 at 09:59 UTC for support_svc and Administrator. Next: confirm the account support_svc is disabled. Owner: IT ops.\n\n## Closed this shift\n\n- AL-2202: benign, the Singapore address is the company VPN exit.\n- AL-2206: benign, the antivirus update retried and worked at 09:25 UTC.\n- AL-2209: benign, a large print job on the second floor printer.\n\n## Watch for\n\n- Any connection from any host to 198.51.100.140 or cdn-update-check.net.\n- Any new account named support_svc on another host.\n- New files ending in .kestrel-locked on any share.\n\n## Calls and messages\n\n- 09:55 UTC: escalated to the incident lead by phone; answered, incident INC-0211 opened.\n- 10:02 UTC: messaged IT ops about the share; answered at 10:06 UTC.\n\n## Tools and access\n\nTemporary proxy block on kestrel-logistlcs.com and cdn-update-check.net added at 09:18 and 09:56 UTC. Review it on 09 Nov; do not remove it without the incident lead.\n", "n": 5, "blank": ["text"]}
```
