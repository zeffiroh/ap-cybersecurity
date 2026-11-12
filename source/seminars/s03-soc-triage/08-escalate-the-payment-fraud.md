## 8. Escalate the payment fraud

Write the one escalation. The person reading it is the Finance controller, who must stop a payment before 3 pm. Put the ask first, and say what you have **not** done (you didn't reply to the sender).

- [ ] The ask, with a time in the reader's time zone and in UTC
- [ ] Why it is high
- [ ] Know and don't know
- [ ] Where the evidence is

> Hint: A call to the CFO on a number you already have is the fastest way to confirm. Never use contact details from the suspicious email.

```tool report
{"tpl": "escalation", "title": "Escalation: payment fraud attempt against Finance", "text": "# Escalation: payment fraud attempt against Finance\n\n## The ask\n\nPlease take the Rs 18,40,000 supplier payment out of today's payment run and call a.kulkarni in Finance now, before the run closes at 15:00 IST (09:30 UTC). Finance controller, please confirm by phone with the CFO on his known number.\n\n## Severity and why\n\nHigh: a payment is due today and the request came from outside the company while pretending to be the CFO.\n\n## What we know\n\n- 2 Nov 11:47 UTC the email arrived; 3 Nov 08:20 UTC Finance forwarded it. It is signed \"Anil Mehta (CFO)\" from anil.mehta.cfo@freemail.example (AL-3102).\n- The email asks for a supplier's bank details to be changed and a payment released before 3 pm, and says to keep it secret and reply only to the freemail address.\n- SPF, DKIM and DMARC all pass for freemail.example: it really came from a free mail account, not from kestrel-logistics.com. Passing proves who sent it, not that it is safe.\n\n## What we don't know\n\n- Whether the CFO knows about the request (he has not been reached yet).\n- Whether other people in Finance got the same email, and whether the supplier's details were already changed in the payment system.\n\n## Impact so far\n\nOne Finance user and one pending payment are at risk. No account or host is known to be compromised.\n\n## What I've done\n\nNothing has been changed. I have not replied to the sender.\n\n## Evidence\n\nreported/bank-details.eml is saved in the case folder with its SHA-256 hash; the queue with dispositions is alerts-tuesday.json.\n", "n": 7, "blank": ["text"]}
```
