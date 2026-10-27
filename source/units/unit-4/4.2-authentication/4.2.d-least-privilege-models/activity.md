# In-class activity, 4.2.d Least privilege and access control models

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students learn to identify which access control model is in play in a described scenario and
judge whether an access request violates the principle of least privilege. Ties to LO 4.2.B
(access control models) and 4.2.C (least privilege / risk of over-privileged accounts).

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario cards below.
- Blank paper for the comparison table (Step 3).

## Steps
1. **Classify the requests (10 min).** Each pair reads the five scenarios below and writes: (a)
   which access control model (DAC, MAC, RBAC, or ABAC) is being used or described, and (b)
   whether the request/situation violates least privilege, and if so, why.

   - **Scenario A:** A marketing intern requests write access to the production customer
     database "just in case it's useful later." No specific task requires it.
   - **Scenario B:** An HR employee transferred to a new department two years ago but still has
     active administrator access to the payroll system from their old role.
   - **Scenario C:** An on-call engineer requests elevated production access for a four-hour
     window to resolve an active incident; the access automatically expires afterward.
   - **Scenario D:** A company file server checks a fixed classification label ("Confidential"
     vs. "Public") on every file and a matching clearance level on every user before allowing
     access, no user, including file owners, can override this.
   - **Scenario E:** A cloud platform grants a contractor access to a project folder only when
     their department = "Engineering," their device is company-managed, and the request happens
     between 8 AM and 6 PM on a weekday.

2. **Compare with the simulation (5 min).** Open the simulation and work through its access-request
   stream to check your classifications. Note any disagreements and discuss why.

3. **Build a comparison table (10 min).** As a pair, fill in the table:

   | Model | Who sets permissions | Flexibility | Common use case |
   |---|---|---|---|
   | DAC | | | |
   | MAC | | | |
   | RBAC | | | |
   | ABAC | | | |

## Collaborate (AP skill 4)
Assign roles: one partner is the "requester" (argues why the access should be granted), the other
is the "auditor" (applies least-privilege reasoning to approve, deny, or flag the request). Swap
roles for the comparison table. Compare your completed tables with another pair, identify any
use case or flexibility note they listed that you missed.

## Exit ticket
Each student submits: their classification of Scenario B + a one-sentence explanation of what
control would have prevented that access from persisting for two years.

## Instructor notes
- Expected answers: A = RBAC context but violates least privilege (no task justifies the
  access, deny); B = privilege creep, violates least privilege (should have been caught by a
  periodic access review); C = just-in-time access, does NOT violate least privilege (time-bound,
  justified); D = MAC (centrally enforced classification labels, no owner override); E = ABAC
  (dynamic evaluation of department, device, and time attributes).
- Common stumble: students confuse RBAC and ABAC because both scenarios "seem to check
  conditions." Clarify that RBAC decisions come from a static role assignment made in advance;
  ABAC decisions are computed fresh from attributes at the moment of the request.
- Comparison table expected highlights: DAC (owner sets, high flexibility, personal file
  shares); MAC (central authority sets, low flexibility, military/government); RBAC (admin sets
  via role, moderate flexibility, enterprise IT); ABAC (policy engine sets via rules, high
  flexibility, cloud/dynamic environments).
- Feeds the unit project (access control policy design) and reinforces the coding problem's
  priority-order reasoning (justification first, then review recency, then time-bound status).
