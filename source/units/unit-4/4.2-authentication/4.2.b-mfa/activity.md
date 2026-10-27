# In-class activity, 4.2.b Multi-factor authentication

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students learn to classify authentication methods by factor category, judge whether a described
login flow is true MFA, and identify the weakest link in a multi-step login. Ties to LO 4.2.A
(explain authentication factors and MFA) and 4.2.B (evaluate the strength of an authentication
scheme against phishing/SIM-swap/push-bombing risk).

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario cards below.
- Blank paper for the classification table (Step 3).

## Steps
1. **Classify the scenarios (10 min).** Each pair reads the five scenarios below and writes: (a)
   which factor category each presented credential belongs to (knowledge / possession /
   inherence), (b) whether the flow is true MFA, and (c) the weakest link, if any.

   - **Scenario A:** A user logs in with a password, then a 6-digit code texted to their phone.
   - **Scenario B:** A user logs in with a password, then taps "Approve" on a push notification
     without reading which device or location triggered it.
   - **Scenario C:** A user logs in with a password and a memorized answer to "What street did
     you grow up on?"
   - **Scenario D:** A user logs in with a password, then inserts a FIDO2 hardware security key
     and taps its button when prompted.
   - **Scenario E:** A user logs in with a fingerprint scan on their phone, which then also
     confirms their identity to unlock a saved password that is auto-filled into the site.

2. **Compare with the simulation (5 min).** Open the simulation and work through its login-attempt stream to
   check your classifications. Note any disagreements and discuss why.

3. **Build a comparison table (10 min).** As a pair, fill in the table:

   | MFA method | Factor category | Resistant to phishing? | Resistant to SIM-swap? | Recommended use case |
   |---|---|---|---|---|
   | Password only | | | | |
   | SMS one-time code | | | | |
   | Authenticator app (TOTP) | | | | |
   | Push notification | | | | |
   | Hardware key (FIDO2) | | | | |
   | Biometric | | | | |

## Collaborate (AP skill 4)
Assign roles: one partner is the "login auditor" (classifies each scenario's factor categories and
explains the reasoning), the other is the "risk advisor" (recommends whether the scheme is
acceptable for a high-value account like a bank or admin login, and what to upgrade). Swap roles
for the comparison table. Compare your completed table with another pair and reconcile any
disagreement on phishing/SIM-swap resistance.

## Exit ticket
Each student submits: their classification of Scenario B (true MFA or not, and why) plus one
sentence naming the attack technique that Scenario B is vulnerable to.

## Instructor notes
- Expected answers: A = knowledge + possession, true MFA but phishable (SMS/SIM-swap risk).
  B = knowledge + possession, technically true MFA but the weakest link is the unverified push
  approval, vulnerable to MFA fatigue/push bombing. C = knowledge + knowledge (a security
  question is still "something you know"), NOT true MFA. D = knowledge + possession, true MFA and
  phishing-resistant (FIDO2). E = inherence unlocking a stored knowledge credential on the same
  device, commonly marketed as MFA but functions closer to single-device convenience; discuss
  whether the biometric and password are truly independent factors here (both live on/protect the
  same device) versus being combined with a genuinely separate possession factor.
- Common stumble: students assume any two-step login is MFA. Reinforce the category rule: same
  category twice (Scenario C) is not MFA regardless of step count.
- Table expected highlights: password-only (knowledge, not phishing/SIM-swap resistant, avoid
  alone); SMS (knowledge+possession, not resistant to either, acceptable only as fallback); TOTP
  app (knowledge+possession, resists SIM-swap but not real-time phishing relay); push (same as
  TOTP but adds MFA-fatigue risk if unverified); hardware key (knowledge+possession, resists both,
  recommended for admin/high-value accounts); biometric (inherence, device-bound, good UX layer
  but not a network-facing factor on its own).
- Feeds the unit project (authentication hardening plan) and scenario stage covering credential
  theft and account takeover.
