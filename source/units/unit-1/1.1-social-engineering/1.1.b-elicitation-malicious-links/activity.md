# In-class activity, 1.1.b Elicitation; malicious links and files

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice two skills: (1) recognizing when a conversation is extracting information
through elicitation gambits, and (2) reading URLs and filenames methodically to flag malicious
indicators. Ties to LO 1.1.A (identify attack indicators) and 1.1.C (describe delivery vectors
for social-engineering attacks).

## Materials (all local)
- the SimLab simulation on each machine, or printed URL/message set below.
- Pen and paper for the "elicitation transcript" exercise.

## Steps

### Part A, URL/file inspection (15 min)
1. Each pair opens the simulation and works through the message set together, agreeing on every
   indicator before submitting each entry. They must reach the target score.
2. For any message they got wrong, each partner writes one sentence explaining the rule they
   missed, why that indicator applies.

### Part B, Elicitation role-play (10 min)
1. Partner A plays a social engineer trying to find out the name of the company's backup server
   using only indirect questions (no direct "what is the server called?"). Partner B plays a
   receptionist who will answer natural conversational questions but should refuse direct requests.
2. After 4 minutes, partners swap roles. The new attacker tries a different gambit
   (flattery, wrong-statement, or mutual disclosure).
3. After both rounds, both partners write: which gambit was used, what information was
   extracted, and what the receptionist should have done differently.

## Collaborate (AP skill 4)
After Part B, each pair teams up with another pair. Share the gambits used and compare what
information leaked. Discuss: is it possible to have a normal helpful conversation AND protect
sensitive details? What is the minimum a receptionist should reveal to a stranger?

## Exit ticket
Each student submits: one URL they find in their (personal, non-school) email that contains at
least one indicator from the lesson, or "none found", plus which indicator type and why.
(If using school devices, the instructor provides a printed set of sample URLs instead.)

## Instructor notes
- Sim target score is 5 out of 7 messages; most pairs reach it in 10-12 minutes.
- Common stumble on URLs: students read left-to-right and see the trusted brand first, missing
  that the actual registrable domain (rightmost before the first slash) is attacker-controlled.
  Reinforce the right-to-left reading rule explicitly.
- Common stumble on elicitation: students think they "gave nothing away" but the conversation
  may have revealed org chart details, software names, or processes. Debrief by listing every
  specific fact Partner B disclosed during the role-play.
- Feeds the unit project (phishing analyzer) and scenario stage 1 (attacker uses elicitation
  to map Meridian Health's infrastructure before sending a malicious link).
