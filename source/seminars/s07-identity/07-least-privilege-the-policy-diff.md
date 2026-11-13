## 7. Least privilege: the policy diff

Rewrite the policies so the attacker's actions fail and normal work goes on. Replay the audit log after each change: the simulator says how many attacker actions would still be allowed and how many normal actions you broke. Aim for 0 and 0.

```tool cloudiam
{"pol": "{\n \"account\": \"nimbus-prod\",\n \"identities\": [\n  {\n   \"name\": \"reporting-sync\",\n   \"type\": \"user\",\n   \"note\": \"access key saved in C:\\\\Reports\\\\sync.ps1 on app02; uploads the nightly KPI files\",\n   \"policies\": [\n    {\n     \"name\": \"reporting-put-only\",\n     \"statements\": [\n      {\n       \"effect\": \"Allow\",\n       \"actions\": [\n        \"PutObject\"\n       ],\n       \"resources\": [\n        \"bucket/nimbus-reports/*\"\n       ],\n       \"conditions\": {\n        \"source_ip\": [\n         \"203.0.113.60/32\"\n        ]\n       }\n      }\n     ]\n    }\n   ]\n  },\n  {\n   \"name\": \"k.nair\",\n   \"type\": \"user\",\n   \"note\": \"Kavya Nair, cloud administrator\",\n   \"policies\": [\n    {\n     \"name\": \"admin\",\n     \"statements\": [\n      {\n       \"effect\": \"Allow\",\n       \"actions\": [\n        \"*\"\n       ],\n       \"resources\": [\n        \"*\"\n       ]\n      }\n     ]\n    }\n   ]\n  },\n  {\n   \"name\": \"m.joshi\",\n   \"type\": \"user\",\n   \"note\": \"Meera Joshi, reads reports\",\n   \"policies\": [\n    {\n     \"name\": \"reports-read\",\n     \"statements\": [\n      {\n       \"effect\": \"Allow\",\n       \"actions\": [\n        \"ConsoleLogin\",\n        \"ListBuckets\",\n        \"GetObject\"\n       ],\n       \"resources\": [\n        \"*\",\n        \"bucket/nimbus-reports/*\"\n       ]\n      }\n     ]\n    }\n   ]\n  }\n ],\n \"org_guardrails\": [\n  {\n   \"name\": \"protect-audit-trail\",\n   \"statements\": [\n    {\n     \"effect\": \"Deny\",\n     \"actions\": [\n      \"StopLogging\",\n      \"DeleteTrail\"\n     ],\n     \"resources\": [\n      \"*\"\n     ]\n    }\n   ]\n  },\n  {\n   \"name\": \"identity-changes-need-mfa\",\n   \"statements\": [\n    {\n     \"effect\": \"Deny\",\n     \"actions\": [\n      \"CreateUser\",\n      \"CreateAccessKey\",\n      \"AttachUserPolicy\"\n     ],\n     \"resources\": [\n      \"*\"\n     ],\n     \"conditions\": {\n      \"mfa\": false\n     }\n    }\n   ]\n  }\n ],\n \"buckets\": [\n  {\n   \"name\": \"nimbus-reports\",\n   \"public_read\": false,\n   \"encrypted\": true,\n   \"versioning\": true,\n   \"access_logging\": true,\n   \"note\": \"KPI files\"\n  },\n  {\n   \"name\": \"client-exports\",\n   \"public_read\": false,\n   \"encrypted\": true,\n   \"versioning\": false,\n   \"access_logging\": false,\n   \"note\": \"client data extracts for analytics\"\n  }\n ]\n}\n", "n": 0, "broken": 0, "files": ["cloud/policies.json"], "blank": ["pol"]}
```

The diff, in words:

| Before | After |
|---|---|
| reporting-sync: Allow `*` on `*` | reporting-sync: Allow `PutObject` on `bucket/nimbus-reports/*`, only from 203.0.113.60 |
| (nothing) | Guardrail: Deny `CreateUser`, `CreateAccessKey`, `AttachUserPolicy` without MFA |

- [ ] 0 attacker actions allowed
- [ ] 0 normal actions broken
- [ ] Write the diff in two lines someone can review
- [ ] What else should change? (the key out of the script: a role for the server, rotated keys)

> Hint: A condition on the source address alone stops a stolen key used from elsewhere. The MFA guardrail stops anyone, even a real admin's stolen key, from minting new identities quietly.

?> After your policy, how many attacker actions are still allowed? :: 0
