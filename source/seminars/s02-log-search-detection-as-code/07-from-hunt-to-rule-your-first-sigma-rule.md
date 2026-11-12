## 7. From hunt to rule: your first Sigma rule

A hunt you run once finds one attack. A **rule** finds the next one. Sigma is the open format for detection rules: one YAML file that converts to SPL, KQL and others.

Switch to the Windows case. On hr-pc07 Word started cmd.exe. The rule below fires on that, and on Excel or Outlook doing the same. Press **Test**, then **Convert with pySigma** to see the real converter's SPL.

- [ ] Test the rule: how many events match?
- [ ] Convert it with pySigma and compare with a search you would write by hand
- [ ] Why does PowerShell not match? (look at its parent)

> Hint: PowerShell's parent was cmd.exe, not Word. One rule per step of the chain, or a second rule for "cmd.exe starts PowerShell hidden".

```tool siem
{"q": "EventID=4688 | stats count by Computer", "n": 1, "files": ["case/eventlogs/Security.jsonl"], "blank": ["q"]}
```

```tool sigma
{"rule": "title: Office program starts a command shell\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000001\nstatus: experimental\ndescription: Word, Excel or Outlook starting cmd.exe or PowerShell is how most macro malware begins.\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4688\n    ParentProcessName|endswith:\n      - '\\WINWORD.EXE'\n      - '\\EXCEL.EXE'\n      - '\\OUTLOOK.EXE'\n    NewProcessName|endswith:\n      - '\\cmd.exe'\n      - '\\powershell.exe'\n  condition: selection\nfalsepositives:\n  - Office add-ins that call a script on purpose (rare; list them)\nlevel: high\ntags:\n  - attack.execution\n  - attack.t1204.002\n", "n": 1, "ls": true, "blank": ["rule"]}
```

?> How many process-creation events (4688) are in Security.jsonl? :: 15

?> How many events does the Office-starts-a-shell rule match? :: 1
