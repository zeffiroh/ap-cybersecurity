# In-class activity, 5.2.b Roles, permissions, and least privilege

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Students practice auditing role assignments against job functions and identifying least-privilege
violations and candidates for role redesign. Ties to LO 5.2.A, 5.2.B.

## Materials (all local)
- the SimLab simulation on each machine, or the printed roster/role table below.

## Steps
1. Each group opens the simulation and reviews the fictional company's role assignments, flagging any
   user whose permissions exceed their job function before submitting.
2. For each flagged user, the group writes one sentence naming the specific excess permission and
   the likely cause (privilege creep from a past project, an overly broad role, etc.).
3. Groups redesign one over-broad role into two or more narrower roles and explain how the
   redesign reduces blast radius without blocking anyone's actual job.

## Collaborate (AP skill 4)
Assign roles: an "auditor" identifies the violation, a "role designer" proposes the narrower role
split, and a "recorder" documents the before/after. Rotate roles for each flagged user.

## Exit ticket
Each student submits: one flagged user + the excess permission + the proposed fix (remove
permission or split role).

## Instructor notes
- Expected outcome: students should be able to state which specific permission is unnecessary for
  a given job function, not just "this looks like too much access."
- Common stumble: students conflate "this permission might be useful someday" with "this permission
  is needed now", reinforce that least privilege is about current job function, not hypothetical
  future need.
- Feeds the unit project (access-control policy review) and the coding problem's violation detector.
