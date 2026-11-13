## 1. Take custody of the evidence

Before you read anything, hash it, and start a **chain of custody**: who handled which file, when, and what its hash was. If this ends up with the police, an insurer or a court, the custody log is what makes your evidence count.

```tool hex
{"file": "suspect/RESTORE-FILES.txt", "sha256": "2958bfbf3ed6df5ef7f177fa6e8307fe21efb29172e73470fdc5aaa949659ad7", "n": 0, "custody": [], "blank": ["sha256"]}
```

- [ ] Hash every file (the Linux cell)
- [ ] In the Hex tool, open the ransom note, hash it and add a custody entry
- [ ] Add a custody entry for locker.strings.txt too
- [ ] Download the chain of custody

> Hint: A custody entry says what you did ("received from IT", "hashed", "copied for analysis"), when, and who you are.

?> How many evidence files are there, including the README and the tabletop? :: 16

?> What are the first 8 characters of the ransom note's SHA-256? :: 2958bfbf
