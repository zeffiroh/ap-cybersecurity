# In-class activity, 5.1.c API vulnerabilities

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice thinking like an API attacker: given a set of endpoint calls and an
object-ownership table, decide which requests should be allowed and which are BOLA violations.
Ties to LO 5.1.B (explain how the vulnerability is exploited).

## Materials (all local)
- the SimLab simulation on each machine, or the printed request log below.

## Steps
1. Each pair opens the simulation and works through the mock API console, varying the object-ID
   parameter on each request and predicting allow/deny before submitting.
2. For each BOLA violation found, partners write one sentence identifying which check the server
   skipped (authentication vs. authorization).
3. Pairs then design one additional endpoint (e.g., `GET /api/invoices/{id}`) and write, in plain
   language, the server-side check that would prevent it from being BOLA-vulnerable.

## Collaborate (AP skill 4)
Assign roles: one partner is the "pentester" (chooses which object IDs to probe and predicts the
result), the other is the "API developer" (proposes the missing ownership check and explains where
in the request-handling code it belongs). Swap roles halfway through.

## Exit ticket
Each student submits: one request they tested + whether it was a BOLA violation + the one-line
server-side check that would fix it.

## Instructor notes
- Expected outcome: students should be able to state "check that request.user owns object_id"
  as the universal fix pattern.
- Common stumble: students think a valid login token is sufficient; redirect them to the
  authentication-vs-authorization distinction in atom.md.
- Feeds the unit project (API security review) and the coding problem's authorization checker.
