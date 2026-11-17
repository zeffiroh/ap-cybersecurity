## 9. Escalate the payment fraud

Write the one escalation. The person reading it is the Finance Controller, Pooja Mathur, who must stop a payment before 2 pm IST. Put the ask first, and say what you have **not** done (you didn't reply to the sender).

- [ ] The ask, with a time in the reader's time zone and in UTC
- [ ] Why it is high
- [ ] Know and don't know
- [ ] Where the evidence is

> Hint: A call on a number you already have is the fastest way to confirm. Never use contact details from the suspicious email.

```tool report
{"tpl": "escalation", "title": "Escalation: payment fraud attempt against Accounts", "text": "# Escalation: payment fraud attempt against Accounts\n\n## The ask\n\nPlease take the Rs 12,60,000 advance to Rang Mahal Decorators out of today's payment run, which closes at 14:00 IST (08:30 UTC). Finance Controller, please call Vikram Shekhawat on his known mobile number to confirm, and call Rang Mahal Decorators on the number in the supplier master file, not the one in the email.\n\n## Severity and why\n\nHigh: a payment is due today, the bank details in the request are new, and the request came from outside the company while pretending to be the General Manager.\n\n## What we know\n\n- Tue 10 Nov 12:05 UTC the email arrived for r.jain; he forwarded it to the SOC on Wed 11 Nov 04:20 UTC (AL-4102).\n- It is signed \"Vikram Shekhawat (General Manager)\" but sent from vikram.gm.lotuslake@freemail.example.\n- It asks for the supplier's bank details to be changed and the advance released by 2 pm, says to keep it secret, and says to reply only to the freemail address.\n- SPF, DKIM and DMARC all pass for freemail.example: it really came from a free mail account, not from lotuslakehotels.com. Passing proves who sent it, not that it is safe.\n\n## What we don't know\n\n- Whether the General Manager knows about the request (he has not been reached yet).\n- Whether the supplier's details were already changed in the accounts system, and whether anyone else in Accounts got the same email.\n\n## Impact so far\n\nOne accounts user and one pending payment are at risk. No account or computer is known to be compromised.\n\n## What I've done\n\nNothing has been changed. I have not replied to the sender.\n\n## Evidence\n\nreported/supplier-bank-change.eml is saved in the case folder with its SHA-256 hash; the queue with dispositions is alerts-wednesday.json.\n", "n": 7, "blank": ["text"]}
```
