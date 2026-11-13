## 4. Write the design review memo

The memo turns the model into decisions. Ranked, short, with **conditions for go-live** (must), things to fix soon (should), and what's good. Write it in a Notes cell. A model:

<details><summary>Model memo</summary>

**Design review: Parent Pay v0.9**  ·  To: Kunal Desai (Product), Sana Pillai (Engineering)  ·  From: Security  ·  16 November 2026

**Decision asked for:** go-live on 4 December only if the three conditions below are met. Otherwise delay.

**Go-live conditions (must):**
1. The webhook checks PayGate's signature, and the Fees API confirms each payment with PayGate before marking it paid. (Today anyone can mark any fee paid with one request.)
2. The Fees API takes the amount from the database, never from the app.
3. A signed data processing agreement with the SMS vendor, and the receipt text cut to "Fee received: Rs X, ref Y" (no child's name or class).

**Before the end of the term (should):** MFA and named accounts on the admin console; refunds over Rs 5,000 need a second approver; logs record events, not request bodies, for 30 days.

**Accepted risks (need sign-off):** none proposed. The one-click refund risk is high and can't be accepted by Product alone.

**What's good:** card data never touches Banyan (PayGate); the database is encrypted; OTP sign-in for parents.

</details>

- [ ] The decision asked for is the first line
- [ ] At most three must-fix conditions, each with the reason in one line
- [ ] Accepted risks say who signs them

> Hint: A memo with twenty "musts" means nothing launches or nothing gets fixed. Choose the ones that would cost the school money or a child's data on day one.
