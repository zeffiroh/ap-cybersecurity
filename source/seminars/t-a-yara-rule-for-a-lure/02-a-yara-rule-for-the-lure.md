## 2. A YARA rule for the lure

Write a YARA rule that finds the overdue-invoice lure in mail, so the mail gateway can catch the next one. Test it on **every** file in the case. The first rule below matches on the domain alone: see what else it catches. The tuned rule needs three things that only the lure email has.

- [ ] Test the noisy rule: which files does it match? Are they emails?
- [ ] Test the tuned rule: it should match only invoice.eml
- [ ] Test the third rule on the malware's strings
- [ ] Write one line on what each rule would miss

> Hint: The intel feed and the proxy log mention the domain too. A rule for email should need things only the email has: the subject, the link path and the threat.

```tool yara
{"rule": "rule kestrel_lookalike_domain\n{\n  meta:\n    description = \"Anything that mentions the look-alike domain\"\n  strings:\n    $d = \"kestrel-logistlcs.com\"\n  condition:\n    $d\n}\n", "n": 6, "files": ["alerts-tuesday.json", "intel.json", "invoice.eml", "known_bad.txt", "mail.log", "proxy.log"], "blank": ["rule"]}
```

```tool yara
{"rule": "rule kestrel_invoice_lure\n{\n  meta:\n    description = \"The overdue-invoice lure email from the look-alike domain\"\n    author = \"SOC\"\n    reference = \"AL-2201, message 4A1F21C02\"\n  strings:\n    $subject = \"Subject: FINAL NOTICE: overdue invoice\"\n    $link = \"kestrel-logistlcs.com/invoices/INV-\"\n    $press = \"service suspension\"\n  condition:\n    all of them\n}\n", "n": 1, "files": ["invoice.eml"], "blank": ["rule"]}
```

```tool yara
{"rule": "rule ksl_ransomware_strings\n{\n  meta:\n    description = \"Strings from svchost-upd.exe, the KSL ransomware\"\n  strings:\n    $mutex = \"Global\\\\ksl-mutex-4471\"\n    $ext = \".kestrel-locked\"\n    $note = \"README_RESTORE.txt\"\n    $walk = \"--walk\"\n  condition:\n    3 of them\n}\n", "n": 1, "files": ["suspect/svchost-upd.strings.txt"], "blank": ["rule"]}
```

?> How many files does the domain-only rule match? :: 6

?> How many files does the tuned lure rule match? :: 1
