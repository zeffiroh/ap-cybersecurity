# In-class activity, 1.4.a Voice/image cloning for impersonation

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students apply the classification rules from the lesson to realistic caller scenarios and design
a verification procedure for their fictional organization. Ties to LO 1.4.A (identify deepfake
indicators) and AP skill "Analyze Risk."

## Materials (all local)
- the SimLab simulation on each machine.
- Printed scenario cards below (or displayed on screen from atom.md).

## Steps
1. Each pair works through the the simulation verify-the-caller game. They must reach the target
   score (5 correct) before moving to step 2. One partner narrates the reasoning aloud while the
   other drives.
2. Using the rules in `problem/interface.md`, each pair writes a one-paragraph "Caller
   Verification Policy" for a fictional company (Meridian Health). The policy must specify which
   signals trigger a "suspect" flag and what the employee should do next.
3. Pairs swap policies with another pair and critique: does the swapped policy cover all seven
   signal types? Does it tell an employee what action to take on a "suspect" call?

## Scenario cards (use if the simulation is unavailable)

**Card A.** A call arrives on an internal extension from "the CFO." The voice sounds correct but
the CFO asks to wire $45,000 before end of day and specifically says "don't use email, just call
me back on this line." The shared code word is not offered when you ask.
- Expected classification: suspect (no_shared_secret + refused_callback pattern).

**Card B.** A video call from your manager. The lighting on her face looks slightly different
from the background and her lips seem a fraction out of sync with the audio.
- Expected classification: suspect (video_face_mismatch).

**Card C.** A call from the IT help desk on the official help-desk number asking you to confirm
your employee ID for a directory update. No urgency, no financial request.
- Expected classification: ok.

## Collaborate (AP skill 4)
Assign roles in step 3: one partner is the "security auditor" (finds gaps in the swapped
policy), the other is the "policy author" (defends or revises). After critique, both agree on
a final merged policy.

## Exit ticket
Each student writes: one signal they would add to the policy that is NOT in the default list,
and explains why it would help detect a cloned call.

## Instructor notes
- Expected shared-secret questions often miss the "refused callback" rule, highlight card A.
- Students sometimes argue that a live video call is "obviously real." Use card B to drive home
  that real-time face-swapping exists.
- This feeds the unit project (building a call-screening tool) and scenario stage 1 (the
  deepfake vishing entry vector at Meridian Health).
