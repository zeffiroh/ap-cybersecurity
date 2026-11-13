## 8. Contain and fix

Order the containment, then prove the cloud fix with a replay.

```tool cloudiam
{"pol": "{\n \"account\": \"indigo-prod\",\n \"identities\": [\n  {\n   \"name\": \"payroll-backup\",\n   \"type\": \"user\",\n   \"note\": \"key in backup-config.ps1; nightly upload of D:\\\\exports from pay-app01 (office egress 203.0.113.88)\",\n   \"policies\": [\n    {\n     \"name\": \"upload-exports-only\",\n     \"statements\": [\n      {\n       \"effect\": \"Allow\",\n       \"actions\": [\n        \"PutObject\"\n       ],\n       \"resources\": [\n        \"bucket/payroll-exports/*\"\n       ],\n       \"conditions\": {\n        \"source_ip\": [\n         \"203.0.113.88/32\"\n        ]\n       }\n      }\n     ]\n    }\n   ]\n  },\n  {\n   \"name\": \"c.iyer\",\n   \"type\": \"user\",\n   \"note\": \"cloud administrator\",\n   \"policies\": [\n    {\n     \"name\": \"admin\",\n     \"statements\": [\n      {\n       \"effect\": \"Allow\",\n       \"actions\": [\n        \"*\"\n       ],\n       \"resources\": [\n        \"*\"\n       ]\n      }\n     ]\n    }\n   ]\n  }\n ],\n \"org_guardrails\": [\n  {\n   \"name\": \"protect-audit-trail\",\n   \"statements\": [\n    {\n     \"effect\": \"Deny\",\n     \"actions\": [\n      \"StopLogging\",\n      \"DeleteTrail\"\n     ],\n     \"resources\": [\n      \"*\"\n     ]\n    }\n   ]\n  },\n  {\n   \"name\": \"reads-of-client-data-need-mfa\",\n   \"statements\": [\n    {\n     \"effect\": \"Deny\",\n     \"actions\": [\n      \"GetObject\",\n      \"ListObjects\"\n     ],\n     \"resources\": [\n      \"bucket/payroll-exports*\"\n     ],\n     \"conditions\": {\n      \"mfa\": false\n     }\n    }\n   ]\n  }\n ],\n \"buckets\": [\n  {\n   \"name\": \"payroll-exports\",\n   \"public_read\": false,\n   \"encrypted\": true,\n   \"versioning\": true,\n   \"access_logging\": true,\n   \"note\": \"clients' payroll exports\"\n  }\n ]\n}\n", "n": 0, "broken": 0, "files": ["cloud/policies.json"], "blank": ["pol"]}
```

| Order | Action |
|---|---|
| 1 | Cut the VPN session; disable intern.payroll; block 198.51.100.150 and 203.0.113.230 |
| 2 | Revoke the backup key; reset localadmin on every server (unique passwords per server) |
| 3 | Isolate pay-app01; keep its disk image |
| 4 | Remove secrets from the IT$ scripts; restrict the share to IT |
| 5 | MFA on every VPN account; disable accounts on leaving day |
| 6 | Backup key: upload only, only from the office; reads of client data need MFA |

?> After the policy change, how many attacker actions are still allowed? :: 0
