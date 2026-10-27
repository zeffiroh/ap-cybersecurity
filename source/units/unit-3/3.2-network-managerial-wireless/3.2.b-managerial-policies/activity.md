# In-class activity, 3.2.b Managerial controls and security policies

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as a security program team building a control matrix for a small company, classifying
each existing control by family (managerial, technical, physical) and identifying one gap where a
managerial control is missing. Ties to LO 3.2.A, 3.2.B and the course skill Mitigate Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario list below.

## Scenario list (print or project)

| # | Scenario | Control type? |
|---|----------|-----------------|
| 1 | New hires sign an AUP before receiving a laptop. | ? |
| 2 | The office VPN requires MFA for remote login. | ? |
| 3 | The finance office door requires a keycard. | ? |
| 4 | Managers review each employee's file-share access every 6 months. | ? |
| 5 | The company has no documented policy for what happens when a laptop is lost or stolen. | (gap, discuss) |

## Steps
1. (5 min) Each group reads rows 1-2 individually and classifies them (managerial, technical,
   physical) using the three-family rule from the lesson.
2. (5 min) Group discusses row 3: is a keycard door reader a "technical" control (it's electronic)
   or a "physical" control (it restricts physical access)? Resolve using the lesson's definition, what the control restricts, not what it's made of.
3. (7 min) Group works row 4: this is a recurring process, not a single event. Decide whether it's
   managerial or technical, and explain how it relates to "privilege creep."
4. (5 min) Each group opens the simulation and checks their calls against the sim's scoring for
   analogous scenarios; groups revise any incorrect calls.
5. (3 min) Row 5 (the gap): each group drafts one sentence of what a lost-device policy should
   require (e.g., mandatory reporting window, remote wipe authorization, password reset).

## Collaborate (AP skill 4)
Assign roles: one member is the "policy author" (drafts language for row 5's missing policy), one
is the "auditor" (challenges whether each classification in rows 1-4 is correct), and remaining
members are "control matrix builders" (compile the group's final table mapping scenario -> type).
For row 3, the group must specifically debate the keycard reader's classification and defend their
answer using the lesson's definition rather than intuition about "electronics = technical."

## Exit ticket
Each student writes one sentence: "Scenario X is a [MANAGERIAL / TECHNICAL / PHYSICAL] control
because [it governs behavior via policy / it enforces automatically via hardware-software / it
restricts physical access]."

## Answer key (instructor only)

| # | Type | Reasoning |
|---|------|-----------|
| 1 | Managerial | A signed policy document governing behavior. |
| 2 | Technical | MFA is enforced automatically by software/hardware at login. |
| 3 | Physical | Restricts physical entry to a space, regardless of the reader being electronic. |
| 4 | Managerial | A documented, recurring access-review process (least privilege policy in action). |
| 5 | Gap | No managerial control exists; a documented lost-device / incident policy is needed. |

## Instructor notes
- Timing: rows 1-2 are the core rule cases; row 3 is the deliberate "electronic but still
  physical" teaching moment; row 4 tests recognition of an ongoing process as managerial rather
  than technical; row 5 requires students to author policy language themselves.
- Common stumble: students assume anything involving a device or electronics must be "technical" —
  reinforce that the classification depends on WHAT the control restricts (access to a physical
  space vs. automatic software/hardware enforcement vs. documented behavior/process), not on
  whether it involves technology.
- Feeds forward to the Unit 3 project, where students build a full control matrix for a
  fictional small business network.
