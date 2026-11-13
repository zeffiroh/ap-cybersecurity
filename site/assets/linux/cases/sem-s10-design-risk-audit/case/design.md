# Parent Pay: design for review (v0.9, 13 November 2026)

Owner: Kunal Desai, Product. Engineering lead: Sana Pillai. Launch target: 4 December 2026.

## What it does
Parents open the Banyan app, see the fees due for their child, and pay. A receipt arrives by SMS and in the app.

## Parts
- **Banyan app** (Android, iOS): parents sign in with mobile number and a one-time code (OTP).
- **Fees API** (new): lists fees, starts a payment, receives the payment result. Runs in our cloud account.
- **Student records DB** (existing): names, classes, parents' mobile numbers, fee amounts.
- **PayGate** (payment provider): the parent is redirected to PayGate's page to enter card or UPI details. We never see the card number.
  PayGate calls our **webhook** /fees/paid with the result.
- **TextBridge** (SMS vendor): we send it the parent's mobile number and the receipt text.
- **Admin console** (existing): school office staff mark fees paid by cash and issue refunds.

## Decisions taken
1. The webhook accepts a JSON body with order_id and status. (Signature checking "later".)
2. Refunds from the admin console need one click by any office staff member.
3. Fee amounts are sent from the app to the Fees API when the payment starts.
4. Logs keep the full request body for 90 days, for debugging.
5. TextBridge was chosen for price; the contract is not yet signed.
