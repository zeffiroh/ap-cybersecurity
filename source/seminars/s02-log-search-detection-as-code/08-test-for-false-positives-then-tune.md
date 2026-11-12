## 8. Test for false positives, then tune

A rule that fires on everything is worse than no rule: people stop reading it. Test every rule twice: does it catch the attack (**true positives**) and does it stay quiet on normal work (**false positives**)?

The first rule below is deliberately noisy. Tick the events that are really malicious; the tool scores precision. Then use the tuned rules, which each describe one thing an attacker did.

- [ ] Run the noisy rule and tick the malicious events
- [ ] Run each tuned rule: each should match only attack events
- [ ] Write one tuning note per rule: what it misses, and what would make it noisy

> Hint: Good rules describe behaviour that normal users don't have: a program in C:\Users\Public, shadow copies deleted, a new member of Administrators.

```tool sigma
{"rule": "title: Any new process on a workstation\nstatus: experimental\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4688\n  condition: selection\nlevel: low\n", "n": 15, "ls": true, "blank": ["rule"]}
```

```tool sigma
{"rule": "title: Program started from C:\\Users\\Public\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000002\nstatus: experimental\ndescription: Programs should not run from the Public profile, which every user can write to.\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4688\n    NewProcessName|contains: '\\Users\\Public\\'\n  condition: selection\nfalsepositives:\n  - Badly packaged software installed to the Public profile (check with IT)\nlevel: high\ntags:\n  - attack.defense_evasion\n  - attack.t1036.005\n", "n": 2, "ls": true, "blank": ["rule"]}
```

```tool sigma
{"rule": "title: Shadow copies deleted\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000003\nstatus: experimental\ndescription: Ransomware deletes Volume Shadow Copies so files can't be restored.\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4688\n    CommandLine|contains|all:\n      - 'vssadmin'\n      - 'delete shadows'\n  condition: selection\nfalsepositives:\n  - Backup software clearing old copies (it rarely uses /all /quiet)\nlevel: critical\ntags:\n  - attack.impact\n  - attack.t1490\n", "n": 1, "ls": true, "blank": ["rule"]}
```

```tool sigma
{"rule": "title: Account added to the local Administrators group\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000004\nstatus: experimental\ndescription: A new member of Administrators on a workstation needs a change ticket.\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4732\n    TargetUserName: 'Administrators'\n  condition: selection\nfalsepositives:\n  - IT adding a helpdesk account during a planned change\nlevel: high\ntags:\n  - attack.persistence\n  - attack.t1136.001\n", "n": 1, "ls": true, "blank": ["rule"]}
```

?> How many events does the noisy "any new process" rule match? :: 15

?> Which command deleted the shadow copies? (program name) :: vssadmin.exe
