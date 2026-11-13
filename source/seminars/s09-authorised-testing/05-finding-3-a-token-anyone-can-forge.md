## 5. Finding 3: a token anyone can forge

The staging bundle holds a login token. A JWT is three parts: header, payload, signature. The signature only protects the token if its secret is hard to guess. Load the token in the JWT inspector, read what it says, and check its secret against the wordlist. That's an offline check: nothing is sent to the server.

```tool jwt
{"tok": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsImVtYWlsIjoiZGVtb0BuaW1idS5zaG9wIiwicm9sZSI6ImN1c3RvbWVyIiwiaWF0IjoxNzk0Nzg3MjAwLCJleHAiOjE3OTUzOTIwMDB9.Fzr9zEuwVnUnfgATCUbpvWEij5UTAph5ZiS5msv6EUM", "secret": "nimbu2026", "blank": ["secret"]}
```

- [ ] What's in the header and payload? Which algorithm?
- [ ] Is the secret in the wordlist? Which word?
- [ ] With the secret, what could an attacker change? (role: admin)
- [ ] Two fixes: a long random secret from a vault, and the token out of the bundle

> Hint: The shop's own mission "Forge a token" shows the other classic JWT mistake: a server that accepts `alg: none`.

?> Which signing algorithm does the token use? :: HS256

?> What is the token's secret? :: nimbu2026
