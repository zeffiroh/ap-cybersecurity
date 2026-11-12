## 7. Leave a new detection behind

The client's rule fired 32 minutes after the tunnel started. Write a better one: something the tunnel does that normal programs don't. Test it, and write what would make it noisy.

- [ ] A Sigma rule on Sysmon DNS events
- [ ] Test it: it should match the tunnel and not the browser
- [ ] One tuning note

> Hint: Browsers and the Windows resolver live in Program Files and System32. The tunnel program lives in AppData and asks for TXT records.

```tool sigma
{"rule": "title: TXT lookups from a program in the user profile\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000401\nstatus: experimental\ndescription: Programs in AppData making DNS TXT queries is how DNS tunnels move data. Browsers and the OS resolver don't live there.\nlogsource:\n  product: windows\n  service: sysmon\ndetection:\n  selection:\n    EventID: 22\n    QueryType: 'TXT'\n    Image|contains: '\\\\AppData\\\\'\n  condition: selection\nfalsepositives:\n  - Some chat and sync apps install per user in AppData; list the ones you allow\nlevel: high\ntags:\n  - attack.exfiltration\n  - attack.t1048.003\n", "n": 26, "ls": true, "blank": ["rule"]}
```

?> How many events does your TXT-from-AppData rule match? :: 26
