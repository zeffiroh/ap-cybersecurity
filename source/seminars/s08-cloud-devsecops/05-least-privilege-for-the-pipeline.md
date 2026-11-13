## 5. Least privilege for the pipeline

The CI key only ever deploys cart-api, from the CI runners. Rewrite its policy to exactly that, add a guardrail, close the invoices bucket, and replay the audit trail until the attacker gets nothing and the deploys still work.

```tool cloudiam
{"pol": "{\n \"account\": \"monsoon-prod\",\n \"identities\": [\n  {\n   \"name\": \"ci-deployer\",\n   \"type\": \"user\",\n   \"note\": \"used by the CI runners (egress 203.0.113.20) to deploy cart-api\",\n   \"policies\": [\n    {\n     \"name\": \"deploy-cart-api-only\",\n     \"statements\": [\n      {\n       \"effect\": \"Allow\",\n       \"actions\": [\n        \"DeployService\"\n       ],\n       \"resources\": [\n        \"service/cart-api\"\n       ],\n       \"conditions\": {\n        \"source_ip\": [\n         \"203.0.113.20/32\"\n        ]\n       }\n      }\n     ]\n    }\n   ]\n  },\n  {\n   \"name\": \"ananya\",\n   \"type\": \"user\",\n   \"note\": \"Ananya Rao, CTO\",\n   \"policies\": [\n    {\n     \"name\": \"admin\",\n     \"statements\": [\n      {\n       \"effect\": \"Allow\",\n       \"actions\": [\n        \"*\"\n       ],\n       \"resources\": [\n        \"*\"\n       ]\n      }\n     ]\n    }\n   ]\n  }\n ],\n \"org_guardrails\": [\n  {\n   \"name\": \"keys-and-new-regions-need-mfa\",\n   \"statements\": [\n    {\n     \"effect\": \"Deny\",\n     \"actions\": [\n      \"CreateAccessKey\",\n      \"RunInstances\"\n     ],\n     \"resources\": [\n      \"*\"\n     ],\n     \"conditions\": {\n      \"mfa\": false\n     }\n    }\n   ]\n  }\n ],\n \"buckets\": [\n  {\n   \"name\": \"monsoon-invoices\",\n   \"public_read\": false,\n   \"encrypted\": true,\n   \"versioning\": true,\n   \"access_logging\": true,\n   \"note\": \"customer invoices, meant to be private\"\n  },\n  {\n   \"name\": \"monsoon-assets\",\n   \"public_read\": true,\n   \"encrypted\": true,\n   \"versioning\": true,\n   \"access_logging\": true,\n   \"note\": \"product images, meant to be public\"\n  }\n ]\n}\n", "n": 0, "broken": 0, "files": ["cloud/policies.json"], "blank": ["pol"]}
```

| Before | After |
|---|---|
| ci-deployer: AdministratorAccess (`*` on `*`) | ci-deployer: `DeployService` on `service/cart-api`, only from 203.0.113.20 |
| no guardrails | Deny `CreateAccessKey` and `RunInstances` without MFA |
| monsoon-invoices public, no versioning, no logging | private, versioning on, access logging on |

- [ ] 0 attacker actions allowed, 0 deploys broken
- [ ] Bucket check: only monsoon-assets is public
- [ ] Better still: what replaces a long-lived key in CI? (short-lived credentials the CI asks for at deploy time)

?> After the fix, how many normal actions are broken? :: 0
