# In-class activity, 4.2.a Passwords and password policies

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students learn to classify candidate passwords as compliant or non-compliant against a stated
policy, and connect each individual policy rule to the specific attack it defends against. Ties
to LO 4.2.A (evaluate a password against a formal policy and explain why each rule reduces risk).

## Materials (all local)
- the SimLab simulation on each machine, or the printed candidate cards below.
- Blank paper for the attack-mapping table (Step 3).

## Steps
1. **Classify the candidates (10 min).** The active policy for this exercise is: `min_length: 12`,
   `require_upper: true`, `require_lower: true`, `require_digit: true`, `require_symbol: true`,
   `banned_list: ["password123", "letmein", "qwerty123456"]`, `history: ["OldPass2023!"]`. Each
   pair reads the five candidate passwords below and writes ACCEPT or REJECT plus a one-sentence
   justification for each.

   - **Candidate A:** `abc123`
   - **Candidate B:** `password123`
   - **Candidate C:** `Tr0ub4dor&3xtra!`
   - **Candidate D:** `OldPass2023!`
   - **Candidate E:** `correcthorsebatterystaple9`

2. **Compare with the simulation (5 min).** Open the simulation and work through its candidate queue to
   check your classifications. Note any disagreements and discuss why.

3. **Build an attack-mapping table (10 min).** As a pair, fill in the table, for each policy
   rule, name the specific attack class it defends against:

   | Policy rule | Attack it defends against | Why |
   |---|---|---|
   | Minimum length | | |
   | Complexity ban on common patterns | | |
   | History / reuse check | | |
   | Account lockout after N failures | | |
   | Breach/banned-list check | | |

## Collaborate (AP skill 4)
Assign roles: one partner is the "policy auditor" (states ACCEPT/REJECT and cites the exact rule
violated), the other is the "attacker" (explains which attack technique the auditor's decision
blocks). Swap roles for the attack-mapping table. Compare your completed tables with another
pair, identify any attack mapping they listed that you missed.

## Exit ticket
Each student submits: their classification of Candidate E + a one-sentence explanation of why a
26-character password can still be rejected by a policy.

## Instructor notes
- Expected answers: A=reject (too short, no upper, no symbol), B=reject (on banned_list despite
  looking complex), C=accept (meets all five rules), D=reject (reused_password, matches
  history), E=reject (no_upper and no_symbol, length alone does not satisfy complexity rules
  when they are turned on).
- Common stumble: students accept Candidate E because it is long and "looks like NIST would
  approve it." Clarify that this specific policy still has `require_upper`/`require_symbol`
  turned on, the sim/problem enforces whatever policy dict is given, not the NIST-recommended
  policy. Distinguish "what NIST recommends" (lesson content) from "what this policy enforces"
  (the exercise).
- Attack-mapping table expected highlights: minimum length -> brute-force (exponentially larger
  search space); complexity ban on predictable patterns -> dictionary attack (blocks common
  words/substitutions); history/reuse check -> password cycling (Password1 -> Password2 ->
  Password1); account lockout -> online guessing (attacker cannot make unlimited interactive
  attempts); breach/banned-list check -> credential stuffing (blocks passwords already known
  from other breaches).
- Feeds the unit project (device hardening plan) and reinforces the coding problem
  (`problem/validate_password`), which formalizes the same classification logic.
