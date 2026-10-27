# In-class activity, 5.5.c Application security testing (SAST/DAST)

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups triage a mixed batch of security findings, sort each into SAST-catchable,
DAST-catchable, or human-pentest-only, and justify the sort. Ties to LO 5.5.B, 5.5.C.

## Materials (all local)
- the SimLab simulation / `problem/` / printed finding cards below.

## Steps
1. Each group receives (or works through in the simulation) a shuffled set of findings: some are
   source-code snippets, some are live-scan results, some are business-logic descriptions.
2. Groups sort each finding into three piles: SAST, DAST, NEITHER (human pentest needed), and
   for each finding write one sentence explaining the sorting rule they applied (does it require
   a running app? does it require reasoning about intent/business rules?).
3. Groups then design a one-line CI/CD pipeline order (e.g. "SAST on every commit -> DAST against
   staging before release -> periodic manual pentest") and justify why that order minimizes wasted
   effort.

## Collaborate (AP skill 4)
Assign roles: a "static reviewer" argues the SAST case for ambiguous findings, a "dynamic
tester" argues the DAST case, and a "pentester" argues for findings that need human judgment.
Debate any finding the group disagrees on before recording a final answer.

## Exit ticket
Each group submits: the one finding they debated most, their final classification, and the
one-sentence rule that settled it.

## Instructor notes
- Expected reasoning: "does this require the app to be running?" separates SAST from DAST; "does
  this require knowing what the *correct* business behavior should be?" separates automated
  tooling from human pentesting.
- Common stumble: students assume a clean SAST/DAST scan means "no vulnerabilities", remind them
  both tools only find what they are built to look for.
- Feeds the coding problem's SAST rule engine and the sim's classification task.
