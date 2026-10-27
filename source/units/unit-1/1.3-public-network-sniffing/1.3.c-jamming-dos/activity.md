# In-class activity, 1.3.c Jamming / denial-of-service attack

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Students practice reading a noise-floor sample series and applying the consecutive-threshold
detection rule to classify each series as "jamming" or "clean." They also practice reasoning
about why the rule is tuned (what happens when T or N is too low or too high). Ties to LO
1.3.B (identify indicators of wireless denial-of-service attacks).

## Materials (all local)
- the SimLab simulation, noise-floor monitor
- `problem/`, coding challenge
- Printed sample series table below

## Printed sample series

Detection rule (from interface.md): **T = 80, N = 5**
(a sample series flags as jamming if 5 or more consecutive samples exceed 80)

| Series | Samples                                           | Jamming? |
|--------|---------------------------------------------------|----------|
| A      | 20, 25, 90, 22, 30, 18, 24                        | ?        |
| B      | 15, 82, 85, 88, 91, 83, 87, 20                    | ?        |
| C      | 70, 72, 75, 71, 73, 74, 76                        | ?        |
| D      | 50, 81, 82, 83, 84, 85, 86, 87, 88, 30            | ?        |
| E      | 90, 91, 92, 88, 87, 86, 85, 84, 83, 82, 25, 10   | ?        |

## Steps
1. (5 min) Each student reads the table individually and classifies each series using the rule
   T = 80, N = 5. No discussion yet, write down "jamming" or "clean" with a one-sentence
   justification citing the consecutive-sample run they found.
2. (7 min) Compare with your partner. For any disagreement, step through the series together
   sample by sample, counting the run. Agree on a final answer for each.
3. (5 min) Open the simulation. Toggle the simulated jammer and observe how the noise floor
   changes. Discuss: could you distinguish a jammer from a microwave oven in the sim data?
4. (3 min) Optional extension: what would happen to false-positive and false-negative rates if
   you changed N from 5 to 2? If you raised T from 80 to 95?

## Collaborate (AP skill 4)
Assign roles: one partner is the **network monitor** (reads and classifies the data), the
other is the **analyst** (explains why the rule fires or does not fire for each series).
After the table, swap: analyst proposes a new sample series, monitor classifies it.

## Exit ticket
Each student writes the detection rule from memory (threshold value, minimum consecutive
samples, and the Boolean return value) and gives one example of a real-world event that could
cause a true positive versus a false positive using this rule.

## Instructor notes
- Expected answers: A = clean (only one spike at position 3); B = jamming (positions 2-7 are
  all above 80, run = 6); C = clean (all below 80); D = jamming (positions 2-10 are above 80,
  run = 9); E = jamming (positions 1-10 are above 80, run = 10).
- Common stumble: students count the threshold as inclusive vs. exclusive. The rule uses
  strictly greater than T (> 80), so a sample of exactly 80 does not count. Verify with
  series C (max 76 = clean) vs. series B (min 82 = jamming).
- Feeds the unit project (wireless threat report) and scenario stage 3 (detecting the physical
  intrusion support operation).
