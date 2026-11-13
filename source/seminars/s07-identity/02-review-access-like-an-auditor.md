## 2. Review access like an auditor

The **Access review** tab flags the classic problems: no MFA, admin rights outside IT, temporary staff with admin, stale accounts, disabled accounts still in groups, leavers. Make a decision for each flagged account and write one line of why.

```tool identity
{"decisions": {"t.mehta": "reduce", "s.rao": "disable", "p.das": "delete", "svc-sql": "reduce", "a.khan": "keep", "h.verma": "keep"}, "n": 2, "blank": ["decisions"]}
```

- [ ] A decision for every high-risk account
- [ ] For service accounts: what replaces MFA? (long random passwords, managed service accounts, no interactive logon)
- [ ] Which finding would you fix first, and why?

> Hint: A contractor in Server-Admins is critical. An account unused for 140 days should be disabled, not deleted, until its owner confirms.

?> Which account does the review mark as critical? :: t.mehta
