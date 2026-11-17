## 6. A YARA rule for the lure

Write a YARA rule that finds the guest-complaint lure in mail, so the mail gateway can catch the next one. Test it on **every** file. The first rule below matches on the phishing domain alone: see what else it catches. The tuned rule needs three things that only the lure email has.

- [ ] Test the noisy rule: which files does it match? Are they emails?
- [ ] Test the tuned rule: it should match only guest-complaint.eml
- [ ] Test the third rule on the quarantined file's strings
- [ ] Write one line on what each rule would miss

> Hint: The intel feed, the block list, the alert queue and the proxy log all mention the domain too. A rule for email should need things only the email has: the subject, the link path and the threat.

```tool yara
{"rule": "rule llh_phishing_domain\n{\n  meta:\n    description = \"Anything that mentions the phishing domain\"\n  strings:\n    $d = \"login-verify.example\"\n  condition:\n    $d\n}\n", "n": 5, "files": ["alerts-wednesday.json", "ai-verdicts.json", "intel.json", "known_bad.txt", "mail.log", "proxy.log", "reported/guest-complaint.eml"], "blank": ["rule"]}
```

```tool yara
{"rule": "rule llh_guest_complaint_lure\n{\n  meta:\n    description = \"The fake guest-complaint email aimed at hotel reservations teams\"\n    author = \"SOC\"\n    reference = \"AL-4101, message 7C1A20F11\"\n  strings:\n    $subject = \"Subject: Guest complaint BKG-\"\n    $link = \"login-verify.example/complaints/\"\n    $press = \"hidden from search results\"\n  condition:\n    all of them\n}\n", "n": 1, "files": ["reported/guest-complaint.eml"], "blank": ["rule"]}
```

```tool yara
{"rule": "rule bp_grab_stealer_strings\n{\n  meta:\n    description = \"Strings from Boarding_Pass.pdf.exe, a password stealer left on guest USB sticks\"\n  strings:\n    $mutex = \"Global\\\\bp-grab-7731\"\n    $chrome = \"\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data\"\n    $flag = \"--grab-all\"\n    $exfil = \"telegram-relay.example/bot\"\n  condition:\n    3 of them\n}\n", "n": 1, "files": ["suspect/boarding-pass.strings.txt"], "blank": ["rule"]}
```

?> How many files does the domain-only rule match? :: 5

?> How many files does the tuned lure rule match? :: 1
