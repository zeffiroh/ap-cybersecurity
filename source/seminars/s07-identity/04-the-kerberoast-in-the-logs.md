## 4. The kerberoast in the logs

The attacker didn't even need the password reset. Any domain user can ask for a **service ticket** for any account with a service name (SPN), and part of that ticket is encrypted with the service account's password. With the old RC4 cipher it can be cracked offline. That's kerberoasting. Find it on the domain controller, then in Zeek's Kerberos log.

```tool events
{"file": "eventlogs/dc01-Security.jsonl", "ids": "4769", "q": "0x17", "n": 6, "blank": ["ids", "src", "q"]}
```

- [ ] Who asked for RC4 tickets (0x17), from where, for which services, how fast?
- [ ] What does normal look like? (0x12 is AES)
- [ ] Find the same requests in zeek-kerberos.log

> Hint: Six service tickets in ten seconds, all RC4, from a helpdesk PC, is not how people work. Normal users ask for tickets to the servers they use, with AES.

?> How many RC4 service tickets did h.verma request? :: 6

?> What does encryption type 0x17 mean? (the cipher name) :: rc4-hmac
