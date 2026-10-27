# In-class activity, 5.6.c Digital evidence analysis and attack classification

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups review evidence bundles, classify each incident, and practice writing a short,
honest incident summary that states the classification and any remaining uncertainty. Ties to
LO 5.6.B, 5.6.C.

## Materials (all local)
- the SimLab simulation / `problem/` / printed evidence cards below.

## Steps
1. Each group works through the the simulation evidence-triage cases (or a printed handout of the
   same bundles), classifying each as brute-force, SQL injection, malware, or phishing.
2. For one case, the group writes a two-sentence incident summary in the style a SOC analyst
   would submit: the classification, the specific evidence that supports it, and (if applicable)
   any indicator that doesn't fully fit and should be flagged as open uncertainty.
3. Groups discuss chain-of-custody: for the evidence in their case, what would the group need to
   document (who collected it, how it was stored) for the classification to hold up under review?

## Collaborate (AP skill 4)
Assign roles: a "junior analyst" collects and lists the evidence, a "senior analyst" challenges
the classification and asks "what indicator would change your mind?", and a "reporter" writes the
final incident summary combining both perspectives.

## Exit ticket
Each group submits: their classification, the strongest piece of supporting evidence, and one
sentence naming any remaining uncertainty (or "none" if the evidence was conclusive).

## Instructor notes
- Expected reasoning: students should cite specific evidence items, not just restate the category
  name, and should recognize when a bundle is ambiguous (e.g. mixed weak signals) rather than
  forcing false confidence.
- Common stumble: students anchor on the first indicator they read rather than weighing the full
  bundle; prompt them to list every piece of evidence before concluding.
- Feeds the coding problem's attack classifier and the unit's incident-response tabletop.
