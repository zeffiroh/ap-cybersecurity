## 7. The DPDP pack: the Board note and the notice

Two more readers. The **Board** needs to decide; the **customers** need to know what happened to them and what to do. The notice must be short and plain, in the language the customer uses with Kaveri, and say five things: what happened (nature, extent, timing), the likely consequences, what Kaveri has done, what the person can do, and who to contact.

```tool report
{"tpl": "escalation", "title": "Note to the Board: personal data breach in the loan app", "text": "# Note to the Board: personal data breach in the loan app\n\n## The ask\n\nPlease note this breach today and approve: free fraud-alert SMS for the 2,060 customers for 12 months, and an external review of the app's access checks before the next release.\n\n## Severity and why\n\nHigh. 2,060 customers' names, mobile numbers, addresses, loan amounts and the last four digits of their Aadhaar were taken. That is enough for convincing fraud calls.\n\n## What we know\n\n- On 8 June 2027, 03:10 to 04:18 UTC, one client (198.51.100.66) using one customer's session read 2,060 other customers' KYC records through the app's API.\n- The cause: a missing ownership check, released on 21 May. We searched back to then and found no other client doing this.\n- The fix went live at 07:15 UTC; the address is blocked and the token revoked.\n\n## What we don't know\n\n- Who is behind 198.51.100.66, and whether the records have been shared. A journalist says she has a sample.\n\n## Impact so far\n\n2,060 customers in India (1,932), the UAE (64), Germany (41) and Ireland (23). No money was moved and no passwords were exposed.\n\n## What I've done\n\nCERT-In filed 08:15 UTC and updated 09:35; RBI filed 08:30; the Data Protection Board told at 09:10; customers are being told by SMS and email from 10:00. The detailed report to the Board is due by 11 June 04:50 UTC.\n\n## Evidence\n\napi_access.log, affected_customers.csv and the WAF alert, preserved with hashes; the CERT-In reference is in the filing.\n", "n": 7, "blank": ["text"]}
```

Write the notice to customers in a Notes cell. A model:

<details><summary>Model notice to customers</summary>

Subject: We are writing to tell you about a problem with your Kaveri account details

On 8 June 2027, between 8:40 and 9:48 in the morning, someone used a fault in the Kaveri app to see some customers' details. Your details were among them.

What they saw: your name, mobile number, address, loan amount and the last four digits of your Aadhaar number. They did not see your password, your full Aadhaar number or your bank details, and no money was taken from any account.

What could happen: you may get calls or messages from people pretending to be Kaveri or a bank, who already know some of your details.

What we have done: we fixed the fault the same morning, blocked the person responsible, and reported it to CERT-In, the Reserve Bank of India and the Data Protection Board.

What you can do: Kaveri will never ask for your OTP, PIN or password by phone or message. If someone does, hang up and call us. We are sending you free fraud-alert messages for 12 months.

Questions: call 1800 000 4321 (free, 8 am to 8 pm) or write to dpo@kaveri.example. Arvind Shetty, Data Protection Officer, will answer.

</details>

- [ ] Board note: the ask first, then the facts
- [ ] Notice: all five parts, no jargon, no "we take your privacy seriously"
- [ ] Notice: what Kaveri will never ask for
- [ ] A contact who can actually answer

> Hint: Read your notice aloud. If your grandmother couldn't act on it, rewrite it.

?> How many affected customers live in India? :: 1932
