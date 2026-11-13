## 8. Detections for next time

The review and the policy close today's doors. Detections catch the next attempt. Write two Sigma rules, test them on the domain controller's log, and check they don't fire on normal traffic.

```tool sigma
{"rule": "title: Kerberoasting - many RC4 service tickets from one client\nid: 7b2c4f10-3a51-4e7d-9a2e-0c1d00000701\nstatus: experimental\ndescription: RC4 (0x17) service tickets for service accounts. Normal clients ask for AES tickets; an attacker asks for RC4 because it cracks offline.\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4769\n    TicketEncryptionType: '0x17'\n    ServiceName|startswith: 'svc-'\n  condition: selection\nfalsepositives:\n  - Very old systems that only speak RC4; list them and exclude by client address\nlevel: high\ntags:\n  - attack.credential_access\n  - attack.t1558.003\n", "n": 6, "ls": true, "blank": ["rule"]}
```

```tool sigma
{"rule": "title: DCSync - replication rights used by an account that isn't a domain controller\nid: 7b2c4f10-3a51-4e7d-9a2e-0c1d00000702\nstatus: experimental\ndescription: 4662 with DS-Replication-Get-Changes rights. Domain controllers (accounts ending in $) do this all day; a user account never should.\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4662\n    Properties|contains:\n      - '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2'\n      - '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'\n  filter_dcs:\n    SubjectUserName|endswith: '$'\n  condition: selection and not filter_dcs\nfalsepositives:\n  - Directory sync tools that run as a user account; give them a named exception\nlevel: critical\ntags:\n  - attack.credential_access\n  - attack.t1003.006\n", "n": 2, "ls": true, "blank": ["rule"]}
```

- [ ] The kerberoast rule matches the six RC4 tickets and no AES ones
- [ ] The DCSync rule matches adm.k.nair and not DC02$
- [ ] One line on how each rule could be evaded

> Hint: The DCSync rule uses a filter: match the replication right, then remove accounts ending in $. Without the filter it fires every two hours.

?> How many events does the DCSync rule match? :: 2
