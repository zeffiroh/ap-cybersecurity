## 4. What the leaked key did

Follow the key from the history patch through the audit trail. Then check the buckets in the Cloud IAM simulator.

- [ ] From where was ci-deployer used, besides the CI runners?
- [ ] What did it launch, where, and what did it create to keep access?
- [ ] Which bucket is public that shouldn't be? Which public bucket is fine?

> Hint: `grep -c RunInstances` counts launches. The assets bucket holds product images and is meant to be public; the invoices bucket isn't.

?> How many instances did the attacker launch? :: 8

?> From which address was the leaked key used? :: 198.51.100.91
