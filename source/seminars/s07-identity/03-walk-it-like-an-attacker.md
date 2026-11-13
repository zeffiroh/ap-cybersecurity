## 3. Walk it like an attacker

Now switch sides. In the **Attack paths** tab, start from h.verma (the phished account) and ask for paths to Domain-Admins. Each arrow is one thing the attacker can do with what they already have.

```tool identity
{}
```

- [ ] Write the path hop by hop, with what each hop means
- [ ] Which hop needs a password, which needs nothing new?
- [ ] Which other accounts could walk the same path from Server-Admins onwards?
- [ ] Which single change breaks the most paths?

> Hint: "HasSessionOn" means a saved login: whoever is admin on app02 can take adm.k.nair's credentials from it. The scheduled task keeps that login there every night.

?> Which service account is on the path from h.verma to Domain-Admins? :: svc-sql

?> On which server is the Domain Admin's login saved? :: app02
