## 10. A web rule, tested on two web logs

Sigma works for web logs too. The first version below matches any `%27` (a quote), the word UNION, or the tool's name. `lookbook_access.log` is an hour of normal visitors to the company's lookbook site: see who the noisy version accuses there. The tuned version keys on the tool's name and on `UNION%20SELECT`.

- [ ] Test both versions on both web logs
- [ ] Which requests does the noisy version catch that the tuned one doesn't? Are they attacks?
- [ ] One attack request did not come from sqlmap. Which part of the tuned rule catches it?
- [ ] Write the tuning note: when would the tuned rule miss an attack?

> Hint: An attacker can change the user agent in one flag, and here they did, by pasting a payload into a browser. That's why the rule keeps a second selection for the injection itself.

```tool sigma
{"rule": "title: SQL injection in a web request\nstatus: experimental\nlogsource:\n  category: webserver\ndetection:\n  keywords:\n    - '%27'\n    - 'UNION'\n    - 'sqlmap'\n  condition: keywords\nlevel: high\n", "n": 10, "ls": true, "blank": ["rule"]}
```

```tool sigma
{"rule": "title: SQL injection tool or UNION SELECT in a web request\nid: 5a1c7e10-0b8f-4a59-9a3e-2c1f00000005\nstatus: experimental\nlogsource:\n  category: webserver\ndetection:\n  tool:\n    - 'sqlmap/'\n  union:\n    - 'UNION%20SELECT'\n  condition: tool or union\nfalsepositives:\n  - Your own authorised scans (exclude the scanner's address in the tuning notes)\nlevel: high\ntags:\n  - attack.initial_access\n  - attack.t1190\n", "n": 8, "ls": true, "blank": ["rule"]}
```

?> How many web requests does the noisy version match? :: 10

?> How many web requests does the tuned rule match? :: 8
