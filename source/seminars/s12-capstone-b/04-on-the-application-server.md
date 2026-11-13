## 4. On the application server

Read pay-app01's Security log.

```tool events
{"file": "eventlogs/pay-app01-Security.jsonl", "q": "localadmin", "n": 7, "blank": ["ids", "src", "q"]}
```

- [ ] Who logged on, how, from where?
- [ ] What did they run, in order?
- [ ] Where did the data go?
- [ ] What did they try to hide?

?> Which domain received the uploaded archive? :: upload.drop-files.example

?> Which event ID shows the log was cleared? :: 1102
