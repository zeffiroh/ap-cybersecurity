# In-class activity, 5.2.a Access control models (RBAC, DAC, MAC)

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Students practice identifying which access control model (DAC, MAC, or RBAC) is in play in a
scenario, and evaluate whether a specific access request should be allowed. Ties to LO 5.2.A.

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario cards below.

## Steps
1. Each group opens the simulation and works through the access-request queue, agreeing on ALLOW or
   DENY for each request under the model/policy shown before submitting.
2. For each request, the group also names which model (DAC, MAC, or RBAC) is being enforced and
   points to the specific rule that produced the decision (owner grant, label comparison, or role
   permission).
3. Groups design one original scenario (a subject, object, and model) and trade with another group
   to decide ALLOW/DENY.

## Collaborate (AP skill 4)
Assign roles: a "policy owner" states the rule in plain language, an "auditor" verifies the
decision against the rule, and a "recorder" writes the justification. Rotate roles each request.

## Exit ticket
Each student submits: one request they evaluated + the model in play + the ALLOW/DENY decision and
why.

## Instructor notes
- Expected reasoning: DAC decisions hinge on an owner's grant list, MAC decisions hinge on a label
  comparison (subject clearance >= object classification), RBAC decisions hinge on whether the
  subject's assigned role includes the requested permission.
- Common stumble: students conflate RBAC with "just having an admin decide", clarify that RBAC
  decisions come from a role's fixed permission set, not case-by-case admin judgment.
- Feeds the unit project (access-control policy review) and the coding problem's decision function.
