# In-class activity, 4.4.b Log analysis

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students manually correlate a printed authentication log to find a brute-force pattern, then
practice choosing a detection threshold and discussing its false-positive/false-negative
tradeoffs. Ties to LO 4.4.B (detect attacks via log correlation).

## Materials (all local)
- the SimLab simulation on each machine, or the printed log below.
- Blank paper for the threshold-tuning table (Step 3).

## Printed authentication log (use if devices are unavailable)
```
09:10:02  user=mchen    ip=198.51.100.9   result=SUCCESS
09:12:01  user=jsmith   ip=203.0.113.44   result=FAILED
09:12:14  user=jsmith   ip=203.0.113.44   result=FAILED
09:12:22  user=jsmith   ip=203.0.113.44   result=FAILED
09:12:31  user=jsmith   ip=203.0.113.44   result=FAILED
09:12:39  user=jsmith   ip=203.0.113.44   result=FAILED
09:12:47  user=jsmith   ip=203.0.113.44   result=SUCCESS
09:15:10  user=agarcia  ip=198.51.100.22  result=FAILED
09:41:02  user=agarcia  ip=198.51.100.22  result=FAILED
```

## Steps
1. **Manual correlation (10 min).** Each pair reads the printed log and answers: (a) which
   username shows a brute-force pattern, (b) how many failed attempts occurred and over what
   time span, (c) what happened at the end of that sequence, and (d) why the two `agarcia`
   entries do NOT count as a brute-force pattern.
2. **Check with the simulation (5 min).** Open the simulation and work through its authentication log
   stream to confirm your answer.
3. **Threshold-tuning table (10 min).** As a pair, fill in the table below for three candidate
   detection thresholds, predicting whether each would have caught the `jsmith` attack and
   whether it risks false-positiving on ordinary users:

   | Threshold | Would catch jsmith's attack? | False-positive risk on typo-prone users |
   |---|---|---|
   | 2 failures / 60s | | |
   | 5 failures / 60s | | |
   | 20 failures / 60s | | |

## Collaborate (AP skill 4)
Assign roles: one partner is the "SOC Analyst" (argues for a stricter/lower threshold to catch
attacks fast), the other is the "Help Desk Lead" (argues for a looser/higher threshold to avoid
paging analysts every time a user mistypes a password). Negotiate a threshold both roles can
justify, and write one sentence explaining the compromise.

## Exit ticket
Each student submits: the threshold their pair agreed on, plus one sentence on what could go
wrong if the threshold were set too low.

## Instructor notes
- Expected answer: `jsmith` shows a brute-force pattern, 5 failed attempts within 46 seconds
  (09:12:01 to 09:12:47), followed immediately by a success from the SAME IP, consistent with an
  automated tool that guessed the password on the sixth attempt.
- `agarcia`'s two failures are 26 minutes apart, far outside any reasonable correlation window,
  consistent with an ordinary person mistyping a password twice, not an attack.
- Threshold table expected highlights: 2/60s would catch the attack but generates heavy false
  positives (many users fail twice); 5/60s catches the attack with much lower false-positive
  risk (this is the rule used in the coding problem); 20/60s would miss slower or smaller
  brute-force attempts entirely.
- Feeds the coding problem's exact detection rule (5+ failures within any 60-second window per
  user) and reinforces the unit's alert-fatigue theme from EDR (4.4.a).
