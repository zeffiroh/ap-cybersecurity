# In-class activity, 1.2.b Weak authentication patterns; adversary dictionary construction

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Students apply the four password weakness rules to a set of candidate passwords, predict which
will be flagged and why, and then reason about how an adversary would construct a wordlist to
crack each weak password. Ties to LO 1.2.B (evaluate authentication strength; explain dictionary
construction).

## Materials (all local)
- the SimLab simulation on each machine, or the printed password list below.

## Steps
1. Each pair opens the simulation. For each password in the simulator, they discuss and agree on
   every weakness flag before clicking Check. They record their prediction in writing before
   submitting.
2. For each password that is flagged, they write one sentence describing exactly which wordlist
   entry and mangling rule an attacker would use to crack it (e.g., "'sunshine' appears verbatim
   in rockyou.txt; no mangling required").
3. Pairs design one password that passes all four rules and one that fails exactly two rules.
   They trade with another pair, who must name the exact failing rules without using the sim.

## Collaborate (AP skill 4)
Assign roles: one partner is the "password auditor" (applies the rules, names the flags), the
other is the "attacker analyst" (explains how the cracking tool would find it). Swap roles for
steps 2 and 3.

## Exit ticket
Each student submits: one password they designed that passes all four rules + a one-sentence
explanation of why length matters more than complexity substitutions.

## Instructor notes
- Expected stumble: students think `P@ssword!2024` is strong because it has symbols. Point out
  that "password" is in the COMMON_WORDS list, and the checker flags `in_dictionary` regardless
  of the mangling appended, the base word match is enough.
- Rule 4 (sequential_or_repeated) is often surprising: `HelloWorld111` looks strong but fails
  because `111` is three identical characters. Use this to discuss entropy vs. apparent complexity.
- Common Q: "Does the 12-character minimum mean passphrases are better?" Yes, a four-word
  random passphrase is typically 20+ characters, passes all rules, and is more memorable.
- Feeds the unit project (building an authentication policy) and scenario stage 2 (adversary
  attempts credential stuffing with a dictionary attack against the school Wi-Fi portal).
