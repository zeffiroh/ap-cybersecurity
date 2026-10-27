# In-class activity, 1.2.a Password-attack signs

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Students practice reading an authentication log excerpt, identifying the three signals of a
password attack (failure spikes, unusual times, unknown devices), and writing a plain-English
detection rule, tying to LO 1.2.A (detect attacks).

## Materials (all local)
- the SimLab simulation, login-attempt monitor simulation.
- Printed or projected log excerpt below (or use sim for digital-only).

## Steps
1. Each pair opens the simulation. They watch the real-time log scroll and must flag which account
   is under attack before the attacker succeeds. They may click the suspect username at any time;
   the sim scores their timing (early = fewer false positives = better).
2. After the sim, pairs answer: Which of the three signals (failure spike, unusual time, unknown
   device) did they use to make their decision? Write one sentence per signal observed.
3. Pairs write a plain-English detection rule: "Flag an account when ..." filling in the exact
   threshold they would choose and why. They compare rules with another pair.

## Log excerpt (fallback if sim unavailable)
```
2024-03-15 02:13:44  FAIL  admin       192.168.1.201
2024-03-15 02:13:45  FAIL  admin       192.168.1.201
2024-03-15 02:13:46  FAIL  admin       192.168.1.201
2024-03-15 02:13:47  FAIL  admin       192.168.1.201
2024-03-15 02:13:48  FAIL  admin       192.168.1.201
2024-03-15 02:13:49  OK    admin       192.168.1.201   <-- DEVICE UNKNOWN
2024-03-15 08:45:02  OK    jsmith      192.168.1.10    (normal)
```
Ask: (a) How many signals do you see for `admin`? (b) When was this? (c) Is 192.168.1.201 in
your known-device list?

## Collaborate (AP skill 4)
Assign roles: one partner is the "blue-team analyst" (flags the attack and explains the signals),
the other is the "attacker" (argues why the legitimate user might have done this). After two
minutes, the attacker must concede if all three signals are present simultaneously. Swap roles
for a second scenario.

## Exit ticket
Each student submits a one-paragraph incident report: "At [time], account [X] showed [signals].
I conclude [determination]. Recommended response: [action]." Model answer: lockout + side-channel
notification + log review for prior success.

## Instructor notes
- Expected signals in the log excerpt: failure spike (6 in 5s), unusual time (02:13), unknown
  device (192.168.1.201 not in known list).
- Common stumble: students fixate on the raw failure count and miss the time-of-day anomaly.
  Ask "What time is it in the log? Is that normal?"
- Common stumble 2: students think the lockout prevents compromise. Point out the success event
  at 02:13:49, the attack succeeded before any lockout would have fired.
- Feeds the unit scenario (1.2 stage: investigate the router admin login) and the coding problem.
