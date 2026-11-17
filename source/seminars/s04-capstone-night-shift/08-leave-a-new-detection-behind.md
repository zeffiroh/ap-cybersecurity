## 8. Leave a new detection behind

The client's upload rule (AL-8406) fired at 00:46, thirty minutes after the copy started, because it waits for 1 GB. Write a better one: something the copy tool did **before** any data moved, that normal programs don't do. Test it, and write what would make it noisy.

- [ ] A Sigma rule on Sysmon process events
- [ ] Test it: it should match the renamed copy tool and nothing else
- [ ] When would it have fired, compared with AL-8406?
- [ ] One tuning note

> Hint: Sysmon records OriginalFileName from inside the program, so renaming the file doesn't change it. A program whose OriginalFileName is rclone.exe but whose file name is something else is hiding.

```tool sigma
{"rule": "title: Renamed rclone\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000402\nstatus: experimental\ndescription: rclone copies files to cloud storage. Running it under another name is how attackers hide data theft.\nlogsource:\n  product: windows\n  service: sysmon\ndetection:\n  selection:\n    EventID: 1\n    OriginalFileName: 'rclone.exe'\n  filter:\n    Image|endswith: '\\rclone.exe'\n  condition: selection and not filter\nfalsepositives:\n  - IT tools that bundle rclone under their own name (list them by path and signer)\nlevel: high\ntags:\n  - attack.exfiltration\n  - attack.t1567.002\n  - attack.defense_evasion\n  - attack.t1036\n", "n": 3, "ls": true, "blank": ["rule"]}
```

?> How many events does your renamed-rclone rule match? :: 3

?> How many minutes before AL-8406 would it have fired? :: 32
