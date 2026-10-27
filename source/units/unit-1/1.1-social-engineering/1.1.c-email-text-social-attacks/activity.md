# In-class activity, 1.1.c Email, text, and social media attacks

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice identifying channel-specific phishing indicators across email, SMS, and social
media messages, and explain why each channel's trust model makes it exploitable. Ties to
LO 1.1.A (identify indicators) and 1.1.C (distinguish attack channels and their characteristics).

## Materials (all local)
- Printed message set below (one copy per pair), or the simulation on each machine.
- One blank label sheet per pair (for tagging indicators).

## Message set (print and cut into cards)

### Card A, Email
> From: security-alert@amaz0n-security.net
> Subject: Your Amazon account has been locked
> Body: "We detected unusual activity on your Amazon account. Verify your account
> immediately or your access will be permanently suspended. Click the link below."
> Link: http://bit.ly/amz-verify

### Card B, SMS
> From: +1-888-555-0134
> "USPS: Your package cannot be delivered. Reroute at http://192.168.0.22/usps or it
> will be returned to sender within 24 hours."

### Card C, Social media DM
> From: @NetflixHelpCenter_ (note trailing underscore)
> "Hi! Your Netflix subscription expires tonight. Confirm your payment info at the link
> below to keep streaming."
> Link: https://cutt.ly/netflix-renew

### Card D, Email
> From: ceo@yourcompany-finance.net
> Subject: Urgent, wire transfer needed today
> Body: "I am in a meeting and cannot talk. Please wire $8,500 to the vendor below
> immediately. Do not loop in accounting. I will explain when I return."

### Card E, SMS
> From: MOM
> "Hey, dinner is at 7pm tonight. Can you pick up bread on the way?"

## Steps
1. Each pair reads all five cards and assigns every applicable indicator label to each card.
   Use these labels: **lookalike-domain**, **urgent-money-request**, **credential-request**,
   **mismatched-sender**, **shortened-link**. A card may have zero, one, or several labels.
   Write the labels directly on the card (or on a sticky note attached to it).
2. For each label they assign, pairs write one sentence explaining WHY that indicator matters:
   what trust assumption does the attacker exploit on this specific channel?
3. For cards A, B, and C (multi-indicator cards), pairs identify which single indicator they
   would notice FIRST if they received this message on their own device, and discuss whether
   a different channel would have made the same indicator harder to spot.

## Collaborate (AP skill 4)
Assign roles: one partner is the "analyst" (names and defends each label), the other is the
"attacker" (argues why the message looks convincing and why a victim might miss that indicator).
After completing cards A-E, swap roles and draft one original phishing message of their own, choosing a channel, a brand, and at least two indicators, then trade with another pair to
classify.

## Exit ticket
Each student submits in writing:
1. Which card was hardest to classify and why.
2. One original phishing message they drafted, with the channel they chose and every indicator
   label it uses.
3. The single defensive action a recipient should take upon receiving any of these messages.

## Instructor notes
- Expected indicator assignments:
  - Card A: lookalike-domain (amaz0n-security.net), credential-request, mismatched-sender,
    shortened-link (bit.ly)
  - Card B: shortened-link (bare IP 192.168.0.22), credential-request (reroute = verify)
  - Card C: lookalike-domain (trailing underscore handle), credential-request, shortened-link
    (cutt.ly), mismatched-sender (Netflix not in sender handle)
  - Card D: urgent-money-request, (no shortened link, no lookalike, BEC relies on authority +
    secrecy, not technical deception)
  - Card E: none, legitimate family text
- Common stumbles: students label Card D with lookalike-domain because the domain looks odd;
  push them to apply the defined rule (is a known brand substituted with look-alike chars?).
  Card E stumps some students who expect every card to have an indicator.
- The BEC pattern on Card D (bypass normal process + urgency + secrecy) is the hardest to
  detect technically, discuss why procedural controls (dual-authorization for wires) matter.
- Feeds the unit project (phishing analyzer) and scenario stage 1 (social-engineering entry).
