## 7. Write the audit exception

Internal audit found three critical vulnerabilities past the 15-day target. Fixing all three today isn't possible. An **exception** is how a company says "not yet" honestly: what isn't met, why, the risk meanwhile, the **compensating controls**, an owner, an **expiry**, and who approved it. Write it in a Notes cell. A model:

<details><summary>Model exception</summary>

**Exception EX-2026-04 to control 8.8 (vulnerability management)**  ·  Responds to audit finding IA-2026-07

**What isn't met:** VM-311, VM-318 and VM-322 are past the 15-day target for critical vulnerabilities.

**Why:** VM-311's fix breaks the refund screen (fix in development); VM-318 is fixed on 20 November; VM-322 needs a 2-hour VPN outage, booked for Saturday 28 November.

**Risk while open:** an attacker reaching the admin console or VPN appliance could take control of it.

**Compensating controls (in place from 17 November):** the admin console is reachable only over the VPN; a WAF rule blocks the known exploit pattern for VM-311; the VPN appliance's management page is closed to the internet; daily log review of both by the SOC.

**Owner:** IT manager (A. Fernandes).  **Expires:** 31 January 2027, or when the last item is fixed. No renewal without a new review.

**Approved:** CISO and the risk owner (Head of Finance, for the admin console), signatures and date.

</details>

- [ ] A compensating control for each open item
- [ ] An expiry date, not "until fixed"
- [ ] Approved by someone who owns the risk, not only by IT

> Hint: An exception without an expiry is a permanent decision dressed up as a temporary one. Auditors reject those.
