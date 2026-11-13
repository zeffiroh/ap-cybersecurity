## 7. Write the pipeline gate

A gate is a policy the pipeline enforces. Decide what **blocks a merge**, what **blocks a deploy**, what only **warns**, and how exceptions work. Make it strict where a mistake is expensive and light where it isn't, or people will route around it.

```tool report
{"tpl": "policy", "title": "Security policy: the cart-api pipeline gate", "text": "# Security policy: the cart-api pipeline gate\n\n## Purpose\n\nStop secrets, critical vulnerabilities and unsafe settings from reaching production, without blocking ordinary work.\n\n## Scope\n\nEvery merge to main and every deploy of cart-api and the worker, including emergency fixes.\n\n## Roles\n\nDevelopers fix what the gate finds. The platform team owns the gate and the exceptions list. The CTO approves exceptions over 7 days.\n\n## Policy statements\n\n- **Blocks the merge:** any secret in the change or its history (key, token, password, private key); any critical or high advisory with a fixed version available; Terraform that makes a bucket or database public or opens 22/3389 to 0.0.0.0/0.\n- **Blocks the deploy:** an image that runs as root, uses :latest or an unpinned base, or has a critical OS package; a manifest without runAsNonRoot, allowPrivilegeEscalation: false and resource limits.\n- **Warns only:** medium and low findings, which go to the register with an owner.\n- CI uses short-lived cloud credentials scoped to one service; no long-lived keys in variables or files.\n\n## Exceptions\n\nWritten, with an owner, a reason and an end date of at most 30 days; listed in the exceptions file in the repo. A secret is never an exception.\n\n## Enforcement\n\nThe gate runs in CI and can't be skipped from a branch. Merges that bypass it are reverted and reviewed.\n\n## Review\n\nEvery quarter, and after any incident the gate didn't stop.\n", "n": 7, "blank": ["text"]}
```

- [ ] Every critical finding from today would have been stopped
- [ ] Medium and low findings warn, they don't block
- [ ] Exceptions have an owner and an end date
- [ ] A secret is never an exception
