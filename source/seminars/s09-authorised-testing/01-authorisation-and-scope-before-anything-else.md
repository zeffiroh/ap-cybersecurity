## 1. Authorisation and scope, before anything else

A test without written permission is an attack. Read the letter of authorisation all the way through, then turn it into **rules of engagement**: who authorised it, exactly what is in and out of scope, the window, what you may and may not do, when you stop and who you call, and how you treat data.

```tool report
{"tpl": "roe", "title": "Rules of engagement: NimbuMart test, 16 to 20 November 2026", "text": "# Rules of engagement: NimbuMart test, 16 to 20 November 2026\n\n## Parties and authorisation\n\nNimbuMart Retail Pvt Ltd (client), represented by Ritu Malhotra, Head of Engineering, who signed the letter of authorisation on 12 November 2026. The tester works under that letter only.\n\n## In scope\n\nhttps://nimbu.shop and its /api; 192.0.2.10 shop-staging.nimbu.shop; 192.0.2.11 api-staging.nimbu.shop.\n\n## Out of scope\n\n192.0.2.12 pay.nimbu.shop (third-party payment provider); staff, phones and email; denial of service and load testing; changing or deleting other customers' data.\n\n## Test window\n\nMonday 16 November 09:00 to Friday 20 November 18:00 IST. No testing outside it.\n\n## Allowed and forbidden techniques\n\nAllowed: port and service scans of in-scope addresses, manual testing through an intercept proxy, offline checks of token secrets against a short wordlist. Forbidden: brute force against live logins, exploits that change data, anything against out-of-scope hosts.\n\n## Stop conditions and contacts\n\nStop and call Ritu Malhotra (+91 98000 11223), or Dev Anand (+91 98000 44556), if live card data or real people's personal data appears, if something breaks, or if there are signs of a real attacker.\n\n## Data handling\n\nUse only the demo account. Read other customers' data only to prove a finding, one record at most. No copies leave the lab; screenshots cropped; working files deleted after the report.\n", "n": 7, "blank": ["text"]}
```

- [ ] Every in-scope address and URL, and every out-of-scope one
- [ ] The stop contact and number, written where you'll see it
- [ ] What data you may touch, and how much

> Hint: A host can be on the same network and look like part of the shop and still be out of scope. Only the owner of a system can authorise testing it.

?> Which IP address is out of scope? :: 192.0.2.12

?> Who is the stop contact? (full name) :: Ritu Malhotra
