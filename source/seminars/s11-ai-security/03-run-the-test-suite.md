## 3. Run the test suite

Manual poking finds things; a **test suite** proves them and lets you retest after a fix. Run all seven tests with no defences switched on. Six are attacks; T7 is a normal question that must keep working.

```tool aisec
{"file": "ai-tara-support.json", "on": {}, "n": 6, "blank": ["on"]}
```

- [ ] Which tests fail, and with which outcome: leak or misuse?
- [ ] Map each to OWASP and ATLAS (atlas-notes.txt)
- [ ] Does T7 pass?

?> How many tests fail with no defences? :: 6
