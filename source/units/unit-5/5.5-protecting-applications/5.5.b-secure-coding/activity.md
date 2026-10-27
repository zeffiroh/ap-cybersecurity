# In-class activity, 5.5.b Secure coding practices

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups perform a mini code review on a printed set of snippets, flagging every secure-coding
violation and proposing the one-line fix for each. Ties to LO 5.5.A, 5.5.B.

## Materials (all local)
- the SimLab simulation / `problem/` / printed snippet set below.

## Steps
1. Each group works through the the simulation review queue (or a printed handout of the same
   snippets), marking each PASS or FLAG.
2. For every FLAG, the group writes the one-line fix (e.g. "switch to a parameterized query",
   "load the key from an environment variable", "run as a non-root service account").
3. Groups then pick their own two-line code/config snippet (from a past project, a textbook
   example, or invented) and challenge another group to find the violation.

## Collaborate (AP skill 4)
Assign roles: a "reviewer" flags violations, a "fixer" proposes the one-line remediation, and a
"referee" checks the fix actually addresses the root cause (not just silences the symptom).
Rotate roles partway through.

## Exit ticket
Each group submits: the snippet they wrote for the challenge round, its violation (if any), and
the fix.

## Instructor notes
- Expected reasoning: students should connect each violation to the specific attack it enables
  (concatenated SQL -> injection; verbose errors -> reconnaissance; root process -> full
  compromise on exploit).
- Common stumble: students propose "add input validation" as a universal fix even when the real
  issue is a query-building pattern or a privilege setting that validation cannot touch.
- Feeds the coding problem's configuration auditor and the sim's PASS/FLAG review task.
