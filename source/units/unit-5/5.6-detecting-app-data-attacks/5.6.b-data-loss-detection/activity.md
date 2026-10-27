# In-class activity, 5.6.b Data loss detection (DLP)

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups triage a batch of outbound transfer events, decide which are exfiltration alerts under a
fixed DLP rule, and design an approved-destination list that would reduce false positives without
missing real threats. Ties to LO 5.6.B.

## Materials (all local)
- the SimLab simulation / `problem/` / printed transfer log below.

## Steps
1. Each group works through the the simulation egress queue, deciding ALERT or OK for each transfer
   against the >100 MB / non-approved-destination rule.
2. The group lists every destination that appeared across all cases and sorts them into
   "should be on the approved list" vs. "should stay unapproved," with a one-sentence
   justification for each (is it an internal system, a known partner, or an unknown host?).
3. Groups discuss: could an attacker deliberately keep transfers just under the volume threshold
   to avoid detection ("low and slow" exfiltration)? What additional signal (time of day, account
   baseline, destination reputation) would catch that?

## Collaborate (AP skill 4)
Assign roles: an "analyst" applies the fixed rule to each case, a "policy owner" curates the
approved-destination list, and a "red teamer" argues how an attacker would evade the rule as
written. Debate the red teamer's evasion case as a group.

## Exit ticket
Each group submits: their final approved-destination list, and the one evasion technique the red
teamer proposed plus a mitigation for it.

## Instructor notes
- Expected reasoning: internal/known-partner systems belong on the allowlist; unfamiliar external
  hosts do not, regardless of transfer size.
- Common stumble: students treat "big transfer = always bad" without checking the destination
  first, or vice versa, both signals (size AND destination) matter together, not separately.
- Feeds the coding problem's DLP egress rule and previews "low and slow" exfiltration, a common
  advanced-attacker technique, for later discussion.
