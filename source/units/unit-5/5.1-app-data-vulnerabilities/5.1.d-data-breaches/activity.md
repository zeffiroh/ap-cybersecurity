# In-class activity, 5.1.d Data breaches and their impact

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Students practice triaging breach reports by severity, reasoning jointly about data sensitivity,
scale, and detection time. Ties to LO 5.1.C (explain the impact of a data breach).

## Materials (all local)
- the SimLab simulation on each machine, or the printed breach-report set below.

## Steps
1. Each group opens the simulation and works through the queue of synthetic breach reports, agreeing
   on a severity score for each before submitting.
2. For the two highest-severity reports in the queue, the group writes two sentences: what data
   category drove the severity, and what the organization's first containment action should be.
3. Groups rank all reports in the queue from most to least severe and justify any close calls
   (e.g., a small breach of health records vs. a large breach of email addresses).

## Collaborate (AP skill 4)
Assign roles within the group: a "triage lead" reads the report aloud, a "scorer" proposes the
severity score against the rubric, and a "recorder" writes the one-line justification. Rotate
roles each report.

## Exit ticket
Each student submits: the report they found hardest to score + the severity they assigned + one
sentence justifying it.

## Instructor notes
- Expected reasoning: severity should track sensitivity of data category, then scale, then
  detection speed, in roughly that priority order (a small breach of very sensitive data can
  outrank a large breach of low-sensitivity data).
- Common stumble: students default to "bigger record count = always worse," ignoring data
  sensitivity; use the health-records-vs-newsletter-emails example from atom.md to correct this.
- Feeds the unit project (incident-response tabletop) and the coding problem's severity scorer.
