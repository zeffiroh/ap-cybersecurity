## 9. A web rule, tested on the web log

Sigma works for web logs too. The first version below matches any `%27` (a quote) or the word UNION. `shop2_access.log` is an hour of normal shoppers: run the noisy version on it and see who it accuses. The tuned version keys on the tool's name and on `UNION%20SELECT`.

- [ ] Test both versions on both web logs
- [ ] Which requests does the noisy version catch that the tuned one doesn't? Are they attacks?
- [ ] Write the tuning note: when would the tuned rule miss an attack?

> Hint: An attacker can change the user agent in one flag. Keep a second rule for the injection itself, not just the tool.

```tool sigma
{"rule": "title: SQL injection in a web request\nstatus: experimental\nlogsource:\n  category: webserver\ndetection:\n  keywords:\n    - '%27'\n    - 'UNION'\n    - 'sqlmap'\n  condition: keywords\nlevel: high\n", "n": 6, "ls": true, "blank": ["rule"]}
```

```tool sigma
{"rule": "title: SQL injection tool or UNION SELECT in a web request\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000005\nstatus: experimental\nlogsource:\n  category: webserver\ndetection:\n  tool:\n    - 'sqlmap/'\n  union:\n    - 'UNION%20SELECT'\n  condition: tool or union\nfalsepositives:\n  - Your own authorised scans (exclude the scanner's address in the tuning notes)\nlevel: high\ntags:\n  - attack.initial_access\n  - attack.t1190\n", "n": 4, "ls": true, "blank": ["rule"]}
```

?> How many web requests does the noisy version match? :: 6

?> How many web requests does the tuned rule match? :: 4
