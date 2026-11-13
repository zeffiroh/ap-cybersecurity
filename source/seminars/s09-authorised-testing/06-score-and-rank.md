## 6. Score and rank

Score each finding's CVSS vector, then rank the register. CVSS describes the flaw; the ranking adds whether it's reachable from the internet and whether anyone is exploiting it.

```tool patch
{"vec": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "n": 9.8, "blank": ["vec"]}
```

- [ ] Score all three vectors
- [ ] Rank the register: which is first, and why?
- [ ] For NM-02, why is Privileges Required "Low"?

> Hint: The IDOR needs a customer account, which anyone can create for free. So PR:L is honest, but don't let it make the finding sound minor.

?> What is the CVSS base score of the login bypass? :: 9.8
