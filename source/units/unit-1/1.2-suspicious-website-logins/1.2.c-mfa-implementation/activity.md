# In-class activity -- 1.2.c Strengthening authentication: length/complexity, randomness, MFA

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students work through the TOTP algorithm by hand (with a calculator) for one time step, verify
their result matches the simulator, and then reason about the security properties that emerge from
the algorithm's design. Ties to LO 1.2.C (evaluate stronger authentication: length, randomness,
MFA).

## Materials (all local)
- the SimLab simulation on each machine.
- Calculator (phone or software; no internet needed).
- Printed TOTP trace sheet (optional -- instructor prints from the legend in the simulation).

## Steps
1. Pairs open the simulation and read Scenario 1 (fixed key and timestamp). Before entering anything,
   they write out the algorithm steps on paper:
   a. Compute the time step: step = floor(t / 30).
   b. Note the key bytes from the hex string.
   c. The sim uses a deterministic synthetic HMAC (documented in the legend). Predict the code
      by working through the JavaScript in the sim (open browser DevTools console and call
      `computeTOTP("0a1b2c3d", 1700000010)` to verify).
   d. Enter the code in the sim and submit.
2. For Scenario 2 (expired code), both partners predict whether the code will be valid 35 seconds
   later BEFORE reading the sim feedback. They write their prediction and the reasoning.
3. For Scenario 4 (replay attack), partners write one paragraph explaining why the 30-second
   window defeats replay even if the attacker acts within 10 seconds of interception.

## Collaborate (AP skill 4)
Assign roles: one partner is the "authenticator" (computes what code the app would show), the
other is the "server" (checks whether the submitted code matches the current step). Swap for
Scenario 3. For the replay scenario, one partner plays the attacker; the other argues why the
defense works.

## Exit ticket
Each student submits: (1) the correct TOTP code for Scenario 1 with the algorithm trace showing
step, digest concept, and final 6-digit code; (2) one sentence explaining what a time-step window
prevents and one sentence describing what it does NOT prevent (real-time phishing relay).

## Instructor notes
- The sim's TOTP uses a synthetic (non-SHA1) HMAC for offline reproducibility. The algorithm
  structure is identical to RFC 6238; only the underlying hash is replaced with an LCG for
  teaching. Students implementing the real solution in problem/ use Python's hmac + hashlib.
- Common stumble: students confuse the time step (an integer) with the timestamp. Clarify:
  two timestamps 5 seconds apart in the same 30-second window share the same step number and
  would produce the same code.
- Common Q: "Can't the attacker just try all million 6-digit codes?" In an online attack with
  rate limiting (5 attempts per minute), exhausting 1,000,000 codes would take 200,000 minutes.
  TOTP codes also change every 30 seconds, resetting the window. Rate limiting + TOTP together
  make online brute-force impractical.
- Feeds the unit project (authentication policy design) and scenario stage 3 (implementing MFA
  for the school Wi-Fi portal to prevent the credential-stuffing attack from 1.2.b).
